"""
generate_audit_report.py
Runs three security scanners and compiles their output into a PDF report.

Usage (from project root with venv active):
    python generate_audit_report.py
"""

import subprocess
import sys
import os
from datetime import date


# ---------------------------------------------------------------------------
# Scan helpers
# ---------------------------------------------------------------------------

def run_scan(cmd: list[str]) -> str:
    """
    Run *cmd* as a subprocess, capture stdout + stderr, and return the
    combined output string.  Handles:
      - FileNotFoundError  → tool not on PATH
      - Non-zero exit code → scanners exit non-zero when findings exist; we
                             still want the output
    """
    tool_name = cmd[0]
    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        return result.stdout or ""
    except FileNotFoundError:
        msg = f"[ERROR] Tool not found: '{tool_name}'. Install it and re-run."
        print(msg, file=sys.stderr)
        return msg


# ---------------------------------------------------------------------------
# PDF builder
# ---------------------------------------------------------------------------

def build_pdf(sections: list[tuple[str, str]], output_path: str) -> None:
    """
    Write a PDF to *output_path* with a cover page followed by one page per
    section in *sections* (list of (title, content) tuples).
    """
    try:
        from fpdf import FPDF
    except ImportError:
        print(
            "[ERROR] fpdf2 is not installed. Run: pip install fpdf2",
            file=sys.stderr,
        )
        sys.exit(1)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # --- Cover page ---
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 24)
    pdf.ln(30)
    pdf.cell(0, 12, "AegisDesk", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Security Audit Log", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 12)
    pdf.ln(6)
    pdf.cell(0, 8, f"Date: {date.today().isoformat()}", align="C", new_x="LMARGIN", new_y="NEXT")

    # --- One section per scan ---
    for section_title, content in sections:
        pdf.add_page()
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, section_title, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

        # Contextual dev note for the deploy-check section
        if "check --deploy" in section_title:
            pdf.set_font("Helvetica", "I", 10)
            note = (
                "Note: DEBUG=True and ALLOWED_HOSTS=[] are intentional "
                "development-only settings and are expected to appear as warnings."
            )
            pdf.multi_cell(0, 6, note, align="L")
            pdf.ln(4)

        body = content.strip() if content.strip() else "No issues found."
        pdf.set_font("Courier", "", 9)
        pdf.multi_cell(0, 5, body, align="L")

    pdf.output(output_path)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    project_root = os.path.dirname(os.path.abspath(__file__))

    scans = [
        (
            "Dependency Vulnerability Scan (pip-audit)",
            [sys.executable, "-m", "pip_audit"],
        ),
        (
            "Static Code Analysis (bandit)",
            [sys.executable, "-m", "bandit", "-r", ".", "--exclude", "./venv"],
        ),
        (
            "Django Deployment Security Check (check --deploy)",
            [sys.executable, "manage.py", "check", "--deploy"],
        ),
    ]

    sections: list[tuple[str, str]] = []
    raw_lines: list[str] = []

    # Cover info for raw text file
    raw_lines.append("AegisDesk")
    raw_lines.append("Security Audit Log")
    raw_lines.append(f"Date: {date.today().isoformat()}")
    raw_lines.append("")

    for section_title, cmd in scans:
        print(f"Running: {' '.join(cmd)} …")
        output = run_scan(cmd)
        sections.append((section_title, output))

        raw_lines.append(f"=== {section_title} ===")
        raw_lines.append(output.strip() if output.strip() else "No issues found.")
        raw_lines.append("")

    # Write plain-text intermediate
    raw_path = os.path.join(project_root, "audit_report_raw.txt")
    with open(raw_path, "w", encoding="utf-8") as f:
        f.write("\n".join(raw_lines))
    print(f"Raw text saved to {raw_path}")

    # Write PDF
    pdf_path = os.path.join(project_root, "AegisDesk_Security_Audit_Report.pdf")
    build_pdf(sections, pdf_path)
    print(f"PDF report saved to {pdf_path}")


if __name__ == "__main__":
    main()
