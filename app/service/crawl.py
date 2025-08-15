import requests
from bs4 import BeautifulSoup
from app.schema.category import CategoryIn
from app.repo import category
import datetime
from sqlalchemy.orm import Session
from app.schema.news_content import NewsContentIn
from app.repo import news_content



def crawl_content_to_db(db: Session):

    categories = category.get_all_categories(db)

    for cat in categories:
        res = requests.get(cat.link)
        soup = BeautifulSoup(res.text, "html.parser")

        card_content_tags = soup.select("div.loop-card__content")
        all_href, titles = [card_content_tag.find('h3').find('a')['href'] for card_content_tag in card_content_tags], [card_content_tag.find('h3').find('a').get_text(strip=True) for card_content_tag in card_content_tags]
        print("======= CATEGORY: ", cat.name, " =======")

        for href, title in zip(all_href, titles):
        
            res_content = requests.get(href)
            soup_content = BeautifulSoup(res_content.text, "html.parser")
            
            main_content = soup_content.select("main.wp-block-group.template-content")
            
            p_tags = main_content[0].find("div", class_="entry-content wp-block-post-content is-layout-constrained wp-block-post-content-is-layout-constrained").find_all("p")

            full_content = ""
            for p_tag in p_tags:
                full_content += p_tag.get_text() + " "


            newsContentCreate = NewsContentIn(content=full_content, category_id=cat.category_id, title=title, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
            news_content.create_news_content(db, newsContentCreate)
            print("--------------------------------")    
            print(f""" Link: {href} """)
            print("--------------------------------")


def crawl_category_to_db(db: Session):
    category.delete_all_categories(db)
    URL = "https://techcrunch.com"
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, "html.parser")

    li_tags = soup.select("div.wp-block-techcrunch-main-navigation__inner")[0].find_all("li")

    for li_tag in li_tags:
        a_tag = li_tag.find("a")
        href = a_tag["href"]
        print(href)
        
        categoryCreate = CategoryIn(name=li_tag.get_text(strip=True), link=f"""{URL}{href}""", category_id="techcrunch", source="techcrunch", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        category.create_category(db, categoryCreate)
        print("Created category: ", li_tag.get_text(strip=True))



