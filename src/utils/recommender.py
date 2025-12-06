import json
import os
from src.config import settings

class HeartRecommender:
    def __init__(self):
        # Load the advice database
        # We look for the file relative to the project root or data path
        db_path = os.path.join(settings.DATA_PATH, "advice_db.json")
        
        try:
            with open(db_path, 'r', encoding='utf-8') as f:
                self.advice_db = json.load(f)
            print("  Recommender System: Knowledge Base Loaded.")
        except FileNotFoundError:
            print(f"  WARNING: advice_db.json not found at {db_path}")
            self.advice_db = []

def generate_tags(self, risk_score, weather_data, pollution_data, patient_data={}):
        """
        Converts numbers into tags.
        Now accepts optional 'patient_data' dict to check BP, Chol, etc.
        """
        tags = set()
        
        # 1. RISK SCORES
        if risk_score > 0.80:
            tags.add("emergency")
        elif risk_score > 0.50:
            tags.add("high_risk")
        elif risk_score > 0.30:
            tags.add("moderate_risk")
        else:
            tags.add("low_risk")
            tags.add("healthy")

        # 2. ENVIRONMENTAL CONTEXT
        temp = weather_data.get('temp', 20)
        if temp > 30:
            tags.add("heatwave")
        elif temp < 5:
            tags.add("cold_snap")

        aqi = pollution_data.get('aqi', 1)
        if aqi > 3:
            tags.add("high_pollution")

        # 3. MEDICAL CONTEXT (The New Smart Logic)
        # We check if specific keys exist in the patient_data dict
        if patient_data.get('chol', 0) > 240:
            tags.add("high_chol")
        
        if patient_data.get('trestbps', 0) > 140:
            tags.add("high_bp")
            
        if patient_data.get('fbs', 0) == 1:
            tags.add("high_fbs")
            
        if patient_data.get('thalach', 0) > 170:
            tags.add("high_heart_rate")
            
        # Check Chest Pain (Value 1, 2, or 3 means some pain)
        if patient_data.get('cp', 0) in [0, 1, 2]: # Based on your Schema mapping where 0=Typical Angina
             tags.add("chest_pain_active")

        return tags

def get_recommendations(self, risk_score, weather_data={}, pollution_data={}):
        """
        The Logic: Matches Patient Tags -> Advice Tags
        """
        # Step 1: Generate Patient Profile
        patient_tags = self.generate_tags(risk_score, weather_data, pollution_data)
        
        recommendations = []
        
        # Step 2: Filter Database
        for item in self.advice_db:
            # Check overlap: Does the advice have tags that match the patient?
            item_tags = set(item['tags'])
            if not item_tags.isdisjoint(patient_tags):
                recommendations.append(item)
        
        # Step 3: Sort by Priority (Critical warnings first)
        recommendations.sort(key=lambda x: x['priority'], reverse=True)
        
        return {
            "generated_tags": list(patient_tags),
            "recommendations": [rec['text'] for rec in recommendations]
        }