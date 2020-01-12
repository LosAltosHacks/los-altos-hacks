import boto3
import requests
from botocore.exceptions import ClientError
from main import app

def read_email(name):
    prefix = f'email_templates/{name}/'
    return read_file(prefix + "subject"), read_file(prefix + "header_1"), read_file(prefix + "header_2"), read_file(prefix + "body"), read_file(prefix + "text")

def read_templates(*templates):
    temps = {}
    for t in templates:
        subject, header_1, header_2, body, text = read_email(t)
        temps[t] = {}
        temps[t]['subject'] = subject
        temps[t]['header_1'] = header_1
        temps[t]['header_2'] = header_2
        temps[t]['body'] = body
        temps[t]['text'] = text
    return temps

HTML_TEMPLATE = read_file('email_templates/html')
TEMPLATES = read_templates("confirmation", "mentor_confirmation")

def format_email(template, data):
    text = TEMPLATES[template]['text'].format(**data)
    subject = TEMPLATES[template]['subject'].format(**data)
    header_1 = TEMPLATES[template]['header_1'].format(**data)
    header_2 = TEMPLATES[template]['header_2'].format(**data)
    body = TEMPLATES[template]['body'].format(**data)

    message = {**data, 'header_1': header_1, 'header_2': header_2, 'body': body}
    return subject, text, HTML_TEMPLATE.format(**message)

def send_email_template(data, template):
    role = requests.get(f'http://169.254.170.2{os.environ["AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"]}').json()
    client = boto3.Session(
        aws_access_key_id=role["AccessKeyId"],
        aws_secret_access_key=role["SecretAccessKey"],
        aws_session_token=role["Token"],
    ).client('ssm')

    SES_REGION = client.get_parameter(Name="/ses/aws-region")["Parameter"]["Value"].encode('utf-8')
    SES_SENDER = client.get_parameter(Name="/ses/sender")["Parameter"]["Value"].encode('utf-8')

    client = boto3.client('ses', region_name=SES_REGION)

    try:
        subject, text, html = format_email(template, data)
        response = client.send_email(
            Destination = {'ToAddresses': [data['email']]},
            Message = {
                'Body': {
                    'Html': {
                        'Charset': "UTF-8",
                        'Data': html
                    },
                    'Text': {
                        'Charset': "UTF-8",
                        'Data': text
                    }
                },
                'Subject': {
                    'Charset': "UTF-8",
                    'Data': subject
                }
            },
            Source = SES_SENDER)
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Sent email to " + data['email'] + "; MessageId: '" + response['MessageId'] + "'")

def read_file(filename):
    with open(filename, 'r') as f:
        return f.read()
