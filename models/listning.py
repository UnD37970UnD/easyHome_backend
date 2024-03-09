from datetime import datetime
from pydantic import BaseModel, Field, create_model

class Listning(BaseModel):
    id: str
    title: str
    description: str
    url: str
    created_time: datetime = Field(default_factory=datetime.utcnow)
    photos: list
    location: dict
    category_id: int
    camere:str
    price:int
    currency:str
    negotiable:str
    floor: str
    construction_date: str
    surface: str
    city: str
    district: str
    judet: str
    platforma: str
    what_for: str
    precise_location: str

class Parameters:
    query_params = {
        "city": (str, ""),
        "camere": (str, ""),
        "platforma": (str, ""),
        "from_price": (int, 0),
        "to_price": (int, 99999999),
        "sort": (str, ""),
        "skip": (int, 0),
        "lenght": (int, 40)
    }

    param = create_model("Query", **query_params)