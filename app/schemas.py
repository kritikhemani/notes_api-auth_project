from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "user"
    
class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    
    class Config:
        from_attributes = True
    
    
class NoteCreate(BaseModel):
    title: str
    content: str
    
class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    
class NoteRead(BaseModel):
    id: int
    title: str
    content: str
    owner_id: int
    
    class Config:
        from_attributes = True
