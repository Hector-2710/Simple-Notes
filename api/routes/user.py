from fastapi import APIRouter
from db.session import SessionDep
from services.user import create_user_service 
from schemas.user import UserResponse, UserCreate
from exceptions.responses import EmailAlreadyExists, DatabaseError

user = APIRouter(prefix="/users", tags=["Users"])

@user.post("/", description="Create a new user",response_description="User created successfully", responses={409: {"model": EmailAlreadyExists,"description": "User with this email already exists"}, 500: {"model": DatabaseError,"description": "A database error occurred"}},summary="Create User",status_code=201)
def create_user(user: UserCreate, db_session : SessionDep) -> UserResponse:
    created_user = create_user_service(user, db_session)
    return created_user

