from fastapi import HTTPException
from app.models.user_model import users_collection
from app.utils.password_handler import (
    hash_password,
    verify_password
)
from app.utils.jwt_handler import create_access_token


def register_controller(user):

    existing_user = users_collection.find_one({
        "email": user.email
    })

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )
    if len(user.password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password cannot exceed 72 bytes"
        )
        
    user_dict = user.dict()
    user_dict["password"] = hash_password(user.password)
    user_dict["active"] = True
    user_dict["role"] = "user"  # always force "user" — never trust client-supplied role

    users_collection.insert_one(user_dict)

    return {
        "message": "User registered successfully"
    }


def login_controller(user):

    db_user = users_collection.find_one({
        "email": user.email
    })

    if not db_user:
        raise HTTPException(
            status_code=400,
            detail="Invalid email"
        )

    if db_user.get("active") is False:
        raise HTTPException(
            status_code=403,
            detail="Account is deactivated"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid password"
        )

    token = create_access_token({
        "id": str(db_user["_id"]),
        "role": db_user["role"]
    })

    return {
        "access_token": token,
        "role": db_user["role"]
    }
