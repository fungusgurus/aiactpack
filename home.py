# streamlit_app.py
import streamlit as st
from datetime import datetime
import json

st.set_page_config(page_title="AI-Act Packager", page_icon="📜", layout="centered")
st.title("📜 Reg-Tech Prompt-Packager")
st.markdown("Answer 10 questions and get a full compliance bundle in <2 min.")

# ---------- 10 QUESTIONS ----------
with st.form("intake_form"):
    col1, col2 = st.columns(2)
    with col1:
        sector        = st.selectbox("1. Industry sector*", 
                                     ["FinTech", "HealthTech", "HR-tech", "AdTech", 
                                      "Retail", "CyberSec", "Auto", "Other"])
        model_name    = st.text_input("2. Model trade name*", 
                                      placeholder="e.g. CreditGPT-3")
        model_type    = st.selectbox("3. Model family*", 
                                     ["GPT-4", "Llama-3", "Claude-3", "Gemini", 
                                      "Custom transformer", "Random-Forest", "XGBoost"])
        data_types    = st.multiselect("4. Data modalities*", 
                                       ["Text", "Image", "Tabular", "Audio", "Video"])
        data_sources  = st.text_area("5. Training data sources (one per line)*", 
                                     placeholder="wikimedia.org\ninternal CRM 2022-2024")
    with col2:
        n_users       = st.number_input("6. Expected EU users*", min_value=0, max_value=100_000_000, step=1, value=5000)
        high_risk_annex = st.selectbox("7. High-risk use-case per Annex III?*", 
                                       ["Biometric ID", "HR recruitment", "Credit scoring", "Insurance", "None of these"])
        deploy_env    = st.selectbox("8. Deployment environment*", 
                                     ["On-prem", "AWS", "Azure", "GCP", "Private cloud"])
        ce_mark       = st.selectbox("9. Already CE-marked hardware/software?*", 
                                     ["Yes", "No", "Partial"])
        target_market = st.multiselect("10. Target jurisdictions*", 
                                       ["EU", "UK", "USA", "Canada", "APAC"])
    
    submitted = st.form_submit_button("Generate pack →", type="primary")

# ---------- POST-SUBMIT ----------
if submitted:
    if not (model_name and data_sources):
        st.error("Please fill all mandatory fields (*).")
        st.stop()
    
    # Build JSON payload for back-end prompt loop
    answers = {
        "sector": sector,
        "model_name": model_name,
        "model_type": model_type,
        "data_types": data_types,
        "data_sources": data_sources.splitlines(),
        "n_users": n_users,
        "high_risk_annex": high_risk_annex,
        "deploy_env": deploy_env,
        "ce_mark": ce_mark,
        "target_market": target_market,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # ---- mock API call ----
    with st.spinner("Running 47-prompt chain…"):
        # your real back-end receives `answers` and returns zip file
        zip_path = f"/tmp/{model_name.replace(' ','_')}_pack.zip"
        # placeholder: write json as demo
        with open(zip_path, "w") as f:
            f.write(json.dumps(answers, indent=2))
    
    st.success("Pack generated!")
    with open(zip_path, "rb") as f:
        st.download_button("⬇️ Download compliance bundle", 
                           data=f, file_name=zip_path.split("/")[-1])
