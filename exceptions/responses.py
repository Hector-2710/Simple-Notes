from pydantic import BaseModel

class DatabaseError(BaseModel):
    detail : str = "A database error occurred"
        
class EmailAlreadyExists(BaseModel):
    detail : str = "User with this email already exists"

class invalidCredentials(BaseModel):
    detail : str = "Invalid email or password"