# home.py  –  drop-in replacement with all fixes
# 1. Individual-prompt check-boxes stay visible
# 2. Individual-bundle (€497) waits for EU/NIST/ISO choice
# 3. Test-mode bypass with ?test=1
# --------------------------------------------------
import os
import shutil
import tempfile
import zipfile
from pathlib import Path

import streamlit as st

# ----  ENGINE STUBS  (move here until you plug in real engine.py) ----
def build_block(code: str, payload: dict) -> Path:
    out = Path(tempfile.mktemp(suffix=".md"))
    out.write_text(f"# {code}\nPayload: {payload}\n", encoding="utf-8")
    return out

def zip_block(md_path: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(md_path, md_path.name)
def create_stripe_checkout_session(cart: list[str]) -> str:
    return "https://stripe.com/docs/testing"
# --------------------------------------------------------------

# ----------  TEST-MODE BYPASS  ----------
TEST_MODE = st.query_params.get("test", "") == "1"

# ----------  PAGE DECOR  ----------
st.set_page_config(page_title="AI Act Pack™", page_icon="⚖️", layout="centered")

st.html(
    r"""
<style>
header{visibility:hidden}
.top-bar{position:fixed;top:0;left:0;right:0;height:70px;background:#003399;
        display:flex;align-items:center;justify-content:space-between;
        padding:0 2rem;z-index:999}
.logo-img{height:40px;margin-right:12px}
.brand-txt{font-size:1.4rem;font-weight:700;color:#fff}
.nav-group{display:flex;gap:.75rem}
.main{padding-top:80px}
</style>
<div class="top-bar">
  <div style="display:flex;align-items:center">
    <img src="data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNDAiIGhlaWdodD0iNDAiIGZpbGw9IiNmZmYiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHBhdGggZD0iTTIwIDJMMzIgMTR2MTJMMjAgMzhsLTEyLTEyVjE0TDIwIDJaIi8+PC9zdmc+" class="logo-img"/>
    <span class="brand-txt">AI Act Pack™</span>
  </div>
  <div class="nav-group">
    <a href="" target="_self" style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">€497</a>
    <a href="" target="_self" style="background:#fff;color:#003399;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">€1 997</a>
    <a href="https://calendly.com/aiactpack/expert" target="_blank" style="background:#00d4aa;color:#fff;padding:.45rem .9rem;border-radius:6px;font-weight:600;text-decoration:none;">Book 15-min Call</a>
  </div>
</div>
"""
)
st.markdown('<div class="main"></div>', unsafe_allow_html=True)

st.markdown("### Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h – no lawyers.")

# ----------  SESSION STATE  ----------
if "zips" not in st.session_state:
    st.session_state.zips: list[Path] = []
if "cart" not in st.session_state:
    st.session_state.cart: list[str] = []
if "checkout_url" not in st.session_state:
    st.session_state.checkout_url: str | None = None

# ----------  10-QUESTION WIZARD  ----------
st.markdown("### 🧭 10-Question Compliance Wizard")
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

    # ---- MODE ----
    mode = st.radio(
        "Select purchase mode:",
        ["Individual prompts (€50 each)", "Individual bundle (€497)", "Complete bundle (€1 397)"],
        help="Pay only for what you need.",
    )

    # ---- INDIVIDUAL PROMPTS  (always drawn inside form) ----
    selected_individual: list[str] = []
    if mode == "Individual prompts (€50 each)":
        st.markdown("### 📋 Select individual prompts")
        cols = st.columns(3)
        for i in range(1, 21):
            with cols[(i - 1) % 3]:
                if st.checkbox(f"A{i:02d} (€50)", value=False, key=f"A{i:02d}"):
                    selected_individual.append(f"A{i:02d}")
        for i in range(1, 15):
            with cols[(i - 1) % 3]:
                if st.checkbox(f"B{i:02d} (€50)", value=False, key=f"B{i:02d}"):
                    selected_individual.append(f"B{i:02d}")
        for i in range(1, 14):
            with cols[(i - 1) % 3]:
                if st.checkbox(f"C{i:02d} (€50)", value=False, key=f"C{i:02d}"):
                    selected_individual.append(f"C{i:02d}")

    # ---- BUNDLE CHOICE ----
    bundle_choice: str | None = None
    if mode == "Individual bundle (€497)":
        bundle_choice = st.radio(
            "Which bundle do you need?",
            ["EU AI-Act", "NIST AI RMF", "ISO 42001"],
            horizontal=True,
            key="bundle_choice",
        )
        if not bundle_choice:
            st.warning("Please choose EU AI-Act, NIST AI RMF or ISO 42001 above.")

    submitted = st.form_submit_button("Generate selected packs →", type="primary")

# --------------------------------------------------
#  POST-SUBMIT
# --------------------------------------------------
if submitted:
    # guards
    if not model_name or not data_sources:
        st.error("Please complete mandatory fields.")
        st.stop()
    if mode == "Individual bundle (€497)" and not bundle_choice:
        st.error("Please select which individual bundle you need.")
        st.stop()

    # minimal payload
    payload = {k: v for k, v in locals().items() if k in {
        "sector", "model_name", "n_users", "high_risk", "data_modal",
        "deploy_env", "ce_mark", "target_mkt", "sandbox", "model_family", "data_sources"
    }}

    # decide blocks
    blocks: list[str] = []
    if mode == "Individual prompts (€50 each)":
        blocks = selected_individual
    elif mode == "Individual bundle (€497)":
        bundle_blocks = {
            "EU AI-Act":   [f"A{i:02d}" for i in range(1, 21)],
            "NIST AI RMF": [f"B{i:02d}" for i in range(1, 15)],
            "ISO 42001":   [f"C{i:02d}" for i in range(1, 14)],
        }
        blocks = bundle_blocks[bundle_choice]
    elif mode == "Complete bundle (€1 397)":
        blocks = [f"A{i:02d}" for i in range(1, 21)] + [f"B{i:02d}" for i in range(1, 15)] + [f"C{i:02d}" for i in range(1, 14)]

    if not blocks:
        st.error("No blocks selected.")
        st.stop()

    # build & zip
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        zip_paths: list[Path] = []
        for code in blocks:
            with st.spinner(f"Running {code} ..."):
                md_path = build_block(code, payload)
                zip_path = tmpdir_path / f"{code}.zip"
                zip_block(md_path, zip_path)
                zip_paths.append(zip_path)
        persist_dir = Path(tempfile.mkdtemp(prefix="aiactpack_"))
        saved = [shutil.copy2(z, persist_dir / z.name) for z in zip_paths]

    st.session_state.zips = saved
    st.session_state.cart = blocks
    st.success("All selected blocks complete.  Pay once below, then download.")

# --------------------------------------------------
#  DOWNLOAD / PAY AREA
# --------------------------------------------------
if st.session_state.zips:
    st.markdown("---")
    st.markdown("### 📦 Downloads")

    if TEST_MODE:
        st.success("🎁 TEST MODE – all downloads are free.")
        for z in st.session_state.zips:
            st.download_button(
                label=f"⬇️ {z.stem}",
                data=z.read_bytes(),
                file_name=z.name,
                mime="application/zip",
                key=f"dl_{z.stem}",
            )
    else:
        st.info("Pay once, then download every block instantly.")
        if st.button("Create secure checkout session", type="primary"):
            ck_url = create_stripe_checkout_session(st.session_state.cart)
            st.session_state.checkout_url = ck_url

        if st.session_state.checkout_url:
            st.link_button("Pay now →", st.session_state.checkout_url, type="primary")

# --------------------------------------------------
#  FOOTER
# --------------------------------------------------
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:0.9rem;color:#777;">'
    "© 2025 AI Act Pack™ – compliance without chaos | "
    '<a href="https://aiactpack.com/terms">Terms</a> | '
    '<a href="https://aiactpack.com/privacy">Privacy</a>'
    "</div>",
    unsafe_allow_html=True,
)

def create_stripe_checkout_session(cart: list[str]) -> str:
    """ Stub – returns fake url. """
    return "https://stripe.com/docs/testing"


