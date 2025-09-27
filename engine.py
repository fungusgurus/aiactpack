"""
Reg-Tech Packager back-end
Loops 47 prompts → markdown + csv → zip
"""
import os, json, csv, zipfile, tempfile, pathlib
from datetime import datetime
from jinja2 import Template  # pip install jinja2

# ---------- LLM PROVIDER ----------
# 1 line switch
USE_LOCAL = True   # False → OpenAI

if USE_LOCAL:
    from llama_cpp import Llama          # pip install llama-cpp-python
    llm = Llama(model_path="models/llama-3-8b-instruct.Q4_K_M.gguf",
                n_ctx=4096, n_threads=4)
    def call_llm(prompt: str) -> str:
        out = llm.create_chat_completion(
              messages=[{"role":"user","content":prompt}],
              temperature=0.2, max_tokens=1200)
        return out["choices"][0]["message"]["content"]
else:
    import openai
    openai.api_key = os.getenv("OPENAI_KEY")
    def call_llm(prompt: str) -> str:
        resp = openai.ChatCompletion.create(
               model="gpt-4", messages=[{"role":"user","content":prompt}],
               temperature=0.2, max_tokens=1200)
        return resp.choices[0].message.content

# ---------- PROMPT LOADER ----------
PROMPTS_DIR = pathlib.Path(__file__).with_suffix('').parent / "prompts"
def load_prompt(code: str) -> str:
    return (PROMPTS_DIR / f"{code}.txt").read_text(encoding="utf-8")

# ---------- ARTEFACT BUILDERS ----------
def run_prompt(code: str, context: dict) -> str:
    tmpl = Template(load_prompt(code))
    filled = tmpl.render(ctx=context)
    return call_llm(filled)

def md_table(rows: list[dict]) -> str:
    if not rows: return ""
    header = "| " + " | ".join(rows[0].keys()) + " |"
    divider = "|" + "|".join("---" for _ in rows[0]) + "|"
    body = "\n".join("| " + " | ".join(str(v) for v in r.values()) + " |" for r in rows)
    return "\n".join([header, divider, body])

# ---------- MASTER FUNCTION ----------
def generate_pack(payload: dict) -> pathlib.Path:
    stamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    tmpdir = pathlib.Path(tempfile.mkdtemp(prefix=f"pack_{stamp}_"))
    artefacts_dir = tmpdir / "artefacts"
    artefacts_dir.mkdir()

    # 1. Executive summary
    summary = run_prompt("A00_summary", payload)
    (artefacts_dir / "00_Executive_Summary.md").write_text(summary, encoding="utf-8")

    # 2. EU AI Act loop (A1-A20)
    eu_md = "# EU AI Act Evidence\n\n"
    eu_csv = []
    for i in range(1, 21):
        code = f"A{i:02d}"
        resp = run_prompt(code, payload)
        eu_md += f"\n## {code}\n\n{resp}\n"
        eu_csv.append({"Clause": code, "Evidence": resp[:200] + "..."})
    (artefacts_dir / "01_EU_AI_Act.md").write_text(eu_md, encoding="utf-8")
    with open(artefacts_dir / "01_EU_AI_Act.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["Clause", "Evidence"]).writerows(eu_csv)

    # 3. NIST loop (B1-B14)
    nist_md = "# NIST AI RMF Evidence\n\n"
    nist_csv = []
    for i in range(1, 15):
        code = f"B{i:02d}"
        resp = run_prompt(code, payload)
        nist_md += f"\n## {code}\n\n{resp}\n"
        nist_csv.append({"SubCategory": code, "Evidence": resp[:200] + "..."})
    (artefacts_dir / "02_NIST_AI_RMF.md").write_text(nist_md, encoding="utf-8")
    with open(artefacts_dir / "02_NIST_AI_RMF.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["SubCategory", "Evidence"]).writerows(nist_csv)

    # 4. ISO 42001 loop (C1-C13)
    iso_md = "# ISO 42001 Evidence\n\n"
    iso_csv = []
    for i in range(1, 14):
        code = f"C{i:02d}"
        resp = run_prompt(code, payload)
        iso_md += f"\n## {code}\n\n{resp}\n"
        iso_csv.append({"Control": code, "Evidence": resp[:200] + "..."})
    (artefacts_dir / "03_ISO_42001.md").write_text(iso_md, encoding="utf-8")
    with open(artefacts_dir / "03_ISO_42001.csv", "w", newline='', encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=["Control", "Evidence"]).writerows(iso_csv)

    # 5. EU Declaration of Conformity (template + auto-fill)
    decl_tmpl = Template((pathlib.Path("templates") / "EU_declaration.md").read_text())
    declaration = decl_tmpl.render(ctx=payload, date=datetime.utcnow().strftime("%d %B %Y"))
    (artefacts_dir / "04_EU_Declaration_of_Conformity.md").write_text(declaration, encoding="utf-8")

    # 6. Zip everything
    zip_path = tmpdir / f"AIACTPACK_{stamp}.zip"
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for file in artefacts_dir.rglob("*"):
            zf.write(file, file.relative_to(tmpdir))
    return zip_path
