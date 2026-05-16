from app.models.user_model import users_collection
from bson import ObjectId
from fastapi import HTTPException


def get_users_controller():

    users = []

    for user in users_collection.find():

        user["_id"] = str(user["_id"])

        del user["password"]

        users.append(user)

    return users


def get_profile_controller(current_user):

    user = users_collection.find_one({
        "_id": ObjectId(current_user["id"])
    })

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    user["_id"] = str(user["_id"])
    del user["password"]

    return user


def update_user_status_controller(user_id, status):

    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"active": status.active}}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User status updated successfully"
    }


def delete_user_controller(user_id):

    result = users_collection.delete_one({
        "_id": ObjectId(user_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return {
        "message": "User deleted successfully"
    }
