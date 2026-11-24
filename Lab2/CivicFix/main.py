from pydantic import BaseModel

from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import User, Issue, Comment


# Run when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


# Create the FastAPI application
app = FastAPI(lifespan=lifespan)

class UserCreate(BaseModel):
    email: str
    role: str = "resident"

class IssueCreate(BaseModel):
    title: str
    description: str
    category: str
    location: str
    reporter_id: int

class CommentCreate(BaseModel):
    body: str
    author_id: int

# GET all issues with optional filters
@app.get("/issues", response_model=list[Issue])
def list_issues(
    status: str | None = None,
    category: str | None = None,
    session: Session = Depends(get_session)
):
    statement = select(Issue)

    if status:
        statement = statement.where(Issue.status == status)

    if category:
        statement = statement.where(Issue.category == category)

    issues = session.exec(statement).all()

    return issues

# GET a specific issue
@app.get("/issues/{issue_id}", response_model=Issue)
def get_issue(
    issue_id: int,
    session: Session = Depends(get_session)
):
    issue = session.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    return issue

# UPDATE an existing issue
@app.put("/issues/{issue_id}", response_model=Issue)
def update_issue(
    issue_id: int,
    issue_data: IssueCreate,
    session: Session = Depends(get_session)
):
    issue = session.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    reporter = session.get(User, issue_data.reporter_id)

    if not reporter:
        raise HTTPException(
            status_code=404,
            detail="Reporter not found"
        )

    issue.title = issue_data.title
    issue.description = issue_data.description
    issue.category = issue_data.category
    issue.location = issue_data.location
    issue.reporter_id = issue_data.reporter_id

    session.add(issue)
    session.commit()
    session.refresh(issue)

    return issue

# DELETE an existing issue
@app.delete("/issues/{issue_id}")
def delete_issue(
    issue_id: int,
    session: Session = Depends(get_session)
):
    issue = session.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    session.delete(issue)
    session.commit()

    return {"message": "Issue deleted"}

# POST a comment on an issue
@app.post("/issues/{issue_id}/comments", response_model=Comment, status_code=201)
def create_comment(
    issue_id: int,
    comment_data: CommentCreate,
    session: Session = Depends(get_session)
):
    # Check whether the issue exists
    issue = session.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    # Check whether the author exists
    author = session.get(User, comment_data.author_id)

    if not author:
        raise HTTPException(
            status_code=404,
            detail="Author not found"
        )

    # Create the comment
    comment = Comment(
        body=comment_data.body,
        author_id=comment_data.author_id,
        issue_id=issue_id
    )

    session.add(comment)
    session.commit()
    session.refresh(comment)

    return comment

# GET all comments for a specific issue
@app.get("/issues/{issue_id}/comments", response_model=list[Comment])
def get_issue_comments(
    issue_id: int,
    session: Session = Depends(get_session)
):
    # Check whether the issue exists
    issue = session.get(Issue, issue_id)

    if not issue:
        raise HTTPException(
            status_code=404,
            detail="Issue not found"
        )

    # Retrieve comments belonging to this issue
    statement = select(Comment).where(Comment.issue_id == issue_id)
    comments = session.exec(statement).all()

    return comments  

# GET all comments written by a specific user
@app.get("/users/{user_id}/comments", response_model=list[Comment])
def get_user_comments(
    user_id: int,
    session: Session = Depends(get_session)
):
    # Check whether the user exists
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Retrieve comments written by this user
    statement = select(Comment).where(Comment.author_id == user_id)
    comments = session.exec(statement).all()

    return comments

@app.post("/users", response_model=User, status_code=201)
def create_user(
    user_data: UserCreate,
    session: Session = Depends(get_session)
):
    user = User(
        email=user_data.email,
        role=user_data.role
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@app.post("/issues", response_model=Issue, status_code=201)
def create_issue(
    issue_data: IssueCreate,
    session: Session = Depends(get_session)
):
    # Check whether the reporter exists
    reporter = session.get(User, issue_data.reporter_id)

    if not reporter:
        raise HTTPException(
            status_code=404,
            detail="Reporter not found"
        )

    # Create the issue
    issue = Issue(
        title=issue_data.title,
        description=issue_data.description,
        category=issue_data.category,
        location=issue_data.location,
        reporter_id=issue_data.reporter_id,
        status="Reported"
    )

    # Save the issue
    session.add(issue)
    session.commit()
    session.refresh(issue)

    return issue