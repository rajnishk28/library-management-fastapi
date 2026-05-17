from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str
    # role is intentionally NOT accepted from the client.
    # Public signup always creates a "user" role account.
    # Admin accounts must be seeded directly in the database.


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserStatusSchema(BaseModel):
    active: bool


class UpdateProfileSchema(BaseModel):
    name: str
    email: EmailStr


class ChangePasswordSchema(BaseModel):
    current_password: str
    new_password: str
