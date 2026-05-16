from fastapi import APIRouter, Depends

from app.controllers.user_controller import (
    get_users_controller,
    get_profile_controller,
    update_user_status_controller,
    delete_user_controller
)

from app.schemas.user_schema import UserStatusSchema
from app.middleware.auth_middleware import verify_token, admin_only

router = APIRouter()


@router.get("/")
def get_users(admin=Depends(admin_only)):
    return get_users_controller()


@router.get("/me")
def get_profile(user=Depends(verify_token)):
    return get_profile_controller(user)


@router.patch("/{user_id}/status")
def update_user_status(
    user_id: str,
    status: UserStatusSchema,
    admin=Depends(admin_only)
):
    return update_user_status_controller(user_id, status)


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    admin=Depends(admin_only)
):
    return delete_user_controller(user_id)
