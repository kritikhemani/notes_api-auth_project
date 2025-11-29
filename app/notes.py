from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.deps import get_current_user, get_db
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])

@router.post("/", response_model=NoteRead)
def create_note(payload: NoteCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = Note(title=payload.title, content=payload.content, owner_id=user.id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note

@router.get("/", response_model=list[NoteRead])
def read_notes(skip: int = Query(0, ge=0), limit: int = Query(10, le=100), db: Session = Depends(get_db), user=Depends(get_current_user)):
    notes = db.query(Note).filter(Note.owner_id == user.id).offset(skip).limit(limit).all()
    return notes