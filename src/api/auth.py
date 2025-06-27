from fastapi import APIRouter, status, Depends
from fastapi.security import HTTPAuthorizationCredentials

from src.services import cognito as cognito_service
from src.schemas.auth import (
    AuthInput,
    ForgotPasswordInput,
    ResetPasswordInput,
    ChangePasswordInput,
    ConfirmSignupInput,
)
from src.schemas.standard import SuccessResponse
from src.settings.security import bearer_auth
from src.utils.auth import handle_client_error
from src.docs.cognito import generate_responses_for_errors


router = APIRouter(tags=["authentication"])


@router.post(
    "/signup",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses=generate_responses_for_errors([
        "UsernameExistsException",
        "InvalidPasswordException",
        "TooManyRequestsException"
    ]),
)
@handle_client_error("Signup failed!")
def signup(user: AuthInput):
    cognito_service.signup_user(user.email, user.password)
    return SuccessResponse(
        message="Signup successful. Check email to confirm.",
        data={"email": user.email}
    )


@router.post(
    "/confirm-signup",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses_for_errors([
        "ExpiredCodeException",
        "TooManyRequestsException"
    ])
)
@handle_client_error("Confirm signup failed!")
def confirm_signup(data: ConfirmSignupInput):
    cognito_service.confirm_signup(data.email, data.code)
    return SuccessResponse(
        message="Signup confirmed successfully.",
        data={"email": data.email}
    )


@router.post(
    "/login",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses_for_errors([
        "NotAuthorizedException",
        "TooManyRequestsException"
    ])
)
@handle_client_error("Login failed!")
def login(user: AuthInput):
    tokens = cognito_service.login_user(user.email, user.password)
    return SuccessResponse(
        message="Login successful.",
        data=tokens
    )


@router.post(
    "/forgot-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses_for_errors([
        "InvalidParameterException"
        "TooManyRequestsException"
    ]),
)
@handle_client_error("Forgot password failed!")
def forgot_password(data: ForgotPasswordInput):
    cognito_service.forgot_password(data.email)
    return SuccessResponse(
        message="Confirmation code sent to your email."
    )


@router.post(
    "/reset-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses_for_errors([
        "ExpiredCodeException",
        "InvalidPasswordException",
        "TooManyRequestsException"
    ])
)
@handle_client_error("Reset password failed!")
def reset_password(data: ResetPasswordInput):
    cognito_service.confirm_forgot_password(
        email=data.email,
        code=data.code,
        new_password=data.new_password
    )
    return SuccessResponse(
        message="Password reset successfully."
    )


@router.post(
    "/change-password",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses_for_errors([
        "NotAuthorizedException",
        "InvalidPasswordException",
        "TooManyRequestsException"
    ]),
)
@handle_client_error("Change password failed!")
def change_password(
    data: ChangePasswordInput,
    token: HTTPAuthorizationCredentials = Depends(bearer_auth)
):
    access_token = token.credentials
    cognito_service.change_password(access_token, data.old_password, data.new_password)
    return SuccessResponse(
        message="Password changed successfully."
    )


@router.post(
    "/logout",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    responses=generate_responses_for_errors([
        "NotAuthorizedException",
        "TooManyRequestsException"
    ]),
)
@handle_client_error("Logout failed!")
def logout(token: HTTPAuthorizationCredentials = Depends(bearer_auth)):
    access_token = token.credentials
    cognito_service.logout(access_token)
    return SuccessResponse(
        message="Logged out successfully."
    )
