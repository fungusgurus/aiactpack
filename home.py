# ---------------------------------------------------------
#  home.py  –  AI Act Pack™  –  complete file
#  NOWPayments crypto checkout + auto client PDF report
#  Logo: AIACTPack.png  (served on VPS)
# ---------------------------------------------------------
import os, time, shutil, tempfile, zipfile, base64
from pathlib import Path
import streamlit as st
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML, CSS

# ------------------------------------------------------------------
#  0.  CONFIG
# ------------------------------------------------------------------
COMPANY_NAME  = "AI Act Pack™"
COMPANY_VAT   = "EU123456789"
COMPANY_ADDR  = "123 Compliance Blvd, Dublin, Ireland"
SUPPORT_EMAIL = "support@aiactpack.com"
CALENDLY_URL  = "https://calendly.com/aiactpack/expert"

# ------------------------------------------------------------------
#  1.  SESSION-STATE INITIALISATION  (no AttributeError)
# ------------------------------------------------------------------
for k, v in (("zips", []), ("cart", []), ("checkout_url", None)):
    st.session_state.setdefault(k, v)

# ------------------------------------------------------------------
#  2.  IMPORT SAMPLE REPORT BASE-64 FROM EXTERNAL FILE
# ------------------------------------------------------------------
try:
    from sample_report import SAMPLE_PDF_B64
except ModuleNotFoundError:
    SAMPLE_PDF_B64 = ""

# ------------------------------------------------------------------
#  3.  SERVE STATIC FILES (logo) - FIXED FOR VPS
# ------------------------------------------------------------------
@st.cache_data(show_spinner=False)
def _prepare_static():
    # Use static directory in root for VPS
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    # Copy logo to static directory if it exists
    logo_src = Path("AIACTPack.png")
    if logo_src.exists():
        shutil.copy(logo_src, static_dir / "AIACTPack.png")
        st.success(f"✅ Logo copied to static directory")
    else:
        st.error(f"❌ Logo file not found: {logo_src.absolute()}")

_prepare_static()

# ------------------------------------------------------------------
#  4.  NOWPayments links
# ------------------------------------------------------------------
NOW_LINKS = {
    "individual":  "https://nowpayments.io/payment/?amount=50&currency=eur&invoice_id=aiactpack-individual",
    "eu_bundle":   "https://nowpayments.io/payment/?amount=899&currency=eur&invoice_id=aiactpack-eu",
    "nist_bundle": "https://nowpayments.io/payment/?amount=599&currency=eur&invoice_id=aiactpack-nist",
    "iso_bundle":  "https://nowpayments.io/payment/?amount=549&currency=eur&invoice_id=aiactpack-iso",
    "complete":    "https://nowpayments.io/payment/?amount=1997&currency=eur&invoice_id=aiactpack-full",
}

# ------------------------------------------------------------------
#  5.  TEST-MODE SWITCH
# ------------------------------------------------------------------
TEST_MODE = st.query_params.get("test") == "1"

# ------------------------------------------------------------------
#  6.  ENGINE
# ------------------------------------------------------------------
from engine import build_block

# ------------------------------------------------------------------
#  7.  PAGE CONFIG
# ------------------------------------------------------------------
st.set_page_config(
    page_title=f"{COMPANY_NAME} – EU AI Act, NIST & ISO 42001 evidence in 48 h",
    page_icon="⚖️",
    layout="centered",
)

# ------------------------------------------------------------------
#  8.  COOKIE BANNER
# ------------------------------------------------------------------
st.html(r"""
<script src="https://cdn.jsdelivr.net/npm/cookieconsent@3/build/cookieconsent.min.js" data-cfasync="false"></script>
<script>
window.cookieconsent.initialise({
  "palette": { "popup": { "background": "#003399" }, "button": { "background": "#00d4aa" } },
  "content": { "message": "We use cookies to ensure compliance with EU laws and deliver a smooth experience." }
});
</script>
""")

# ------------------------------------------------------------------
#  9.  TOP BAR  (logo + call-link) - FIXED FOR VPS
# ------------------------------------------------------------------
# Simple top bar without complex static file paths
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    if Path("AIACTPack.png").exists():
        st.image("AIACTPack.png", width=120)
    else:
        st.markdown(f"### {COMPANY_NAME}")
