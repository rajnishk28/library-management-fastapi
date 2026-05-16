from app.models.book_model import books_collection
from app.models.user_model import users_collection
from app.models.issue_model import issues_collection
from bson import ObjectId


def get_admin_stats_controller():
    """Lightweight stats for the admin dashboard — no N+1 queries."""

    total_books = books_collection.count_documents({})
    total_copies = 0
    available_copies = 0
    for b in books_collection.find({}, {"quantity": 1, "available": 1}):
        total_copies += b.get("quantity", 0)
        available_copies += b.get("available", 0)

    total_users = users_collection.count_documents({"role": "user"})
    active_users = users_collection.count_documents({"role": "user", "active": {"$ne": False}})

    pending = issues_collection.count_documents({"status": "pending"})
    alloted = issues_collection.count_documents({"status": "alloted"})
    return_requested = issues_collection.count_documents({"status": "return_requested"})
    returned = issues_collection.count_documents({"status": "returned"})
    rejected = issues_collection.count_documents({"status": "rejected"})
    total_issues = issues_collection.count_documents({})

    return {
        "books": {
            "total": total_books,
            "total_copies": total_copies,
            "available_copies": available_copies,
            "issued_copies": total_copies - available_copies,
        },
        "users": {
            "total": total_users,
            "active": active_users,
            "inactive": total_users - active_users,
        },
        "requests": {
            "total": total_issues,
            "pending": pending,
            "alloted": alloted,
            "return_requested": return_requested,
            "returned": returned,
            "rejected": rejected,
        },
    }


def get_user_stats_controller(current_user):
    """Stats for a specific user's dashboard."""
    user_id = current_user["id"]

    pending = issues_collection.count_documents({"user_id": user_id, "status": "pending"})
    alloted = issues_collection.count_documents({"user_id": user_id, "status": "alloted"})
    return_requested = issues_collection.count_documents({"user_id": user_id, "status": "return_requested"})
    returned = issues_collection.count_documents({"user_id": user_id, "status": "returned"})
    rejected = issues_collection.count_documents({"user_id": user_id, "status": "rejected"})
    total = issues_collection.count_documents({"user_id": user_id})

    total_books = books_collection.count_documents({})
    available_books = books_collection.count_documents({"available": {"$gt": 0}})

    return {
        "issues": {
            "total": total,
            "pending": pending,
            "alloted": alloted,
            "return_requested": return_requested,
            "returned": returned,
            "rejected": rejected,
        },
        "library": {
            "total_books": total_books,
            "available_books": available_books,
        },
    }
