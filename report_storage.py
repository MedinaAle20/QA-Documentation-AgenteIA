#!/usr/bin/env python3
"""
Guardado de reportes
--------------------
Centraliza donde se guardan los Excel generados por la app local.
"""

import re
import unicodedata
from datetime import datetime
from pathlib import Path

from markdown_exporter import export_to_markdown
from qa_agent import export_to_excel


REPORTS_DIR = Path.home() / "Documents" / "QA Documentation IA Agent" / "reportes"


def slugify_project_name(project_name: str) -> str:
    """Convierte el nombre del proyecto en una parte segura para nombre de archivo."""
    normalized = unicodedata.normalize("NFKD", project_name or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_text).strip("_").lower()
    return slug or "proyecto"


def build_report_path(project_name: str, generated_at: datetime | None = None) -> Path:
    """Arma una ruta unica para el reporte."""
    generated_at = generated_at or datetime.now()
    timestamp = generated_at.strftime("%Y%m%d_%H%M%S")
    filename = f"documentacion_qa_{slugify_project_name(project_name)}_{timestamp}.xlsx"
    return REPORTS_DIR / filename


def save_report(data: dict, project_name: str) -> Path:
    """Guarda el Excel en la carpeta local de reportes y devuelve la ruta."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)
    output_path = build_report_path(project_name)
    export_to_excel(data, output_path)
    return output_path


def save_markdown_report(data: dict, excel_path: Path) -> Path:
    """Guarda una version Markdown junto al Excel generado."""
    markdown_path = excel_path.with_suffix(".md")
    markdown_path.write_text(export_to_markdown(data), encoding="utf-8")
    return markdown_path
