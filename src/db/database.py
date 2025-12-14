from sqlmodel import SQLModel, create_engine, Session
# Import both models so the DB knows they exist
from src.models.user_model import User
from src.models.prediction_model import Prediction

sqlite_file_name = "heart_app.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

# check_same_thread=False is required for SQLite with FastAPI
engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session