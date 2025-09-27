# Home.py
import streamlit as st, os, tempfile, pathlib, datetime
from dummy_zip import dummy_zip   # swap to engine.generate_pack later

##############################################################################
# PAGE CONFIG
##############################################################################
st.set_page_config(page_title="AI Act Pack™", page_icon="⚖️", layout="centered")
st.scroll_to("pricing") (or st.session_state jump)
st.link_button(..., type="secondary") opens Calendly in new tab — no iframe block.

  
##############################################################################
# 0.  PAGE CONFIG  +  ELEGANT TOP-BAR  (sticky, dark, full-width)
##############################################################################
st.set_page_config(page_title="AI Act Pack™", page_icon="⚖️", layout="centered")

st.html("""
<style>
/* ---- reset ---- */
header {visibility:hidden}   /* hide default Streamlit header */
/* ---- top-bar ---- */
.top-bar{
  position:fixed;
  top:0;left:0;right:0;
  height:70px;
  background:#003399;
  display:flex;
  align-items:center;
  justify-content:space-between;
  padding:0 2rem;
  z-index:999;
  box-shadow:0 2px 8px rgba(0,0,0,.15);
}
.top-bar a{
  color:#ffffff;
  text-decoration:none;
  margin-left:2rem;
  font-weight:500;
  transition:opacity .2s;
}
.top-bar a:hover{opacity:.8}
.logo-img{height:40px;margin-right:12px}
.brand-txt{font-size:1.4rem;font-weight:700;color:#fff}
/* ---- push page down ---- */
.main {padding-top:80px}
</style>
<div class="top-bar">
  <div style="display:flex;align-items:center">
    <!--  REPLACE WITH YOUR LOGO (base64 or url)  -->
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDJMMzIgMTR2MTJMMjAgMzhsLTEyLTEyVjE0TDIwIDJaIi8+PC9zdmc+" class="logo-img"/>
    <span class="brand-txt">AI Act Pack™</span>
  </div>
  <nav>
    <a href="#wizard">Wizard</a>
    <a href="#pricing">Pricing</a>
    <a href="https://calendly.com/aiactpack/expert" target="_blank">Book Call</a>
  </nav>
</div>
""")
##############################################################################
# 1. HEADER & LOGO
##############################################################################
c1, c2 = st.columns([1, 20])
with c1:
    st.html('<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIGZpbGw9IiMwMDMzOTkiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTI0IDJMNDAgMTZ2MTZMMjQgNDZMOCAzMlYxNkwyNCAyWiIvPjwvc3ZnPg==" width="48">')
with c2:
    st.title("AI Act Pack™")
st.markdown("Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h – no lawyers.")

##############################################################################
# 2. 10-QUESTION WIZARD
##############################################################################
st.markdown("### 🧭 10-Question Compliance Wizard")
with st.form("wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector     = st.selectbox("Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
        model_name = st.text_input("Model trade name *", placeholder="CreditGPT-3")
        n_users    = st.number_input("Expected EU users *", min_value=0, max_value=50_000_000, value=5_000, step=1_000)
        high_risk  = st.selectbox("High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"])
        data_modal = st.multiselect("Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"])
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
        payload = {**locals()}  # captures all above vars
        with st.spinner("Running 47-prompt chain…"):
            zip_path = dummy_zip(payload)
        with open(zip_path, "rb") as f:
            st.download_button("⬇️ Download bundle", f, file_name=zip_path.name)
        os.remove(zip_path)
        st.success("Check your email for the invoice. Need more? See pricing below.")

##############################################################################
# 3. PRICING
##############################################################################
st.markdown("---")
st.markdown("## 💳 Transparent Pricing")
c1, c2, c3 = st.columns(3)
with c1:
    st.link_button("Pay €497 – Starter", "https://buy.stripe.com/xxxxx497")
with c2:
    st.link_button("Pay €1 997 – Growth", "https://buy.stripe.com/xxxxx1997")
with c3:
    st.link_button("Pay €7 500 – Enterprise", "https://buy.stripe.com/xxxxx7500")

##############################################################################
# 4. CALENDLY
##############################################################################
st.markdown("---")
st.markdown("### 📞 Book a 15-min Expert Call")
st.html('<div class="calendly-inline-widget" data-url="https://calendly.com/aiactpack/expert" style="min-width:320px;height:630px;"></div><script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>')

##############################################################################
# 5. FOOTER
##############################################################################
st.markdown("---")
st.markdown('<div style="text-align:center;font-size:0.9rem;color:#777;">© 2025 AI Act Pack™ – compliance without chaos | <a href="https://www.aiactpack.com/terms">Terms</a> | <a href="https://www.aiactpack.com/privacy">Privacy</a></div>', unsafe_allow_html=True)




