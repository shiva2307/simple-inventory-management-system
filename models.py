
from pydantic import BaseModel


class Productc(BaseModel):
        id: int
        name: str
        description: str
        price: float
        quantity: int