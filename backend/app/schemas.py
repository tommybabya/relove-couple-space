from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

# Album schemas
class AlbumBase(BaseModel):
    name: str
    description: Optional[str] = None

class AlbumCreate(AlbumBase):
    pass

class Album(AlbumBase):
    id: int
    created_at: datetime
    user_id: int
    photos: List["Photo"] = []

    class Config:
        from_attributes = True

# Photo schemas
class PhotoBase(BaseModel):
    url: str
    description: Optional[str] = None

class PhotoCreate(PhotoBase):
    pass

class Photo(PhotoBase):
    id: int
    created_at: datetime
    album_id: int
    user_id: int

    class Config:
        from_attributes = True

# Message schemas
class MessageBase(BaseModel):
    content: str
    type: str  # text, sticker, image

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

# Task schemas
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    completed: bool
    created_at: datetime
    completed_at: Optional[datetime]
    user_id: int

    class Config:
        from_attributes = True

# Event schemas
class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    date: datetime
    type: str  # anniversary, memory, etc.

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True

# Update forward references
Album.model_rebuild()
