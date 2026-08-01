#!/usr/bin/env python3
"""
Excepción compartida
-----------------------
QAAgentError es la excepción base para cualquier error conocido y ya
traducido a un mensaje entendible (config faltante, error de API, JSON
inválido, etc.). qa_agent.py solo necesita atrapar esta clase en un único
try/except en main(): no importa si el error vino de la factory, de un
provider específico, o de la validación de la respuesta.

Cualquier excepción que NO sea QAAgentError es un bug real y debe romper
con traceback completo, para poder diagnosticarlo.
"""


class QAAgentError(Exception):
    """Error conocido y manejado por QA Agent (se muestra como mensaje, sin traceback)."""
    pass
