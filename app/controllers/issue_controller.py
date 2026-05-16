from fastapi import HTTPException
from bson import ObjectId

from app.models.issue_model import issues_collection
from app.models.book_model import books_collection
from app.models.user_model import users_collection

# ---------------------------------------------------------------------------
# Status transition rules
# ---------------------------------------------------------------------------
# pending        → alloted (admin approve)
# pending        → rejected (admin reject)
# alloted        → return_requested (user requests return)
# return_requested → returned (admin marks returned)
# return_requested → alloted (admin rejects return request)
# alloted        → returned (admin force-return)
# ---------------------------------------------------------------------------

ADMIN_ALLOWED_TRANSITIONS = {
    "pending": ["alloted", "rejected"],
    "alloted": ["returned"],
    "return_requested": ["returned", "alloted"],
}

USER_ALLOWED_TRANSITIONS = {
    "alloted": ["return_requested"],
}


def issue_book_controller(issue, current_user):
    if current_user["role"] != "admin" and issue.user_id != current_user["id"]:
        raise HTTPException(
            status_code=403,
            detail="You can only request books for your own account",
        )

    book = books_collection.find_one({"_id": ObjectId(issue.book_id)})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book["available"] <= 0:
        raise HTTPException(status_code=400, detail="Book unavailable")

    # Prevent duplicate pending/alloted requests for the same book by the same user
    existing = issues_collection.find_one({
        "user_id": issue.user_id,
        "book_id": issue.book_id,
        "status": {"$in": ["pending", "alloted", "return_requested"]},
    })
    if existing:
        raise HTTPException(
            status_code=400,
            detail="You already have an active request or issued copy of this book",
        )

    issue_data = issue.dict()
    issue_data["returned"] = False
    issue_data["status"] = "pending"

    issues_collection.insert_one(issue_data)
    return {"message": "Book request created successfully"}


def request_return_controller(issue_id, current_user):
    """User submits a return request — sets status to return_requested."""
    issue = issues_collection.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    if current_user["role"] != "admin" and issue["user_id"] != current_user["id"]:
        raise HTTPException(status_code=403, detail="You can only return your own books")

    current_status = issue.get("status", "alloted")

    allowed = USER_ALLOWED_TRANSITIONS if current_user["role"] != "admin" else {"alloted": ["return_requested"]}
    if current_status not in allowed or "return_requested" not in allowed[current_status]:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot request return from status '{current_status}'",
        )

    issues_collection.update_one(
        {"_id": ObjectId(issue_id)},
        {"$set": {"status": "return_requested"}},
    )
    return {"message": "Return request submitted successfully"}


def get_issues_controller(current_user):
    query = {} if current_user["role"] == "admin" else {"user_id": current_user["id"]}
    return [format_issue(issue) for issue in issues_collection.find(query)]


def update_issue_status_controller(issue_id, status_schema):
    """Admin-only: transition an issue to a new status."""
    issue = issues_collection.find_one({"_id": ObjectId(issue_id)})
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    current_status = issue.get("status", "pending")
    next_status = status_schema.status

    if current_status == next_status:
        return {"message": "Status already set"}

    allowed = ADMIN_ALLOWED_TRANSITIONS.get(current_status, [])
    if next_status not in allowed:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot transition from '{current_status}' to '{next_status}'",
        )

    book = books_collection.find_one({"_id": ObjectId(issue["book_id"])})
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = {
        "status": next_status,
        "returned": next_status == "returned",
    }

    # Decrement available when approving (pending → alloted)
    if next_status == "alloted" and current_status == "pending":
        if book["available"] <= 0:
            raise HTTPException(status_code=400, detail="Book unavailable")
        books_collection.update_one(
            {"_id": ObjectId(issue["book_id"])},
            {"$inc": {"available": -1}},
        )

    # Increment available when marking returned
    if next_status == "returned" and current_status in ("alloted", "return_requested"):
        books_collection.update_one(
            {"_id": ObjectId(issue["book_id"])},
            {"$inc": {"available": 1}},
        )

    # Admin rejects a return request → book stays alloted, no inventory change
    # (transition return_requested → alloted handled above without inventory change)

    issues_collection.update_one(
        {"_id": ObjectId(issue_id)},
        {"$set": update_data},
    )
    return {"message": "Request status updated successfully"}


def get_inventory_controller():
    """Returns inventory summary: total books, total copies, available copies."""
    books = list(books_collection.find())
    total_books = len(books)
    total_copies = sum(b.get("quantity", 0) for b in books)
    available_copies = sum(b.get("available", 0) for b in books)
    issued_copies = total_copies - available_copies

    pending_requests = issues_collection.count_documents({"status": "pending"})
    active_issues = issues_collection.count_documents({"status": "alloted"})
    return_requests = issues_collection.count_documents({"status": "return_requested"})

    return {
        "total_books": total_books,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "issued_copies": issued_copies,
        "pending_requests": pending_requests,
        "active_issues": active_issues,
        "return_requests": return_requests,
    }


def format_issue(issue):
    issue["_id"] = str(issue["_id"])

    user = users_collection.find_one({"_id": ObjectId(issue["user_id"])})
    book = books_collection.find_one({"_id": ObjectId(issue["book_id"])})

    if user:
        user["_id"] = str(user["_id"])
        user.pop("password", None)

    if book:
        book["_id"] = str(book["_id"])

    issue["user"] = user
    issue["book"] = book

    return issue
