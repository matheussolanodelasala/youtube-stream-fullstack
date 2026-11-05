from sqlmodel import select, func
from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from app.db import SessionDep
from app.models import Videos

router = APIRouter(prefix="/videos", tags=["Videos"])

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

# --- NUEVO ENDPOINT PARA ELIMINAR VIDEOS ---
@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_video(id: int, session: SessionDep):
    video_db = session.get(Videos, id)
    if not video_db:
        raise HTTPException(status_code=404, detail="El video no fue encontrado")
    
    session.delete(video_db)
    session.commit()
    return {"mensaje": "Video eliminado con éxito de la base de datos"}