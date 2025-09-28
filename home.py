# home.py
import streamlit as st, os, tempfile, pathlib, datetime, zipfile, json
from engine import generate_pack

##############################################################################
# PAGE CONFIG
##############################################################################
st.set_page_config(page_title="AI Act Pack™", page_icon="⚖️", layout="centered")

##############################################################################
# STICKY TOP-BAR (logo left, buttons right)
##############################################################################
st.html(r"""
<style>
header{visibility:hidden}.top-bar{position:fixed;top:0;left:0;right:0;height:70px;background:#003399;display:flex;align-items:center;justify-content:space-between;padding:0 2rem;z-index:999;box-shadow:0 2px 8px rgba(0,0,0,.15);}
.logo-img{height:40px;margin-right:12px}.brand-txt{font-size:1.4rem;font-weight:700;color:#fff}.nav-group{display:flex;align-items:center;gap:.75rem}.main{padding-top:80px}
</style>
<div class="top-bar">
  <div style="display:flex;align-items:center">
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDJMMzIgMTR2MTJMMjAgMzhsLTEyLTEyVjE0TDIwIDJaIi8+PC9zdmc+" class="logo-img"/>
    <span class="brand-txt">AI Act Pack™</span>
  </div>
  <div class="nav-group">
    <a href="https://buy.stripe.com/xxxxx497" target="_blank" style="background:#ffffff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">€497</a>
    <a href="https://buy.stripe.com/xxxxx1997" target="_blank" style="background:#ffffff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">€1 997</a>
    <a href="https://calendly.com/aiactpack/expert" target="_blank" style="background:#00d4aa;color:#fff;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">Book 15-min Call</a>
  </div>
</div>
""")
st.markdown('<div class="main"></div>', unsafe_allow_html=True)

##############################################################################
# HEADLINE
##############################################################################
st.markdown("### Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h – no lawyers.")

##############################################################################
# 10-QUESTION WIZARD (with help & dropdowns)
##############################################################################
st.markdown('<a name="wizard"></a>', unsafe_allow_html=True)
st.markdown("### 🧭 10-Question Compliance Wizard")
with st.form("aiactpack_wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector = st.selectbox("Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"], help="Pick the market you operate in – determines high-risk classification under EU AI-Act Annex III.")
        model_name = st.text_input("Model trade name *", placeholder="CreditGPT-3", help="Public-facing product name (used in CE-marking declaration).")
        n_users = st.number_input("Expected EU users *", min_value=0, max_value=50_000_000, value=5_000, step=1_000, help=">10 000 users triggers mandatory Notified-Body audit.")
        high_risk = st.selectbox("High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"], help="If you pick anything except 'None' the system is HIGH-RISK under EU AI-Act.")
        data_modal = st.multiselect("Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"], default=["Text"], help="Which data types does the model ingest?  Affects bias tests & cyber-security controls.")
    with col2:
        deploy_env = st.selectbox("Deployment environment", ["AWS", "Azure", "GCP", "On-prem", "Hybrid"], help="Cloud vs. on-prem determines encryption & supply-chain evidence required.")
        ce_mark = st.selectbox("Already CE-marked HW/SW ?", ["Yes", "No", "Partial"], help="If hardware is already CE-marked you only need a delta-assessment.")
        target_mkt = st.multiselect("Target jurisdictions", ["EU", "UK", "USA", "Canada", "APAC"], default=["EU"], help="Extra jurisdictions add extra rules (UK White-Paper, USA NIST, etc.).")
        sandbox = st.selectbox("Participated in EU AI sandbox ?", ["Yes", "No"], help="Sandbox exit gives you a lighter conformity route.")
        model_family = st.selectbox("Model family", ["GPT-3.5-turbo", "GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"], help="Transformer vs. tree-based = different adversarial tests & metrics.")
    data_sources = st.text_area("Training data sources (1 per line) *", placeholder="wikimedia.org\ninternal-2022-2024.csv", help="List every source – regulators check representativeness & rights.")

    # ---------- GENERATE BUTTON ----------
    submitted = st.form_submit_button("Generate compliance pack →", type="primary")
    if submitted:
        if not model_name or not data_sources:
            st.error("Please complete mandatory fields.")
            st.stop()
        payload = {**locals()}
        with st.spinner("Running 47-prompt chain…"):
            zip_path = generate_pack(payload)
        with open(zip_path, "rb") as f:
            st.download_button("⬇️ Download bundle", f, file_name=zip_path.name)
        os.remove(zip_path)
        st.success("Check your email for the invoice. Need more? See pricing below.")

##############################################################################
# PRICING SECTION
##############################################################################
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

##############################################################################
# BOOK CALL
##############################################################################
st.markdown("---")
st.markdown("### 📞 Book a 15-min Expert Call")
st.markdown("Choose a slot → receive Zoom link instantly.")
st.link_button("Open Calendly", "https://calendly.com/aiactpack/expert", type="primary")

##############################################################################
# FOOTER
##############################################################################
st.markdown("---")
st.markdown('<div style="text-align:center;font-size:0.9rem;color:#777;">© 2025 AI Act Pack™ – compliance without chaos | <a href="?page=terms">Terms</a> | <a href="?page=privacy">Privacy</a></div>', unsafe_allow_html=True)
