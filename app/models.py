from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Shipment(Base):
    __tablename__ = "shipments"
    id                  = Column(Integer, primary_key=True, index=True)
    delivery_id         = Column(String, unique=True, index=True)
    customer_name       = Column(String)
    customer_phone      = Column(String)
    customer_email      = Column(String)
    package_type        = Column(String)
    vehicle_type        = Column(String)
    delivery_mode       = Column(String)
    region              = Column(String)
    weather_condition   = Column(String)
    distance_km         = Column(Float)
    package_weight_kg   = Column(Float)
    delivery_cost       = Column(Float)
    delayed             = Column(Integer, default=0)
    delivery_partner    = Column(String)
    risk_score          = Column(Float, default=0.0)
    risk_level          = Column(String, default="LOW")
    delivery_status     = Column(String, default="pending")
    customer_preference = Column(String, nullable=True)
    created_at          = Column(DateTime, server_default=func.now())

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    email         = Column(String, unique=True, index=True)
    name          = Column(String)
    role          = Column(String, default="dispatcher")
    hashed_password = Column(String)
    created_at    = Column(DateTime, server_default=func.now())