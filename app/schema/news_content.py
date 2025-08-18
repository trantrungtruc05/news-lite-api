from datetime import datetime
from pydantic import BaseModel

class NewsContentIn(BaseModel):
    content: str
    category_id: str
    title: str
    href: str
    summary_content: str
    created_at: datetime
    updated_at: datetime


class NewsContentOut(BaseModel):
    id: int
    category_id: str
    title: str
    href: str
    summary_content: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True