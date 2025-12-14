from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    hashed_password: str
    
    # "user" = Normal Patient, "admin" = Doctor/Admin
    role: str = Field(default="user")
    
    # Connects User to their History
    predictions: List["Prediction"] = Relationship(back_populates="user")