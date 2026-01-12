from fastapi import APIRouter, Depends
from schemas.note import NoteCreate, NoteResponse
from core.security import GetCurrentUser
from db.session import SessionDep
from models.models import User
from services.note import create_note_for_user_service, get_notes_for_user_service, get_note_for_user_service, delete_note_for_user_service

note = APIRouter(prefix="/notes", tags=["notes"])  

@note.post("/")
def create_note( note: NoteCreate, session: SessionDep, user : GetCurrentUser,) -> NoteResponse:
    created_note = create_note_for_user_service(user.email, note, session)
    return created_note

@note.get("/")
def get_notes_for_user(session: SessionDep, user: GetCurrentUser) -> list[NoteResponse]:
    notes = get_notes_for_user_service(user.email, session)
    return notes

@note.get("/{title}")
def get_note_for_user(title: str, session: SessionDep, user: GetCurrentUser) -> NoteResponse:
    note = get_note_for_user_service(user.email, title, session)
    return note

@note.delete("/{title}")
def delete_note_for_user(title: str, session: SessionDep, user: GetCurrentUser):
    note = delete_note_for_user_service(user.email, title, session)
    return note
  
