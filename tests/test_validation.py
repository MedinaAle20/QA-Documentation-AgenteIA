from copy import deepcopy

import pytest

from errors import QAAgentError
from mock_test import MOCK_DATA
from qa_agent import _normalize_document, _validate_document_structure


def test_mock_data_matches_required_document_contract():
    _validate_document_structure(deepcopy(MOCK_DATA))


def test_validation_rejects_missing_required_top_level_section():
    data = deepcopy(MOCK_DATA)
    data.pop("plan_pruebas")

    with pytest.raises(QAAgentError, match="Faltan campos: plan_pruebas"):
        _validate_document_structure(data)


def test_validation_rejects_empty_test_case_list():
    data = deepcopy(MOCK_DATA)
    data["casos_prueba"] = []

    with pytest.raises(QAAgentError, match="casos_prueba"):
        _validate_document_structure(data)


def test_legacy_case_payload_is_normalized_to_stlc_document():
    legacy_data = {
        "feature": "Login",
        "resumen": "Validar login.",
        "alcance": {
            "incluye": ["Login web"],
            "no_incluye": ["Login social"],
        },
        "estrategia": "Probar camino feliz y errores principales.",
        "supuestos_y_riesgos": ["Usuario existente en QA."],
        "casos": [
            {
                "id": "TC-001",
                "titulo": "Login exitoso",
                "tipo": "Positivo",
                "prioridad": "Alta",
                "precondiciones": "Usuario activo",
                "pasos": ["Ir a login", "Ingresar credenciales"],
                "resultado_esperado": "Acceso al dashboard",
                "notas": "",
            }
        ],
    }

    normalized = _normalize_document(legacy_data)

    assert normalized["feature"] == "Login"
    assert normalized["plan_pruebas"]["alcance"] == ["Login web"]
    assert normalized["casos_prueba"][0]["id"] == "TC-001"
    assert normalized["test_summary"]["decision"] == "Pendiente de ejecucion"
