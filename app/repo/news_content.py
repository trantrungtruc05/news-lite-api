from sqlalchemy.orm import Session
from app.models.news_content import NewsContent
from app.schema.news_content import NewsContentIn
from datetime import datetime


def create_news_content(db: Session, news_content: NewsContentIn):
    db_news_content = NewsContent(
        content=news_content.content,
        category_id=news_content.category_id,
        title=news_content.title,
        href=news_content.href,
        summary_content=news_content.summary_content,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_news_content)
    db.commit()
    db.refresh(db_news_content)
    return db_news_content

def get_news_content_by_href(db: Session, href: str):
    return db.query(NewsContent).filter(NewsContent.href == href).first()

def get_news_content_by_category_id(db: Session, category_id: str):
    return db.query(NewsContent).filter(NewsContent.category_id == category_id).all()