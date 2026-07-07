import streamlit as st
import pandas as pd
import numpy as np


st.set_page_config(
    page_title="ESG Claims Verification Engine",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');
    
    /* Global Typography Reset */
    html, body, [class*="css"] { 
        font-family: 'Plus Jakarta Sans', sans-serif; 
    }
    
    .stApp { 
        background-color: #fdfdfd; 
    }
    
    /* Premium Minimal KPI Cards */
    .metric-container {
        display: flex;
        gap: 24px;
        margin-bottom: 30px;
    }
    .metric-card-custom {
        flex: 1;
        background: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border: 1px solid #f1f5f9;
        box-shadow: 0 10px 15px -3px rgba(15, 23, 42, 0.02), 0 4px 6px -4px rgba(15, 23, 42, 0.02);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .metric-card-custom:hover {
        transform: translateY(-2px);
        box-shadow: 0 20px 25px -5px rgba(15, 23, 42, 0.04), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
    }
    .metric-label-custom {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748b;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .metric-value-custom {
        font-size: 1.8rem;
        font-weight: 700;
        color: #0f172a;
    }
    .metric-sub-custom {
        font-size: 0.85rem;
        margin-top: 6px;
        font-weight: 500;
    }
    
    /* Live Status Badge Styling */
    .badge-good { color: #059669; background: #ecfdf5; padding: 2px 8px; border-radius: 6px; font-weight: 600; }
    .badge-warning { color: #d97706; background: #fffbeb; padding: 2px 8px; border-radius: 6px; font-weight: 600; }
    .badge-bad { color: #dc2626; background: #fef2f2; padding: 2px 8px; border-radius: 6px; font-weight: 600; }
    
    /* Corporate Branding Title Banner */
    .brand-banner {
        background: linear-gradient(135deg, #1e3a8a 0%, #0f172a 100%);
        padding: 35px;
        border-radius: 20px;
        color: #ffffff;
        margin-bottom: 30px;
        box-shadow: 0 4px 20px rgba(30, 58, 138, 0.15);
    }
    </style>
""", unsafe_allow_html=True)


if "master_db" not in st.session_state:
    st.session_state.master_db = pd.DataFrame({
        "Company": ["Microsoft", "Walmart", "ExxonMobil", "Apple", "Tesla"],
        "Sector": ["Technology", "Retail", "Energy", "Technology", "Automotive"],
        "Stated Target %": [100, 50, 40, 100, 80],
        "Target Year": [2030, 2025, 2030, 2030, 2035],
        "Audit Status": ["Greenvalidated", "Greenwashed", "RedFlag", "Greenvalidated", "Caution"],
        "Score": [95, 80, 35, 92, 65],
        "Claim": [
            "Carbon negative by 2030 through direct investment in carbon capture.",
            "Achieving zero waste in global operations by the end of 2025.",
            "Reducing absolute methane emissions intensity by 40% across all fields.",
            "100% carbon neutral across supply chain and products by 2030.",
            "Displacing fossil-fuel vehicles through massive scale battery efficiency."
        ]
    })


st.markdown("""
    <div class="brand-banner">
        <h1 style='margin:0; font-size: 2.3rem; font-weight:700; letter-spacing:-0.03em;'>🛡️ ESG Claims Verification Engine</h1>
        <p style='margin: 8px 0 0 0; color: #93c5fd; font-size: 1.1rem; font-weight: 400; opacity: 0.9;'>
            Neural Network Risk Screening & Regulatory Compliance Auditing Dashboard
        </p>
    </div>
""", unsafe_allow_html=True)


total_entities = len(st.session_state.master_db)
avg_score = round(st.session_state.master_db["Score"].mean(), 1)
greenwash_cases = len(st.session_state.master_db[st.session_state.master_db["Audit Status"].isin(["Greenwashed", "RedFlag"])])


summary_html = f"""
<div class="metric-container">
    <div class="metric-card-custom">
        <div class="metric-label-custom">Audited Entities</div>
        <div class="metric-value-custom">{total_entities} Active</div>
        <div class="metric-sub-custom" style="color:#059669;">✨ Live tracking database</div>
    </div>
    <div class="metric-card-custom">
        <div class="metric-label-custom">Model Credibility Avg</div>
        <div class="metric-value-custom">{avg_score} / 100</div>
        <div class="metric-sub-custom" style="color:#2563eb;">⚡ Neural risk evaluation</div>
    </div>
    <div class="metric-card-custom">
        <div class="metric-label-custom">Flagged Violations</div>
        <div class="metric-value-custom">{greenwash_cases} Cases</div>
        <div class="metric-sub-custom" style="color:#dc2626;">⚠️ Requires active intervention</div>
    </div>
</div>
"""
st.markdown(summary_html, unsafe_allow_html=True)


layout_left, layout_right = st.columns([1, 1.8], gap="large")

with layout_left:
    st.markdown("### 🧪 Real-time Simulation Engine")
    st.caption("Adjust variables live to predict structural data alignment parameters.")
    

    with st.container(border=True):
        user_company = st.text_input("Target Corporate Entity:", value="Tata Motors")
        user_sector = st.selectbox("Market Sector Class:", ["Technology", "Retail", "Energy", "Automotive", "Manufacturing"])
        user_pct = st.slider("Target Mitigation Level (%)", min_value=10, max_value=100, value=75)
        user_year = st.slider("Target Target Horizon Year", min_value=2026, max_value=2050, value=2032)
        user_claim = st.text_area("Stated Environmental Claim Statement:", value="Pledging transition across core facilities to carbon-neutral microgrids.")
        
       
        year_bonus = (user_year - 2026) * 0.8
        live_score = int(98 - (user_pct * 0.35) + year_bonus)
        live_score = max(10, min(100, live_score))
        
        if live_score >= 82:
            live_status, badge_class = "Greenvalidated", "badge-good"
        elif 50 <= live_score < 82:
            live_status, badge_class = "Greenwashed", "badge-warning"
        else:
            live_status, badge_class = "RedFlag", "badge-bad"

    st.write("")
    
   
    if st.button("📥 Push and Append to Master Record Ledger", use_container_width=True, type="primary"):
        if user_company.strip() == "":
            st.error("Operation Denied: Corporate Name Input Field Cannot Be Blank.")
        else:
            existing_entities = st.session_state.master_db["Company"].astype(str).str.lower().str.strip().values
            final_name = user_company.strip()
            
            if final_name.lower() in existing_entities:
                final_name = f"{final_name} ({np.random.randint(10, 99)})"
                
            new_record = pd.DataFrame({
                "Company": [final_name],
                "Sector": [user_sector],
                "Stated Target %": [user_pct],
                "Target Year": [user_year],
                "Audit Status": [live_status],
                "Score": [live_score],
                "Claim": [user_claim]
            })
            
            st.session_state.master_db = pd.concat([st.session_state.master_db, new_record], ignore_index=True)
            st.toast(f"Data Ledger Pipeline updated with {final_name}!", icon="🚀")
            st.rerun()

with layout_right:
    st.markdown("### 📊 Interactive Neural Telemetry Matrix")
    st.caption("Instant preview evaluation score output mapped to user side control positions:")
    
    
    live_preview_html = f"""
    <div class="metric-container" style="margin-bottom:15px;">
        <div class="metric-card-custom" style="padding:15px;">
            <div class="metric-label-custom">Target Subject</div>
            <div style="font-size:1.2rem; font-weight:700; color:#1e293b;">{user_company if user_company else "Awaiting Name"}</div>
            <div style="font-size:0.8rem; color:#64748b; margin-top:2px;">{user_sector} Division</div>
        </div>
        <div class="metric-card-custom" style="padding:15px;">
            <div class="metric-label-custom">Calculated Score</div>
            <div style="font-size:1.2rem; font-weight:700; color:#1e293b;">{live_score} / 100</div>
            <div style="font-size:0.8rem; margin-top:2px;"><span class="{badge_class}">Floating Metrics</span></div>
        </div>
        <div class="metric-card-custom" style="padding:15px;">
            <div class="metric-label-custom">Assessed Decision</div>
            <div style="font-size:1.2rem; font-weight:700; color:#1e293b;">{live_status}</div>
            <div style="font-size:0.8rem; margin-top:2px;"><span class="{badge_class}">System Verdict</span></div>
        </div>
    </div>
    """
    st.markdown(live_preview_html, unsafe_allow_html=True)
    
    
    st.markdown("### 🔗 Project Redirection & Deep-Dive Hub")
    
    # Interactive visual container for handling platform outputs or context updates
    with st.container(border=True):
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
           
                "📂 Open Project Repository Source", 
                url="https://github.com/Sandhya02508/esg-claims-validator", 
                use_container_width=True,
                help="Click here to inspect model weights, source architecture pipelines, and developer documentation modules."
            )
        with col_btn2:
            
            st.link_button(
                "📈 View Live Regulatory Standards", 
                url="https://www.sec.gov/securities-topics/esg", 
                use_container_width=True,
                help="Redirect out to real-time external greenwashing compliance frameworks."
            )
            
    st.markdown("### 📋 System Historic Core Master Ledger Database")
    

    display_cols = ["Company", "Sector", "Stated Target %", "Target Year", "Audit Status", "Score", "Claim"]
    st.dataframe(
        st.session_state.master_db[display_cols], 
        use_container_width=True, 
        height=280,
        hide_index=True
    ) 
