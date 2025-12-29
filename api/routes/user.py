from fastapi import APIRouter
from db.session import SessionDep
from services.user import create_user_service 
from schemas.user import UserResponse, UserCreate

router = APIRouter()

@router.post("/users")
def create_user(user: UserCreate, db_session : SessionDep) -> UserResponse:
    created_user = create_user_service(user, db_session)
    return created_user

