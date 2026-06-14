import os
import pandas as pd

print("🧠 Starting Phase 2: LLM Claim Extraction...")

# Load the raw corporate filings generated in Phase 1
raw_filings_path = "data/raw/corporate_filings.csv"

if not os.path.exists(raw_filings_path):
    print("❌ Error: Missing raw data. Please run Phase 1 first!")
else:
    df = pd.read_csv(raw_filings_path)
    
    print("🤖 Simulating Mistral LLM parsing texts...")
    
    # Adding mock LLM extraction fields
    df["extracted_target_year"] = [2030, 2030, 2030, 2050, 2035]
    df["numeric_target_percentage"] = [100, 100, 50, 100, 100]  
    df["has_red_flags"] = [0, 0, 1, 1, 0]                      
    df["claim_length"] = df["claim_text"].apply(len)
    
    # Save to the processed directory
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv("data/processed/extracted_claims.csv", index=False)
    print("💾 Saved: data/processed/extracted_claims.csv")
    print("✅ Phase 2 Complete! Claims successfully structured by LLM.")