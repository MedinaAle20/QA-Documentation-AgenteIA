#!/usr/bin/env python3
"""
Factory de proveedores
-------------------------
Punto único donde se decide qué proveedor de IA instanciar. La CLI y el
resto del núcleo nunca deberían tener un if/else por proveedor: siempre
pasan por acá.
"""

import os

from errors import QAAgentError
from llm_providers.base_provider import LLMProvider
from local_config import load_local_env


class ProviderConfigError(QAAgentError):
    """Falta configuración necesaria para instanciar un proveedor (API key, etc.)."""


def create_provider(provider_name: str | None = None, model: str | None = None) -> LLMProvider:
    """
    Crea el proveedor de IA correspondiente.

    Prioridad de configuración:
    1. Argumentos explícitos (provider_name, model).
    2. Variables de entorno (LLM_PROVIDER, LLM_MODEL).
    3. Valor por defecto seguro: gemini.

    Args:
        provider_name: "gemini" o "anthropic". Si es None, se lee de LLM_PROVIDER.
        model: nombre del modelo específico. Si es None, se lee de LLM_MODEL
            (o se usa el default de cada proveedor si tampoco está seteado).

    Raises:
        ProviderConfigError: si el proveedor no es soportado o falta la API key.
    """
    load_local_env()

    provider_name = (provider_name or os.environ.get("LLM_PROVIDER") or "gemini").lower()
    model = model or os.environ.get("LLM_MODEL")

    if provider_name == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ProviderConfigError(
                "No se encontró GEMINI_API_KEY en las variables de entorno.\n"
                '   Conseguí una gratis en https://aistudio.google.com/ y corré:\n'
                '   export GEMINI_API_KEY="tu-api-key"'
            )
        from llm_providers.gemini_provider import GeminiProvider, DEFAULT_MODEL

        return GeminiProvider(api_key=api_key, model=model or DEFAULT_MODEL)

    if provider_name == "anthropic":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise ProviderConfigError(
                "No se encontró ANTHROPIC_API_KEY en las variables de entorno.\n"
                '   export ANTHROPIC_API_KEY="tu-api-key"'
            )
        from llm_providers.anthropic_provider import AnthropicProvider, DEFAULT_MODEL

        return AnthropicProvider(api_key=api_key, model=model or DEFAULT_MODEL)

    raise ProviderConfigError(
        f"Proveedor de IA no soportado: '{provider_name}'. "
        "Opciones válidas: gemini, anthropic."
    )
