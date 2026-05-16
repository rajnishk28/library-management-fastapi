from fastapi import APIRouter
from app.schemas.user_schema import (
    UserRegister,
    UserLogin
)

from app.controllers.auth_controller import (
    register_controller,
    login_controller
)

router = APIRouter()


@router.post("/register")
def register(user: UserRegister):
    return register_controller(user)


@router.post("/login")
def login(user: UserLogin):
    return login_controller(user)