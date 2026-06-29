#!/usr/bin/env python3
"""
generate_uat_report.py — Generate UAT review guide HTML/PDF

Usage:
  pip install markdown
  python reports/UAT_Reports/scripts/generate_uat_report.py

  # For PDF:
  pip install markdown weasyprint
  python reports/UAT_Reports/scripts/generate_uat_report.py --engine weasyprint
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

_SCRIPT_DIR = Path(__file__).resolve().parent   # UAT_Reports/scripts/
_UAT_DIR = _SCRIPT_DIR.parent                   # UAT_Reports/
_REPORTS_DIR = _UAT_DIR.parent                  # reports/
_KIT_ROOT = _REPORTS_DIR.parent                 # kit root
SUMMARIES_DIR = _UAT_DIR / "summaries"
DATA_DIR = _REPORTS_DIR / "data"

SUMMARY_FILES = [
    "00_overview_and_objectives.md",
    "01_data_validation_checklist.md",
    "02_genie_qa_checklist.md",
    "03_insights_action_plans_checklist.md",
]

CSS = """
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 11pt; color: #333; line-height: 1.6; }
h1 { color: #1a365d; border-bottom: 3px solid #2b6cb0; padding-bottom: 8px; page-break-before: always; }
h1:first-of-type { page-break-before: avoid; }
h2 { color: #2b6cb0; border-bottom: 1px solid #bee3f8; padding-bottom: 4px; }
h3 { color: #2c5282; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 10pt; }
th { background-color: #2b6cb0; color: white; padding: 8px 10px; text-align: left; }
td { padding: 6px 10px; border-bottom: 1px solid #e2e8f0; }
tr:nth-child(even) td { background-color: #f7fafc; }
code { background-color: #edf2f7; padding: 2px 5px; border-radius: 3px; font-size: 9.5pt; }
.cover { text-align: center; padding: 100px 40px 60px; page-break-after: always; }
.cover h1 { font-size: 28pt; border: none; page-break-before: avoid; }
"""


def load_room_identity():
    path = DATA_DIR / "room_identity.json"
    if path.exists():
        with open(path) as f:
            return json.load(f)
    try:
        import yaml
        config = yaml.safe_load(open(_KIT_ROOT / "room.config.yml"))
        return {"room_name": config.get("room_name", "genie_room"), "title": config.get("title", "Genie Room")}
    except Exception:
        return {"room_name": "genie_room", "title": "Genie Room"}


def main():
    parser = argparse.ArgumentParser(description="Generate UAT review guide")
    parser.add_argument("--engine", choices=["weasyprint", "pdfkit", "html-only"], default="html-only")
    parser.add_argument("--output-dir", default=str(_UAT_DIR))
    args = parser.parse_args()

    room = load_room_identity()
    room_name = room.get("room_name", "genie_room")
    title = room.get("title", room_name)
    today = datetime.utcnow().strftime("%Y-%m-%d")
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Generating UAT review guide for: {title}")

    try:
        import markdown
        md_ext = ["tables", "fenced_code"]
        convert = lambda text: markdown.markdown(text, extensions=md_ext)
    except ImportError:
        convert = lambda text: "<pre>" + text + "</pre>"

    parts = []
    for fname in SUMMARY_FILES:
        path = SUMMARIES_DIR / fname
        if path.exists():
            with open(path, encoding="utf-8") as f:
                parts.append(convert(f.read()))
        else:
            print(f"  WARN: Missing: {fname}")

    cover = f'''<div class="cover"><h1>{title}</h1><div style="font-size:16pt;color:#4a5568;margin-top:20px">UAT Review Guide</div><div style="font-size:12pt;color:#718096;margin-top:30px">Review Date: {today}</div></div>'''
    body = "<hr>".join(parts)
    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><title>{title} — UAT Review Guide</title><style>{CSS}</style></head><body>{cover}{body}</body></html>"""

    html_path = output_dir / f"{room_name}_UAT_Guide.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML saved: {html_path}")

    if args.engine == "weasyprint":
        from weasyprint import HTML
        pdf_path = output_dir / f"{room_name}_UAT_Guide.pdf"
        HTML(string=html).write_pdf(str(pdf_path))
        print(f"  PDF saved: {pdf_path}")
    elif args.engine == "pdfkit":
        import pdfkit
        pdf_path = output_dir / f"{room_name}_UAT_Guide.pdf"
        pdfkit.from_string(html, str(pdf_path))
        print(f"  PDF saved: {pdf_path}")
    else:
        print(f"Open {html_path} in a browser and print to PDF.")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
