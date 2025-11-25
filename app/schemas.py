from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str
    
class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
