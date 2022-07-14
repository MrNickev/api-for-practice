from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import crud, models, schemas
import parser
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def print_hello_phrase():
    return "Welcome to my api page"


@app.get("/prices/", response_model=List[schemas.Price])
def read_prices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    prices = crud.get_prices(db, skip=skip, limit=limit)
    return prices


@app.get("/prices/{price_id}", response_model=schemas.Price)
def read_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud.get_price(db, price_id=price_id)
    if db_price is None:
        raise HTTPException(status_code=404, detail="Price not found")
    return db_price


# пасрером заполняет базу данных данными о товарах с сайта hoff
@app.get("/prices/fill")
def fill_db():
    parser.fill_db()


@app.post("/prices/", response_model=schemas.Price)
def create_price(price: schemas.PriceCreate, db: Session = Depends(get_db)):
    db_price = crud.get_price_by_name(db, name=price.name)
    if db_price and db_price.price_int == price.price_int:
        raise HTTPException(status_code=400, detail="Price already exist")
    return crud.create_price(db=db, price=price)


@app.delete("/prices/{price_id}/", response_model=schemas.Price)
def del_price(price_id: int, db: Session = Depends(get_db)):
    db_price = crud.get_price(db, price_id)
    if not db_price:
        raise HTTPException(status_code=400, detail="There are no price with such id in DB")
    return crud.delete_price(db=db, price_id=price_id)


@app.put("/prices/{price_id}", response_model=schemas.Price)
def update_price(price_id: int, price: schemas.PriceCreate, db: Session = Depends(get_db)):
    db_price = crud.get_price(db, price_id)
    if not db_price:
        raise HTTPException(status_code=400, detail="There are no price with such id in DB")
    return crud.update_price(db, price_id, price)
