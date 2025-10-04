# ---------------------------------------------------------
#  home.py  –  AI Act Pack™  –  redesigned 2025-06-XX
#  NOWPayments crypto checkout + royalty-free icons
# ---------------------------------------------------------
import os, time, shutil, tempfile, zipfile, json
from pathlib import Path
import streamlit as st

# ------------------------------------------------------------------
#  0.  CONFIG –  fill once
# ------------------------------------------------------------------
COMPANY_NAME   = "AI Act Pack™"
COMPANY_VAT    = "EU123456789"                # ← your real VAT ID
COMPANY_ADDR   = "123 Compliance Blvd, Dublin, Ireland"
SUPPORT_EMAIL  = "support@aiactpack.com"
CALENDLY_URL   = "https://calendly.com/aiactpack/expert"

NOW_LINKS = {
    "individual":  "https://nowpayments.io/payment/?amount=50&currency=eur&invoice_id=aiactpack-individual",
    "eu_bundle":   "https://nowpayments.io/payment/?amount=899&currency=eur&invoice_id=aiactpack-eu",
    "nist_bundle": "https://nowpayments.io/payment/?amount=599&currency=eur&invoice_id=aiactpack-nist",
    "iso_bundle":  "https://nowpayments.io/payment/?amount=549&currency=eur&invoice_id=aiactpack-iso",
    "complete":    "https://nowpayments.io/payment/?amount=1997&currency=eur&invoice_id=aiactpack-full",
}

# ------------------------------------------------------------------
#  1.  ICONS (inline SVG)
# ------------------------------------------------------------------
ICON_SVG = {
    "document":  """<svg …> … </svg>""",   # shortened for brevity – keep your originals
    "shield":    """<svg …> … </svg>""",
    "clipboard": """<svg …> … </svg>""",
    "box":       """<svg …> … </svg>""",
    "coin":      """<svg …> … </svg>""",
    "qr":        """<svg …> … </svg>""",
}

# ------------------------------------------------------------------
#  2.  TEST-MODE SWITCH
# ------------------------------------------------------------------
TEST_MODE = st.query_params.get("test") == "1"

# ------------------------------------------------------------------
#  3.  ENGINE
# ------------------------------------------------------------------
from engine import build_block

