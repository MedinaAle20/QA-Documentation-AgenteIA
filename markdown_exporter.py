#!/usr/bin/env python3
"""
Exportacion Markdown
--------------------
Genera una version Markdown de la documentacion QA para GitHub o portfolio.
"""

from datetime import datetime


def _list_items(items) -> str:
    if not items:
        return "_Sin datos._"

    lines = []
    for item in items:
        if isinstance(item, dict):
            technique = item.get("tecnica") or item.get("nombre") or ""
            application = item.get("aplicacion") or item.get("detalle") or ""
            lines.append(f"- **{technique}:** {application}")
        else:
            lines.append(f"- {item}")
    return "\n".join(lines)


def _table(headers: list[str], rows: list[list[str]]) -> str:
    header = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    body = []
    for row in rows or [["" for _ in headers]]:
        body.append("| " + " | ".join(_clean_cell(value) for value in row) + " |")
    return "\n".join([header, separator, *body])


def _clean_cell(value) -> str:
    return str(value or "").replace("\n", "<br>").replace("|", "\\|")


def _steps(steps: list[str]) -> str:
    if not steps:
        return "_Sin pasos._"
    return "\n".join(f"{index}. {step}" for index, step in enumerate(steps, start=1))


def export_to_markdown(data: dict) -> str:
    analysis = data.get("analisis_requerimientos") or {}
    plan = data.get("plan_pruebas") or {}
    cases = data.get("casos_prueba") or []
    env_items = data.get("checklist_entorno") or []
    execution = data.get("reporte_ejecucion") or {}
    summary = data.get("test_summary") or {}

    lines = [
        f"# QA Documentation - {data.get('feature', 'Proyecto')}",
        "",
        data.get("resumen", ""),
        "",
        f"_Generado: {datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "",
        "## 1. Analisis de Requerimientos",
        "",
        analysis.get("objetivo", "_Sin objetivo._"),
        "",
        "### Dudas y Ambiguedades",
        "",
        _list_items(analysis.get("dudas_ambiguedades") or []),
        "",
        "### Riesgos del Requerimiento",
        "",
        _list_items(analysis.get("riesgos_requerimiento") or []),
        "",
        "### RTM",
        "",
        _table(
            ["Req ID", "Descripcion", "Estado QA", "Casos asignados"],
            [
                [
                    item.get("req_id", ""),
                    item.get("descripcion", ""),
                    item.get("estado_qa", ""),
                    ", ".join(item.get("casos_asignados") or []),
                ]
                for item in analysis.get("rtm", [])
            ],
        ),
        "",
        "## 2. Plan de Pruebas",
        "",
        "### Alcance",
        "",
        _list_items(plan.get("alcance") or []),
        "",
        "### Fuera de Alcance",
        "",
        _list_items(plan.get("fuera_de_alcance") or []),
        "",
        "### Tipos de Prueba",
        "",
        _list_items(plan.get("tipos_prueba") or []),
        "",
        "### Tecnicas de Diseno Sugeridas",
        "",
        _list_items(plan.get("tecnicas_diseno") or []),
        "",
        "### Estrategia",
        "",
        plan.get("estrategia", "_Sin estrategia._"),
        "",
        "### Criterios de Entrada",
        "",
        _list_items(plan.get("criterios_entrada") or []),
        "",
        "### Criterios de Salida",
        "",
        _list_items(plan.get("criterios_salida") or []),
        "",
        "### Supuestos",
        "",
        _list_items(plan.get("supuestos") or []),
        "",
        "### Riesgos",
        "",
        _list_items(plan.get("riesgos") or []),
        "",
        "## 3. Casos de Prueba",
        "",
        _table(
            ["ID", "Modulo", "Titulo", "Tipo", "Tecnica", "Prioridad", "Estado"],
            [
                [
                    case.get("id", ""),
                    case.get("modulo", ""),
                    case.get("titulo", ""),
                    case.get("tipo", ""),
                    case.get("tecnica_diseno", ""),
                    case.get("prioridad", ""),
                    case.get("estado", "Pendiente"),
                ]
                for case in cases
            ],
        ),
        "",
    ]

    for case in cases:
        lines.extend(
            [
                f"### {case.get('id', '')} - {case.get('titulo', '')}",
                "",
                f"**Modulo:** {case.get('modulo', '')}",
                "",
                f"**Tipo:** {case.get('tipo', '')}",
                "",
                f"**Tecnica de diseno:** {case.get('tecnica_diseno', '')}",
                "",
                f"**Prioridad:** {case.get('prioridad', '')}",
                "",
                f"**Precondiciones:** {case.get('precondiciones', '')}",
                "",
                f"**Datos de prueba:** {case.get('datos_prueba', '')}",
                "",
                "**Pasos:**",
                "",
                _steps(case.get("pasos") or []),
                "",
                f"**Resultado esperado:** {case.get('resultado_esperado', '')}",
                "",
                "**Resultado obtenido:** _Pendiente de ejecucion._",
                "",
                f"**Estado:** {case.get('estado', 'Pendiente')}",
                "",
                f"**Notas:** {case.get('notas', '')}",
                "",
            ]
        )

    lines.extend(
        [
            "## 4. Checklist de Entorno",
            "",
            _table(
                ["ID", "Item", "Responsable", "Estado", "Notas"],
                [
                    [
                        item.get("id", ""),
                        item.get("item", ""),
                        item.get("responsable", ""),
                        item.get("estado", "Pendiente"),
                        item.get("notas", ""),
                    ]
                    for item in env_items
                ],
            ),
            "",
            "## 5. Reporte Diario de Ejecucion",
            "",
            _table(
                ["Fecha", "Planificados", "Ejecutados", "Pasados", "Fallados", "Bloqueados", "Comentarios"],
                [[
                    execution.get("fecha", ""),
                    execution.get("total_planificados", ""),
                    execution.get("ejecutados", ""),
                    execution.get("pasados", ""),
                    execution.get("fallados", ""),
                    execution.get("bloqueados", ""),
                    execution.get("comentarios", ""),
                ]],
            ),
            "",
            "## 6. Defect Log",
            "",
            "_Plantilla para completar durante la ejecucion. No se inventan defectos._",
            "",
            "## 7. Test Summary / Sign-off",
            "",
            f"**Decision:** {summary.get('decision', 'Pendiente de ejecucion')}",
            "",
            "_Plantilla para completar al cierre real de pruebas._",
            "",
        ]
    )

    return "\n".join(lines).strip() + "\n"
