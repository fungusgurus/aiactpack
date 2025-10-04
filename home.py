# --------------------------------------------------
#  home.py  –  AI Act Pack™
#  NOWPayments crypto checkout + royalty-free generic icons
# --------------------------------------------------
import os, time, shutil, tempfile, zipfile
from pathlib import Path
import streamlit as st

# ------------------------------------------------------------------
#  0.  CONFIG –  paste your NOWPayments permanent links here
# ------------------------------------------------------------------
NOW_LINKS = {
    "individual":  "https://nowpayments.io/payment/?amount=50&currency=eur&invoice_id=aiactpack-individual",
    "eu_bundle":   "https://nowpayments.io/payment/?amount=899&currency=eur&invoice_id=aiactpack-eu",
    "nist_bundle": "https://nowpayments.io/payment/?amount=599&currency=eur&invoice_id=aiactpack-nist",
    "iso_bundle":  "https://nowpayments.io/payment/?amount=549&currency=eur&invoice_id=aiactpack-iso",
    "complete":    "https://nowpayments.io/payment/?amount=1997&currency=eur&invoice_id=aiactpack-full",
}

# ------------------------------------------------------------------
#  1.  ROYALTY-FREE ICONS  (inline SVG)
# ------------------------------------------------------------------
ICON_SVG = {
    "document": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#003399" stroke-width="2" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/><path stroke-linecap="round" stroke-linejoin="round" d="M9 17l-2 2 2 2 4-4"/></svg>""",
    "shield": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#003399" stroke-width="2" viewBox="0 0 24 24"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="M9 12l2 2 4-4"/></svg>""",
    "clipboard": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#003399" stroke-width="2" viewBox="0 0 24 24"><path d="M16 4h2a2 2 0 012 2v14a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2h2"/><rect x="8" y="2" width="8" height="4" rx="1" ry="1"/><path d="M9 14h6M9 18h6"/></svg>""",
    "box": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#00d4aa" stroke-width="2" viewBox="0 0 24 24"><path d="M21 16V8a2 2 0 00-1-1.73l-7-4a2 2 0 00-2 0l-7 4A2 2 0 003 8v8a2 2 0 001 1.73l7 4a2 2 0 002 0l7-4A2 2 0 0021 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>""",
    "coin": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#f7931a" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg>""",
    "qr": """<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#f7931a" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/><rect x="9" y="3" width="4" height="4" rx="1"/><rect x="3" y="11" width="4" height="4" rx="1"/><rect x="11" y="11" width="4" height="4" rx="1"/><rect x="15" y="7" width="4" height="4" rx="1"/><rect x="7" y="15" width="4" height="4" rx="1"/></svg>""",
}

# ------------------------------------------------------------------
#  2.  TEST-MODE SWITCH  (?test=1  in URL)
# ------------------------------------------------------------------
TEST_MODE = any(
    str(v).lower() == "1" for k, v in st.query_params.items() if k.lower() == "test"
)

# ------------------------------------------------------------------
#  3.  ENGINE IMPORT
# ------------------------------------------------------------------
from engine import build_block

# ------------------------------------------------------------------
#  4.  PAGE SET-UP
# ------------------------------------------------------------------
st.set_page_config(page_title="AI Act Pack™", page_icon="⚖️", layout="centered")

# --- premium gradient background + fixed top bar (no images) -----
st.html("""
<style>
header{visibility:hidden}
.top-bar{position:fixed;top:0;left:0;right:0;height:70px;background:#003399;
        display:flex;align-items:center;justify-content:space-between;
        padding:0 2rem;z-index:999;}
.logo-img{height:40px;margin-right:12px}
.brand-txt{font-size:1.4rem;font-weight:700;color:#fff}
.nav-group{display:flex;gap:.75rem}
.main{padding-top:80px}
body{background:linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
     background-attachment:fixed;}
@media (max-width:768px){
  body{background:linear-gradient(135deg, #eef2f6 0%, #dfe9f3 100%);}
}
</style>
<div class="top-bar">
  <div style="display:flex;align-items:center">
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDJMMzIgMTR2MTJMMjAgMzhsLTEyLTEyVjE0TDIwIDJaIi8+PC9zdmc+" class="logo-img"/>
    <span class="brand-txt">AI Act Pack™</span>
  </div>
  <div class="nav-group">
    <span style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;">€50</span>
    <span style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;">€899</span>
    <span style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;">€599</span>
    <span style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;">€549</span>
    <span style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;">€1997</span>
    <a href="https://calendly.com/aiactpack/expert" target="_blank" style="background:#00d4aa;color:#fff;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">Book 15-min Call</a>
  </div>
</div>
<div class="main"></div>
""")

