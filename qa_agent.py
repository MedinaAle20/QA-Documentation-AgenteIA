#!/usr/bin/env python3
"""
QA Documentation Agent
----------------------
Genera documentacion QA manual siguiendo STLC y la exporta a Excel.
"""

import argparse
import os
import sys
from datetime import datetime

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
except ImportError:
    print("Falta instalar openpyxl. Corre: pip install -r requirements.txt")
    sys.exit(1)

from errors import QAAgentError
from llm_providers.factory import create_provider


REQUIRED_TOP_LEVEL_KEYS = [
    "feature",
    "resumen",
    "analisis_requerimientos",
    "plan_pruebas",
    "casos_prueba",
    "checklist_entorno",
    "reporte_ejecucion",
    "defect_log",
    "test_summary",
]

REQUIRED_CASE_KEYS = [
    "id",
    "modulo",
    "titulo",
    "tipo",
    "tecnica_diseno",
    "prioridad",
    "precondiciones",
    "datos_prueba",
    "pasos",
    "resultado_esperado",
    "resultado_obtenido",
    "estado",
    "notas",
]

HEADER_FILL = PatternFill(start_color="1F4E79", end_color="1F4E79", fill_type="solid")
SUBTITLE_FILL = PatternFill(start_color="D9EAF7", end_color="D9EAF7", fill_type="solid")
HEADER_FONT = Font(color="FFFFFF", bold=True, size=11)
TITLE_FONT = Font(bold=True, size=14, color="1F4E79")
SECTION_FONT = Font(bold=True, size=12, color="1F4E79")
BODY_FONT = Font(size=11)
MUTED_FONT = Font(size=9, color="666666")
WRAP = Alignment(wrap_text=True, vertical="top")
THIN = Side(style="thin", color="D9D9D9")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)


def generate_test_cases(requirement_text: str, provider_name: str = None, model: str = None) -> dict:
    """Genera documentacion QA parseada desde el proveedor configurado."""
    if not requirement_text or not requirement_text.strip():
        raise QAAgentError(
            "El requerimiento esta vacio. Pasa un texto con --text o un archivo "
            "con contenido en --input."
        )

    provider = create_provider(provider_name=provider_name, model=model)
    data = provider.generate_test_cases(requirement_text)

    if not isinstance(data, dict):
        raise QAAgentError("La respuesta del modelo no tiene la estructura esperada.")

    if "casos_prueba" not in data and "casos" not in data:
        raise QAAgentError(
            "La respuesta del modelo no tiene casos de prueba. Falta 'casos_prueba'."
        )

    normalized = _normalize_document(data)
    _validate_document_structure(normalized)
    return normalized


def _validate_document_structure(data: dict) -> None:
    """Valida que el JSON tenga la estructura minima esperada para STLC."""
    missing = [key for key in REQUIRED_TOP_LEVEL_KEYS if key not in data]
    if missing:
        raise QAAgentError(
            "La respuesta del modelo esta incompleta. Faltan secciones: "
            + ", ".join(missing)
        )

    if not isinstance(data.get("casos_prueba"), list) or not data["casos_prueba"]:
        raise QAAgentError("La respuesta del modelo no genero casos de prueba.")

    for index, case in enumerate(data["casos_prueba"], start=1):
        if not isinstance(case, dict):
            raise QAAgentError(f"El caso de prueba #{index} no tiene formato valido.")
        missing_case_keys = [key for key in REQUIRED_CASE_KEYS if key not in case]
        if missing_case_keys:
            case_id = case.get("id", f"#{index}")
            raise QAAgentError(
                f"El caso {case_id} esta incompleto. Faltan campos: "
                + ", ".join(missing_case_keys)
            )
        if not isinstance(case.get("pasos"), list):
            case_id = case.get("id", f"#{index}")
            raise QAAgentError(f"El caso {case_id} debe tener 'pasos' como lista.")


