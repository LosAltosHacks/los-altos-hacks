from ..common import *

_SSM_CLIENT = None
_SSM_PREFIX = "lah_registration"
def get_param(param_name, with_decryption=True):
    # https://aws.amazon.com/blogs/compute/managing-secrets-for-amazon-ecs-applications-using-parameter-store-and-iam-roles-for-tasks/
    import boto3
    import requests
    # https://docs.aws.amazon.com/AmazonECS/latest/userguide/task-iam-roles.html
    # This env var is populated by the container agent, we get our assigned ECS task role from this endpoint
    if not _SSM_CLIENT:
        role = requests.get(f'http://169.254.170.2{os.environ["AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"]}').json()
        _SSM_CLIENT = boto3.Session(
            aws_access_key_id=role["AccessKeyId"],
            aws_secret_access_key=role["SecretAccessKey"],
            aws_session_token=role["Token"],
        ).client('ssm')
    return _SSM_CLIENT.get_parameter(Name=f"/{_SSM_PREFIX}/{param_name}", WithDecryption=with_decryption)["Parameter"]["Value"].encode('utf-8')

SQLALCHEMY_DATABASE_URL = get_param("database_url")
SES_AWS_REGION = get_param("ses_region")
SES_SENDER = get_param("ses_sender")
JWT_SECRET_KEY = get_param("jwt_secret")
