from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str

    @field_validator("role")
    def role_must_be_valid(cls, v):
        if v not in ["user", "admin"]:
            raise ValueError("Role must be either 'user' or 'admin'")
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserStatusSchema(BaseModel):
    active: bool
