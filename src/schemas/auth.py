import re

from pydantic import BaseModel, EmailStr, Field, ValidationInfo, field_validator
from typing import Annotated


COGNITO_PASSWORD_COMPLEXITY_REGEX = re.compile(
    r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\^$*.[\]{}()?\"!@#%&/\\,><':;|_~`=+-\\]).{8,256}$"
)


PasswordBaseStr = Annotated[
    str,
    Field(
        min_length=8,
        max_length=256,
    )
]

CodeBaseStr = Annotated[
    str,
    Field(
        min_length=6,
        max_length=6,
        pattern=r"^\d{6}$"
    )
]

class AuthInput(BaseModel):
    email: EmailStr
    password: PasswordBaseStr

    @field_validator('password')
    @classmethod
    def validate_password_complexity(cls, value: str, info: ValidationInfo) -> str:
        if not COGNITO_PASSWORD_COMPLEXITY_REGEX.match(value):
            raise ValueError(
                'Password must contain at least one lowercase letter, '
                'one uppercase letter, one digit, and one special character.'
            )
        return value

class ConfirmSignupInput(BaseModel):
    email: EmailStr
    code: CodeBaseStr

class ForgotPasswordInput(BaseModel):
    email: EmailStr

class ResetPasswordInput(BaseModel):
    email: EmailStr
    code: CodeBaseStr
    new_password: PasswordBaseStr

    @field_validator('new_password')
    @classmethod
    def validate_new_password_complexity(cls, value: str, info: ValidationInfo) -> str:
        if not COGNITO_PASSWORD_COMPLEXITY_REGEX.match(value):
            raise ValueError(
                'New password must contain at least one lowercase letter, '
                'one uppercase letter, one digit, and one special character.'
            )
        return value

class ChangePasswordInput(BaseModel):
    old_password: PasswordBaseStr
    new_password: PasswordBaseStr

    @field_validator('old_password', 'new_password')
    @classmethod
    def validate_password_complexity_change(cls, value: str, info: ValidationInfo) -> str:
        if not COGNITO_PASSWORD_COMPLEXITY_REGEX.match(value):
            raise ValueError(
                'Password must contain at least one lowercase letter, '
                'one uppercase letter, one digit, and one special character.'
            )
        return value
