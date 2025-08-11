from sqlalchemy.orm import Session
from app.models.category import Category
from app.schema.category import CategoryIn, CategoryOut 
from datetime import datetime

def create_category(db: Session, category: CategoryIn):
    db_category = Category(
        name=category.name,
        link=category.link,
        category_id=category.category_id,
        source=category.source,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_all_categories(db: Session):
    return db.query(Category).all()

def delete_all_categories(db: Session):
    db.query(Category).delete()
    db.commit()