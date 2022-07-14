from datetime import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup

import database
import models
from database import SessionLocal, engine
from sqlalchemy.orm import Session

from models import Price

product_url = "https://hoff.ru/catalog/tovary_dlya_doma/tekstil/postelnoe_bele/"


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def parse_soup_from_page(products_url:str):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(products_url)

    html = driver.page_source

    driver.close()
    driver.quit()
    return html


def parse_prices_from_page(products_url:str):
    html = parse_soup_from_page(products_url)
    print(html)
    soup = BeautifulSoup(html, "lxml")

    title = soup.find_all(class_="product-name")
    price = soup.find_all(class_="current-price")
    print("\n ################# \n")
    print(len(price), len(title))
    print("\n ################# \n")

    prices = []

    for i in range(min(len(title), len(price))):
        print(title[i].get_text(), price[i].get_text(), int(price[i].get_text().replace(' ', '').replace('P', '')))
        prices.append(Price(name = title[i].get_text(),
                            url=title[i]['href'],
                            price=price[i].get_text(),
                            price_int=int(price[i].get_text().replace(' ', '').replace('P', '')),
                            datetime=datetime.now()))

    return prices


def insert_parsed_data_to_db(db: Session):
    prices = parse_prices_from_page(product_url)
    for price in prices:
        db.add(price)
        db.commit()
        db.refresh(price)

def fill_db():
    models.Base.metadata.create_all(bind=engine)
    session = database.SessionLocal()
    insert_parsed_data_to_db(db=session)
