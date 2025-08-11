from sqlalchemy import Column, Integer, String, DateTime
from app.db.base import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    link = Column(String, nullable=False)
    category_id = Column(Integer, nullable=True)
    source = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)