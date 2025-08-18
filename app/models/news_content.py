from sqlalchemy import Column, Integer, String, Text, DateTime
from app.db.base import Base


class NewsContent(Base):
    __tablename__ = "news_content"
    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(Text, nullable=False)
    category_id = Column(String, nullable=True)
    title = Column(String, nullable=True)
    href = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    summary_content = Column(Text, nullable=True)