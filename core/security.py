from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Annotated

import jwt  # Ahora usa PyJWT
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash # Nueva recomendación para hashing
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.settings import settings
from db.session import SessionDep
from schemas.token import TokenData
from models.models import User
from exceptions.excep import InvalidToken, UserNotExists

# Configuración de hashing (usa Argon2id por defecto, que es más seguro que bcrypt)
password_hash_context = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def password_hash(password: str) -> str:
    return password_hash_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash_context.verify(plain_password, hashed_password)

def create_access_token(data: Dict[str, Any]) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # PyJWT maneja objetos datetime directamente para la clave 'exp'
    to_encode.update({"exp": expire, "iat": now})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub: str | None = payload.get("sub")
        if sub is None:
            # Reutilizamos tu excepción personalizada
            raise InvalidToken()
        return TokenData(sub=sub)
    except InvalidTokenError: # Cambio de JWTError a InvalidTokenError
        raise InvalidToken() 

def get_current_user(db_session: SessionDep, token: Annotated[str, Depends(oauth2_scheme)]) -> User:
    from services.user import get_user_by_email  
    
    token_data = decode_token(token)
    user = get_user_by_email(token_data.sub, db_session)
    
    if not user:
        raise UserNotExists(email=token_data.sub)
    return user

# Alias para usar en los Endpoints
GetCurrentUser = Annotated[User, Depends(get_current_user)]