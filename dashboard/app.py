import os
import pandas as pd
import streamlit as st
import plotly.express as px
import pickle  # <-- Added to load model directly

# Set up page configurations
st.set_page_config(page_title="ESG Claims Verification Hub", page_icon="🌿", layout="wide")

# Inject Custom CSS
st.markdown("""
    <style>
        .main { background-color: #f8f9fa; }
        .metric-card {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            border-left: 5px solid #2ecc71;
            margin-bottom: 20px;
        }
        .metric-card.red { border-left-color: #e74c3c; }
        .metric-card.yellow { border-left-color: #f1c40f; }
        
        .status-badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-weight: bold;
            font-size: 13px;
            display: inline-block;
        }
        .badge-green { background-color: #d4edda; color: #155724; }
        .badge-yellow { background-color: #fff3cd; color: #856404; }
        .badge-red { background-color: #f8d7da; color: #721c24; }
    </style>
""", unsafe_allow_html=True)

# Helper Function: Server ke bina direct model prediction karne ke liye
def predict_risk_locally(year, percentage, red_flags):
    model_path = "data/models/credibility_classifier.pkl"
    encoder_path = "data/models/label_encoder.pkl"
    
    if os.path.exists(model_path) and os.path.exists(encoder_path):
        with open(model_path, 'rb') as m_file:
            model = pickle.load(m_file)
        with open(encoder_path, 'rb') as e_file:
            le = pickle.load(e_file)
            
        # Creating dummy feature row matching your XGBoost input shape
        # Adjust these columns based on your exact training features if needed
        input_data = pd.DataFrame([{
            "extracted_target_year": year,
            "numeric_target_percentage": percentage,
            "has_red_flags": red_flags
        }])
        
        pred_encoded = model.predict(input_data)[0]
        pred_status = le.inverse_transform([pred_encoded])[0]
        return pred_status
    else:
        return "Caution" # Fallback if models aren't found

# --- SIDEBAR: LIVE ML SIMULATION SANDBOX ---
st.sidebar.markdown("<h2 style='color: #1e3a2f;'>🤖 Live ML Risk Sandbox</h2>", unsafe_allow_html=True)
st.sidebar.markdown("Simulate a new corporate statement directly using the embedded XGBoost model.")

sandbox_text = st.sidebar.text_area("Corporate Claim Text Statement:", 
                                   value="We will slash overall net emissions by 80% by the year 2040.")
sandbox_year = st.sidebar.number_input("Target Year Horizon:", min_value=2025, max_value=2100, value=2040)
sandbox_pct = st.sidebar.slider("Target Reduction Percentage (%):", min_value=0, max_value=100, value=80)
sandbox_flag = st.sidebar.selectbox("LLM Red Flags Detected?", options=["No", "Yes"])

flag_value = 1 if sandbox_flag == "Yes" else 0

if st.sidebar.button("🔮 Run Live Risk Prediction"):
    st.sidebar.markdown("---")
    try:
        # FastAPI url hit karne ke bajay hum direct function call kar rahe hain
        risk_status = predict_risk_locally(int(sandbox_year), int(sandbox_pct), flag_value)
        
        # Map visual color cues based on output
        badge_color = "badge-green" if risk_status == "Greenvalidated" else "badge-yellow" if risk_status == "Caution" else "badge-red"
        
        st.sidebar.success("🎉 Prediction Completed Successfully!")
        st.sidebar.markdown(f"""
            <div style="background-color: #ffffff; padding: 15px; border-radius: 8px; border: 1px solid #ddd; text-align: center;">
                <p style="margin: 0; font-size: 12px; color: #7f8c8d; text-transform: uppercase; font-weight: bold;">Embedded XGBoost Model</p>
                <h3 style="margin: 5px 0 10px 0; color: #2c3e50;">Risk Result</h3>
                <span class="status-badge {badge_color}">{risk_status}</span>
            </div>
        """, unsafe_allow_html=True)
            
    except Exception as e:
        st.sidebar.error(f"❌ Prediction Failed: {str(e)}")


# --- MAIN HEADER SECTION ---
st.markdown("<h1 style='text-align: center; color: #1e3a2f; font-family: sans-serif;'>🌿 ESG Claims Verification Hub</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #555; margin-bottom: 40px;'>Enterprise Fraud Detection Engine: Validating Corporate Statements Against Live EPA & EIA Records</p>", unsafe_allow_html=True)

VALIDATED_DATA_PATH = "data/processed/validated_claims.csv"

if not os.path.exists(VALIDATED_DATA_PATH):
    st.error("⚠️ Audited dataset not found. Please run your data pipeline first!")
