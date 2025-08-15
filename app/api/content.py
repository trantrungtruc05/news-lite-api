from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.get_db import get_db
from app.service.crawl import crawl_content_to_db

router = APIRouter()

@router.post("/content/crawl/")
def test(db: Session = Depends(get_db)):
    
    crawl_content_to_db(db)
    return {"message": "Crawled content successfully"}
