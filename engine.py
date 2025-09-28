# engine.py
import os, pathlib, datetime, zipfile, csv, json, tempfile, time
from jinja2 import Template
import openai
from openai import RateLimitError
import streamlit as st

##############################################################################
# CONFIG
##############################################################################
PROMPTS_DIR   = pathlib.Path(__file__).with_suffix('').parent / "prompts"
TEMPLATES_DIR = pathlib.Path(__file__).with_suffix('').parent / "templates"
client        = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
RATE_LIMIT_PAUSE = 10          # seconds between calls
MAX_RETRIES      = 3
TOTAL_PROMPTS    = 47          # A01-A20 + B01-B14 + C01-C13

##############################################################################
# HELPERS
##############################################################################
def load_prompt(code: str) -> str:
    return (PROMPTS_DIR / f"{code}.txt").read_text(encoding="utf-8")

def call_llm(code: str, prompt: str) -> str:
    """GPT-3.5-turbo with retry + rate-limit back-off."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=700
            )
            return response.choices[0].message.content
        except RateLimitError:
            time.sleep(RATE_LIMIT_PAUSE * attempt)
    return f"[Rate-limit – verify manually] {code}"

##############################################################################
# MASTER PACK BUILDER  (batched + progress bar)
##############################################################################
def generate_pack(payload: dict) -> pathlib.Path:
    stamp   = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    tmpdir  = pathlib.Path(tempfile.mkdtemp(prefix=f"pack_{stamp}_"))
    artefacts_dir = tmpdir / "artefacts"
    artefacts_dir.mkdir(exist_ok=True)

    progress = st.progress(0)
    done     = 0

    # ---- 1. Executive summary (A00) ----
    with st.spinner("A00 Executive Summary..."):
        summary = call_llm("A00", Template(load_prompt("A00")).render(ctx=payload))
    (artefacts_dir / "00_Executive_Summary.md").write_text(summary, encoding="utf-8")
    done += 1; progress.progress(done / TOTAL_PROMPTS)

    # ---- 2. EU AI-Act A01-A20 (20 calls) ----
    eu_md = "# EU AI Act Evidence\n\n";  eu_csv = []
    for i in range(1, 21):
        code = f"A{i:02d}"
        with st.spinner(f"EU {code} ..."):
            resp = call_llm(code, Template(load_prompt(code)).render(ctx=payload))
        eu_md += f"\n## {code}\n\n{resp}\n"
        eu_csv.append({"Clause": code, "Evidence": resp[:200] + "..."})
        done += 1; progress.progress(done / TOTAL_PROMPTS)
        time.sleep(10)   # stay under 60 requests / minute

    (artefacts_dir / "01_EU_AI_Act.md").write_text(eu_md, encoding="utf-8")
    with open(artefacts_dir / "01_EU_AI_Act.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["Clause", "Evidence"]).writerows(eu_csv)

    # ---- 3. NIST AI RMF B01-B14 (14 calls) ----
    nist_md = "# NIST AI RMF Evidence\n\n";  nist_csv = []
    for i in range(1, 15):
        code = f"B{i:02d}"
        with st.spinner(f"NIST {code} ..."):
            resp = call_llm(code, Template(load_prompt(code)).render(ctx=payload))
        nist_md += f"\n## {code}\n\n{resp}\n"
        nist_csv.append({"SubCategory": code, "Evidence": resp[:200] + "..."})
        done += 1; progress.progress(done / TOTAL_PROMPTS)
        time.sleep(10)

    (artefacts_dir / "02_NIST_AI_RMF.md").write_text(nist_md, encoding="utf-8")
    with open(artefacts_dir / "02_NIST_AI_RMF.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["SubCategory", "Evidence"]).writerows(nist_csv)

    # ---- 4. ISO 42001 C01-C13 (13 calls) ----
    iso_md = "# ISO 42001 Evidence\n\n";  iso_csv = []
    for i in range(1, 14):
        code = f"C{i:02d}"
        with st.spinner(f"ISO {code} ..."):
            resp = call_llm(code, Template(load_prompt(code)).render(ctx=payload))
        iso_md += f"\n## {code}\n\n{resp}\n"
        iso_csv.append({"Control": code, "Evidence": resp[:200] + "..."})
        done += 1; progress.progress(done / TOTAL_PROMPTS)
        time.sleep(10)

    (artefacts_dir / "03_ISO_42001.md").write_text(iso_md, encoding="utf-8")
    with open(artefacts_dir / "03_ISO_42001.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["Control", "Evidence"]).writerows(iso_csv)

    # ---- 5. EU Declaration of Conformity (template) ----
    decl_tmpl = Template((TEMPLATES_DIR / "EU_declaration.md").read_text())
    declaration = decl_tmpl.render(ctx=payload, date=datetime.datetime.utcnow().strftime("%d %B %Y"))
    (artefacts_dir / "04_EU_Declaration_of_Conformity.md").write_text(declaration, encoding="utf-8")

    # ---- 6. Zip everything ----
    zip_path = tmpdir / f"AIACTPACK_{stamp}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in artefacts_dir.rglob("*"):
            zf.write(file, file.relative_to(tmpdir))
    return zip_path
