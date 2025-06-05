import boto3
from app.config import COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID, AWS_REGION

client = boto3.client('cognito-idp', region_name=AWS_REGION)

def signup_user(email, password):
    return client.sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=email,
        Password=password,
        UserAttributes=[
            {'Name': 'email', 'Value': email},
        ]
    )

def confirm_user(email, code):
    return client.confirm_sign_up(
        ClientId=COGNITO_CLIENT_ID,
        Username=email,
        ConfirmationCode=code
    )

def login_user(email, password):
    return client.initiate_auth(
        ClientId=COGNITO_CLIENT_ID,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': email,
            'PASSWORD': password
        }
    )
