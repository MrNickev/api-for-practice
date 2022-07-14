from datetime import datetime
from sqlalchemy.orm import Session
import models, schemas


def get_price(db: Session, price_id: int):
    return db.query(models.Price).filter(models.Price.id == price_id).first()


def get_price_by_name(db: Session, name: str):
    return db.query(models.Price).filter(
        models.Price.name == name
    ).order_by(models.Price.datetime.desc()).first()


def get_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Price).offset(skip).limit(limit).all()


def create_price(db: Session, price: schemas.PriceCreate):
    dt = datetime.now()
    db_price = models.Price(
        name=price.name,
        url=price.url,
        price=price.price,
        price_int=price.price_int,
        datetime=dt
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price


def delete_price(db: Session, price_id: int):
    price_for_delete = get_price(db, price_id)
    db.delete(price_for_delete)
    db.commit()
    return price_for_delete


def update_price(db: Session, price_id: int, price: schemas.PriceCreate):
    price_for_update = get_price(db=db, price_id=price_id)
    price_for_update.name = price.name
    price_for_update.url = price.url
    price_for_update.price = price.price
    price_for_update.price_int = price.price_int
    db.add(price_for_update)
    db.commit()
    db.refresh(price_for_update)
    return price_for_update

