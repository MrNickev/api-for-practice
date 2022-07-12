from pydantic import BaseModel


class Price(BaseModel):
    name: str
    price: float