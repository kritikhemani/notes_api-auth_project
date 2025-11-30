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

@router.get("/{note_id}", response_model=NoteRead)
def get_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@router.put("/{note_id}", response_model=NoteRead)
def update_note(note_id: int, payload: NoteUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    note.title = payload.title
    note.content = payload.content
    db.commit()
    db.refresh(note)
    return note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    note = db.query(Note).filter(Note.id == note_id, Note.owner_id == user.id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(note)
    db.commit()
    return {"detail": "Note deleted"}   