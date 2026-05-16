from fastapi import APIRouter, Depends

from app.schemas.issue_schema import IssueSchema, IssueStatusSchema

from app.controllers.issue_controller import (
    issue_book_controller,
    request_return_controller,
    get_issues_controller,
    update_issue_status_controller,
    get_inventory_controller,
)

from app.middleware.auth_middleware import verify_token, admin_only

router = APIRouter()


@router.post("/")
def issue_book(issue: IssueSchema, user=Depends(verify_token)):
    return issue_book_controller(issue, user)


@router.put("/return/{issue_id}")
def request_return(issue_id: str, user=Depends(verify_token)):
    """User submits a return request (sets status to return_requested)."""
    return request_return_controller(issue_id, user)


@router.get("/inventory")
def get_inventory(admin=Depends(admin_only)):
    return get_inventory_controller()


@router.get("/")
def get_issues(user=Depends(verify_token)):
    return get_issues_controller(user)


@router.patch("/{issue_id}/status")
def update_issue_status(
    issue_id: str,
    status: IssueStatusSchema,
    admin=Depends(admin_only),
):
    return update_issue_status_controller(issue_id, status)