# ------------------------------------------------------------------
#  4.  PAGE CONFIG  (SEO meta + accessibility)
# ------------------------------------------------------------------
st.set_page_config(
    page_title=f"{COMPANY_NAME} – EU AI Act, NIST & ISO 42001 evidence in 48 h",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ------------------------------------------------------------------
#  5.  INJECT <HEAD>  (JSON-LD + GDPR cookie script)
# ------------------------------------------------------------------
st.html(f"""
<script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js" data-cfasync="false"></script>
<script>
window.cookieconsent.initialise({{
  "palette": {{ "popup": { "background": "#003399" }, "button": { "background": "#00d4aa" } }},
  "content": {{ "message": "We use cookies to ensure compliance with EU laws and deliver a smooth experience." }}
}});
</script>

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "{COMPANY_NAME}",
  "url": "https://aiactpack.com",
  "potentialAction": {{
    "@type": "SearchAction",
    "target": "https://aiactpack.com/?search={{search_term_string}}",
    "query-input": "required name=search_term_string"
  }}
}}
</script>
""")

# ------------------------------------------------------------------
#  6.  CSS  (premium gradient + top bar)
# ------------------------------------------------------------------
st.html("""
<style>
header{visibility:hidden}
.top-bar{position:fixed;top:0;left:0;right:0;height:70px;background:#003399;
        display:flex;align-items:center;justify-content:space-between;
        padding:0 2rem;z-index:999;color:#fff;font-weight:600}
.top-bar a{color:#fff;text-decoration:none}
.hero{padding:6rem 1rem 3rem;text-align:center}
.hero h1{font-size:2.5rem;color:#003399;margin-bottom:.5rem}
.hero p{font-size:1.1rem;color:#444;max-width:600px;margin:auto}
.proof-bar{display:flex;justify-content:center;gap:2rem;margin-top:2rem;font-size:.9rem}
.proof-bar div{display:flex;align-items:center;gap:.3rem}
.cta-group{margin-top:2rem;display:flex;gap:1rem;justify-content:center}
.cta-group a{padding:.75rem 1.5rem;border-radius:6px;font-weight:600;text-decoration:none}
.btn-primary{background:#00d4aa;color:#fff}
.btn-secondary{background:#fff;color:#003399;border:2px solid #003399}
@media(max-width:768px){.proof-bar{flex-direction:column;gap:.5rem}}
</style>
""")

# ------------------------------------------------------------------
#  7.  TOP BAR
# ------------------------------------------------------------------
st.html(f"""
<div class="top-bar">
  <div style="display:flex;align-items:center">
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDJMMzIgMTR2MTJMMjAgMzhsLTEyLTEyVjE0TDIwIDJaIi8+PC9zdmc+" alt="logo" style="height:40px;margin-right:12px">
    <span>{COMPANY_NAME}</span>
  </div>
  <div style="display:flex;gap:1rem;align-items:center">
    <a href="{CALENDLY_URL}" target="_blank">Book 15-min Call</a>
  </div>
</div>
""")

# ------------------------------------------------------------------
#  8.  HERO  (value prop + social proof)
# ------------------------------------------------------------------
st.html("""
<div class="hero">
  <h1>Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h—no lawyers.</h1>
  <p>Up to €30 M fines apply from 2 Aug 2025.  Save €15 k+ in advisory fees with battle-tested templates trusted by 200+ AI teams.</p>
  <div class="proof-bar">
    <div>✅ 217 AI systems assessed</div>
    <div>✅ 38 Notified-Body-ready reports</div>
    <div>✅ 12-day average time-saving</div>
  </div>
  <div class="cta-group">
    <a href="#wizard" class="btn-primary">Start 10-Question Wizard</a>
    <a href="https://www.aiactpack.com/samples" class="btn-secondary">See sample report</a>
  </div>
</div>
""")

# ------------------------------------------------------------------
#  9.  LEAD MAGNET  (email gate → free readiness score)
# ------------------------------------------------------------------
with st.container(border=True):
    st.markdown("### 🎯 Free EU AI-Act Readiness Score (2 min)")
    c1, c2 = st.columns([2, 1])
    with c1:
        email = st.text_input("Business email", placeholder="alice@company.com")
    with c2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Get my score →", type="primary"):
            if "@" not in email:
                st.error("Please enter a valid email.")
            else:
                # TODO: store email + redirect to Typeform / Tally
                st.success("Check your inbox—link on its way!")
                st.balloons()

# ------------------------------------------------------------------
#  10.  10-QUESTION WIZARD  (anchor link #wizard)
# ------------------------------------------------------------------
st.html('<div id="wizard"></div>')
st.markdown("### 🧭 10-Question Compliance Wizard")
with st.form("aiactpack_wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector      = st.selectbox("Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
        model_name  = st.text_input("Model trade name *", placeholder="CreditGPT-3")
        n_users     = st.number_input("Expected EU users *", 0, 50_000_000, 5_000, 1_000)
        high_risk   = st.selectbox("High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"])
        data_modal  = st.multiselect("Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"], default=["Text"])
    with col2:
        deploy_env  = st.selectbox("Deployment environment", ["AWS", "Azure", "GCP", "On-prem", "Hybrid"])
        ce_mark     = st.selectbox("Already CE-marked HW/SW ?", ["Yes", "No", "Partial"])
        target_mkt  = st.multiselect("Target jurisdictions", ["EU", "UK", "USA", "Canada", "APAC"], default=["EU"])
        sandbox     = st.selectbox("Participated in EU AI sandbox ?", ["Yes", "No"])
        model_family= st.selectbox("Model family", ["GPT-3.5-turbo", "GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"])
    data_sources = st.text_area("Training data sources (1 per line) *", placeholder="wikimedia.org\ninternal-2022-2024.csv")

    # ------------- purchase mode ----------------
    mode = st.radio(
        "Select purchase mode:",
        ["Individual prompts (€50 each)", "Individual bundle", "Complete bundle (€1 997)"],
        help="Pay only for what you need.",
    )
    selected_individual: list[str] = []
    bundle_choice: str | None = None

    if mode == "Individual prompts (€50 each)":
        st.markdown("#### Select individual prompts")
        for family, codes, cols, icon in (
            ("EU AI-Act",   ["A00"] + [f"A{j:02d}" for j in range(1, 21)], 4, "document"),
            ("NIST AI RMF", [f"B{j:02d}" for j in range(1, 15)],          4, "shield"),
            ("ISO 42001",   [f"C{j:02d}" for j in range(1, 14)],          4, "clipboard"),
        ):
            st.markdown(f"**{family}**")
            columns = st.columns(cols)
            for i, code in enumerate(codes):
                with columns[i % cols]:
                    if st.checkbox(f"{code} (€50)", value=False, key=code):
                        selected_individual.append(code)

    elif mode == "Individual bundle":
        bundle_choice = st.radio(
            "Which bundle do you need?",
            ["EU AI-Act  (€899)", "NIST AI RMF  (€599)", "ISO 42001  (€549)"],
            horizontal=True,
        )

    submitted = st.form_submit_button("Generate selected packs →", type="primary")

