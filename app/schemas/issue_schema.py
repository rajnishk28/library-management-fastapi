from pydantic import BaseModel, field_validator

VALID_STATUSES = ["pending", "alloted", "return_requested", "returned", "rejected"]


class IssueSchema(BaseModel):
    user_id: str
    book_id: str
    issue_date: str
    due_date: str


class IssueStatusSchema(BaseModel):
    status: str

    @field_validator("status")
    def status_must_be_valid(cls, value):
        if value not in VALID_STATUSES:
            raise ValueError(f"Status must be one of: {', '.join(VALID_STATUSES)}")
        return value