def _normalize_document(data: dict) -> dict:
    """Adapta respuestas viejas al formato STLC actual."""
    if "casos_prueba" in data:
        return data

    alcance = data.get("alcance") or {}
    casos = data.get("casos") or []
    normalized_cases = []
    for caso in casos:
        normalized_cases.append(
            {
                "id": caso.get("id", ""),
                "modulo": data.get("feature", ""),
                "titulo": caso.get("titulo", ""),
                "tipo": caso.get("tipo", ""),
                "prioridad": caso.get("prioridad", ""),
                "precondiciones": caso.get("precondiciones", ""),
                "datos_prueba": "",
                "tecnica_diseno": "",
                "pasos": caso.get("pasos", []),
                "resultado_esperado": caso.get("resultado_esperado", ""),
                "resultado_obtenido": "",
                "estado": "Pendiente",
                "notas": caso.get("notas", ""),
            }
        )

    return {
        "feature": data.get("feature", "Feature"),
        "resumen": data.get("resumen", ""),
        "analisis_requerimientos": {
            "objetivo": data.get("resumen", ""),
            "dudas_ambiguedades": [],
            "riesgos_requerimiento": data.get("supuestos_y_riesgos", []),
            "rtm": [],
        },
        "plan_pruebas": {
            "alcance": alcance.get("incluye", []),
            "fuera_de_alcance": alcance.get("no_incluye", []),
            "tipos_prueba": ["Funcional manual"],
            "tecnicas_diseno": [],
            "estrategia": data.get("estrategia", ""),
            "criterios_entrada": [],
            "criterios_salida": [],
            "supuestos": data.get("supuestos_y_riesgos", []),
            "riesgos": [],
        },
        "casos_prueba": normalized_cases,
        "checklist_entorno": [],
        "reporte_ejecucion": _empty_execution_report(),
        "defect_log": [_empty_defect()],
        "test_summary": _empty_summary(),
    }


def _empty_execution_report() -> dict:
    return {
        "fecha": "",
        "total_planificados": "",
        "ejecutados": "",
        "pasados": "",
        "fallados": "",
        "bloqueados": "",
        "comentarios": "",
        "bloqueos": [],
    }


def _empty_defect() -> dict:
    return {
        "bug_id": "",
        "resumen": "",
        "severidad": "",
        "prioridad": "",
        "estado": "",
        "asignado_a": "",
        "pasos_reproduccion": "",
        "resultado_esperado": "",
        "resultado_obtenido": "",
        "evidencia": "",
        "notas": "",
    }


def _empty_summary() -> dict:
    return {
        "resumen_ejecucion": "",
        "estado_bugs": "",
        "riesgos_residuales": "",
        "decision": "Pendiente de ejecucion",
        "comentarios_signoff": "",
    }


def _setup_sheet(ws, title: str, data: dict) -> int:
    ws.sheet_view.showGridLines = False
    ws.cell(row=1, column=1, value=title).font = TITLE_FONT
    ws.cell(row=2, column=1, value=f"Feature: {data.get('feature', 'N/A')}").font = BODY_FONT
    ws.cell(row=3, column=1, value=data.get("resumen", "")).font = MUTED_FONT
    ws.cell(row=4, column=1, value=f"Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}").font = MUTED_FONT
    return 6


def _write_section(ws, row: int, title: str, value) -> int:
    ws.cell(row=row, column=1, value=title).font = SECTION_FONT
    ws.cell(row=row, column=1).fill = SUBTITLE_FILL
    row += 1
    if isinstance(value, list):
        formatted_items = []
        for item in value:
            if isinstance(item, dict):
                technique = item.get("tecnica") or item.get("nombre") or ""
                application = item.get("aplicacion") or item.get("detalle") or ""
                formatted_items.append(f"- {technique}: {application}".strip())
            else:
                formatted_items.append(f"- {item}")
        text = "\n".join(formatted_items) if formatted_items else ""
    else:
        text = value or ""
    cell = ws.cell(row=row, column=1, value=text)
    cell.font = BODY_FONT
    cell.alignment = WRAP
    row += 2
    return row


def _write_table(ws, row: int, headers: list[str], rows: list[list], widths: list[int]) -> int:
    for col, header in enumerate(headers, start=1):
        cell = ws.cell(row=row, column=col, value=header)
        cell.fill = HEADER_FILL
        cell.font = HEADER_FONT
        cell.alignment = WRAP
        cell.border = BORDER

    for index, width in enumerate(widths, start=1):
        ws.column_dimensions[get_column_letter(index)].width = width

    row += 1
    if not rows:
        rows = [["" for _ in headers]]

    for row_values in rows:
        for col, value in enumerate(row_values, start=1):
            cell = ws.cell(row=row, column=col, value=value)
            cell.font = BODY_FONT
            cell.alignment = WRAP
            cell.border = BORDER
        row += 1

    ws.freeze_panes = "A7"
    return row + 1


