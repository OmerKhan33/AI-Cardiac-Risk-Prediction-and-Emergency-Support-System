from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session
import joblib
import pandas as pd
import numpy as np
import os
import json
from src.config import settings
from src.db.database import create_db_and_tables, get_session
from src.models.user_model import User
from src.models.prediction_model import Prediction
from src.auth.security import get_current_user
from src.api import auth_routes
from src.api.schemas import PatientData, AssessmentResponse
from src.utils.live_data import LiveDataClient
from src.utils.bayesian_network import EnvironmentalBayesNet
from src.utils.recommender import HeartRecommender

# Initialize App
app = FastAPI(
    title=settings.APP_NAME, 
    version="1.5.0", # Bumped version for Docker + Frontend
    description="AI Cardiac Risk System with Live Environmental Context & User History"
)

# CORS Middleware (Allow frontend to communicate with API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Variables
system = {
    "clf": None,      # Classifier (XGBoost)
    "reg": None,      # Regressor (Random Forest)
    "scaler": None,   # Feature Scaler
    "cols": None,     # Column names
    "sensor": None,   # IoT Client
    "brain": None,    # Bayesian Network
    "advisor": None   # Recommender
}

# --- 1. STARTUP EVENT (DB + MODELS) ---
@app.on_event("startup")
def on_startup():
    print("Starting up Cardiac System...")
    
    # A. Create Database Tables
    create_db_and_tables()
    print("Database tables created (heart_app.db)")
    
    # B. Load ML Artifacts
    try:
        system['clf'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_classification.pkl"))
        system['reg'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_regression.pkl"))
        system['cols'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_columns.pkl"))
        system['scaler'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_scaler.pkl"))
        print(" ML Models & Scaler Loaded")
    except Exception as e:
        print(f" CRITICAL ERROR: Could not load models. {e}")

    # C. Initialize Logic Layers
    system['sensor'] = LiveDataClient()
    system['brain'] = EnvironmentalBayesNet()
    system['advisor'] = HeartRecommender()
    print(" IoT & Logic Engines Ready")

# --- 2. INCLUDE AUTH ROUTES ---
app.include_router(auth_routes.router)

# --- 3. THE SMART ENDPOINT (NOW SECURE) ---
@app.post("/assess", response_model=AssessmentResponse)
async def assess_patient(
    patient: PatientData, 
    # This forces the user to be logged in
    current_user: User = Depends(get_current_user), 
    # This gives us access to the database
    session: Session = Depends(get_session)
):
    """
    Diagnostic Endpoint: 
    1. Authenticates User
    2. Runs AI Models
    3. Fetches Weather
    4. SAVES RESULT TO HISTORY
    """
    
    # --- A. PREPARE DATA ---
    input_dict = json.loads(patient.json())
    city = input_dict.pop("city") 
    
    # DataFrame Conversion
    df = pd.DataFrame([input_dict])
    cat_cols = ['cp', 'restecg', 'slope', 'thal']
    df = pd.get_dummies(df, columns=cat_cols)
    df = df.reindex(columns=system['cols'], fill_value=0)
    
    # Scaling
    num_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    df[num_cols] = system['scaler'].transform(df[num_cols])

    # --- B. EXECUTE AI (Layer 1) ---
    prob_disease = system['clf'].predict_proba(df)[0][1]
    severity_raw = system['reg'].predict(df)[0]
    base_risk = (prob_disease * 0.6) + ((severity_raw / 4.0) * 0.4)

    # --- C. LIVE CONTEXT (Layer 2) ---
    env_data = system['sensor'].get_data(city)
    env_stress = 0.0
    if env_data['success']:
        bayes_res = system['brain'].infer_stress_probability(
            env_data['temp'], env_data['aqi']
        )
        env_stress = bayes_res['p_stress']
    
    # --- D. FUSION (Layer 3) ---
    total_risk = min(base_risk + (env_stress * 0.15), 1.0)
    
    risk_category = "High Risk" if total_risk > 0.7 else "Moderate" if total_risk > 0.3 else "Low"
    
    # Get Advice
    advice = system['advisor'].get_recommendations(
        risk_score=total_risk,
        weather_data={"temp": env_data.get('temp', 0)},
        pollution_data={"aqi": env_data.get('aqi', 0)},
        patient_data=input_dict
    )

    #E. SAVE TO DATABASE
    # We create a new row in the 'prediction' table
    history_entry = Prediction(
        user_id=current_user.id,  # Link to the logged-in user
        
        # Medical Data
        age=patient.age, sex=patient.sex, cp=patient.cp,
        trestbps=patient.trestbps, chol=patient.chol, fbs=patient.fbs,
        restecg=patient.restecg, thalach=patient.thalach, exang=patient.exang,
        oldpeak=patient.oldpeak, slope=patient.slope, ca=patient.ca, thal=patient.thal,
        
        # Results
        prediction=1 if total_risk > 0.5 else 0,
        probability=round(total_risk, 4),
        risk_label=risk_category
    )
    
    session.add(history_entry)
    session.commit() # Save it!
    
    # --- F. RETURN RESPONSE ---
    return {
        "risk_score": round(total_risk * 100, 2),
        "risk_category": risk_category,
        "environment": {
            "city": city,
            "temp": env_data.get('temp'),
            "aqi": env_data.get('aqi'),
            "stress_factor": round(env_stress * 100, 1)
        },
        "recommendations": advice['recommendations']
    }

@app.get("/")
def health_check():
    return {"status": "online", "db": "connected", "auth": "active"}