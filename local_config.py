#!/usr/bin/env python3
"""
Configuracion local
-------------------
Carga y guarda preferencias simples en un archivo .env junto a la app.
"""

import os
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent
ENV_PATH = APP_DIR / ".env"

ENV_KEYS = [
    "LLM_PROVIDER",
    "LLM_MODEL",
    "GEMINI_API_KEY",
    "ANTHROPIC_API_KEY",
]


def load_local_env(path: Path = ENV_PATH) -> None:
    """Carga .env sin pisar variables ya seteadas por el sistema."""
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key:
            os.environ.setdefault(key, value)


def read_local_env(path: Path = ENV_PATH) -> dict:
    """Devuelve los valores guardados en .env."""
    values = {key: "" for key in ENV_KEYS}
    if not path.exists():
        return values

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key in values:
            values[key] = value.strip().strip('"').strip("'")
    return values


def save_local_env(values: dict, path: Path = ENV_PATH) -> None:
    """Guarda la configuracion local minima para abrir la app sin terminal."""
    current = read_local_env(path)
    current.update({key: value for key, value in values.items() if key in ENV_KEYS})

    lines = [
        "# Configuracion local de QA Documentation Agent",
        "# No subir este archivo al repositorio.",
        f"LLM_PROVIDER={current.get('LLM_PROVIDER') or 'gemini'}",
        f"LLM_MODEL={current.get('LLM_MODEL') or ''}",
        "",
        "# Gemini",
        f"GEMINI_API_KEY={current.get('GEMINI_API_KEY') or ''}",
        "",
        "# Anthropic Claude",
        f"ANTHROPIC_API_KEY={current.get('ANTHROPIC_API_KEY') or ''}",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")

    for key in ENV_KEYS:
        value = current.get(key)
        if value:
            os.environ[key] = value
