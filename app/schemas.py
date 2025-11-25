from pydantic import BaseModel, Field, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    role: str = "user"
    
class UserRead(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool
    
