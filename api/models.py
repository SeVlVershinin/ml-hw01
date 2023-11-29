from typing import List, Optional

from pydantic import BaseModel, validator


class Item(BaseModel):
    """Признаковое описание автомобиля"""
    @validator('*', pre=True)
    def empty_str_to_none(cls, v):
        if v == '':
            return None
        return v
    name: str
    year: int
    selling_price: Optional[int] = None
    km_driven: int
    fuel: str
    seller_type: str
    transmission: str
    owner: str
    mileage: Optional[str] = None
    engine: Optional[str] = None
    max_power: Optional[str] = None
    torque: Optional[str] = None
    seats: Optional[float] = None


class Items(BaseModel):
    """Список признаковых описаний автомобилей"""
    objects: List[Item]

    def to_dict(self) -> List[dict]:
        return [dict(item) for item in self.objects]
