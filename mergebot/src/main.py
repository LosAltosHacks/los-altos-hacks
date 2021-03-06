import functools
import os
import time
import traceback
import tempfile
import subprocess
import logging
import hmac
import asyncio
import aiohttp
from aiohttp import web
import github3
from github3 import GitHub

def run_in_executor(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return loop.run_in_executor(None, lambda: f(*args, **kwargs))
    return inner

# TODO better logging + canonical lines
def log():
    return logging.getLogger("ffmergebot")

routes = web.RouteTableDef()

APP_IDENTIFIER_NUMBER = 49662
PRIVATE_KEY = None
WEBHOOK_SECRET = None

def get_pk():
    global PRIVATE_KEY
    global WEBHOOK_SECRET
    if not PRIVATE_KEY or not WEBHOOK_SECRET:
        if os.environ["ENVIRONMENT"] == "prod":
            # https://aws.amazon.com/blogs/compute/managing-secrets-for-amazon-ecs-applications-using-parameter-store-and-iam-roles-for-tasks/
            import boto3
            import requests
            # https://docs.aws.amazon.com/AmazonECS/latest/userguide/task-iam-roles.html
            # This env var is populated by the container agent, we get our assigned ECS task role from this endpoint
            role = requests.get(f'http://169.254.170.2{os.environ["AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"]}').json()
            client = boto3.Session(
                aws_access_key_id=role["AccessKeyId"],
                aws_secret_access_key=role["SecretAccessKey"],
                aws_session_token=role["Token"],
            ).client('ssm')
            PRIVATE_KEY = client.get_parameter(Name="/ffmergebot/private-key", WithDecryption=True)["Parameter"]["Value"].encode('utf-8')
            WEBHOOK_SECRET = client.get_parameter(Name="/ffmergebot/webhook-secret", WithDecryption=True)["Parameter"]["Value"].encode('utf-8')
        elif os.environ["ENVIRONMENT"] == "dev":
            DEV_PRIVATE_KEY_PATH = "ffmergebot.private-key.pem"
            PRIVATE_KEY = open(DEV_PRIVATE_KEY_PATH, 'rb').read()
            if len(PRIVATE_KEY) == 0:
                raise RuntimeError("Found private key file with length 0. Did you remember to supply a real cert for development?")
            DEV_WEBHOOK_SECRET_PATH = "webhook-secret.txt"
            WEBHOOK_SECRET = open(DEV_WEBHOOK_SECRET_PATH, 'rb').read().strip()
            if len(WEBHOOK_SECRET) == 0:
                raise RuntimeError("Found webhook secret file with length 0. Did you remember to supply a real cert for development?")
        else:
            raise ValueError(f'Invalid value for ENVIRONMENT: {os.environ["ENVIRONMENT"]}')
    return PRIVATE_KEY

def get_webhook_secret():
    get_pk()
    return WEBHOOK_SECRET

def github_installation(installation_id):
    g = GitHub()
    g.login_as_app_installation(get_pk(), APP_IDENTIFIER_NUMBER, installation_id)
    return g

@routes.get("/")
async def aws_health_check(request):
    return web.Response(status=200)

@routes.post("/")
async def recv_webhook(request):
    if "x-github-event" in request.headers and request.headers["x-github-event"] == "issue_comment":
        log().info("Received issue_comment webhook.")
        # Verify webhook before proceeding
        if not "x-hub-signature" in request.headers:
            return web.Response(status=400)
        header = request.headers["x-hub-signature"]
        sig = hmac.new(get_webhook_secret(), msg=(await request.read()), digestmod="sha1")
        if not hmac.compare_digest('sha1='+sig.hexdigest(), header):
            log().info("Github signature did not verify against secret")
            return web.Response(status=400)
        return await handle_comment(request)
    return web.Response(status=200)

async def handle_comment(request):
    json_body = await request.json()
    if "action" not in json_body or json_body["action"] != "created":
        return web.Response(status=200)
    comment_text = json_body["comment"]["body"]
    stripped_lines = [line.strip() for line in comment_text.split("\n")]
    if "ffmerge" in stripped_lines:
        log().info("Responding to ffmerge command.")
        return await attempt_merge(request, json_body)
    return web.Response(status=200)

@run_in_executor
def attempt_merge(request, json):
    gh = github_installation(json["installation"]["id"])
    if not "issue" in json:
        return web.Response(status=400)
    issue = github3.issues.issue.ShortIssue(json["issue"], gh.session)
    try:
        pr = issue.pull_request()
        if not pr:
            log().info("Command not on a PR.")
            issue.create_comment("This doesn't look like a pull request to me.")
            return web.Response(status=200)
        if not user_has_merge_permission(gh, json):
            log().info("Commander does not have permission.")
            issue.create_comment(f"User @{ json['sender']['login'] } does not have permission to merge.")
            return web.Response(status=200)
        if not pr.mergeable:
            log().info("PR is not mergeable.")
            issue.create_comment("PR is not mergeable.")
            return web.Response(status=200)
        if not checks_passed(pr):
            log().info("Merging is blocked on checks.")
            issue.create_comment("Merging is blocked on checks.")
            return web.Response(status=200)
        log().info("Attempting ffmerge.")
        try:
            do_ff_merge(gh, pr)
            log().info(f"Successful merge of {pr.url}")
            log().debug(f"Successful merge of {pr.as_json()} based on event {json}")
        except Exception as e:
            issue.create_comment(
                "Could not perform FF merge. This likely means you need to rebase your branch. " +
                "A different error may have also occured. " +
                "If this is a protected branch, make sure I have been given explicit push access. " +
                "To protect access tokens, a stacktrace is unavailable here. " +
                f"Examine the logs around time `f{time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}`."
            )
            log().exception(f"Failed to merge {pr.as_json()} based on event {json}")
    except Exception as e:
        issue.create_comment(f"Encountered exception:\r\n\r\n```\r\n{traceback.format_exc()}\r\n```")
        log().exception(f"Failure when running merge choice logic of {pr.as_json()} based on event {json}")
    return web.Response(status=200)

def user_has_merge_permission(gh, webhook_json):
    url = webhook_json["repository"]["collaborators_url"].replace("{/collaborator}", f'/{webhook_json["sender"]["login"]}/permission')
    permissions = gh.session.get(url).json()
    return permissions["permission"] in ("admin", "write")

def checks_passed(pr):
    statuses = pr.session.get(pr.statuses_url).json()
    seen = set({})
    for status in statuses:
        if status["state"] != "success" and status["context"] not in seen:
            return False
        seen.add(status["context"])
    return True

def do_ff_merge(gh, pr):
    # if the merge is to be FF, that means we can just pull the head branch shallow
    # and then push it right back to the remote as the other branch
    # ordinary push behavior fails on no FF
    pwd = tempfile.TemporaryDirectory(prefix="ffmergebot", suffix=".git")
    headbranchref = pr.head.ref
    basebranchref = pr.base.ref

    # what are api boundaries anyway
    access_token = gh.session.auth.token

    headrepourl = get_authed_repo_url(access_token, pr.head.repository.clone_url)
    baserepourl = get_authed_repo_url(access_token, pr.base.repository.clone_url)
    if headrepourl == baserepourl:
        # we can do fast path shallow clone since we know the remotes are the same
        run_with_log_checked(["git", "clone", "--bare", "--branch", headbranchref, "--shallow-exclude", basebranchref, headrepourl, pwd.name])
        try:
            run_with_log_checked(["git", "--git-dir", pwd.name, "fetch", "--deepen", "1"])
        except Exception as e:
            log().info("Deepen failed, falling back to full checkout...")
            pwd.cleanup()
            pwd = tempfile.TemporaryDirectory(prefix="ffmergebot", suffix=".git")
            run_with_log_checked(["git", "clone", "--bare", "--branch", headbranchref, headrepourl, pwd.name])
    else:
        # full clone to ensure we have all the refs
        run_with_log_checked(["git", "clone", "--bare", "--branch", headbranchref, headrepourl, pwd.name])

    run_with_log_checked(["git", "--git-dir", pwd.name, "push", baserepourl, f"{headbranchref}:{basebranchref}"])
    pwd.cleanup()

def run_with_log_checked(args, **kwargs):
    cprcs = subprocess.run(args, capture_output=True, **kwargs)
    log().info(f'Process {cprcs.args} finished with code {cprcs.returncode}.')
    level = logging.INFO
    if cprcs.returncode == 0:
        level = logging.DEBUG
    log().log(level, f'Process {cprcs.args} had output to follow. STDOUT: """{cprcs.stdout}""" STDERR: """\n{cprcs.stderr}"""')
    cprcs.check_returncode()
    return cprcs

def get_authed_repo_url(token, clone_url):
    # https://x-access-token:<token>@github.com/owner/repo.git
    comps = clone_url.split("//")
    comps.insert(1, f"//x-access-token:{token}@")
    return "".join(comps)

if __name__ == "__main__":
    FORMAT = '%(asctime)s %(name)s %(levelname)s : %(message)s'
    # use UTC
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.DEBUG)

    # Fail early on the PK, the app is useless without it
    get_pk()

    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, port=8000)