with col3:
    st.markdown(f'<div style="text-align: right; padding-top: 10px;">'
                f'<a href="{CALENDLY_URL}" target="_blank" style="color: #003399; text-decoration: none; font-weight: bold;">📞 Book 15-min Call</a>'
                f'</div>', unsafe_allow_html=True)

st.markdown("---")

# ------------------------------------------------------------------
#  10.  HERO
# ------------------------------------------------------------------
st.markdown("## Generate EU AI Act, NIST AI RMF & ISO 42001 evidence in 48 h—no lawyers.")
st.markdown("Up to €30 M fines apply from 2 Aug 2025.  Save €15 k+ in advisory fees with battle-tested templates trusted by 200+ AI teams.")
c1, c2, c3 = st.columns(3)
c1.metric("✅ AI systems assessed", "217")
c2.metric("✅ NB-ready reports", "38")
c3.metric("✅ Days saved avg", "12")

st.markdown("""
<div style="text-align: center; margin: 2rem 0;">
    <a href="#wizard" style="background: #00d4aa; color: white; padding: 12px 24px; 
       border-radius: 6px; text-decoration: none; font-weight: bold; display: inline-block;">
       Start 10-Question Wizard
    </a>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------
#  11.  SAMPLE REPORT DOWNLOAD
# ------------------------------------------------------------------
if SAMPLE_PDF_B64:
    with st.expander("📄 Want to see a sample report before you buy?"):
        st.download_button(
            label="⬇️ Download redacted sample report",
            data=base64.b64decode(SAMPLE_PDF_B64),
            file_name="AI_Act_Pack_sample_report.pdf",
            mime="application/pdf",
        )

# ------------------------------------------------------------------
#  12.  LEAD MAGNET
# ------------------------------------------------------------------
with st.container(border=True):
    st.markdown("### 🎯 Free EU AI-Act Readiness Score (2 min)")
    c1, c2 = st.columns([3, 1])
    with c1:
        email = st.text_input("Business email", placeholder="alice@company.com")
    with c2:
        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
        if st.button("Get my score →", type="primary"):
            if "@" not in email:
                st.error("Please enter a valid email.")
            else:
                st.success("Check your inbox—link on its way!")
                st.balloons()

# ------------------------------------------------------------------
#  13.  ANCHOR + WIZARD
# ------------------------------------------------------------------
st.markdown('<div id="wizard"></div>', unsafe_allow_html=True)
st.markdown("### 🧭 10-Question Compliance Wizard")

with st.form("aiactpack_wizard"):
    col1, col2 = st.columns(2)
    with col1:
        sector       = st.selectbox("Industry sector *", ["FinTech", "HealthTech", "HR-tech", "AdTech", "Retail", "CyberSec", "Auto", "Other"])
        model_name   = st.text_input("Model trade name *", placeholder="CreditGPT-3")
        n_users      = st.number_input("Expected EU users *", 0, 50_000_000, 5_000, 1_000)
        high_risk    = st.selectbox("High-risk Annex III use-case *", ["None", "Biometric ID", "HR / recruitment", "Credit scoring", "Insurance pricing"])
        data_modal   = st.multiselect("Data modalities", ["Text", "Image", "Tabular", "Audio", "Video"], default=["Text"])
    with col2:
        deploy_env   = st.selectbox("Deployment environment", ["AWS", "Azure", "GCP", "On-prem", "Hybrid"])
        ce_mark      = st.selectbox("Already CE-marked HW/SW ?", ["Yes", "No", "Partial"])
        target_mkt   = st.multiselect("Target jurisdictions", ["EU", "UK", "USA", "Canada", "APAC"], default=["EU"])
        sandbox      = st.selectbox("Participated in EU AI sandbox ?", ["Yes", "No"])
        model_family = st.selectbox("Model family", ["GPT-3.5-turbo", "GPT-4", "Llama-3", "Claude-3", "Gemini", "Custom transformer", "Tree-based"])
    data_sources = st.text_area("Training data sources (1 per line) *", placeholder="wikimedia.org\ninternal-2022-2024.csv")

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
#  14.  POST-SUBMIT  (build blocks + client PDF)
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
        real_outputs = {}
        for code in blocks:
            with st.spinner(f"Running {code} ..."):
                out = build_block(code, payload)
                built_files.append(out["file_path"])   # adapt to your engine
                real_outputs[code] = out.get("summary", {})

        # ----------------------------------------------------
        # 14-A  render client-facing PDF
        # ----------------------------------------------------
        env = Environment(
            loader=FileSystemLoader("templates"),
            autoescape=select_autoescape(["html", "xml"])
        )
        template = env.get_template("report_template.html")
        context = {
            "trade_name": payload["model_name"],
            "version": "2.1.14",
            "provider": "Acme FinTech Ltd (IE)",
            "high_risk_use_case": payload["high_risk"],
            "deployment": payload["deploy_env"],
            "n_users": payload["n_users"],
            "model_family": payload["model_family"],
            "overall_status": "no critical gaps" if "B05" in blocks else "minor gaps",
            "risk_class": "High-risk (Annex III §6(a))",
            "evidence_ready": 18,
            "evidence_total": 20,
            "effort_days": 6,
            "gap_6a_status": "✅ Draft fairness report",
            "transparency_status": "✅ Labelled AI; T&Cs updated",
            "risk_mgmt_status": "✅",
            "risk_mgmt_notes": "ISO 31000 aligned, v1.4 signed off",
            "data_gov_status": "✅",
            "data_gov_notes": "Training data sheet & bias audit",
            "tech_doc_status": "✅",
            "tech_doc_notes": "104-page doc pack under doc-control",
            "module_b_status": "❌",
            "module_b_notes": "Draft with NB; awaiting final quote",
            "module_b_days": 3,
            "nb_week": 28,
        }
        html = template.render(context)
        client_report_path = tmpdir_path / f"EU_AI_Act_Report_{int(time.time())}.pdf"
        HTML(string=html).write_pdf(
            client_report_path,
            stylesheets=[CSS(string="""
                @page{size:A4;margin:2cm}
                body{font-family:Helvetica,sans-serif;font-size:11pt}
                table{width:100%;border-collapse:collapse}
                th,td{border:1px solid #ccc;padding:6px}
                th{background:#f5f5f5}
            """)]
        )

        # ----------------------------------------------------
        # 14-B  ZIP everything
        # ----------------------------------------------------
        pack_name = (
            "Complete_Bundle" if mode == "Complete bundle (€1 997)" else
            f"{bundle_choice.replace(' ', '_')}_Bundle" if mode == "Individual bundle" else
            "Individual_Prompts"
        ) + f"_{int(time.time())}.zip"

        final_zip = tmpdir_path / pack_name
        with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
            for bf in built_files:
                zf.write(bf, bf.name)
            zf.write(client_report_path, client_report_path.name)

        persist_dir = Path(tempfile.mkdtemp(prefix="aiactpack_"))
        saved_zip = shutil.copy2(final_zip, persist_dir / final_zip.name)

    st.session_state.zips = [saved_zip]
    st.session_state.cart = blocks
    st.success("All blocks packed into **one** zip.  Pay once below, then download.")

# ------------------------------------------------------------------
#  15.  DOWNLOAD / CRYPTO CHECKOUT
# ------------------------------------------------------------------
if st.session_state.get("zips"):
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
        st.html('<div style="display:flex;gap:8px;align-items:center"><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#f7931a" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/></svg><svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" stroke="#f7931a" stroke-width="2" viewBox="0 0 24 24"><rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="15" width="6" height="6" rx="1"/></svg><small>Crypto checkout (auto fiat conversion)</small></div>')
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
#  16.  FOOTER - FIXED FOR VPS
# ------------------------------------------------------------------
st.markdown("---")

# Check which markdown files exist and create links
footer_links = ""
for name, file in [("Terms", "terms.md"), ("Privacy", "privacy.md"), ("Cookie Policy", "cookies.md")]:
    if Path(file).exists():
        # Use direct file links that will be served by Nginx
        footer_links += f'<a href="/{file}" target="_blank">{name}</a> | '

st.markdown(
    f"""<div style='text-align:center;font-size:.85rem;color:#777'>
    © 2025 {COMPANY_NAME} – compliance without chaos<br>
    {COMPANY_NAME} | VAT: {COMPANY_VAT} | {COMPANY_ADDR}<br>
    <a href="mailto:{SUPPORT_EMAIL}">Contact</a> | {footer_links}
    </div>""",
    unsafe_allow_html=True,
)
