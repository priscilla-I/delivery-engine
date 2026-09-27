import joblib
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import os

BASE = os.path.dirname(__file__)

model = xgb.XGBClassifier()
model.load_model(os.path.join(BASE, "models/delivery_model.json"))
FEATURES  = joblib.load(os.path.join(BASE, "models/features.pkl"))
THRESHOLD = joblib.load(os.path.join(BASE, "models/threshold.pkl"))

CAT_COLS = ['package_type','vehicle_type','delivery_mode',
            'region','weather_condition','delivery_partner']

ENCODERS = {}
for col in CAT_COLS:
    le = LabelEncoder()
    le.fit(['automobile parts','cosmetics','groceries','electronics',
            'clothing','furniture','books','toys',
            'bike','ev van','truck','car','scooter',
            'same day','express','two day','standard',
            'north','south','east','west','central',
            'clear','rainy','foggy','stormy','cold','windy',
            'delhivery','xpressbees','shadowfax','dhl','fedex','bluedart'])
    ENCODERS[col] = le

def score_shipment(data: dict) -> dict:
    df = pd.DataFrame([data])

    for col in CAT_COLS:
        if col in df.columns:
            try:
                df[col] = ENCODERS[col].transform(df[col].astype(str))
            except ValueError:
                df[col] = 0

    # Zone risk mapping
    zone_risk_map = {
        'north': 0.12, 'south': 0.09,
        'east': 0.15,  'west': 0.11, 'central': 0.10
    }
    raw_region = data.get('region', 'central')
    df['zone_risk'] = zone_risk_map.get(raw_region, 0.10)

    row = df[FEATURES]
    prob = float(model.predict_proba(row)[0][1])

    if prob >= 0.6:
        level  = "HIGH"
        action = "Trigger customer notification immediately"
    elif prob >= THRESHOLD:
        level  = "MEDIUM"
        action = "Send delivery preference options"
    else:
        level  = "LOW"
        action = "Proceed with standard delivery"

    return {
        "risk_score":  round(prob, 4),
        "risk_level":  level,
        "action":      action,
        "risk_pct":    f"{prob:.1%}"
    }