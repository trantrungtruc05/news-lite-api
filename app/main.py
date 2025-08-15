from fastapi import FastAPI
from app.db.session import engine
from app.db.base import Base
from app.api import category, content

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(category.router, prefix="/api/v1", tags=["Categories"])
app.include_router(content.router, prefix="/api/v1", tags=["New Content"])