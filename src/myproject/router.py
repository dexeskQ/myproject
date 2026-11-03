from collections import UserString

from fastapi import APIRouter, status
from myproject.schemas import StatusResponse, User, UserResponse, emailResponse
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT

router = APIRouter()
users_database = dict[str, User]()


@router.get("/status")
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")


@router.get("/email")
def get_email() -> emailResponse:
    return emailResponse(email="123@gmail.com")


@router.post(
    "/signup",
    status_code=HTTP_201_CREATED,
)
def signup(user: User):
    global users_database
    if user.login in users_database:
        raise HTTPException(HTTP_409_CONFLICT)
    users_database[user.login] = user


@router.get("/users/{login}")
def get_user(login: str) -> UserResponse:
    if login not in users_database:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    user = users_database[login]
    return UserResponse(name=user.name, email=user.email)
