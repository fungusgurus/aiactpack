# engine.py
import os, pathlib, datetime, zipfile, csv, json, tempfile, time
import streamlit as st          #  ← add this
from jinja2 import Template
import openai
from openai import RateLimitError

client = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))

##############################################################################
# CONFIG
##############################################################################
PROMPTS_DIR  = pathlib.Path(__file__).with_suffix('').parent / "prompts"
TEMPLATES_DIR = pathlib.Path(__file__).with_suffix('').parent / "templates"
RATE_LIMIT_PAUSE = 10          # seconds between calls
MAX_RETRIES = 3

##############################################################################
# HELPERS
##############################################################################
def load_prompt(code: str) -> str:
    return (PROMPTS_DIR / f"{code}.txt").read_text(encoding="utf-8")

def call_llm(prompt: str) -> str:
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800
            )
            return response.choices[0].message.content
        except RateLimitError:
            time.sleep(RATE_LIMIT_PAUSE * attempt)
    return f"[Rate-limit – verify manually] {prompt[:60]}..."

##############################################################################
# MASTER PACK BUILDER  (batched + progress bar)
##############################################################################
def generate_pack(payload: dict) -> pathlib.Path:
    stamp   = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    tmpdir  = pathlib.Path(tempfile.mkdtemp(prefix=f"pack_{stamp}_"))
    artefacts_dir = tmpdir / "artefacts"
    artefacts_dir.mkdir()

    # ---- 1. Executive summary (A00) ----
    with st.spinner("A00 Executive Summary..."):
        summary = call_llm(Template(load_prompt("A00")).render(ctx=payload))
    (artefacts_dir / "00_Executive_Summary.md").write_text(summary, encoding="utf-8")

    # ---- 2. EU AI-Act A01-A20 (batched) ----
    eu_md = "# EU AI Act Evidence\n\n";  eu_csv = []
    progress = st.progress(0)
    for i in range(1, 21):
        code = f"A{i:02d}"
        with st.spinner(f"EU {code} ..."):
            resp = call_llm(Template(load_prompt(code)).render(ctx=payload))
        eu_md += f"\n## {code}\n\n{resp}\n"
        eu_csv.append({"Clause": code, "Evidence": resp[:200] + "..."})
        progress.progress(i / 47)
    (artefacts_dir / "01_EU_AI_Act.md").write_text(eu_md, encoding="utf-8")
    with open(artefacts_dir / "01_EU_AI_Act.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["Clause", "Evidence"]).writerows(eu_csv)

    # ---- 3. NIST B01-B14 (batched) ----
    nist_md = "# NIST AI RMF Evidence\n\n";  nist_csv = []
    for i in range(1, 15):
        code = f"B{i:02d}"
        with st.spinner(f"NIST {code} ..."):
            resp = call_llm(Template(load_prompt(code)).render(ctx=payload))
        nist_md += f"\n## {code}\n\n{resp}\n"
        nist_csv.append({"SubCategory": code, "Evidence": resp[:200] + "..."})
        progress.progress((20 + i) / 47)
    (artefacts_dir / "02_NIST_AI_RMF.md").write_text(nist_md, encoding="utf-8")
    with open(artefacts_dir / "02_NIST_AI_RMF.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["SubCategory", "Evidence"]).writerows(nist_csv)

    # ---- 4. ISO 42001 C01-C13 (batched) ----
    iso_md = "# ISO 42001 Evidence\n\n";  iso_csv = []
    for i in range(1, 14):
        code = f"C{i:02d}"
        with st.spinner(f"ISO {code} ..."):
            resp = call_llm(Template(load_prompt(code)).render(ctx=payload))
        iso_md += f"\n## {code}\n\n{resp}\n"
        iso_csv.append({"Control": code, "Evidence": resp[:200] + "..."})
        progress.progress((34 + i) / 47)
    (artefacts_dir / "03_ISO_42001.md").write_text(iso_md, encoding="utf-8")
    with open(artefacts_dir / "03_ISO_42001.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["Control", "Evidence"]).writerows(iso_csv)

    # ---- 5. EU Declaration (template) ----
    decl_tmpl = Template((TEMPLATES_DIR / "EU_declaration.md").read_text())
    declaration = decl_tmpl.render(ctx=payload, date=datetime.datetime.utcnow().strftime("%d %B %Y"))
    (artefacts_dir / "04_EU_Declaration_of_Conformity.md").write_text(declaration, encoding="utf-8")

    # ---- 6. Zip everything ----
    zip_path = tmpdir / f"AIACTPACK_{stamp}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in artefacts_dir.rglob("*"):
            zf.write(file, file.relative_to(tmpdir))
    return zip_path
