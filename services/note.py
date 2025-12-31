from sqlmodel import Session
from models.models import Note, User
from exceptions.excep import UserNotExists, DatabaseError
from schemas.note import NoteCreate, NoteResponse

def create_note_for_user_service(user_id: int, note: NoteCreate, db_session: Session) -> NoteResponse:
    user = db_session.get(User, user_id)
    if not user:
        raise UserNotExists(user_id)
    
    try:
        new_note = Note(title=note.title, content=note.content)
        new_note.users.append(user)
        db_session.add(new_note)
        db_session.commit()
        db_session.refresh(new_note)
        return NoteResponse(id=new_note.id, title=new_note.title, content=new_note.content, created=True)
       
    except Exception as e:
        db_session.rollback()
        raise DatabaseError()