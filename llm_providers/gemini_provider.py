#!/usr/bin/env python3
"""
Proveedor Gemini
------------------
Implementación de LLMProvider usando la API de Gemini (Google AI Studio).
Es el proveedor gratuito por defecto: no requiere tarjeta y el free tier
alcanza de sobra para uso personal.
"""

import json

from errors import QAAgentError
from llm_providers.base_provider import LLMProvider
from prompts import SYSTEM_PROMPT

DEFAULT_MODEL = "gemini-3.5-flash-lite"


class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str, model: str = DEFAULT_MODEL):
        # Import scoped acá adentro: si no está instalado el SDK de Gemini,
        # el resto del programa (Anthropic, mocks, export a Excel) sigue andando.
        from google import genai
        from google.genai import types

        self.client = genai.Client(api_key=api_key)
        self.types = types
        self.model = model

    def generate_test_cases(self, requirement_text: str) -> dict:
        from google.genai import errors as genai_errors

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=f"Requerimiento a testear:\n\n{requirement_text}",
                config=self.types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=8192,
                    response_mime_type="application/json",
                ),
            )
        except genai_errors.ClientError as e:
            # 400/401/403/404/429, etc. Distinguimos los casos más comunes.
            if e.code in (401, 403):
                raise QAAgentError(
                    "[Gemini] API key inválida o sin permisos. Verificá GEMINI_API_KEY."
                )
            if e.code == 429:
                raise QAAgentError(
                    "[Gemini] Se alcanzó el límite de rate del free tier. Esperá un momento y reintentá."
                )
            if e.code == 404:
                raise QAAgentError(
                    "[Gemini] El modelo configurado ya no está disponible. Actualizá el modelo de Gemini en el proyecto."
                )
            raise QAAgentError(f"[Gemini] Error en la solicitud (status {e.code}): {e.message}")
        except genai_errors.ServerError as e:
            raise QAAgentError(
                f"[Gemini] Error del lado del servidor (status {e.code}). Reintentá en unos minutos."
            )
        except OSError:
            raise QAAgentError(
                "[Gemini] No se pudo conectar con la API. Revisá internet, firewall o permisos de red."
            )
        except genai_errors.APIError as e:
            raise QAAgentError(f"[Gemini] Error inesperado al llamar a la API: {e}")

        raw_text = (response.text or "").strip()

        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            print("Aviso: no se pudo parsear la respuesta de Gemini como JSON. Respuesta cruda:")
            print(raw_text)
            raise QAAgentError(
                "[Gemini] La respuesta del modelo no es un JSON válido "
                "(puede ser un corte por longitud u otro problema de formato)."
            )
