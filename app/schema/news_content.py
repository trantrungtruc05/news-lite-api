from datetime import datetime
from pydantic import BaseModel

class NewsContentIn(BaseModel):
    content: str
    category_id: str
    title: str
    created_at: datetime
    updated_at: datetime


class NewsContentOut(BaseModel):
    id: int
    content: str
    category_id: str
    title: str
    created_at: datetime
    updated_at: datetime