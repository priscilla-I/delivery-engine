from pydantic import BaseModel
from typing import Optional

class ShipmentCreate(BaseModel):
    delivery_id:       str
    customer_name:     str
    customer_phone:    str
    customer_email:    str
    package_type:      str
    vehicle_type:      str
    delivery_mode:     str
    region:            str
    weather_condition: str
    distance_km:       float
    package_weight_kg: float
    delivery_cost:     float
    delayed:           int
    delivery_partner:  str

class ShipmentOut(ShipmentCreate):
    id:                 int
    risk_score:         float
    risk_level:         str
    delivery_status:    str
    customer_preference: Optional[str]
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email:    str
    name:     str
    password: str
    role:     str = "dispatcher"

class Token(BaseModel):
    access_token: str
    token_type:   str