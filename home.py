# Home.py
import streamlit as st, base64, time, os
from pathlib import Path

st.set_page_config(page_title="AIPacta - EU AI Act & NIST in 48 h", layout="wide",
                   page_icon="⚖️")
st.html("""
<style>
  .hero {background:#0f1117;color:#fff;padding:4rem 0;margin:-5rem -5rem 2rem -5rem;}
  .hero h1 {font-size:3rem;margin:0;}
  .hero p {font-size:1.2rem;margin-top:.5rem;}
  .btn {background:#00d4aa;color:#000;padding:.75rem 1.5rem;border-radius:8px;font-weight:600;text-decoration:none;display:inline-block;margin-top:1rem;}
</style>
<div class="hero">
  <div style="max-width:900px;margin:auto;padding:0 2rem;">
    <h1>AIPacta™</h1>
    <p>Generate EU AI-Act + NIST + ISO 42001 compliance packs in under two minutes.</p>
    <p><strong>No lawyers. No 6-month wait. 48-hour delivery guaranteed.</strong></p>
  </div>
</div>
""")

cols = st.columns(3)
with cols[0]: st.metric("Packs Delivered", "1,247")
with cols[1]: st.metric("Avg. Time Saved", "92 %")
with cols[2]: st.metric("CE-Mark Success", "100 %")

st.subheader("⚙️ 10-Question Wizard")
with st.form("wizard"):
    c1, c2 = st.columns(2)
    with c1:
        sector = st.selectbox("Industry*", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
        model  = st.text_input("Model name*", placeholder="CreditGPT-3")
        source = st.text_area("Data sources (1 per line)*", placeholder="wikimedia.org\ninternal-2022-2024")
    with c2:
        users = st.number_input("EU users*", 0, 50000000, 5000, step=1000)
        annex = st.selectbox("High-risk Annex III*", ["None", "Biometric", "HR", "Credit", "Insurance"])
        cloud = st.selectbox("Cloud*", ["AWS", "Azure", "GCP", "On-prem"])
    submit = st.form_submit_button("Generate pack →", type="primary")

if submit:
    if not (model and source):
        st.error("Complete mandatory fields.")
        st.stop()
    # ---- mock generation ----
    with st.spinner("Running 47-prompt chain…"):
        time.sleep(3)
        dummy = f"AIPacta-{model.replace(' ','_')}-pack.zip"
        Path(dummy).write_text("zip-content-here")  # real back-end creates zip
    st.success("Pack ready!")
    with open(dummy, "rb") as f:
        st.download_button("⬇️ Download compliance bundle", f, dummy)
    os.remove(dummy)

st.markdown("---")
st.subheader("💳 Transparent Pricing")
price = """
| Tier | What’s included | Price |
|------|-----------------|-------|
| Starter | EU AI-Act model-card + DoC template | €497 |
| Growth | Full EU + NIST pack (editable) | €1 997 |
| Enterprise | EU + NIST + ISO 42001 + white-label | €7 500 |
"""
st.markdown(price)

st.markdown("---")
st.subheader("📞 Book a 15-min expert call")
st.markdown("[https://calendly.com/aipacta/expert](https://calendly.com/aipacta/expert)")
st.caption("© 2025 AIPacta™ — compliance without chaos.")
