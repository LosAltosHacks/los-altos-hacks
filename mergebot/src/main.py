import functools
import time
import traceback
import tempfile
import subprocess
import logging
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
PRIVATE_KEY_PATH = "noffmergebot.2019-12-21.private-key.pem"

PRIVATE_KEY = None

def get_pk():
    global PRIVATE_KEY
    if not PRIVATE_KEY:
        PRIVATE_KEY = open(PRIVATE_KEY_PATH, 'rb').read()
    return PRIVATE_KEY

def github_installation(installation_id):
    g = GitHub()
    g.login_as_app_installation(get_pk(), APP_IDENTIFIER_NUMBER, installation_id)
    return g

@routes.post("/")
async def recv_webhook(request):
    if "x-github-event" in request.headers and request.headers["x-github-event"] == "issue_comment":
        log().info("Acting on a comment.")
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
        run_with_log_checked(["git", "--git-dir", pwd.name, "fetch", "--deepen", "1"])
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
    import os

    FORMAT = '%(asctime)s %(name)s %(levelname)s : %(message)s'
    # use UTC
    logging.Formatter.converter = time.gmtime
    logging.basicConfig(format=FORMAT)
    logging.getLogger().setLevel(logging.DEBUG)

    app = web.Application()
    app.add_routes(routes)
    port = os.environ.get("PORT")
    if port is not None:
        port = int(port)
    web.run_app(app, port=port)
