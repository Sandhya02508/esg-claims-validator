import os
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.preprocessing import LabelEncoder

print("🤖 Starting Phase 4: Machine Learning Model Training...")

validated_data_path = "data/processed/validated_claims.csv"

if not os.path.exists(validated_data_path):
    print("❌ Error: Missing Phase 3 data! Please run Phase 3 first.")
else:
    df = pd.read_csv(validated_data_path)
    
    # Select features (X) and target variable (y)
    X = df[["extracted_target_year", "numeric_target_percentage", "has_red_flags", "claim_length"]]
    y = df["validation_status"]
    
    # Encode target text labels (Greenvalidated, Caution, RedFlag) into numbers (0, 1, 2)
    le = LabelEncoder()
    y_encoded = le.fit_transform(y)
    
    print("🏋️ Training XGBoost Classifier...")
    # Initialize and fit the XGBoost Model
    model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
    model.fit(X, y_encoded)
    
    # Ensure directory exists and serialize/save the model and label encoder
    os.makedirs("data/models", exist_ok=True)
    
    with open("data/models/credibility_classifier.pkl", "wb") as f:
        pickle.dump(model, f)
        
    with open("data/models/label_encoder.pkl", "wb") as f:
        pickle.dump(le, f)
        
    print("💾 Saved model: data/models/credibility_classifier.pkl")
    print("💾 Saved encoder: data/models/label_encoder.pkl")
    print("✅ Phase 4 Complete! Machine learning backend is fully trained.")