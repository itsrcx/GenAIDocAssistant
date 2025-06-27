from botocore.exceptions import ClientError

from src.settings.config import COGNITO_DOMAIN, USER_POOL_ID, CLIENT_ID, AWS_REGION, boto3_session
from src.utils.auth import get_secret_hash


cognito = boto3_session.client("cognito-idp", region_name=AWS_REGION)


def signup_user(email: str, password: str):
    try:
        response = cognito.sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(email),
            Username=email,
            Password=password,
            UserAttributes=[{"Name": "email", "Value": email}],
        )
        return response
    except ClientError as e:
        raise e

def confirm_signup(email: str, code: str):
    try:
        response = cognito.confirm_sign_up(
            ClientId=CLIENT_ID,
            SecretHash=get_secret_hash(email),
            Username=email,
            ConfirmationCode=code
        )
        return response
    except ClientError as e:
        raise e

def login_user(email: str, password: str):
    try:
        response = cognito.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': email,
                'PASSWORD': password,
                'SECRET_HASH': get_secret_hash(email)
            }
        )
        return response['AuthenticationResult']
    except ClientError as e:
        raise e

def forgot_password(email: str):
    return cognito.forgot_password(ClientId=CLIENT_ID, SecretHash=get_secret_hash(email), Username=email)

def confirm_forgot_password(email: str, code: str, new_password: str):
    return cognito.confirm_forgot_password(
        ClientId=CLIENT_ID,
        SecretHash=get_secret_hash(email),
        Username=email,
        ConfirmationCode=code,
        Password=new_password
    )

def change_password(access_token: str, old_password: str, new_password: str):
    return cognito.change_password(
        PreviousPassword=old_password,
        ProposedPassword=new_password,
        AccessToken=access_token
    )

def logout(access_token: str):
    return cognito.global_sign_out(AccessToken=access_token)
