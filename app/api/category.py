import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repo import category
from app.schema.category import CategoryIn, CategoryOut
from app.repo.category import create_category, get_all_categories
from app.db.session import SessionLocal
import requests
from bs4 import BeautifulSoup
from app.service.crawl import crawl_category_to_db
from app.db.get_db import get_db

router = APIRouter()




@router.get("/categories", response_model=list[CategoryOut])
def read_all(db: Session = Depends(get_db)):
    return category.get_all_categories(db)


@router.post("/categories/crawl/")
def create(db: Session = Depends(get_db)):
    crawl_category_to_db(db)
    return {"message": "Crawled categories successfully"}