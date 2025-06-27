from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app import models, schemas
import os
from dotenv import load_dotenv

load_dotenv()

# Secret and algorithm
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def register_user(user: schemas.UserCreate, db: Session):
    existing_user = db.query(models.User).filter(
        (models.User.email == user.email) | 
        (models.User.username == user.username)
    ).first()
    if existing_user:
        return None  # User already exists

    hashed_password = hash_password(user.password)
    new_user = models.User(
    username=user.username,
    email=user.email,
    hashed_password=hashed_password,
    role=user.role,
    manager_id=user.manager_id
)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
