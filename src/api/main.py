from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
import numpy as np
import os
import json
from src.config import settings
from src.api.schemas import PatientData, AssessmentResponse
from src.utils.live_data import LiveDataClient
from src.utils.bayesian_network import EnvironmentalBayesNet
from src.utils.recommender import HeartRecommender

# Initialize App
app = FastAPI(
    title=settings.APP_NAME, 
    version=settings.VERSION,
    description="AI Cardiac Risk System with Live Environmental Context"
)

# Global Variables to hold loaded components
system = {
    "clf": None,      # Classifier (XGBoost)
    "reg": None,      # Regressor (Random Forest)
    "scaler": None,   # Feature Scaler
    "cols": None,     # Column names
    "sensor": None,   # IoT Client
    "brain": None,    # Bayesian Network
    "advisor": None   # Recommender
}

@app.on_event("startup")
async def load_system():
    """
    Startup Event: Loads all ML models and API connections once.
    """
    print("Loading Medical AI System...")
    
    # 1. Load ML Artifacts
    try:
        system['clf'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_classification.pkl"))
        system['reg'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_regression.pkl"))
        system['cols'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_columns.pkl"))
        system['scaler'] = joblib.load(os.path.join(settings.MODEL_PATH, "model_scaler.pkl"))
        print("  ML Models & Scaler Loaded")
    except Exception as e:
        print(f" CRITICAL ERROR: Could not load models. Check src/models/. Error: {e}")
    
    # 2. Initialize Logic Layers
    system['sensor'] = LiveDataClient()
    system['brain'] = EnvironmentalBayesNet()
    system['advisor'] = HeartRecommender()
    print("  IoT & Logic Engines Ready")
    print("System Online. Waiting for requests...")

@app.post("/assess", response_model=AssessmentResponse)
async def assess_patient(patient: PatientData):
    """
    The Core Fusion Endpoint.
    """
    # --- 1. PREPARE DATA ---
    # Convert Pydantic model to dict, handling Enums -> Integers conversion automatically
    input_dict = json.loads(patient.json())
    
    city = input_dict.pop("city")  # Extract city for IoT layer
    
    # Convert to DataFrame
    df = pd.DataFrame([input_dict])
    
    # One-Hot Encoding (Matches Training Logic)
    cat_cols = ['cp', 'restecg', 'slope', 'thal']
    df = pd.get_dummies(df, columns=cat_cols)
    
    # Align Columns (Ensure strict match with training data)
    # This creates missing columns (like cp_2, cp_3) and fills them with 0
    df = df.reindex(columns=system['cols'], fill_value=0)
    
    # Scale Features (Age, BP, etc.)
    num_cols = ['age', 'trestbps', 'chol', 'thalach', 'oldpeak']
    df[num_cols] = system['scaler'].transform(df[num_cols])

    # --- 2. EXECUTE AI MODELS (Layer 1) ---
    # Classifier: Returns probability of "Class 1" (Disease)
    prob_disease = system['clf'].predict_proba(df)[0][1]
    
    # Regressor: Returns severity (0-4)
    severity_raw = system['reg'].predict(df)[0]
    
    # Calculate Base Medical Risk (Normalized 0.0 - 1.0)
    base_risk = (prob_disease * 0.6) + ((severity_raw / 4.0) * 0.4)

    # --- 3. FETCH LIVE CONTEXT (Layer 2) ---
    env_data = system['sensor'].get_data(city)
    env_stress = 0.0
    
    if env_data['success']:
        # Bayesian Inference
        bayes_res = system['brain'].infer_stress_probability(
            env_data['temp'], 
            env_data['aqi']
        )
        env_stress = bayes_res['p_stress']
    
    # --- 4. FUSION & ADVICE (Layer 3) ---
    # Total Risk Formula
    total_risk = min(base_risk + (env_stress * 0.15), 1.0)
    
    # Get Recommendations (Using the NEW logic that checks patient details)
    advice = system['advisor'].get_recommendations(
        risk_score=total_risk,
        weather_data={"temp": env_data.get('temp', 0)},
        pollution_data={"aqi": env_data.get('aqi', 0)},
        patient_data=input_dict  # <--- PASSING MEDICAL DATA HERE
    )
    
    return {
        "risk_score": round(total_risk * 100, 2),
        "risk_category": "High Risk" if total_risk > 0.7 else "Moderate" if total_risk > 0.3 else "Low",
        "environment": {
            "city": city,
            "temp": env_data.get('temp'),
            "aqi": env_data.get('aqi'),
            "stress_factor": round(env_stress * 100, 1)
        },
        "recommendations": advice['recommendations']
    }