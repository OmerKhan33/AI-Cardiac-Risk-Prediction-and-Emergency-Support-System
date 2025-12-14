from typing import Optional
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from src.models.user_model import User

class Prediction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Link to the User Table
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional[User] = Relationship(back_populates="predictions")
    
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    # Medical Data
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    
    # Results
    prediction: int
    probability: float
    risk_label: str