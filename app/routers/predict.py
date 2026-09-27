from fastapi import APIRouter
from pydantic import BaseModel
from app.ml.predictor import score_shipment

router = APIRouter()

class PredictRequest(BaseModel):
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

@router.post("/")
def predict(req: PredictRequest):
    result = score_shipment(req.dict())
    return result