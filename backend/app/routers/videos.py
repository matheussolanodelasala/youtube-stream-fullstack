from sqlmodel import select, func, Field, SQLModel
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.db import SessionDep
from app.models import Videos

router = APIRouter(prefix="/videos", tags=["Videos"])

class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    video_id: int = Field(foreign_key="videos.id")
    texto: str
    user: str

class CommentCreate(SQLModel):
    texto: str
    user: str

@router.get("/", response_model=List[Videos])
def get_videos(category: Optional[str] = Query(None), session: SessionDep = None):
    query = select(Videos)
    if category:
        query = query.where(Videos.category == category)
    return session.exec(query).all()

@router.get("/recommendations", response_model=List[Videos])
def get_recommendations(category: str, current_video_id: Optional[int] = None, session: SessionDep = None):
    query = select(Videos).where(Videos.category == category)
    if current_video_id:
        query = query.where(Videos.id != current_video_id)
    return session.exec(query.order_by(func.random()).limit(10)).all()

@router.get("/{id}", response_model=Videos)
def get_video_by_id(id: int, session: SessionDep):
    video_db = session.get(Videos, id)
    if not video_db:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")
    return video_db

@router.post("/", response_model=Videos, status_code=status.HTTP_201_CREATED)
def create_video(video: Videos, session: SessionDep):
    session.add(video)
    session.commit()
    session.refresh(video)
    return video

@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_video(id: int, session: SessionDep):
    video_db = session.get(Videos, id)
    if not video_db:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")
    
    session.delete(video_db)
    session.commit()
    return {"mensaje": "Video eliminado con éxito de la base de datos"}

@router.get("/{video_id}/comments", response_model=List[Comment])
def get_comments(video_id: int, session: SessionDep):
    statement = select(Comment).where(Comment.video_id == video_id)
    return session.exec(statement).all()

@router.post("/{video_id}/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(video_id: int, comment_data: CommentCreate, session: SessionDep):
    video_db = session.get(Videos, video_id)
    if not video_db:
        raise HTTPException(status_code=404, detail="El video al que intentas comentar no existe")
        
    new_comment = Comment(
        video_id=video_id,
        texto=comment_data.texto,
        user=comment_data.user
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment