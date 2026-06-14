import os
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Corporate Sustainability Claims Validator API")

# Model Paths
MODEL_PATH = "data/models/credibility_classifier.pkl"
ENCODER_PATH = "data/models/label_encoder.pkl"

# Define the structure of an incoming request using Pydantic
class ClaimInput(BaseModel):
    extracted_target_year: int
    numeric_target_percentage: int
    has_red_flags: int
    claim_text: str

@app.get("/")
def home():
    return {"message": "Sustainability Claims Validator API is online. Go to /docs for interactive testing!"}

@app.post("/validate")
def validate_claim(data: ClaimInput):
    # Calculate feature engineering variable on-the-fly
    claim_length = len(data.claim_text)
    
    # Check if machine learning models exist
    if not os.path.exists(MODEL_PATH) or not os.path.exists(ENCODER_PATH):
        return {"error": "ML models have not been trained yet. Please run Phase 4."}
        
    # Load model and encoder
    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    with open(ENCODER_PATH, "rb") as f:
        le = pickle.load(f)
        
    # Format incoming data as a DataFrame for the model
    input_df = pd.DataFrame([{
        "extracted_target_year": data.extracted_target_year,
        "numeric_target_percentage": data.numeric_target_percentage,
        "has_red_flags": data.has_red_flags,
        "claim_length": claim_length
    }])
    
    # Run prediction
    pred_encoded = model.predict(input_df)[0]
    prediction_label = le.inverse_transform([pred_encoded])[0]
    
    return {
        "claim_submitted": data.claim_text,
        "predicted_risk_status": prediction_label,
        "analysis_metrics": {
            "target_year": data.extracted_target_year,
            "target_percentage": f"{data.numeric_target_percentage}%",
            "llm_red_flags": "Yes" if data.has_red_flags == 1 else "No"
        }
    }