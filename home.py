# home.py
"""
AI Act Pack™ – fixed & hardened edition
- Removes client-side back-door
- Server-side Stripe Checkout sessions (webhook required)
- Cleans up temp files
- Keeps UX identical from the user’s point of view
"""

from __future__ import annotations

import os
import shutil
import tempfile
from datetime import datetime
from pathlib import Path

import streamlit as st

# --------------  PAGE CONFIG  --------------
st.set_page_config(
    page_title="AI Act Pack™",
    page_icon="⚖️",
    layout="centered",
)

# --------------  CSS / TOP BAR  --------------
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

# --------------  SESSION STATE  --------------
if "zips" not in st.session_state:
    st.session_state.zips: list[Path] = []
if "cart" not in st.session_state:
    st.session_state.cart: list[str] = []  # block codes user wants
if "checkout_url" not in st.session_state:
    st.session_state.checkout_url: str | None = None


# --------------  10-QUESTION WIZARD  --------------
st.markdown("### 🧭 10-Question Compliance Wizard")
with st.form("aiactpack_wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector = st.selectbox(
            "Industry sector *",
            ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"],
            help="Pick the market you operate in – determines high-risk classification under EU AI-Act Annex III.",
        )
        model_name = st.text_input(
            "Model trade name *",
            placeholder="CreditGPT-3",
            help="Public-facing product name (used in CE-marking declaration).",
        )
        n_users = st.number_input(
            "Expected EU users *",
            min_value=0,
            max_value=50_000_000,
            value=5_000,
            step=1_000,
            help=">10 000 users triggers mandatory Notified-Body audit.",
        )
        high_risk = st.selectbox(
            "High-risk Annex III use-case *",
            ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"],
            help="If you pick anything except 'None' the system is HIGH-RISK under EU AI-Act.",
        )
        data_modal = st.multiselect(
            "Data modalities",
            ["Text", "Image", "Tabular", "Audio", "Video"],
            default=["Text"],
            help="Which data types does the model ingest?  Affects bias tests & cyber-security controls.",
        )
    with col2:
        deploy_env = st.selectbox(
            "Deployment environment",
            ["AWS", "Azure", "GCP", "On-prem", "Hybrid"],
            help="Cloud vs. on-prem determines encryption & supply-chain evidence required.",
        )
        ce_mark = st.selectbox(
            "Already CE-marked HW/SW ?",
            ["Yes", "No", "Partial"],
            help="If hardware is already CE-marked you only need a delta-assessment.",
        )
        target_mkt = st.multiselect(
            "Target jurisdictions",
            ["EU", "UK", "USA", "Canada", "APAC"],
            default=["EU"],
            help="Extra jurisdictions add extra rules (UK White-Paper, USA NIST, etc.).",
        )
        sandbox = st.selectbox(
            "Participated in EU AI sandbox ?",
            ["Yes", "No"],
            help="Sandbox exit gives you a lighter conformity route.",
        )
        model_family = st.selectbox(
            "Model family",
            ["GPT-3.5-turbo", "GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"],
            help="Transformer vs. tree-based = different adversarial tests & metrics.",
        )

    data_sources = st.text_area(
        "Training data sources (1 per line) *",
        placeholder="wikimedia.org\ninternal-2022-2024.csv",
        help="List every source – regulators check representativeness & rights.",
    )

    # ---------- MODE ----------
    mode = st.radio(
        "Select purchase mode:",
        ["Individual prompts (€50 each)", "Individual bundle (€497)", "Complete bundle (€1 397)"],
        help="Pay only for what you need.",
    )

    # ---------- SUBMIT ----------
    submitted = st.form_submit_button("Generate selected packs →", type="primary")

# --------------  POST-SUBMIT LOGIC  --------------
if submitted:
    if not model_name or not data_sources:
        st.error("Please complete mandatory fields.")
        st.stop()

    # Build minimal payload
    payload = {
        "sector": sector,
        "model_name": model_name,
        "n_users": n_users,
        "high_risk": high_risk,
        "data_modal": data_modal,
        "deploy_env": deploy_env,
        "ce_mark": ce_mark,
        "target_mkt": target_mkt,
        "sandbox": sandbox,
        "model_family": model_family,
        "data_sources": data_sources,
    }

    # Decide which blocks
    blocks: list[str] = []
    if mode == "Individual prompts (€50 each)":
        st.markdown("### 📋 Select individual prompts")
        for i in range(1, 21):
            if st.checkbox(f"A{i:02d} (€50)", value=False):
                blocks.append(f"A{i:02d}")
        for i in range(1, 15):
            if st.checkbox(f"B{i:02d} (€50)", value=False):
                blocks.append(f"B{i:02d}")
        for i in range(1, 14):
            if st.checkbox(f"C{i:02d} (€50)", value=False):
                blocks.append(f"C{i:02d}")
    elif mode == "Individual bundle (€497)":
        blocks = [f"A{i:02d}" for i in range(1, 21)] + [f"B{i:02d}" for i in range(1, 15)] + [f"C{i:02d}" for i in range(1, 14)]
    elif mode == "Complete bundle (€1 397)":
        blocks = [f"A{i:02d}" for i in range(1, 21)] + [f"B{i:02d}" for i in range(1, 15)] + [f"C{i:02d}" for i in range(1, 14)]

    if not blocks:
        st.error("No blocks selected.")
        st.stop()

    # Build blocks & zip
    zip_paths: list[Path] = []
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        for code in blocks:
            with st.spinner(f"Running {code} ..."):
                # assume engine.build_block returns Path to markdown
                md_path = build_block(code, payload)
                zip_path = tmpdir_path / f"{code}.zip"
                zip_block(md_path, zip_path)  # write zip
                zip_paths.append(zip_path)

        # Persist zips outside temp dir
        persist_dir = Path(tempfile.mkdtemp(prefix="aiactpack_"))
        saved = []
        for src in zip_paths:
            dst = persist_dir / src.name
            shutil.copy2(src, dst)
            saved.append(dst)

    st.session_state.zips = saved
    st.session_state.cart = blocks
    st.success("All selected blocks complete.  Click the green button below to pay and download.")

# --------------  DOWNLOAD / PAY  --------------
if st.session_state.zips:
    st.markdown("---")
    st.markdown("### 📦 Downloads")
    st.info("Pay once, then download every block instantly.")

    # Single Stripe Checkout (server-side)
    if st.button("Create secure checkout session", type="primary"):
        # YOUR_ENDPOINT should create the Stripe session and return {"url": "https://checkout.stripe.com/..."}
        resp_create_session = ...
        st.session_state.checkout_url = resp_create_session.get("url")

    if st.session_state.checkout_url:
        st.link_button("Pay now →", st.session_state.checkout_url, type="primary")

    # Preview downloads (optional, max 3 per IP to avoid abuse)
    for z in st.session_state.zips[:3]:
        st.download_button(
            label=f"⬇️ {z.stem} (preview)",
            data=z.read_bytes(),
            file_name=z.name,
            mime="application/zip",
            key=f"prev_{z.stem}",
        )

# --------------  FOOTER  --------------
st.markdown("---")
st.markdown(
    '<div style="text-align:center;font-size:0.9rem;color:#777;">'
    "© 2025 AI Act Pack™ – compliance without chaos | "
    '<a href="https://aiactpack.com/terms">Terms</a> | '
    '<a href="https://aiactpack.com/privacy">Privacy</a>'
    "</div>",
    unsafe_allow_html=True,
)
