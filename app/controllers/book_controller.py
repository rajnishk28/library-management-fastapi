from app.models.book_model import books_collection
from bson import ObjectId
from fastapi import HTTPException


def add_book_controller(book, current_user):

    book_data = book.dict()

    book_data["created_by"] = current_user["id"]

    books_collection.insert_one(book_data)

    return {
        "message": "Book added successfully"
    }


def get_books_controller(page: int = 1, limit: int = 10, search: str = None):

    skip = (page - 1) * limit
    
    # Build search filter
    filter_query = {}
    if search and search.strip():
        search_term = search.strip().lower()
        filter_query = {
            "$or": [
                {"title": {"$regex": search_term, "$options": "i"}},
                {"author": {"$regex": search_term, "$options": "i"}},
                {"category": {"$regex": search_term, "$options": "i"}}
            ]
        }
    
    total = books_collection.count_documents(filter_query)
    total_pages = max(1, -(-total // limit))  # ceiling division

    books = []
    for book in books_collection.find(filter_query).skip(skip).limit(limit):
        book["_id"] = str(book["_id"])
        books.append(book)

    return {
        "items": books,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": total_pages,
    }


def delete_book_controller(book_id):

    result = books_collection.delete_one({
        "_id": ObjectId(book_id)
    })

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book deleted successfully"
    }


def update_book_controller(book_id, book):

    update_data = {
        key: value
        for key, value in book.dict(exclude_unset=True).items()
        if value is not None
    }

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields to update"
        )

    result = books_collection.update_one(
        {"_id": ObjectId(book_id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Book not found"
        )

    return {
        "message": "Book updated successfully"
    }
