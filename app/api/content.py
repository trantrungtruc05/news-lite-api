from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.get_db import get_db
from app.service.crawl import crawl_content_to_db
from app.repo import news_content
from app.schema.news_content import NewsContentOut
from typing import List

router = APIRouter()

@router.post("/content/crawl/")
def test(db: Session = Depends(get_db)):
    
    crawl_content_to_db(db)
    return {"message": "Crawled content successfully"}


@router.get("/content/get_by_category_id/{category_id}", response_model=List[NewsContentOut])
def get_by_category_id(category_id: str, db: Session = Depends(get_db)):
    return news_content.get_news_content_by_category_id(db, category_id)