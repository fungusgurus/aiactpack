# Home.py
import streamlit as st
from datetime import datetime
import base64, os

##############################################################################
# 0. PAGE CONFIG & CSS
##############################################################################
st.set_page_config(
    page_title="AI Act Pack™ – EU AI Act compliance in 48 h",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.html("""
<style>
/* Google-font look-alike */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
html, body, [class*="css"]  {font-family: 'Inter', sans-serif;}

/* header bar */
.header {display:flex;align-items:center;padding:1rem 0;margin-bottom:2rem;}
.logo   {width:48px;margin-right:12px;}
.brand  {font-size:1.6rem;font-weight:700;color:#003399;}

/* wizard */
.step   {font-weight:600;margin-bottom:0.4rem;color:#003399;}
.card   {background:#ffffff;border:1px solid #e0e0e0;border-radius:8px;padding:1.5rem;margin-bottom:1rem;}

/* pricing */
.price-card {background:#f7f9fc;border:1px solid #dde4ee;border-radius:10px;padding:2rem;text-align:center;flex:1;margin:0 0.5rem;}
.price-amount{font-size:2.2rem;font-weight:700;color:#003399;}
.price-desc {color:#555;margin:0.8rem 0;}
.btn-primary{background:#003399;color:#fff;border:0;padding:0.75rem 1.5rem;border-radius:6px;font-weight:600;display:inline-block;margin-top:1rem;}

/* footer */
.footer {text-align:center;margin-top:4rem;font-size:0.9rem;color:#777;}
</style>
""")

##############################################################################
# 1. LOGO / HEADER
##############################################################################
c1, c2 = st.columns([1, 20])
with c1:
    # PLACEHOLDER : replace with base64 of your logo
    st.html('<img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDgiIGhlaWdodD0iNDgiIGZpbGw9IiMwMDMzOTkiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTI0IDJMNDAgMTZ2MTZMMjQgNDZMOCAzMlYxNkwyNCAyWiIvPjwvc3ZnPg==" class="logo">')
with c2:
    st.html('<div class="brand">AI Act Pack™</div>')
st.markdown("### Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h – no lawyers.")

##############################################################################
# 2. 10-QUESTION WIZARD (sidebar multi-step)
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

##############################################################################
# 3. DUMMY ZIP (replace with real engine.py call)
##############################################################################
def dummy_zip(payload: dict):
    import tempfile, zipfile, pathlib, json
    tmp = pathlib.Path(tempfile.mkdtemp())
    zip_path = tmp / f"AIACTPACK_{datetime.utcnow():%Y%m%d_%H%M%S}.zip"
    with zipfile.ZipFile(zip_path, 'w') as z:
        z.writestr("Executive_Summary.md", "# EU AI Act Pack\n\nGenerated for " + payload["model_name"])
        z.writestr("payload.json", json.dumps(payload, indent=2))
    return zip_path

##############################################################################
# 4. TRANSPARENT PRICING
##############################################################################
st.markdown("---")
st.markdown("## 💳 Transparent Pricing")
st.markdown('<div style="display:flex;gap:1rem;">', unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown("""<div class="price-card">
    <div class="price-amount">€497</div>
    <div class="price-desc">Starter</div>
    <ul><li>EU model-card + DoC</li><li>48 h delivery</li></ul>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div class="price-card">
    <div class="price-amount">€1 997</div>
    <div class="price-desc">Growth</div>
    <ul><li>EU + NIST packs</li><li>Editable markdown</li></ul>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown("""<div class="price-card">
    <div class="price-amount">€7 500</div>
    <div class="price-desc">Enterprise</div>
    <ul><li>All + ISO 42001</li><li>White-label rights</li></ul>
    </div>""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Stripe buttons (simple redirect links – no server code)
st.markdown("### Upgrade instantly")
c1, c2, c3 = st.columns(3)
with c1:
    st.link_button("Pay €497 – Starter",   "https://buy.stripe.com/xxxxx497")
with c2:
    st.link_button("Pay €1 997 – Growth",  "https://buy.stripe.com/xxxxx1997")
with c3:
    st.link_button("Pay €7 500 – Enterprise", "https://buy.stripe.com/xxxxx7500")

##############################################################################
# 5. BOOK 15-MIN EXPERT CALL (Calendly embed)
##############################################################################
st.markdown("---")
st.markdown("## 📞 Book a 15-min Expert Call")
st.markdown("Choose a slot → receive Zoom link instantly.")
# Inline Calendly embed (popup)
calendly_url = "https://calendly.com/aiactpack/expert"
st.html(f"""
<!-- Calendly inline widget -->
<div class="calendly-inline-widget" data-url="{calendly_url}" style="min-width:320px;height:630px;"></div>
<script type="text/javascript" src="https://assets.calendly.com/assets/external/widget.js" async></script>
""")

##############################################################################
# 6. FOOTER
##############################################################################
st.markdown("---")
st.markdown('<div class="footer">© 2025 AI Act Pack™ – compliance without chaos  |  <a href="https://www.aiactpack.com/terms">Terms</a>  |  <a href="https://www.aiactpack.com/privacy">Privacy</a></div>', unsafe_allow_html=True)

