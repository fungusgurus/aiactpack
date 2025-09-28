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
# MASTER PACK BUILDER  (stream-after-every-block + partial-safe)
##############################################################################
def generate_pack(payload: dict) -> pathlib.Path:
    stamp   = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    tmpdir  = pathlib.Path(tempfile.mkdtemp(prefix=f"pack_{stamp}_"))
    artefacts_dir = tmpdir / "artefacts"
    artefacts_dir.mkdir(exist_ok=True)

    # ---- decide which blocks to run ----
    blocks = []
    if payload.get("do_eu"):   blocks += [f"A{i:02d}" for i in range(1, 21)]
    if payload.get("do_nist"): blocks += [f"B{i:02d}" for i in range(1, 15)]
    if payload.get("do_iso"):  blocks += [f"C{i:02d}" for i in range(1, 14)]

    if not blocks:
        st.warning("No blocks selected – returning empty pack.")
        return tmpdir / "EMPTY.zip"

    total = len(blocks)
    progress = st.progress(0)

    # ---- helper: write block immediately ----
    def write_block(name: str, content: str):
        (artefacts_dir / f"{name}.md").write_text(content, encoding="utf-8")

    # ---- loop: stream each block ----
    for idx, code in enumerate(blocks, 1):
        progress.progress(idx / total)
        with st.spinner(f"{code} ..."):
            try:
                resp = call_llm(code, Template(load_prompt(code)).render(ctx=payload))
            except Exception as e:
                resp = f"[Error – verify manually] {code}: {str(e)[:100]}"
        write_block(code, resp)

        # ---- STREAM ZIP AFTER EVERY BLOCK ----
        zip_path = tmpdir / f"AIACTPACK_partial_{code}.zip"
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file in artefacts_dir.rglob("*"):
                zf.write(file, file.relative_to(tmpdir))

        # ---- OFFER DOWNLOAD NOW ----
        st.success(f"Block {code} done – download even if later blocks fail.")
        with open(zip_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download up to {code}",
                data=f,
                file_name=zip_path.name,
                mime="application/zip",
                key=f"dl_{code}"   # unique key per block
            )

    # ---- final full zip ----
    final_zip = tmpdir / f"AIACTPACK_{stamp}.zip"
    with zipfile.ZipFile(final_zip, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in artefacts_dir.rglob("*"):
            zf.write(file, file.relative_to(tmpdir))

    st.success("All selected blocks complete. Final download below.")
    with open(final_zip, "rb") as f:
        st.download_button(
            label="⬇️ Final bundle",
            data=f,
            file_name=final_zip.name,
            mime="application/zip"
        )
    return final_zip
