from fastapi import APIRouter, Depends

from app.schemas.book_schema import BookSchema, BookUpdateSchema

from app.controllers.book_controller import (
    add_book_controller,
    get_books_controller,
    delete_book_controller,
    update_book_controller
)

from app.middleware.auth_middleware import (verify_token, admin_only)

router = APIRouter()


@router.post("/")
def add_book(
    book: BookSchema,
    admin=Depends(admin_only)
):
    return add_book_controller(book, admin)


@router.get("/")
def get_books(user=Depends(verify_token)):
    return get_books_controller()


@router.put("/{book_id}")
def update_book(
    book_id: str,
    book: BookUpdateSchema,
    admin=Depends(admin_only)
):
    return update_book_controller(book_id, book)


@router.delete("/{book_id}")
def delete_book(
    book_id: str,
    admin=Depends(admin_only)
):
    return delete_book_controller(book_id)