# ------------------------------------------------------------------
#  5.  SESSION STATE
# ------------------------------------------------------------------
for key, default in (("zips", []), ("cart", []), ("checkout_url", None)):
    if key not in st.session_state:
        setattr(st.session_state, key, default)

# ------------------------------------------------------------------
#  6.  CONTENT HEADER
# ------------------------------------------------------------------
st.markdown("### Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 hours – no lawyers.")
st.markdown("### 🧭 10-Question Compliance Wizard")

# ------------------------------------------------------------------
#  7.  WIZARD FORM
# ------------------------------------------------------------------
with st.form("aiactpack_wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector = st.selectbox("Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
        model_name = st.text_input("Model trade name *", placeholder="CreditGPT-3")
        n_users = st.number_input("Expected EU users *", min_value=0, max_value=50_000_000, value=5_000, step=1_000)
        high_risk = st.selectbox("High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"])
        data_modal = st.multiselect("Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"], default=["Text"])
    with col2:
        deploy_env = st.selectbox("Deployment environment", ["AWS", "Azure", "GCP", "On-prem", "Hybrid"])
        ce_mark = st.selectbox("Already CE-marked HW/SW ?", ["Yes", "No", "Partial"])
        target_mkt = st.multiselect("Target jurisdictions", ["EU", "UK", "USA", "Canada", "APAC"], default=["EU"])
        sandbox = st.selectbox("Participated in EU AI sandbox ?", ["Yes", "No"])
        model_family = st.selectbox("Model family", ["GPT-3.5-turbo", "GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"])

    data_sources = st.text_area("Training data sources (1 per line) *", placeholder="wikimedia.org\ninternal-2022-2024.csv")

    mode = st.radio(
        "Select purchase mode:",
        ["Individual prompts (€50 each)", "Individual bundle", "Complete bundle (€1 997)"],
        help="Pay only for what you need.",
    )

    # ------------- dynamic block selector ----------------
    selected_individual: list[str] = []
    bundle_choice: str | None = None

    if mode == "Individual prompts (€50 each)":
        st.markdown("### 📋 Select individual prompts")
        for family, codes, cols, icon in (
            ("EU AI-Act",   ["A00"] + [f"A{j:02d}" for j in range(1, 21)], 4, "document"),
            ("NIST AI RMF", [f"B{j:02d}" for j in range(1, 15)],          4, "shield"),
            ("ISO 42001",   [f"C{j:02d}" for j in range(1, 14)],          4, "clipboard"),
        ):
            st.markdown(f"#### {family}")
            st.html(f'<div style="display:flex;gap:8px;align-items:center;">{ICON_SVG[icon]}<small>{family} prompts</small></div>')
            columns = st.columns(cols)
            for i, code in enumerate(codes):
                with columns[i % cols]:
                    if st.checkbox(f"{code} (€50)", value=False, key=code):
                        selected_individual.append(code)

    elif mode == "Individual bundle":
        st.markdown("### 📦 Choose your bundle")
        st.html(f'<div style="display:flex;gap:8px;align-items:center;">{ICON_SVG["box"]}<small>Bundle icon</small></div>')
        bundle_choice = st.radio(
            "Which bundle do you need?",
            ["EU AI-Act  (€899)", "NIST AI RMF  (€599)", "ISO 42001  (€549)"],
            horizontal=True,
            key="bundle_choice",
        )
        if not bundle_choice:
            st.warning("Please choose a bundle above.")

    elif mode == "Complete bundle (€1 997)":
        st.info("✅ Complete bundle selected – all prompts included.")

    submitted = st.form_submit_button("Generate selected packs →", type="primary")

# ------------------------------------------------------------------
#  8.  POST-SUBMIT
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

    # build everything into ONE zip
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
#  9.  DOWNLOAD / PAYMENT AREA  (NOWPayments crypto checkout)
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
        st.html(f'<div style="display:flex;gap:8px;align-items:center;">{ICON_SVG["coin"]}{ICON_SVG["qr"]}<small>Crypto checkout (auto fiat conversion)</small></div>')
        st.info("Pay once in **crypto** (any wallet).  Fiat conversion & fiat payout handled automatically.")
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
#  10.  FOOTER
# ------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:0.9rem;color:#777;">'
    "© 2025 AI Act Pack™ – compliance without chaos | "
    '<a href="https://www.aiactpack.com/terms.md" target="_blank">Terms</a> | '
    '<a href="https://www.aiactpack.com/privacy.md" target="_blank">Privacy</a>'
    "</div>",
    unsafe_allow_html=True,
)

