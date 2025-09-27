# Home.py
import streamlit as st, os, tempfile, pathlib, datetime, zipfile, json

# ---------- PAGE ----------
st.set_page_config(page_title="AI Act Pack™", page_icon="⚖️", layout="centered")

# ---------- STICKY TOP-BAR ----------
st.html("""
<style>
header{visibility:hidden}.top-bar{position:fixed;top:0;left:0;right:0;height:70px;background:#003399;display:flex;align-items:center;justify-content:space-between;padding:0 2rem;z-index:999;box-shadow:0 2px 8px rgba(0,0,0,.15);}.logo-img{height:40px;margin-right:12px}.brand-txt{font-size:1.4rem;font-weight:700;color:#fff}.nav-buttons{display:flex;gap:1rem}.main{padding-top:80px}
</style>
<div class="top-bar"><div style="display:flex;align-items:center"><img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDJMMzIgMTR2MTJMMjAgMzhsLTEyLTEyVjE0TDIwIDJaIi8+PC9zdmc+" class="logo-img"/><span class="brand-txt">AI Act Pack™</span></div></div>""")
c1, c2, c3 = st.columns([1, 1, 1])
with c2:
    if st.button("📊 Pricing"):
        st.markdown('<meta http-equiv="refresh" content="0; url=#pricing">', unsafe_allow_html=True)
with c3:
    st.link_button("📞 Book 15-min Call", "https://calendly.com/aiactpack/expert", type="secondary")
st.markdown('<div class="main"></div>', unsafe_allow_html=True)

# ---------- HEADLINE ----------
st.markdown("### Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h – no lawyers.")

# ---------- 10-QUESTION WIZARD ----------
st.markdown('<a name="wizard"></a>', unsafe_allow_html=True)
st.markdown("### 🧭 10-Question Compliance Wizard")
with st.form("aiactpack_wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector      = st.selectbox("Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
        model_name  = st.text_input("Model trade name *", placeholder="CreditGPT-3")
        n_users     = st.number_input("Expected EU users *", min_value=0, max_value=50_000_000, value=5_000, step=1_000)
        high_risk   = st.selectbox("High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"])
        data_modal  = st.multiselect("Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"])
    with col2:
        deploy_env = st.selectbox("Deployment environment", ["AWS", "Azure", "GCP", "On-prem", "Hybrid"])
        ce_mark    = st.selectbox("Already CE-marked HW/SW ?", ["Yes", "No", "Partial"])
        target_mkt = st.multiselect("Target jurisdictions", ["EU", "UK", "USA", "Canada", "APAC"], default=["EU"])
        sandbox    = st.selectbox("Participated in EU AI sandbox ?", ["Yes", "No"])
        model_family = st.selectbox("Model family", ["GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"])
    data_sources = st.text_area("Training data sources (1 per line) *", placeholder="wikimedia.org\ninternal-2022-2024.csv")

    submitted = st.form_submit_button("Generate compliance pack →", type="primary")
    if submitted:
        if not model_name or not data_sources:
            st.error("Please complete mandatory fields.")
            st.stop()
        payload = {**locals()}
        with st.spinner("Running 47-prompt chain…"):
            zip_path = dummy_zip(payload)
        with open(zip_path, "rb") as f:
            st.download_button("⬇️ Download bundle", f, file_name=zip_path.name)
        os.remove(zip_path)
        st.success("Check your email for the invoice. Need more? See pricing below.")

# ---------- DUMMY ZIP (swap later) ----------
def dummy_zip(payload: dict):
    tmp = pathlib.Path(tempfile.mkdtemp())
    zip_path = tmp / f"AIACTPACK_{datetime.datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr("Executive_Summary.md", f"# EU AI Act Pack\n\nGenerated for {payload.get('model_name','model')}")
        z.writestr("payload.json", json.dumps(payload, indent=2))
    return zip_path

# ---------- PRICING ----------
st.markdown("---")
st.markdown('<a name="pricing"></a>', unsafe_allow_html=True)
st.markdown("## 💳 Transparent Pricing")
c1, c2, c3 = st.columns(3)
with c1:
    st.link_button("€497 – Starter", "https://buy.stripe.com/xxxxx497", use_container_width=True)
with c2:
    st.link_button("€1 997 – Growth", "https://buy.stripe.com/xxxxx1997", use_container_width=True)
with c3:
    st.link_button("€7 500 – Enterprise", "https://buy.stripe.com/xxxxx7500", use_container_width=True)

# ---------- BOOK CALL ----------
st.markdown("---")
st.markdown("### 📞 Book a 15-min Expert Call")
st.markdown("Choose a slot → receive Zoom link instantly.")
st.link_button("Open Calendly", "https://calendly.com/aiactpack/expert", type="primary")

# ---------- FOOTER ----------
st.markdown("---")
st.markdown('<div style="text-align:center;font-size:0.9rem;color:#777;">© 2025 AI Act Pack™ – compliance without chaos | <a href="https://www.aiactpack.com/terms">Terms</a> | <a href="https://www.aiactpack.com/privacy">Privacy</a></div>', unsafe_allow_html=True)
