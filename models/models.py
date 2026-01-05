from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional

class User_Has_Note(SQLModel, table=True):
    user_id: int = Field(foreign_key="user.id", primary_key=True)
    note_id: int = Field(foreign_key="note.id", primary_key=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str 
    email: str = Field(unique=True, index=True)     
    notes: List["Note"] = Relationship(back_populates="users", link_model=User_Has_Note)

class Note(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    users: List["User"] = Relationship(back_populates="notes", link_model=User_Has_Note)