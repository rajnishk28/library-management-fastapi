from app.models.user_model import users_collection
from app.models.issue_model import issues_collection
from bson import ObjectId
from fastapi import HTTPException
from app.utils.password_handler import hash_password, verify_password


def get_users_controller(page: int = 1, limit: int = 10, search: str = None):
    """Return only non-admin users — admins are not shown in the member management list."""
    skip = (page - 1) * limit
    
    # Build base filter (exclude admins)
    filter_query = {"role": {"$ne": "admin"}}
    
    # Build search filter
    if search and search.strip():
        search_term = search.strip().lower()
        filter_query["$and"] = [
            {"role": {"$ne": "admin"}},
            {
                "$or": [
                    {"name": {"$regex": search_term, "$options": "i"}},
                    {"email": {"$regex": search_term, "$options": "i"}}
                ]
            }
        ]
    
    total = users_collection.count_documents(filter_query)
    total_pages = max(1, -(-total // limit))  # ceiling division

    users = []
    for user in users_collection.find(filter_query).skip(skip).limit(limit):
        user["_id"] = str(user["_id"])
        del user["password"]
        users.append(user)

    return {
        "items": users,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


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


def update_user_status_controller(user_id, status, admin):
    """Admin-only: activate/deactivate a user. Cannot target self or other admins."""

    # Prevent self-deactivation
    if user_id == admin["id"]:
        raise HTTPException(
            status_code=400,
            detail="You cannot change your own account status"
        )

    target = users_collection.find_one({"_id": ObjectId(user_id)})
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent targeting another admin
    if target.get("role") == "admin":
        raise HTTPException(
            status_code=403,
            detail="Cannot change status of an admin account"
        )

    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"active": status.active}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User status updated successfully"}


def delete_user_controller(user_id, admin):
    """Admin-only: delete a user. Cannot delete self or other admin accounts."""

    # Prevent self-deletion
    if user_id == admin["id"]:
        raise HTTPException(
            status_code=400,
            detail="You cannot delete your own account"
        )

    target = users_collection.find_one({"_id": ObjectId(user_id)})
    if not target:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent deleting another admin
    if target.get("role") == "admin":
        raise HTTPException(
            status_code=403,
            detail="Cannot delete an admin account"
        )

    # Delete all issues/book requests associated with the user
    issues_collection.delete_many({"user_id": user_id})

    # Delete the user
    result = users_collection.delete_one({"_id": ObjectId(user_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "User and all related data deleted successfully"}


def update_profile_controller(current_user, data):
    user_id = current_user["id"]

    # Check email uniqueness if changed
    existing = users_collection.find_one({"email": data.email})
    if existing and str(existing["_id"]) != user_id:
        raise HTTPException(
            status_code=400,
            detail="Email already in use by another account"
        )

    result = users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"name": data.name, "email": data.email}}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return {"message": "Profile updated successfully"}


def change_password_controller(current_user, data):
    user_id = current_user["id"]

    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(data.current_password, user["password"]):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if len(data.new_password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Password cannot exceed 72 bytes")

    if len(data.new_password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    users_collection.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"password": hash_password(data.new_password)}}
    )

    return {"message": "Password changed successfully"}
