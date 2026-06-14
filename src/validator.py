import os
import pandas as pd

print("🛡️ Starting Phase 3: Claim Validation & Scoring Engine...")

# Load required datasets
extracted_claims_path = "data/processed/extracted_claims.csv"
epa_data_path = "data/raw/epa_emissions_data.csv"
eia_data_path = "data/raw/eia_energy_data.csv"

if not os.path.exists(extracted_claims_path):
    print("❌ Error: Missing Phase 2 data! Please run Phase 2 first.")
else:
    # Read the data
    claims_df = pd.read_csv(extracted_claims_path)
    epa_df = pd.read_csv(epa_data_path)
    eia_df = pd.read_csv(eia_data_path)
    
    # Merge datasets together on company name
    merged_df = pd.merge(claims_df, epa_df, on="company_name", how="left")
    merged_df = pd.merge(merged_df, eia_df, on="company_name", how="left")
    
    print("🧮 Calculating Credibility Scores (0 - 100)...")
    
    # Core Validation Logic
    scores = []
    status_labels = []
    
    for idx, row in merged_df.iterrows():
        # Start with a baseline score of 80
        score = 80 
        
        # Rule 1: Penalty if the LLM detected red flags (vague language/exaggeration)
        if row["has_red_flags"] == 1:
            score -= 25
            
        # Rule 2: Check actual emissions progress
        # If recorded emissions are close to or higher than baseline, deduct points
        emissions_ratio = row["recorded_emissions_co2e"] / row["baseline_emissions_co2e"]
        if emissions_ratio >= 0.95:
            score -= 20  # Making little to no progress reducing carbon
        elif emissions_ratio < 0.60:
            score += 15  # Making excellent progress reducing carbon
            
        # Rule 3: Check renewable energy usage
        renewable_ratio = row["renewable_energy_mwh"] / row["total_energy_mwh"]
        if row["claim_category"] == "renewable" and renewable_ratio < 0.50:
            score -= 15  # Claims to be clean but uses mostly non-renewable energy
            
        # Keep score strictly within bounds (0 to 100)
        score = max(0, min(100, score))
        scores.append(score)
        
        # Classify based on score threshold
        if score >= 75:
            status_labels.append("Greenvalidated")  # Authentic / Safe
        elif score >= 50:
            status_labels.append("Caution")       # Partially supported / Suspicious
        else:
            status_labels.append("RedFlag")        # High Greenwashing risk
            
    # Add the newly calculated columns to the dataframe
    merged_df["credibility_score"] = scores
    merged_df["validation_status"] = status_labels
    
    # Save the audited data to the processed folder
    merged_df.to_csv("data/processed/validated_claims.csv", index=False)
    print("💾 Saved: data/processed/validated_claims.csv")
    print("✅ Phase 3 Complete! Fact-checking and evaluation finished successfully.")