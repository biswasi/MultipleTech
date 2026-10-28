from pydantic import BaseModel, EmailStr
from typing import Optional

class CustomerCreate(BaseModel):
    id: str  # Unique customer ID or UUID
    name: str
    email: EmailStr
    tier: Optional[str] = "Standard"

class CustomerUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    tier: Optional[str] = None