def _steps_text(steps: list[str]) -> str:
    return "\n".join(f"{index}. {step}" for index, step in enumerate(steps or [], start=1))


def _write_rtm_sheet(wb, data: dict):
    ws = wb.active
    ws.title = "01_RTM"
    row = _setup_sheet(ws, "01 - Analisis de Requerimientos / RTM", data)
    analysis = data.get("analisis_requerimientos") or {}
    row = _write_section(ws, row, "Objetivo QA", analysis.get("objetivo", ""))
    row = _write_section(ws, row, "Dudas y ambiguedades", analysis.get("dudas_ambiguedades", []))
    row = _write_section(ws, row, "Riesgos del requerimiento", analysis.get("riesgos_requerimiento", []))

    headers = ["Req ID", "Descripcion del Requerimiento", "Estado QA", "ID Caso de Prueba Asignado"]
    table_rows = [
        [
            item.get("req_id", ""),
            item.get("descripcion", ""),
            item.get("estado_qa", ""),
            ", ".join(item.get("casos_asignados") or []),
        ]
        for item in analysis.get("rtm", [])
    ]
    _write_table(ws, row, headers, table_rows, [14, 60, 18, 30])


def _write_test_plan_sheet(wb, data: dict):
    ws = wb.create_sheet("02_Test_Plan")
    row = _setup_sheet(ws, "02 - Plan de Pruebas", data)
    plan = data.get("plan_pruebas") or {}
    for title, key in [
        ("Alcance (In-Scope)", "alcance"),
        ("Fuera de Alcance (Out-of-Scope)", "fuera_de_alcance"),
        ("Tipos de prueba", "tipos_prueba"),
        ("Tecnicas de diseno sugeridas (ISTQB)", "tecnicas_diseno"),
        ("Estrategia", "estrategia"),
        ("Criterios de entrada", "criterios_entrada"),
        ("Criterios de salida", "criterios_salida"),
        ("Supuestos", "supuestos"),
        ("Riesgos", "riesgos"),
    ]:
        row = _write_section(ws, row, title, plan.get(key, [] if key != "estrategia" else ""))
    ws.column_dimensions["A"].width = 110


def _write_test_cases_sheet(wb, data: dict):
    ws = wb.create_sheet("03_Test_Cases")
    row = _setup_sheet(ws, "03 - Casos de Prueba", data)
    headers = [
        "ID", "Modulo", "Titulo", "Tipo", "Tecnica de diseno", "Prioridad", "Precondiciones",
        "Datos de prueba", "Pasos", "Resultado esperado", "Resultado obtenido",
        "Estado", "Notas",
    ]
    rows = []
    for case in data.get("casos_prueba", []):
        rows.append(
            [
                case.get("id", ""),
                case.get("modulo", ""),
                case.get("titulo", ""),
                case.get("tipo", ""),
                case.get("tecnica_diseno", ""),
                case.get("prioridad", ""),
                case.get("precondiciones", ""),
                case.get("datos_prueba", ""),
                _steps_text(case.get("pasos", [])),
                case.get("resultado_esperado", ""),
                case.get("resultado_obtenido", ""),
                case.get("estado", "Pendiente"),
                case.get("notas", ""),
            ]
        )
    _write_table(ws, row, headers, rows, [10, 18, 32, 14, 26, 14, 30, 28, 46, 34, 34, 14, 26])


def _write_environment_sheet(wb, data: dict):
    ws = wb.create_sheet("04_Environment")
    row = _setup_sheet(ws, "04 - Checklist de Entorno", data)
    headers = ["ID", "Item", "Responsable", "Estado", "Notas"]
    rows = [
        [
            item.get("id", ""),
            item.get("item", ""),
            item.get("responsable", ""),
            item.get("estado", "Pendiente"),
            item.get("notas", ""),
        ]
        for item in data.get("checklist_entorno", [])
    ]
    _write_table(ws, row, headers, rows, [12, 70, 18, 16, 34])


