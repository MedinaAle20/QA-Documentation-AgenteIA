#!/usr/bin/env python3
"""
Mock Test
---------
Prueba export_to_excel() con datos STLC de ejemplo, sin llamar a ninguna API.
"""

from qa_agent import export_to_excel


MOCK_DATA = {
    "feature": "Login de usuario",
    "resumen": "Documentacion QA para autenticacion de usuarios registrados.",
    "analisis_requerimientos": {
        "objetivo": "Validar que usuarios registrados puedan iniciar sesion y que los errores se informen correctamente.",
        "dudas_ambiguedades": [
            "No se especifica si el bloqueo por intentos fallidos aplica por usuario, IP o dispositivo.",
            "No se define el texto exacto de los mensajes de error.",
        ],
        "riesgos_requerimiento": [
            "Mensajes demasiado especificos podrian revelar si un email existe.",
            "Falta de control de intentos fallidos podria habilitar ataques de fuerza bruta.",
        ],
        "rtm": [
            {
                "req_id": "REQ-001",
                "descripcion": "El usuario debe iniciar sesion con email y contrasena validos.",
                "estado_qa": "Revisado",
                "casos_asignados": ["TC-001"],
            },
            {
                "req_id": "REQ-002",
                "descripcion": "El sistema debe mostrar error ante credenciales invalidas.",
                "estado_qa": "Revisado",
                "casos_asignados": ["TC-002"],
            },
            {
                "req_id": "REQ-003",
                "descripcion": "La contrasena debe respetar la longitud minima definida.",
                "estado_qa": "Duda abierta",
                "casos_asignados": ["TC-003"],
            },
        ],
    },
    "plan_pruebas": {
        "alcance": [
            "Login con email y contrasena desde la pantalla web.",
            "Validaciones de campos obligatorios y credenciales invalidas.",
            "Mensajes de error visibles para el usuario.",
        ],
        "fuera_de_alcance": [
            "Login social con Google/Facebook.",
            "Recuperacion de contrasena.",
            "Pruebas de performance bajo carga.",
        ],
        "tipos_prueba": ["Funcional manual", "Validacion", "Exploratoria"],
        "tecnicas_diseno": [
            {
                "tecnica": "Particion de equivalencia",
                "aplicacion": "Separar credenciales validas e invalidas para cubrir comportamientos esperados.",
            },
            {
                "tecnica": "Analisis de valores limite",
                "aplicacion": "Validar limites de longitud minima de contrasena.",
            },
            {
                "tecnica": "Error guessing",
                "aplicacion": "Cubrir errores frecuentes como contrasenas incorrectas y mensajes ambiguos.",
            },
        ],
        "estrategia": "Priorizar camino feliz, validaciones negativas y limites de campos antes de ejecutar pruebas exploratorias.",
        "criterios_entrada": [
            "Build desplegado en ambiente QA.",
            "Usuario de prueba creado en base QA.",
            "Credenciales de acceso al ambiente disponibles.",
        ],
        "criterios_salida": [
            "Casos de prueba ejecutados y documentados.",
            "Sin bugs criticos o altos abiertos para el modulo.",
            "Defectos conocidos documentados.",
        ],
        "supuestos": [
            "Se asume que el usuario ya existe en la base de datos QA.",
            "Se asume que los mensajes finales pueden cambiar por decision de UX.",
        ],
        "riesgos": [
            "Ambiguedad en reglas de bloqueo por intentos fallidos.",
            "Datos de prueba incompletos podrian bloquear la ejecucion.",
        ],
    },
    "casos_prueba": [
        {
            "id": "TC-001",
            "modulo": "Login",
            "titulo": "Login exitoso con credenciales validas",
            "tipo": "Positivo",
            "prioridad": "Alta",
            "precondiciones": "Usuario registrado y activo en base QA.",
            "datos_prueba": "Email: ana.gomez@gmail.com / Password: Abc12345!",
            "tecnica_diseno": "Particion de equivalencia",
            "pasos": [
                "Ir a la pantalla /login.",
                "Ingresar ana.gomez@gmail.com en el campo email.",
                "Ingresar Abc12345! en el campo contrasena.",
                "Presionar el boton Entrar.",
            ],
            "resultado_esperado": "El sistema redirige al dashboard y muestra la sesion iniciada.",
            "resultado_obtenido": "",
            "estado": "Pendiente",
            "notas": "",
        },
        {
            "id": "TC-002",
            "modulo": "Login",
            "titulo": "Login fallido con contrasena incorrecta",
            "tipo": "Negativo",
            "prioridad": "Alta",
            "precondiciones": "Usuario registrado y activo en base QA.",
            "datos_prueba": "Email: ana.gomez@gmail.com / Password: Wrong123!",
            "tecnica_diseno": "Error guessing",
            "pasos": [
                "Ir a la pantalla /login.",
                "Ingresar ana.gomez@gmail.com.",
                "Ingresar Wrong123!.",
                "Presionar el boton Entrar.",
            ],
            "resultado_esperado": "El sistema muestra un error de credenciales invalidas y no inicia sesion.",
            "resultado_obtenido": "",
            "estado": "Pendiente",
            "notas": "",
        },
    ],
    "checklist_entorno": [
        {
            "id": "ENV-001",
            "item": "Confirmar que el build esta desplegado en ambiente QA.",
            "responsable": "QA / DevOps",
            "estado": "Pendiente",
            "notas": "",
        },
        {
            "id": "ENV-002",
            "item": "Crear usuario de prueba con credenciales conocidas.",
            "responsable": "QA",
            "estado": "Pendiente",
            "notas": "",
        },
    ],
    "reporte_ejecucion": {
        "fecha": "",
        "total_planificados": "",
        "ejecutados": "",
        "pasados": "",
        "fallados": "",
        "bloqueados": "",
        "comentarios": "",
        "bloqueos": [],
    },
    "defect_log": [
        {
            "bug_id": "",
            "resumen": "",
            "severidad": "",
            "prioridad": "",
            "estado": "",
            "asignado_a": "",
            "pasos_reproduccion": "",
            "resultado_esperado": "",
            "resultado_obtenido": "",
            "evidencia": "",
            "notas": "",
        }
    ],
    "test_summary": {
        "resumen_ejecucion": "",
        "estado_bugs": "",
        "riesgos_residuales": "",
        "decision": "Pendiente de ejecucion",
        "comentarios_signoff": "",
    },
}


if __name__ == "__main__":
    export_to_excel(MOCK_DATA, "casos_mock.xlsx")
    print("OK: casos_mock.xlsx generado con documentacion STLC de ejemplo.")
