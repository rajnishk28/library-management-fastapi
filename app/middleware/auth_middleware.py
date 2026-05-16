from fastapi import Header, HTTPException, Depends
from app.utils.jwt_handler import verify_access_token
from app.models.user_model import users_collection
from bson import ObjectId


def verify_token(authorization: str = Header(None)):

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )

    token = authorization.split(" ")[1]

    payload = verify_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    db_user = users_collection.find_one({
        "_id": ObjectId(payload["id"])
    })

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if db_user.get("active") is False:
        raise HTTPException(
            status_code=403,
            detail="Account is deactivated"
        )

    return payload

def admin_only(
    user=Depends(verify_token)
):

    if user["role"] != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )

    return user    
