from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    username: str

class UserResponse(BaseModel):
    email: str
    created : bool