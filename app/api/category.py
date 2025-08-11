import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.repo import category
from app.schema.category import CategoryIn, CategoryOut
from app.repo.category import create_category, get_all_categories
from app.db.session import SessionLocal
import requests
from bs4 import BeautifulSoup
from app.service.summary import get_url_to_summary

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/categories", response_model=list[CategoryOut])
def read_all(db: Session = Depends(get_db)):
    return category.get_all_categories(db)


@router.post("/categories/crawl/")
def create(db: Session = Depends(get_db)):

    category.delete_all_categories(db)
    url = "https://vnexpress.net/"

    # Gửi request lấy HTML
    res = requests.get(url)
    res.raise_for_status()

    # Parse HTML
    soup = BeautifulSoup(res.text, "html.parser")

    # Tìm thẻ ul với class="parent"
    ul_tags = soup.select('section#wrap-main-nav ul.parent')

    # Tìm các thẻ li có data-id
    li_with_data_id = []
    for ul_tag in ul_tags:
        li_elements = ul_tag.find_all('li', attrs={"data-id": True})
        li_with_data_id.extend(li_elements)
    

    # Trích xuất data-id, href và text
    for li in li_with_data_id:
        data_id = li['data-id']
        a_tag = li.find('a')
        
        if a_tag and a_tag.has_attr('href'):
            href = f"https://vnexpress.net{a_tag['href']}"
            value = a_tag.get_text(strip=True)
            print(value)
            categoryCreate = CategoryIn(name=value, link=href, category_id=data_id, source="vnexpress", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            category.create_category(db, categoryCreate)
            print("Created category: ", value)

    return {"message": "Crawled categories successfully"}




@router.post("/categories/test/")
def test(db: Session = Depends(get_db)):
    resp = requests.get("https://vnexpress.net/thoi-su")
    soup = BeautifulSoup(resp.text, 'html.parser')
    titles = [a['href'] for section in soup.find_all('section') 
              for h3 in section.find_all('h3')
              for a in h3.find_all('a') if a.has_attr('title')]
    
    print(len(titles))

    for title in titles:
        print(get_url_to_summary(title))

    return {"message": "Crawled content successfully"}