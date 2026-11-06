from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select, Field, SQLModel
from typing import List
from app.db import get_session 

router = APIRouter(prefix="/videos", tags=["Comments"])

class Comment(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    video_id: int = Field(foreign_key="video.id") 
    texto: str
    user: str

class CommentCreate(SQLModel):
    texto: str
    user: str

@router.get("/{video_id}/comments", response_model=List[Comment])
def get_comments(video_id: int, session: Session = Depends(get_session)):
    statement = select(Comment).where(Comment.video_id == video_id)
    comments = session.exec(statement).all()
    return comments

@router.post("/{video_id}/comments", response_model=Comment)
def create_comment(video_id: int, comment_data: CommentCreate, session: Session = Depends(get_session)):

    new_comment = Comment(
        video_id=video_id,
        texto=comment_data.texto,
        user=comment_data.user
    )
    session.add(new_comment)
    session.commit()
    session.refresh(new_comment)
    return new_comment