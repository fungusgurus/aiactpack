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
# BUILD SINGLE BLOCK (returns pathlib.Path to .md file)
##############################################################################
def build_block(code: str, payload: dict) -> pathlib.Path:
    tmpdir = pathlib.Path(tempfile.mkdtemp(prefix=f"block_{code}_"))
    md_path = tmpdir / f"{code}.md"
    resp = call_llm(code, Template(load_prompt(code)).render(ctx=payload))
    md_path.write_text(resp, encoding="utf-8")
    return md_path

##############################################################################
# ZIP SINGLE BLOCK (returns pathlib.Path to .zip file)
##############################################################################
def zip_block(md_path: pathlib.Path) -> pathlib.Path:
    tmpdir = md_path.parent
    zip_path = tmpdir / f"{md_path.stem}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(md_path, md_path.name)
    return zip_path
