# QA Documentation IA Agent

QA Documentation IA Agent es una aplicacion local que usa IA para convertir requerimientos, historias de usuario o criterios de aceptacion en documentacion QA manual siguiendo STLC y fundamentos ISTQB.

El objetivo del proyecto no es ejecutar pruebas ni automatizar flujos, sino ayudar a preparar documentacion de testing revisable por una persona QA Jr: analisis de requerimientos, RTM, plan de pruebas, casos manuales, checklist de entorno y plantillas para ejecucion, defectos y cierre.

> Proyecto personal de portfolio: IA aplicada a documentacion QA, con foco en criterio, trazabilidad y buenas practicas de testing.

---

## Objetivo

En muchos proyectos, el QA recibe requerimientos incompletos o ambiguos y debe transformarlos en documentacion accionable antes de ejecutar pruebas. Este agente busca acelerar esa etapa sin reemplazar el criterio humano.

El agente ayuda a:

- Identificar requerimientos testeables.
- Detectar dudas, ambiguedades y riesgos.
- Sugerir estrategia y tipos de prueba.
- Aplicar tecnicas de diseno basadas en fundamentos ISTQB.
- Crear casos de prueba manuales estructurados.
- Generar plantillas para completar durante ejecucion real.

---

## Alcance

### Incluye

- Analisis de requerimientos.
- Matriz de trazabilidad (RTM).
- Plan de pruebas.
- Sugerencia de tecnicas de diseno ISTQB.
- Casos de prueba manuales.
- Checklist de entorno.
- Plantilla de reporte diario de ejecucion.
- Plantilla de defect log.
- Plantilla de test summary / sign-off.
- Exportacion a Excel.
- Exportacion a Markdown.
- Hoja Jira-ready para preparar importacion o copia manual.
- Guardado automatico de reportes locales.

### No incluye

- Ejecucion real de pruebas.
- Automatizacion Selenium, Playwright o API.
- Creacion real de bugs en Jira.
- Metricas inventadas de ejecucion.
- Sign-off automatico.
- Validacion de que el sistema bajo prueba funciona.

Las secciones de ejecucion, defectos y cierre se generan como plantillas para completar manualmente despues de probar.

---

## Fundamentos QA / ISTQB

El agente usa una base interna de fundamentos QA para orientar las sugerencias de estrategia y diseno de casos.

Tecnicas consideradas:

- Particion de equivalencia.
- Analisis de valores limite.
- Tabla de decision.
- Transicion de estados.
- Casos de uso.
- Error guessing.
- Pruebas exploratorias.
- Checklist-based testing.
- Priorizacion basada en riesgo.
- Trazabilidad requisito-caso.

Estas tecnicas se reflejan en:

- `02_Test_Plan`: tecnicas sugeridas y razon de uso.
- `03_Test_Cases`: tecnica aplicada por caso.

---

## Excel Generado

Cada reporte se exporta con 8 hojas:

| Hoja | Contenido |
| --- | --- |
| `01_RTM` | Matriz de trazabilidad, dudas y riesgos del requerimiento |
| `02_Test_Plan` | Alcance, fuera de alcance, tipos de prueba, tecnicas, estrategia, entry/exit criteria, supuestos y riesgos |
| `03_Test_Cases` | Casos manuales con tecnica de diseno, datos de prueba, pasos, resultado esperado, resultado obtenido, estado y notas |
| `04_Environment` | Checklist de preparacion del entorno |
| `05_Execution` | Plantilla de reporte diario de ejecucion |
| `06_Defect_Log` | Plantilla de registro de defectos |
| `07_Test_Summary` | Plantilla de cierre y sign-off |
| `08_Jira_Ready` | Casos preparados en formato amigable para Jira/Zephyr/Xray |

Campos como `Resultado obtenido`, `Estado`, metricas de ejecucion, bugs y decision final quedan pendientes para completar luego de la ejecucion real.

El archivo incluye formato profesional basico:

- Encabezados resaltados.
- Filtros en tablas.
- Columnas ajustadas por tipo de informacion.
- Colores por estado y prioridad.
- Campos editables resaltados para completar durante ejecucion.
- Listas desplegables en estado, prioridad y severidad.
- Pestañas diferenciadas por color.

