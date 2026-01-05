from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=20)

class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created : bool 