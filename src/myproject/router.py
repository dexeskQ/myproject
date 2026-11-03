from fastapi import APIRouter, status
from myproject.schemas import Pet, StatusResponse, User, UserResponse, emailResponse
from fastapi.exceptions import HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_409_CONFLICT

router = APIRouter()
users_database = dict[str, User]()
pets_database = dict[int, Pet]()
next_pet_id = 1


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

@router.get("/pets", status_code=status.HTTP_201_CREATED)
def create_pet(pet: Pet):
    global next_pet_id

    pet_id = next_pet_id
    pets_database[pet_id] = pet
    next_pet_id += 1

    return {"id":pet_id, **pet.model_dump()}

@router.post("/pets/{pet_id}")
def get_pet(pet_id: int):
    if pet_id not in pets_database:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return pets_database[pet_id]

@router.get("/pets")
def get_all_pets():
    return [
        {"id": pet_id, **pet.model_dump()}
        for pet_id, pet in pets_database.items()
    ]
