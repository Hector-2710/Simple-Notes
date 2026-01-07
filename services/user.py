from sqlmodel import Session, select
from models.models import User
from exceptions.excep import EmailAlreadyExists, DatabaseError, UserNotExists, InvalidPassword
from schemas.user import UserResponse, UserCreate
from core.security import password_hash
from schemas.token import Token
from core.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

def create_user_service(user_data: UserCreate, db_session: Session) -> UserResponse:
    if get_user_by_email(user_data.email, db_session):
        raise EmailAlreadyExists(user_data.email)

    try:
        new_user = User(email=user_data.email, username=user_data.username, password=password_hash(user_data.password))
        db_session.add(new_user)
        db_session.commit() 
        db_session.refresh(new_user)
        return UserResponse(id=new_user.id, email=new_user.email, created=True)
    
    except Exception as e:  
        db_session.rollback()
        raise DatabaseError()
    
def login_service(form_data: OAuth2PasswordRequestForm, db_session: Session) -> Token:
    user = get_user_by_email(form_data.username, db_session)
    if not user:
        raise UserNotExists(email=form_data.username) 
    
    if not verify_password(form_data.password, user.password):
        raise InvalidPassword()  

    access_token = create_access_token({"sub": user.email})
    return Token(access_token=access_token, token_type="bearer")

    
def get_user_by_email(email: str, db_session: Session) -> User | None:
    statement = select(User).where(User.email == email)
    return db_session.exec(statement).first()