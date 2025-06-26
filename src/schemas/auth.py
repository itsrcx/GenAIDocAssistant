from pydantic import BaseModel, EmailStr

class AuthInput(BaseModel):
    email: EmailStr
    password: str

class ConfirmSignupInput(BaseModel):
    email: EmailStr
    code: str

class ForgotPasswordInput(BaseModel):
    email: EmailStr

class ResetPasswordInput(BaseModel):
    email: EmailStr
    code: str
    new_password: str

class ChangePasswordInput(BaseModel):
    old_password: str
    new_password: str
