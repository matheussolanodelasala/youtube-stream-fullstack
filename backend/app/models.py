from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Videos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    descripcion: str
    category: str = Field(index=True)
    source: str
    thumbnail_url: str
    es_publico: bool = True
    
    comments: List["Comments"] = Relationship(
        back_populates="video", 
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

class Comments(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    content: str
    video_id: Optional[int] = Field(default=None, foreign_key="videos.id")
    
    video: Optional[Videos] = Relationship(back_populates="comments")