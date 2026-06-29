#!/usr/bin/env python3
"""
generate_report.py — Generate HTML/PDF report from markdown summaries

Reads all markdown summaries from reports/summaries/ and combines them
into a single styled HTML or PDF report.

Usage:
  pip install markdown
  python reports/scripts/generate_report.py

  # For PDF output (recommended):
  pip install markdown weasyprint
  python reports/scripts/generate_report.py --engine weasyprint

  # Alternative PDF engine:
  pip install markdown pdfkit
  python reports/scripts/generate_report.py --engine pdfkit

Output:
  reports/<ROOM_NAME>_Report.html
  reports/<ROOM_NAME>_Report.pdf  (if PDF engine available)
"""
import argparse
import json
import sys
from pathlib import Path
from datetime import datetime

_SCRIPT_DIR = Path(__file__).resolve().parent   # reports/scripts/
_REPORTS_DIR = _SCRIPT_DIR.parent               # reports/
_KIT_ROOT = _REPORTS_DIR.parent                 # kit root
SUMMARIES_DIR = _REPORTS_DIR / "summaries"
DATA_DIR = _REPORTS_DIR / "data"

SUMMARY_FILES = [
    "01_executive_summary.md",
    "02_domain_capabilities.md",
    "03_benchmark_coverage.md",
    "04_evaluation_progress.md",
    "05_data_source_reference.md",
    "06_fix_history_and_patterns.md",
]

CSS = """
@page {
    size: A4;
    margin: 2cm 1.5cm;
    @top-center {
        content: attr(data-room-name) " — Room Capability Report";
        font-size: 9pt;
        color: #666;
    }
    @bottom-center {
        content: "Page " counter(page) " of " counter(pages);
        font-size: 9pt;
        color: #666;
    }
}
body {
    font-family: 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #333;
    max-width: 100%;
}
h1 {
    color: #1a365d;
    border-bottom: 3px solid #2b6cb0;
    padding-bottom: 8px;
    margin-top: 40px;
    page-break-before: always;
    font-size: 22pt;
}
h1:first-of-type { page-break-before: avoid; }
h2 {
    color: #2b6cb0;
    border-bottom: 1px solid #bee3f8;
    padding-bottom: 4px;
    margin-top: 24px;
    font-size: 16pt;
}
h3 { color: #2c5282; margin-top: 16px; font-size: 13pt; }
table {
    border-collapse: collapse;
    width: 100%;
    margin: 12px 0;
    font-size: 10pt;
}
th {
    background-color: #2b6cb0;
    color: white;
    padding: 8px 10px;
    text-align: left;
    font-weight: 600;
}
td { padding: 6px 10px; border-bottom: 1px solid #e2e8f0; }
tr:nth-child(even) td { background-color: #f7fafc; }
code {
    background-color: #edf2f7;
    padding: 2px 6px;
    border-radius: 3px;
    font-size: 9.5pt;
    color: #2d3748;
}
pre {
    background-color: #2d3748;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 6px;
    overflow-x: auto;
    font-size: 9pt;
}
pre code { background: none; color: inherit; padding: 0; }
blockquote {
    border-left: 4px solid #2b6cb0;
    margin: 16px 0;
    padding: 8px 16px;
    background-color: #ebf8ff;
    color: #2a4365;
    font-size: 10pt;
}
hr { border: none; border-top: 2px solid #e2e8f0; margin: 24px 0; }
ul, ol { padding-left: 24px; }
li { margin-bottom: 4px; }
.cover {
    text-align: center;
    padding: 120px 40px 60px;
    page-break-after: always;
}
.cover h1 { font-size: 32pt; border: none; page-break-before: avoid; }
.cover .subtitle { font-size: 16pt; color: #4a5568; margin-top: 20px; }
.cover .meta { font-size: 12pt; color: #718096; margin-top: 40px; }
.toc { page-break-after: always; }
.toc h2 { border: none; }
.toc ul { list-style: none; padding: 0; }
.toc li { padding: 6px 0; border-bottom: 1px dotted #ccc; font-size: 12pt; }
"""


