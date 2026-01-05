from sqlmodel import Session, select
from models.models import User
from exceptions.excep import EmailAlreadyExists, DatabaseError, UserInvalidCredentials
from schemas.user import UserResponse, UserCreate, UserLogin

def create_user_service(user_data: UserCreate, db_session: Session) -> UserResponse:
    if get_user_by_email(user_data.email, db_session):
        raise EmailAlreadyExists(user_data.email)

    try:
        new_user = User(email=user_data.email, username=user_data.username)
        db_session.add(new_user)
        db_session.commit() 
        db_session.refresh(new_user)
        return UserResponse(id=new_user.id, email=new_user.email, created=True)
    
    except Exception as e:
        db_session.rollback()
        raise DatabaseError()
    
#agregar manejo para email y password por separado
def login_user_service(login_data: UserLogin, db_session: Session) -> UserResponse:
    user = get_user_by_email(login_data.email, db_session)
    if not user or user.password != login_data.password:
        raise UserInvalidCredentials()  

    return UserResponse(id=user.id, email=user.email)
    
def get_user_by_email(email: str, db_session: Session) -> User | None:
    statement = select(User).where(User.email == email)
    return db_session.exec(statement).first()