# ------------------------------------------------------------------
#  11.  POST-SUBMIT  (same logic as before)
# ------------------------------------------------------------------
if submitted:
    if not model_name or not data_sources:
        st.error("Please complete mandatory fields."); st.stop()
    if mode == "Individual bundle" and not bundle_choice:
        st.error("Please select which individual bundle you need."); st.stop()

    payload = {k: v for k, v in locals().items() if k in {
        "sector", "model_name", "n_users", "high_risk", "data_modal",
        "deploy_env", "ce_mark", "target_mkt", "sandbox", "model_family", "data_sources"
    }}

    if mode == "Individual prompts (€50 each)":
        blocks = selected_individual
    elif mode == "Individual bundle":
        bundle_map = {
            "EU AI-Act  (€899)":   ["A00"] + [f"A{j:02d}" for j in range(1, 21)],
            "NIST AI RMF  (€599)": [f"B{j:02d}" for j in range(1, 15)],
            "ISO 42001  (€549)":   [f"C{j:02d}" for j in range(1, 14)],
        }
        blocks = bundle_map[bundle_choice]
    else:  # complete
        blocks = ["A00"] + [f"A{j:02d}" for j in range(1, 21)] + \
                 [f"B{j:02d}" for j in range(1, 15)] + \
                 [f"C{j:02d}" for j in range(1, 14)]

    if not blocks:
        st.error("No blocks selected."); st.stop()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        built_files: list[Path] = []
        for code in blocks:
            with st.spinner(f"Running {code} ..."):
                built_files.append(build_block(code, payload))

        pack_name = (
            "Complete_Bundle" if mode == "Complete bundle (€1 997)" else
            f"{bundle_choice.replace(' ', '_')}_Bundle" if mode == "Individual bundle" else
            "Individual_Prompts"
        ) + f"_{int(time.time())}.zip"

        final_zip = tmpdir_path / pack_name
        with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for bf in built_files:
                zf.write(bf, bf.name)

        persist_dir = Path(tempfile.mkdtemp(prefix="aiactpack_"))
        saved_zip = shutil.copy2(final_zip, persist_dir / final_zip.name)

    st.session_state.zips = [saved_zip]
    st.session_state.cart = blocks
    st.success("All blocks packed into **one** zip.  Pay once below, then download.")

# ------------------------------------------------------------------
#  12.  DOWNLOAD / CRYPTO CHECKOUT  (unchanged logic)
# ------------------------------------------------------------------
if st.session_state.zips:
    st.markdown("---")
    st.markdown("### 📦 Download")
    z = st.session_state.zips[0]

    if TEST_MODE:
        st.success("🎁 TEST MODE – download is free.")
        st.download_button(
            label=f"⬇️ {z.name}",
            data=z.read_bytes(),
            file_name=z.name,
            mime="application/zip",
            key="final_zip",
        )
    else:
        st.html(f'{ICON_SVG["coin"]}{ICON_SVG["qr"]}<small>Crypto checkout (auto fiat conversion)</small>')
        if st.button("Create crypto checkout session", type="primary"):
            cart = st.session_state.cart
            if set(cart) == set(["A00"] + [f"A{j:02d}" for j in range(1, 21)] +
                                [f"B{j:02d}" for j in range(1, 15)] +
                                [f"C{j:02d}" for j in range(1, 14)]):
                url = NOW_LINKS["complete"]
            elif all(c.startswith("A") for c in cart):
                url = NOW_LINKS["eu_bundle"]
            elif all(c.startswith("B") for c in cart):
                url = NOW_LINKS["nist_bundle"]
            elif all(c.startswith("C") for c in cart):
                url = NOW_LINKS["iso_bundle"]
            else:
                url = NOW_LINKS["individual"]
            st.session_state.checkout_url = url

        if st.session_state.checkout_url:
            st.link_button("Pay now with crypto →", st.session_state.checkout_url, type="primary")

# ------------------------------------------------------------------
#  13.  FOOTER  (GDPR-compliant)
# ------------------------------------------------------------------
st.markdown("---")
st.markdown(
    f"""<div style='text-align:center;font-size:.85rem;color:#777'>
    © 2025 {COMPANY_NAME} – compliance without chaos<br>
    {COMPANY_NAME} | VAT: {COMPANY_VAT} | {COMPANY_ADDR}<br>
    <a href="mailto:{SUPPORT_EMAIL}">Contact</a> |
    <a href="https://www.aiactpack.com/terms" target="_blank">Terms</a> |
    <a href="https://www.aiactpack.com/privacy" target="_blank">Privacy</a> |
    <a href="https://www.aiactpack.com/cookies" target="_blank">Cookie Policy</a>
    </div>""",
    unsafe_allow_html=True,
)
