from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas
from .auth import verify_admin
from .database import get_db

router = APIRouter(prefix="/admin", tags=["admin"])

# User management
@router.get("/users", response_model=List[schemas.User])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/users/{user_id}", response_model=schemas.User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.delete("/users/{user_id}")
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Content management
@router.get("/albums", response_model=List[schemas.Album])
async def list_all_albums(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    albums = db.query(models.Album).offset(skip).limit(limit).all()
    return albums

@router.delete("/albums/{album_id}")
async def delete_album(
    album_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    album = db.query(models.Album).filter(models.Album.id == album_id).first()
    if not album:
        raise HTTPException(status_code=404, detail="Album not found")
    db.delete(album)
    db.commit()
    return {"message": "Album deleted successfully"}

@router.get("/messages", response_model=List[schemas.Message])
async def list_all_messages(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    messages = db.query(models.Message).offset(skip).limit(limit).all()
    return messages

@router.delete("/messages/{message_id}")
async def delete_message(
    message_id: int,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(message)
    db.commit()
    return {"message": "Message deleted successfully"}

# System statistics
@router.get("/stats")
async def get_system_stats(
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    total_users = db.query(models.User).count()
    total_albums = db.query(models.Album).count()
    total_photos = db.query(models.Photo).count()
    total_messages = db.query(models.Message).count()
    total_tasks = db.query(models.Task).count()
    total_events = db.query(models.Event).count()
    completed_tasks = db.query(models.Task).filter(models.Task.completed == True).count()

    return {
        "total_users": total_users,
        "total_albums": total_albums,
        "total_photos": total_photos,
        "total_messages": total_messages,
        "total_tasks": total_tasks,
        "total_events": total_events,
        "completed_tasks": completed_tasks,
        "task_completion_rate": f"{(completed_tasks/total_tasks)*100:.1f}%" if total_tasks > 0 else "0%"
    }

# Content moderation
@router.post("/messages/{message_id}/moderate")
async def moderate_message(
    message_id: int,
    action: str,  # "hide" or "delete"
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    message = db.query(models.Message).filter(models.Message.id == message_id).first()
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if action == "delete":
        db.delete(message)
        db.commit()
        return {"message": "Message deleted successfully"}
    elif action == "hide":
        message.is_hidden = True
        db.commit()
        return {"message": "Message hidden successfully"}
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

# System settings
@router.post("/settings")
async def update_system_settings(
    settings: dict,
    db: Session = Depends(get_db),
    _: models.User = Depends(verify_admin)
):
    # Update system settings (implement as needed)
    return {"message": "Settings updated successfully"}