def load_room_identity():
    identity_path = DATA_DIR / "room_identity.json"
    if identity_path.exists():
        with open(identity_path, encoding="utf-8") as f:
            return json.load(f)
    config_path = _KIT_ROOT / "room.config.yml"
    if config_path.exists():
        import yaml
        with open(config_path) as f:
            data = yaml.safe_load(f)
            return {
                "room_name": data.get("room_name", "genie_room"),
                "title": data.get("title", "Genie Room"),
                "description": data.get("description", ""),
            }
    return {"room_name": "genie_room", "title": "Genie Room", "description": ""}


def load_summaries():
    parts = []
    for fname in SUMMARY_FILES:
        path = SUMMARIES_DIR / fname
        if path.exists():
            with open(path, encoding="utf-8") as f:
                parts.append((fname, f.read()))
        else:
            print(f"  WARN: Missing summary: {fname}")
    return parts


def build_html(md_parts, room_identity):
    room_name = room_identity.get("room_name", "genie_room")
    title = room_identity.get("title", room_name)
    today = datetime.utcnow().strftime("%Y-%m-%d")

    try:
        import markdown
        md_ext = ["tables", "fenced_code"]
        convert = lambda text: markdown.markdown(text, extensions=md_ext)
    except ImportError:
        print("  WARN: markdown not installed. Install with: pip install markdown")
        print("        Falling back to plain text wrapping.")
        convert = lambda text: "<pre>" + text + "</pre>"

    toc_items = []
    body_sections = []
    for i, (fname, content) in enumerate(md_parts):
        html_section = convert(content)
        body_sections.append(html_section)
        first_h1 = None
        import re
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html_section)
        if m:
            first_h1 = re.sub("<[^>]+>", "", m.group(1)).strip()
        toc_items.append(f"<li>{i + 1}. {first_h1 or fname}</li>")

    cover = f"""
    <div class="cover">
        <h1>{title}</h1>
        <div class="subtitle">Room Capability Report</div>
        <div class="meta">
            <p>Databricks Genie AI Data Room</p>
            <p>Report Date: {today}</p>
        </div>
    </div>
    """

    toc = f"""
    <div class="toc">
        <h2>Table of Contents</h2>
        <ul>{chr(10).join(toc_items)}</ul>
    </div>
    """

    body = "<hr>".join(body_sections)

    return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>{title} — Room Capability Report</title>
    <style>{CSS}</style>
</head>
<body data-room-name="{room_name}">
{cover}
{toc}
{body}
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(description="Generate HTML/PDF report from markdown summaries")
    parser.add_argument("--engine", choices=["weasyprint", "pdfkit", "html-only"], default="html-only")
    parser.add_argument("--output-dir", default=str(_REPORTS_DIR))
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    room_identity = load_room_identity()
    room_name = room_identity.get("room_name", "genie_room")
    title = room_identity.get("title", room_name)

    print(f"Generating report for: {title} ({room_name})")

    print("Loading markdown summaries...")
    md_parts = load_summaries()
    print(f"  Loaded {len(md_parts)} sections")

    print("Building HTML...")
    html = build_html(md_parts, room_identity)

    html_path = output_dir / f"{room_name}_Report.html"
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  HTML saved: {html_path}")

    pdf_path = output_dir / f"{room_name}_Report.pdf"
    if args.engine == "weasyprint":
        print("Generating PDF with WeasyPrint...")
        from weasyprint import HTML
        HTML(string=html).write_pdf(str(pdf_path))
        print(f"  PDF saved: {pdf_path}")
    elif args.engine == "pdfkit":
        print("Generating PDF with pdfkit...")
        import pdfkit
        pdfkit.from_string(html, str(pdf_path), options={
            "page-size": "A4", "margin-top": "20mm", "margin-bottom": "20mm",
            "margin-left": "15mm", "margin-right": "15mm", "encoding": "UTF-8",
        })
        print(f"  PDF saved: {pdf_path}")
    else:
        print(f"HTML-only mode. Open {html_path} in browser and print to PDF.")
        print("For direct PDF: pip install markdown weasyprint")
        print("  python reports/scripts/generate_report.py --engine weasyprint")

    print("Done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
