#!/usr/bin/env python3
"""
Proveedor Anthropic (Claude)
------------------------------
Implementación de LLMProvider usando la API de Anthropic. Se mantiene como
opción premium/opcional: no es obligatoria para correr QA Agent.
"""

import json

from errors import QAAgentError
from llm_providers.base_provider import LLMProvider
from prompts import SYSTEM_PROMPT

DEFAULT_MODEL = "claude-sonnet-4-6"


class AnthropicProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        # Import scoped acá adentro: si no está instalado el SDK de Anthropic,
        # el resto del programa (Gemini, mocks, export a Excel) sigue andando.
        from anthropic import Anthropic

        self.client = Anthropic(api_key=api_key)
        self.model = model

    def generate_test_cases(self, requirement_text: str) -> dict:
        import anthropic

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=8192,
                system=SYSTEM_PROMPT,
                messages=[
                    {
                        "role": "user",
                        "content": f"Requerimiento a testear:\n\n{requirement_text}",
                    }
                ],
            )
        except anthropic.AuthenticationError:
            raise QAAgentError(
                "[Anthropic] API key inválida o sin permisos. Verificá ANTHROPIC_API_KEY."
            )
        except anthropic.RateLimitError:
            raise QAAgentError(
                "[Anthropic] Se alcanzó el límite de rate. Esperá un momento y reintentá."
            )
        except anthropic.APITimeoutError:
            raise QAAgentError(
                "[Anthropic] La API tardó demasiado en responder (timeout). Reintentá."
            )
        except anthropic.APIConnectionError:
            raise QAAgentError(
                "[Anthropic] No se pudo conectar con la API. Revisá tu conexión a internet."
            )
        except anthropic.APIStatusError as e:
            raise QAAgentError(
                f"[Anthropic] Error de la API (status {e.status_code}): {e.message}"
            )
        except anthropic.APIError as e:
            raise QAAgentError(f"[Anthropic] Error inesperado al llamar a la API: {e}")

        raw_text = "".join(
            block.text for block in response.content if block.type == "text"
        ).strip()

        # Por si el modelo agrega backticks a pesar de la instrucción
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`")
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
            raw_text = raw_text.strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            print("Aviso: no se pudo parsear la respuesta de Anthropic como JSON. Respuesta cruda:")
            print(raw_text)
            raise QAAgentError(
                "[Anthropic] La respuesta del modelo no es un JSON válido "
                "(puede ser un corte por longitud u otro problema de formato)."
            )