Tambien se genera una version Markdown del documento para subir a GitHub o usar como evidencia de portfolio.

---

## Flujo de Uso

1. Abrir la app.
2. Configurar la API key de Gemini una sola vez desde `Opciones`.
3. Ingresar el nombre del proyecto.
4. Pegar el requerimiento o historia de usuario.
5. Generar la documentacion QA.
6. Revisar el resultado en pantalla.
7. Usar el Excel generado desde la carpeta local de reportes.
8. Usar el Markdown generado si se quiere documentar el caso en GitHub.

Los reportes se guardan automaticamente en:

```text
C:\Users\<tu-usuario>\Documents\QA Documentation IA Agent\reportes
```

Ejemplo de nombre:

```text
documentacion_qa_orangehrm_login_20260731_213000.xlsx
documentacion_qa_orangehrm_login_20260731_213000.md
```

El historial se mantiene como carpeta local de reportes, no como modulo interno de la app. Esto evita agregar base de datos o consumo innecesario de recursos para un uso local.

---

## Interfaz

La interfaz esta pensada para ser simple:

- Campo para nombre del proyecto.
- Campo para requerimiento.
- Boton para generar documentacion.
- Seccion `Opciones` para configurar Gemini.
- Vista del documento generado.
- Boton para descargar Excel.

La API key queda guardada localmente en `.env` y no se muestra en la pantalla principal una vez configurada.

---

## Arquitectura

```text
qa_agent.py          -> Nucleo del agente y exportacion Excel STLC
streamlit_app.py     -> Interfaz local simple
desktop_app.py       -> Ventana de escritorio con pywebview
QA Agent.bat         -> Lanzador de doble clic en Windows
prompts.py           -> Prompt principal orientado a STLC e ISTQB
qa_foundations.py    -> Base interna de tecnicas QA / ISTQB
local_config.py      -> Lectura y escritura de .env local
report_storage.py    -> Guardado automatico de reportes
errors.py            -> Errores legibles para usuario
llm_providers/
  base_provider.py
  gemini_provider.py
  anthropic_provider.py
  factory.py
```

---

## Instalacion

```bash
pip install -r requirements.txt
```

---

## Configuracion

La app usa Gemini como proveedor principal.

La forma recomendada es configurar la API key desde la app, en `Opciones`.

Tambien se puede crear manualmente un archivo `.env` usando `.env.example` como referencia:

```env
LLM_PROVIDER=gemini
LLM_MODEL=
GEMINI_API_KEY=tu-api-key
```

El archivo `.env` esta ignorado por Git para evitar subir credenciales.

---

## Ejecucion

### App local

```bash
streamlit run streamlit_app.py
```

Streamlit abre una direccion local como `http://localhost:8501`. No es un sitio publico; corre en la maquina local.

### App de escritorio

```bash
python desktop_app.py
```

Tambien se puede abrir `QA Agent.bat` con doble clic en Windows.

### CLI

```bash
python qa_agent.py --text "El usuario debe poder iniciar sesion con email y contrasena" --output documentacion_qa.xlsx
```

### Mock sin API

```bash
python mock_test.py
```

Genera `casos_mock.xlsx` para validar el formato del Excel sin consumir Gemini.

---

## Validaciones Realizadas

- Compilacion Python con `compileall`.
- Generacion mock sin API.
- Verificacion de Excel con 8 hojas STLC.
- Generacion real con Gemini usando `gemini-3.5-flash-lite`.
- Guardado local en carpeta de reportes.

---

## Roadmap

- [x] Generacion de documentacion QA con IA.
- [x] Exportacion STLC a Excel.
- [x] Exportacion STLC a Markdown.
- [x] Hoja Jira-ready para importacion/copia manual.
- [x] Fundamentos ISTQB en tecnicas de diseno.
- [x] App local simple con Streamlit.
- [x] Configuracion persistente de API key.
- [x] Guardado automatico de reportes.
- [x] Mejorar diseno visual del Excel.
- [x] Agregar validacion estricta del JSON devuelto por Gemini.
- [x] Historial simple mediante carpeta local de reportes.
- [ ] Empaquetar como `.exe` con PyInstaller.
- [ ] Agregar capturas al README.

---

## Autor

Ale - QA Jr explorando IA aplicada a documentacion de testing.
