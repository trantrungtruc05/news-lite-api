from datetime import datetime
from pydantic import BaseModel

class CategoryIn(BaseModel):
    name: str
    link: str
    category_id: int
    source: str
    created_at: datetime
    updated_at: datetime

class CategoryOut(BaseModel):
    id: int
    name: str
    link: str
    category_id: int
    source: str
    created_at: datetime
    updated_at: datetime