def _write_execution_sheet(wb, data: dict):
    ws = wb.create_sheet("05_Execution")
    row = _setup_sheet(ws, "05 - Reporte Diario de Ejecucion", data)
    report = data.get("reporte_ejecucion") or _empty_execution_report()
    headers = ["Fecha", "Total planificados", "Ejecutados", "Pasados", "Fallados", "Bloqueados", "Comentarios"]
    rows = [[
        report.get("fecha", ""),
        report.get("total_planificados", ""),
        report.get("ejecutados", ""),
        report.get("pasados", ""),
        report.get("fallados", ""),
        report.get("bloqueados", ""),
        report.get("comentarios", ""),
    ]]
    row = _write_table(ws, row, headers, rows, [16, 20, 16, 16, 16, 16, 50])
    _write_section(ws, row, "Bloqueos / pendientes", report.get("bloqueos", []))


def _write_defect_log_sheet(wb, data: dict):
    ws = wb.create_sheet("06_Defect_Log")
    row = _setup_sheet(ws, "06 - Registro de Defectos", data)
    headers = [
        "Bug ID", "Resumen", "Severidad", "Prioridad", "Estado", "Asignado a",
        "Pasos reproduccion", "Resultado esperado", "Resultado obtenido", "Evidencia", "Notas",
    ]
    defects = data.get("defect_log") or [_empty_defect()]
    rows = [
        [
            defect.get("bug_id", ""),
            defect.get("resumen", ""),
            defect.get("severidad", ""),
            defect.get("prioridad", ""),
            defect.get("estado", ""),
            defect.get("asignado_a", ""),
            defect.get("pasos_reproduccion", ""),
            defect.get("resultado_esperado", ""),
            defect.get("resultado_obtenido", ""),
            defect.get("evidencia", ""),
            defect.get("notas", ""),
        ]
        for defect in defects
    ]
    _write_table(ws, row, headers, rows, [12, 34, 14, 14, 16, 18, 44, 34, 34, 24, 24])


def _write_summary_sheet(wb, data: dict):
    ws = wb.create_sheet("07_Test_Summary")
    row = _setup_sheet(ws, "07 - Test Summary / Sign-off", data)
    summary = data.get("test_summary") or _empty_summary()
    for title, key in [
        ("Resumen de ejecucion", "resumen_ejecucion"),
        ("Estado de bugs", "estado_bugs"),
        ("Riesgos residuales", "riesgos_residuales"),
        ("Decision / Sign-off", "decision"),
        ("Comentarios de cierre", "comentarios_signoff"),
    ]:
        row = _write_section(ws, row, title, summary.get(key, ""))
    ws.column_dimensions["A"].width = 110


def export_to_excel(data: dict, output_path: str):
    """Exporta la documentacion STLC a un Excel listo para revisar y completar."""
    data = _normalize_document(data)
    wb = Workbook()
    _write_rtm_sheet(wb, data)
    _write_test_plan_sheet(wb, data)
    _write_test_cases_sheet(wb, data)
    _write_environment_sheet(wb, data)
    _write_execution_sheet(wb, data)
    _write_defect_log_sheet(wb, data)
    _write_summary_sheet(wb, data)
    wb.save(output_path)


def main():
    parser = argparse.ArgumentParser(
        description="Agente de IA que genera documentacion QA siguiendo STLC."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--input", help="Ruta a un archivo .txt/.md con el requerimiento")
    group.add_argument("--text", help="El requerimiento pasado directo como texto")
    parser.add_argument("--output", default="documentacion_qa.xlsx", help="Ruta del Excel de salida")
    parser.add_argument("--provider", default=None, help="Proveedor de IA a usar: gemini")
    parser.add_argument("--model", default=None, help="Modelo especifico a usar")
    args = parser.parse_args()

    if args.input:
        if not os.path.exists(args.input):
            print(f"Error: no se encontro el archivo: {args.input}")
            sys.exit(1)
        with open(args.input, "r", encoding="utf-8") as f:
            requirement_text = f.read()
    else:
        requirement_text = args.text

    print("Generando documentacion QA STLC con IA...")
    try:
        data = generate_test_cases(requirement_text, provider_name=args.provider, model=args.model)
    except QAAgentError as e:
        print(f"Error: {e}")
        sys.exit(1)

    n_cases = len(data.get("casos_prueba", []))
    print(f"OK: se generaron {n_cases} casos de prueba y plantillas STLC.")

    try:
        export_to_excel(data, args.output)
    except Exception as e:
        print(f"Error: no se pudo generar el Excel: {e}")
        sys.exit(1)

    print(f"Excel guardado en: {args.output}")


if __name__ == "__main__":
    main()
