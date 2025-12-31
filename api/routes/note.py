from fastapi import APIRouter
from schemas.note import NoteCreate, NoteResponse
from db.session import SessionDep
from services.note import create_note_for_user_service

note = APIRouter(prefix="/notes", tags=["notes"])  

@note.post("/{user_id}")
def create_note(user_id: int, note: NoteCreate, session: SessionDep) -> NoteResponse:
    created_note = create_note_for_user_service(user_id, note, session)
    return created_note
