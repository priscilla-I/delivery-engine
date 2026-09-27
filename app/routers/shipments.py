from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas
from app.ml.predictor import score_shipment

router = APIRouter()

@router.post("/", response_model=schemas.ShipmentOut)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(get_db)):
    # Score with ML model
    result = score_shipment(shipment.dict())

    db_shipment = models.Shipment(
        **shipment.dict(),
        risk_score = result["risk_score"],
        risk_level = result["risk_level"]
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

@router.get("/", response_model=List[schemas.ShipmentOut])
def get_shipments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Shipment).offset(skip).limit(limit).all()

@router.get("/{delivery_id}", response_model=schemas.ShipmentOut)
def get_shipment(delivery_id: str, db: Session = Depends(get_db)):
    s = db.query(models.Shipment).filter(models.Shipment.delivery_id == delivery_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Shipment not found")
    return s

@router.patch("/{delivery_id}/preference")
def update_preference(delivery_id: str, preference: str, db: Session = Depends(get_db)):
    s = db.query(models.Shipment).filter(models.Shipment.delivery_id == delivery_id).first()
    if not s:
        raise HTTPException(status_code=404, detail="Not found")
    s.customer_preference = preference
    s.delivery_status = "preference_set"
    db.commit()
    return {"message": "Preference updated", "preference": preference}

@router.get("/risk/high")
def get_high_risk(db: Session = Depends(get_db)):
    return db.query(models.Shipment).filter(models.Shipment.risk_level == "HIGH").all()
@router.get("/analytics/summary")
def get_analytics(db: Session = Depends(get_db)):
    from sqlalchemy import func
    total = db.query(models.Shipment).count()
    high  = db.query(models.Shipment).filter(models.Shipment.risk_level == "HIGH").count()
    med   = db.query(models.Shipment).filter(models.Shipment.risk_level == "MEDIUM").count()
    low   = db.query(models.Shipment).filter(models.Shipment.risk_level == "LOW").count()
    failed= db.query(models.Shipment).filter(models.Shipment.delivery_status == "failed").count()
    prefs = db.query(models.Shipment).filter(models.Shipment.customer_preference != None).count()

    return {
        "total":            total,
        "high_risk":        high,
        "medium_risk":      med,
        "low_risk":         low,
        "failed":           failed,
        "preferences_set":  prefs,
        "success_rate":     round((total - failed) / max(total, 1) * 100, 1),
        "intervention_rate":round(prefs / max(high + med, 1) * 100, 1),
    }