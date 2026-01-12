from sqlmodel import Session, select
from models.models import Note, User
from exceptions.excep import UserNotExists, DatabaseError, NoteNotFound
from schemas.note import NoteCreate, NoteResponse

def create_note_for_user_service(user_email: str, note: NoteCreate, db_session: Session) -> NoteResponse:
    statement = select(User).where(User.email == user_email)
    user = db_session.exec(statement).first()
    if not user:
        raise UserNotExists(user_email)
    
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
    
def get_notes_for_user_service(user_email: str, db_session: Session) -> list[NoteResponse]:
    statement = select(User).where(User.email == user_email)
    user = db_session.exec(statement).first()
    
    if not user:
        raise UserNotExists(user_email)
    
    return [
        NoteResponse(id=note.id, title=note.title, content=note.content, created=True) 
        for note in user.notes
    ]

def get_note_for_user_service(user_email: str, title: str, db_session: Session) -> NoteResponse:
    statement = select(User).where(User.email == user_email)
    user = db_session.exec(statement).first()
    
    if not user:
        raise UserNotExists(user_email)
    
    for note in user.notes:
        if note.title == title:
            return NoteResponse(id=note.id, title=note.title, content=note.content)
    
    raise NoteNotFound(title)

def delete_note_for_user_service(user_email: str, title: str, db_session: Session):
    statement = select(User).where(User.email == user_email)
    user = db_session.exec(statement).first()
    
    if not user:
        raise UserNotExists(user_email)
    
    for note in user.notes:
        if note.title == title:
            try:
                user.notes.remove(note)
                db_session.delete(note)
                db_session.commit()
                return NoteResponse(id=note.id, title=note.title, content=note.content)
            except Exception as e:
                db_session.rollback()
                raise DatabaseError()
    
    raise NoteNotFound(title)