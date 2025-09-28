# engine.py
import os, pathlib, datetime, zipfile, csv, json, tempfile, time
from jinja2 import Template
import openai
from openai import RateLimitError

PROMPTS_DIR   = pathlib.Path(__file__).with_suffix('').parent / "prompts"
TEMPLATES_DIR = pathlib.Path(__file__).with_suffix('').parent / "templates"
client        = openai.OpenAI(api_key=os.getenv("OPENAI_KEY"))
RATE_LIMIT_PAUSE = 10
MAX_RETRIES      = 3

def load_prompt(code: str) -> str:
    return (PROMPTS_DIR / f"{code}.txt").read_text(encoding="utf-8")

def call_llm(code: str, prompt: str) -> str:
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
# BUTTON-FREE PACK BUILDER  (only builds zip, no Streamlit calls)
##############################################################################
def generate_pack(payload: dict) -> pathlib.Path:
    stamp   = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    tmpdir  = pathlib.Path(tempfile.mkdtemp(prefix=f"pack_{stamp}_"))
    artefacts_dir = tmpdir / "artefacts"
    artefacts_dir.mkdir(exist_ok=True)

    blocks = []
    if payload.get("do_eu"):   blocks += [f"A{i:02d}" for i in range(1, 21)]
    if payload.get("do_nist"): blocks += [f"B{i:02d}" for i in range(1, 15)]
    if payload.get("do_iso"):  blocks += [f"C{i:02d}" for i in range(1, 14)]

    # ---- A00 Executive Summary (always if EU ticked) ----
    if payload.get("do_eu"):
        summary = call_llm("A00", Template(load_prompt("A00")).render(ctx=payload))
        (artefacts_dir / "A00_Executive_Summary.md").write_text(summary, encoding="utf-8")

    # ---- loop: build each block ----
    for code in blocks:
        resp = call_llm(code, Template(load_prompt(code)).render(ctx=payload))
        (artefacts_dir / f"{code}.md").write_text(resp, encoding="utf-8")

    # ---- EU Declaration (if EU ticked) ----
    if payload.get("do_eu"):
        from jinja2 import Template
        decl_tmpl = Template((TEMPLATES_DIR / "EU_declaration.md").read_text())
        declaration = decl_tmpl.render(ctx=payload, date=datetime.datetime.utcnow().strftime("%d %B %Y"))
        (artefacts_dir / "04_EU_Declaration_of_Conformity.md").write_text(declaration, encoding="utf-8")

    # ---- zip everything ----
    final_zip = tmpdir / f"AIACTPACK_{stamp}.zip"
    with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in artefacts_dir.rglob("*"):
            zf.write(file, file.relative_to(tmpdir))
    return final_zip
