from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from dotenv import load_dotenv
import os

from app.database.connection import SessionLocal
from app.models.user import User

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# создает экземпляр 
oauth2_scheme = OAuth2PasswordBearer(
    # 
    tokenUrl= "/users/login"
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        