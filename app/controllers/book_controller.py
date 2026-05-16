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


def get_books_controller():

    books = []

    for book in books_collection.find():

        book["_id"] = str(book["_id"])

        books.append(book)

    return books


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
