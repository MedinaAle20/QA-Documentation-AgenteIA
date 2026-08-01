#!/usr/bin/env python3
"""
Fundamentos QA
--------------
Base interna de referencia para orientar la documentacion del agente.
"""

ISTQB_TECHNIQUES = {
    "black_box": [
        "Particion de equivalencia",
        "Analisis de valores limite",
        "Tabla de decision",
        "Transicion de estados",
        "Casos de uso",
    ],
    "experience_based": [
        "Error guessing",
        "Pruebas exploratorias",
        "Checklist-based testing",
    ],
    "strategy": [
        "Priorizacion basada en riesgo",
        "Trazabilidad requisito-caso",
        "Cobertura de criterios de aceptacion",
        "Confirmacion y regresion como etapas posteriores a defectos corregidos",
    ],
}


def format_istqb_prompt_reference() -> str:
    """Devuelve una referencia compacta para insertar en el prompt."""
    lines = []
    for category, techniques in ISTQB_TECHNIQUES.items():
        label = category.replace("_", " ").title()
        lines.append(f"{label}: {', '.join(techniques)}")
    return "\n".join(lines)
