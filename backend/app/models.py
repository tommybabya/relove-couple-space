from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Text
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql import func
from .database import Base
from .schemas import UserCreate, UserLogin, AlbumCreate, PhotoCreate, MessageCreate, TaskCreate, EventCreate
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
import jwt

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = "your-secret-key"  # In production, use environment variable
ALGORITHM = "HS256"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String)
    hashed_password = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    albums = relationship("Album", back_populates="owner")
    messages = relationship("Message", back_populates="sender")
    tasks = relationship("Task", back_populates="owner")
    events = relationship("Event", back_populates="owner")

    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def create(db: Session, user: UserCreate):
        hashed_password = pwd_context.hash(user.password)
        db_user = User(email=user.email, name=user.name, hashed_password=hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def authenticate(db: Session, user_credentials: UserLogin):
        user = User.get_by_email(db, user_credentials.email)
        if not user or not pwd_context.verify(user_credentials.password, user.hashed_password):
            return None
        return user

    @staticmethod
    def create_token(user) -> dict:
        access_token_expires = timedelta(minutes=30)
        access_token = create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}

class Album(Base):
    __tablename__ = "albums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="albums")
    photos = relationship("Photo", back_populates="album")

    @staticmethod
    def get_all(db: Session, user_id: int):
        return db.query(Album).filter(Album.user_id == user_id).all()

    @staticmethod
    def create(db: Session, album: AlbumCreate, user_id: int):
        db_album = Album(**album.dict(), user_id=user_id)
        db.add(db_album)
        db.commit()
        db.refresh(db_album)
        return db_album

class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    description = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    album_id = Column(Integer, ForeignKey("albums.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    album = relationship("Album", back_populates="photos")

    @staticmethod
    def create(db: Session, photo: PhotoCreate, album_id: int, user_id: int):
        db_photo = Photo(**photo.dict(), album_id=album_id, user_id=user_id)
        db.add(db_photo)
        db.commit()
        db.refresh(db_photo)
        return db_photo

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    type = Column(String)  # text, sticker, image
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    sender = relationship("User", back_populates="messages")

    @staticmethod
    def get_all(db: Session, user_id: int):
        return db.query(Message).filter(Message.user_id == user_id).all()

    @staticmethod
    def create(db: Session, message: MessageCreate, user_id: int):
        db_message = Message(**message.dict(), user_id=user_id)
        db.add(db_message)
        db.commit()
        db.refresh(db_message)
        return db_message

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="tasks")

    @staticmethod
    def get_all(db: Session, user_id: int):
        return db.query(Task).filter(Task.user_id == user_id).all()

    @staticmethod
    def create(db: Session, task: TaskCreate, user_id: int):
        db_task = Task(**task.dict(), user_id=user_id)
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        return db_task

    @staticmethod
    def complete(db: Session, task_id: int, user_id: int):
        task = db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()
        if task:
            task.completed = True
            task.completed_at = datetime.now()
            db.commit()
            db.refresh(task)
        return task

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String, nullable=True)
    date = Column(DateTime(timezone=True))
    type = Column(String)  # anniversary, memory, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="events")

    @staticmethod
    def get_all(db: Session, user_id: int):
        return db.query(Event).filter(Event.user_id == user_id).all()

    @staticmethod
    def create(db: Session, event: EventCreate, user_id: int):
        db_event = Event(**event.dict(), user_id=user_id)
        db.add(db_event)
        db.commit()
        db.refresh(db_event)
        return db_event

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
