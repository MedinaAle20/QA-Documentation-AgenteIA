#!/usr/bin/env python3
"""
Interfaz base de proveedores de IA
------------------------------------
Contrato común que debe cumplir cualquier proveedor (Gemini, Anthropic, etc.)
para poder ser usado por QA Agent. El núcleo del programa solo conoce esta
interfaz, nunca el SDK específico de cada proveedor.
"""

from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Contrato común para los proveedores de modelos de lenguaje."""

    @abstractmethod
    def generate_test_cases(self, requirement_text: str) -> dict:
        """
        Genera casos de prueba a partir de un requerimiento.

        Args:
            requirement_text: el requerimiento a testear (historia de usuario,
                criterios de aceptación, etc.)

        Returns:
            dict con la estructura {"feature": ..., "resumen": ..., "casos": [...]}
            ya parseado desde JSON.

        Raises:
            json.JSONDecodeError: si la respuesta del modelo no es JSON válido.
            Cualquier excepción propia del SDK del proveedor (autenticación,
            rate limit, etc.) se deja propagar tal cual: el llamador la
            traduce a un mensaje legible en la CLI.
        """
        raise NotImplementedError
