from pydantic import BaseModel, EmailStr, validator

class SignupRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def email_must_be_gmail(cls, value):
        if not str(value).lower().endswith("@gmail.com"):
            raise ValueError("Chỉ chấp nhận email @gmail.com")
        return value

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @validator("email")
    def email_must_be_gmail(cls, value):
        if not str(value).lower().endswith("@gmail.com"):
            raise ValueError("Chỉ chấp nhận email @gmail.com")
        return value

class GoogleLoginRequest(BaseModel):
    id_token: str 

class AuthResponse(BaseModel):
    email: str
    uid: str
    idToken: str | None = None
    refreshToken: str | None = None 

class ResendVerificationRequest(BaseModel):
    email: EmailStr

    @validator("email")
    def email_must_be_gmail(cls, value):
        if not str(value).lower().endswith("@gmail.com"):
            raise ValueError("Chỉ chấp nhận email @gmail.com")
        return value