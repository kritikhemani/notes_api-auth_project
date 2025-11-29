from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.deps import get_current_user, get_db
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate, NoteRead

router = APIRouter(prefix="/notes", tags=["notes"])