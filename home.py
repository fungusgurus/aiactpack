##############################################################################
# 3. 10-QUESTION WIZARD  –  MAIN AREA  (always visible)
##############################################################################
def wizard():
    st.markdown("### 🧭 10-Question Compliance Wizard")
    with st.form("wizard_form"):
        col1, col2 = st.columns(2)
        with col1:
            sector      = st.selectbox("1. Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
            model_name  = st.text_input("2. Model trade name *", placeholder="CreditGPT-3")
            model_family= st.selectbox("3. Model family", ["GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"])
            data_modal  = st.multiselect("4. Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"])
            n_users     = st.number_input("5. Expected EU users *", min_value=0, max_value=50_000_000, value=5_000, step=1_000)
        with col2:
            high_risk   = st.selectbox("6. High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"])
            deploy_env  = st.selectbox("7. Deployment environment", ["AWS", "Azure", "GCP", "On-prem", "Hybrid"])
            ce_mark     = st.selectbox("8. Already CE-marked HW/SW ?", ["Yes", "No", "Partial"])
            target_mkt  = st.multiselect("9. Target jurisdictions", ["EU", "UK", "USA", "Canada", "APAC"], default=["EU"])
            sandbox     = st.selectbox("10. Participated in EU AI sandbox ?", ["Yes", "No"])
        data_sources = st.text_area("Training data sources (1 per line) *", placeholder="wikimedia.org\ninternal-2022-2024.csv")

        submitted = st.form_submit_button("Generate compliance pack →", type="primary")
        if submitted:
            if not model_name or not data_sources:
                st.error("Please complete mandatory fields.")
                st.stop()
            payload = {
                "sector": sector, "model_name": model_name, "model_family": model_family,
                "data_modal": data_modal, "n_users": n_users, "high_risk": high_risk,
                "deploy_env": deploy_env, "ce_mark": ce_mark, "target_mkt": target_mkt,
                "sandbox": sandbox, "data_sources": data_sources
            }
            with st.spinner("Running 47-prompt chain…"):
                zip_path = dummy_zip(payload)   # replace with real engine later
            with open(zip_path, "rb") as f:
                st.download_button("⬇️ Download bundle", f, file_name=zip_path.name)
            os.remove(zip_path)
            st.success("Check your email for the invoice. Need more? See pricing below.")