else:
    df = pd.read_csv(VALIDATED_DATA_PATH)
    
    # --- TOP KPI METRIC CARDS ROW ---
    col_m1, col_m2, col_m3 = st.columns(3)
    
    with col_m1:
        st.markdown(f"""
            <div class="metric-card">
                <p style="color: #7f8c8d; margin: 0; text-transform: uppercase; font-size: 12px; font-weight: bold;">Audited Companies</p>
                <h2 style="margin: 5px 0 0 0; color: #2c3e50;">{len(df["company_name"].unique())}</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m2:
        avg_score = round(df['credibility_score'].mean(), 1)
        st.markdown(f"""
            <div class="metric-card yellow">
                <p style="color: #7f8c8d; margin: 0; text-transform: uppercase; font-size: 12px; font-weight: bold;">Average Credibility Score</p>
                <h2 style="margin: 5px 0 0 0; color: #2c3e50;">{avg_score} <span style="font-size: 16px; color: #7f8c8d;">/ 100</span></h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col_m3:
        red_flags_count = len(df[df["validation_status"] == "RedFlag"])
        st.markdown(f"""
            <div class="metric-card red">
                <p style="color: #7f8c8d; margin: 0; text-transform: uppercase; font-size: 12px; font-weight: bold;">Identified Greenwashing Risks</p>
                <h2 style="margin: 5px 0 0 0; color: #e74c3c;">{red_flags_count} Breach(es)</h2>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- MAIN VISUALS AND DATAFRAME SPLIT LAYOUT ---
    col_layout1, col_layout2 = st.columns([3, 2])
    
    with col_layout1:
        st.markdown("<h3 style='color: #2c3e50;'>📋 High-Fidelity Data Ledger</h3>", unsafe_allow_html=True)
        st.dataframe(
            df[["company_name", "sector", "claim_category", "credibility_score", "validation_status"]], 
            use_container_width=True,
            height=280
        )
        
    with col_layout2:
        st.markdown("<h3 style='color: #2c3e50;'>📊 Compliance Distribution</h3>", unsafe_allow_html=True)
        
        status_counts = df["validation_status"].value_counts().reset_index()
        status_counts.columns = ["Status", "Count"]
        
        color_map = {"Greenvalidated": "#2ecc71", "Caution": "#f1c40f", "RedFlag": "#e74c3c"}
        
        fig = px.pie(
            status_counts, 
            values="Count", 
            names="Status", 
            hole=0.5,
            color="Status",
            color_discrete_map=color_map
        )
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0), 
            height=260, 
            showlegend=True,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<hr style='border-top: 1px solid #ddd;'>", unsafe_allow_html=True)

    # --- ADVANCED COMPANY DEEP-DIVE INSPECTION TOOL ---
    st.markdown("<h3 style='color: #2c3e50;'>🔎 Forensic Audit Deep-Dive</h3>", unsafe_allow_html=True)
    
    selected_company = st.selectbox("Select a corporate entity to inspect:", df["company_name"].unique())
    company_data = df[df["company_name"] == selected_company].iloc[0]
    
    status = company_data['validation_status']
    badge_class = "badge-green" if status == "Greenvalidated" else "badge-yellow" if status == "Caution" else "badge-red"
    
    c1, c2, c3 = st.columns([2, 1, 1])
    
    with c1:
        st.markdown(f"""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); min-height: 160px;">
                <p style="font-weight: bold; margin-top: 0; color: #34495e;">Stated Corporate Filing Claim Text:</p>
                <p style="font-style: italic; color: #555; line-height: 1.6;">"{company_data['claim_text']}"</p>
            </div>
        """, unsafe_allow_html=True)
        
    with c2:
        st.markdown(f"""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); min-height: 160px; text-align: center;">
                <p style="font-weight: bold; margin-top:0; color: #34495e; text-align: left;">Audit Score Card:</p>
                <h1 style="margin: 10px 0 0 0; color: #2c3e50; font-size: 42px;">{company_data['credibility_score']}</h1>
                <span class="status-badge {badge_class}">{status}</span>
            </div>
        """, unsafe_allow_html=True)
        
    with c3:
        st.markdown(f"""
            <div style="background-color: #ffffff; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); min-height: 160px;">
                <p style="font-weight: bold; margin-top: 0; color: #34495e;">Physical Field Records:</p>
                <p style="margin: 5px 0; font-size: 14px;"><b>Category:</b> {company_data['claim_category'].upper()}</p>
                <p style="margin: 5px 0; font-size: 14px;"><b>Recorded EPA Carbon:</b> {company_data['recorded_emissions_co2e']:,} tons</p>
                <p style="margin: 5px 0; font-size: 14px;"><b>Target Horizon Year:</b> {company_data['extracted_target_year']}</p>
            </div>
        """, unsafe_allow_html=True)