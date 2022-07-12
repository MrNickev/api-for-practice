from fastapi import FastAPI, HTTPException
from models import Price

app = FastAPI()

# массив будет заменен на БД
PRICES_DB = [
    Price(name="prod1", price=1000),
    Price(name="prod2", price=2000),
    Price(name="prod3", price=3000),
    Price(name="prod4", price=4000)
]


@app.get("/")
def print_hello_phrase():
    return "Welcome to my api page"


@app.get("/prices")
def read_prices():
    return PRICES_DB


@app.get("/prices/{item_id}")
def read_price(item_id: int):
    if item_id < 0 or item_id > len(PRICES_DB):
        raise HTTPException(status_code=501, detail="item_id not in db")
    return PRICES_DB[item_id]


@app.post("/prices/create/")
def create_price(item: Price):
    PRICES_DB.append(item)
    return "new price in db"


@app.put("/prices/update/{item_id}")
def update_price(item_id: int, item: Price):
    if item_id < 0 or item_id > len(PRICES_DB):
        raise HTTPException(status_code=501, detail="item_id not in db")

    PRICES_DB[item_id] = item
    return "price was updated"


@app.delete("/prices/delete/{item_id}")
def delete_price(item_id: int):
    if item_id < 0 or item_id > len(PRICES_DB):
        raise HTTPException(status_code=501, detail="item_id not in db")

    del PRICES_DB[item_id]
    return "price was deleted"
