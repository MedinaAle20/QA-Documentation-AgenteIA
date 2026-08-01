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


QA_DOCUMENTATION_SKILLS = {
    "documentacion_qa": [
        "Redactar documentacion clara, accionable y revisable por un QA Jr.",
        "Separar hechos, supuestos, dudas y riesgos.",
        "Evitar afirmar ejecucion real cuando solo se esta preparando documentacion.",
    ],
    "rtm": [
        "Mapear cada requerimiento testeable contra uno o mas casos de prueba.",
        "Marcar requerimientos ambiguos como En revision o Duda abierta.",
        "Evitar dejar criterios de aceptacion sin trazabilidad.",
    ],
    "diseno_casos": [
        "Escribir pasos concretos y datos de prueba realistas.",
        "Elegir tecnicas de diseno segun el tipo de regla o flujo.",
        "Mantener resultado obtenido y estado como campos pendientes de ejecucion.",
    ],
    "defect_reporting": [
        "Preparar defect logs con campos profesionales sin inventar bugs.",
        "Distinguir severidad, prioridad, evidencia y pasos de reproduccion.",
    ],
}


def format_istqb_prompt_reference() -> str:
    """Devuelve una referencia compacta para insertar en el prompt."""
    lines = []
    for category, techniques in ISTQB_TECHNIQUES.items():
        label = category.replace("_", " ").title()
        lines.append(f"{label}: {', '.join(techniques)}")
    return "\n".join(lines)


def format_skill_prompt_reference() -> str:
    """Devuelve habilidades internas compactas para orientar la redaccion."""
    lines = []
    for skill, principles in QA_DOCUMENTATION_SKILLS.items():
        label = skill.replace("_", " ").title()
        lines.append(f"{label}:")
        for principle in principles:
            lines.append(f"- {principle}")
    return "\n".join(lines)
