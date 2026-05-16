from fastapi import APIRouter, Depends
from app.controllers.stats_controller import (
    get_admin_stats_controller,
    get_user_stats_controller,
)
from app.middleware.auth_middleware import verify_token, admin_only

router = APIRouter()


@router.get("/admin")
def admin_stats(admin=Depends(admin_only)):
    return get_admin_stats_controller()


@router.get("/user")
def user_stats(user=Depends(verify_token)):
    return get_user_stats_controller(user)
