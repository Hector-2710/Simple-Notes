from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=20)
    password: str = Field(min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserResponse(BaseModel):
    id: int
    email: EmailStr