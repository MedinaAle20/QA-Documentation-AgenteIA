#!/usr/bin/env python3
"""
Interfaz simple de QA Documentation IA Agent.
"""

import io
from datetime import datetime

import streamlit as st

from errors import QAAgentError
from local_config import load_local_env, read_local_env, save_local_env
from markdown_exporter import export_to_markdown
from qa_agent import export_to_excel, generate_test_cases
from report_storage import REPORTS_DIR, save_markdown_report, save_report, slugify_project_name


load_local_env()

st.set_page_config(
    page_title="QA Documentation IA Agent",
    page_icon="QA",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    [data-testid="stHeader"],
    #MainMenu,
    footer {
        display: none;
    }

    .stApp {
        background: #f3f5f8;
        color: #202737;
    }

    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, p, label, span {
        color: #202737;
        letter-spacing: 0;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #ffffff;
        border: 1px solid #dfe3ea;
        border-radius: 8px;
        box-shadow: 0 8px 24px rgba(26, 34, 51, .06);
    }

    .stButton > button,
    .stDownloadButton > button {
        border-radius: 8px;
        min-height: 44px;
        font-weight: 700;
        background-color: #1f4e79 !important;
        color: #ffffff !important;
        border: 1px solid #1f4e79 !important;
    }

    .stButton > button *,
    .stDownloadButton > button * {
        color: #ffffff !important;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        background-color: #173d60 !important;
        border-color: #173d60 !important;
        color: #ffffff !important;
    }

    .stTextInput input,
    .stTextArea textarea {
        background: #ffffff;
        color: #202737;
        border: 1px solid #cfd6e2;
        border-radius: 8px;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #7a8494;
    }

    [data-testid="stMarkdownContainer"] {
        color: #202737;
    }

    .small-muted {
        color: #5f6b7a;
        font-size: .92rem;
        margin-top: -8px;
    }

    .saved-path {
        font-size: .9rem;
        color: #2f5d3b;
        background: #edf8ef;
        border: 1px solid #cfe8d5;
        border-radius: 8px;
        padding: 10px 12px;
        overflow-wrap: anywhere;
    }

    .app-note {
        background: #ffffff;
        border: 1px solid #dfe3ea;
        border-radius: 8px;
        padding: 12px 14px;
        color: #465366;
        margin-bottom: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def _render_list(title: str, items: list[str]) -> None:
    st.markdown(f"**{title}**")
    if not items:
        st.caption("Sin datos.")
        return
    for item in items:
        if isinstance(item, dict):
            technique = item.get("tecnica") or item.get("nombre") or ""
            application = item.get("aplicacion") or item.get("detalle") or ""
            st.markdown(f"- **{technique}:** {application}")
        else:
            st.markdown(f"- {item}")


def _render_results(data: dict) -> None:
    casos = data.get("casos_prueba", [])
    analysis = data.get("analisis_requerimientos") or {}
    plan = data.get("plan_pruebas") or {}

    st.header("Documento generado")
    st.subheader(data.get("feature") or "Feature sin nombre")
    if data.get("resumen"):
        st.write(data["resumen"])

    if st.session_state.get("last_report_path"):
        st.markdown(
            f'<div class="saved-path">Guardado en: {st.session_state["last_report_path"]}</div>',
            unsafe_allow_html=True,
        )
    if st.session_state.get("last_markdown_path"):
        st.caption(f"Markdown: {st.session_state['last_markdown_path']}")

    st.divider()

    st.subheader("1. Analisis de requerimientos")
    if analysis.get("objetivo"):
        st.write(analysis["objetivo"])
    _render_list("Dudas y ambiguedades", analysis.get("dudas_ambiguedades") or [])
    _render_list("Riesgos del requerimiento", analysis.get("riesgos_requerimiento") or [])

    st.markdown("**RTM**")
    st.dataframe(
        [
            {
                "Req ID": item.get("req_id", ""),
                "Descripcion": item.get("descripcion", ""),
                "Estado QA": item.get("estado_qa", ""),
                "Casos": ", ".join(item.get("casos_asignados") or []),
            }
            for item in analysis.get("rtm", [])
        ],
        hide_index=True,
        use_container_width=True,
    )

    st.divider()

    st.subheader("2. Plan de pruebas")
    col_a, col_b = st.columns(2)
    with col_a:
        _render_list("Alcance", plan.get("alcance") or [])
    with col_b:
        _render_list("Fuera de alcance", plan.get("fuera_de_alcance") or [])

    if plan.get("estrategia"):
        st.markdown("**Estrategia**")
        st.write(plan["estrategia"])

    _render_list("Tipos de prueba", plan.get("tipos_prueba") or [])
    _render_list("Tecnicas de diseno sugeridas (ISTQB)", plan.get("tecnicas_diseno") or [])
    _render_list("Criterios de entrada", plan.get("criterios_entrada") or [])
    _render_list("Criterios de salida", plan.get("criterios_salida") or [])
    _render_list("Supuestos", plan.get("supuestos") or [])
    _render_list("Riesgos", plan.get("riesgos") or [])

    st.divider()

    st.subheader("3. Casos de prueba")
    st.dataframe(
        [
            {
                "ID": caso.get("id", ""),
                "Modulo": caso.get("modulo", ""),
                "Titulo": caso.get("titulo", ""),
                "Tipo": caso.get("tipo", ""),
                "Tecnica": caso.get("tecnica_diseno", ""),
                "Prioridad": caso.get("prioridad", ""),
                "Estado": caso.get("estado", "Pendiente"),
            }
            for caso in casos
        ],
        hide_index=True,
        use_container_width=True,
    )

    with st.expander("Ver detalle de los casos", expanded=False):
        for caso in casos:
            st.markdown(f"**{caso.get('id', '')} - {caso.get('titulo', '')}**")
            st.caption(f"{caso.get('tipo', '')} · Prioridad {caso.get('prioridad', '')}")
            st.markdown(f"**Precondiciones:** {caso.get('precondiciones', '')}")
            st.markdown(f"**Datos de prueba:** {caso.get('datos_prueba', '')}")
            st.markdown(f"**Tecnica de diseno:** {caso.get('tecnica_diseno', '')}")
            pasos = caso.get("pasos") or []
            if pasos:
                st.markdown("**Pasos:**")
                for index, paso in enumerate(pasos, start=1):
                    st.markdown(f"{index}. {paso}")
            st.markdown(f"**Resultado esperado:** {caso.get('resultado_esperado', '')}")
            st.markdown("**Resultado obtenido:**")
            st.caption("Pendiente de completar durante la ejecucion.")
            if caso.get("notas"):
                st.markdown(f"**Notas:** {caso.get('notas')}")
            st.divider()

    st.divider()
    st.subheader("4. Plantillas para completar")
    st.markdown(
        "- Checklist de entorno\n"
        "- Reporte diario de ejecucion\n"
        "- Registro de defectos\n"
        "- Test Summary / Sign-off"
    )
    st.caption("Estas secciones se exportan al Excel como plantillas para completar manualmente.")

    buffer = io.BytesIO()
    export_to_excel(data, buffer)
    buffer.seek(0)

    project_name = st.session_state.get("last_project_name") or "proyecto"
    filename = (
        f"documentacion_qa_{slugify_project_name(project_name)}_"
        f"{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
    )
    st.download_button(
        "Descargar Excel",
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    markdown_text = export_to_markdown(data)
    st.download_button(
        "Descargar Markdown",
        data=markdown_text,
        file_name=filename.replace(".xlsx", ".md"),
        mime="text/markdown",
        use_container_width=True,
    )


saved_env = read_local_env()
saved_gemini_key = saved_env.get("GEMINI_API_KEY") or ""

st.title("QA Documentation IA Agent")
st.markdown(
    '<div class="app-note">Genera documentacion QA siguiendo STLC y fundamentos ISTQB: RTM, plan, tecnicas de diseno, casos, entorno, ejecucion, defectos y cierre.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.subheader("Datos del documento")
    project_name = st.text_input(
        "Nombre del proyecto",
        placeholder="Ej: OrangeHRM, ParaBank, Login e-commerce",
    )
    requirement_text = st.text_area(
        "Requerimiento",
        height=260,
        placeholder=(
            "Pega aca la historia de usuario, requisito funcional o criterios de aceptacion..."
        ),
    )

    generate_clicked = st.button(
        "Generar documentacion QA",
        use_container_width=True,
    )

with st.expander("Opciones", expanded=not bool(saved_gemini_key)):
    if saved_gemini_key:
        st.success("Gemini ya esta configurado.")
        replace_key = st.checkbox("Cambiar API key")
    else:
        st.warning("Falta configurar Gemini para poder generar documentos.")
        replace_key = True

    gemini_key = saved_gemini_key
    if replace_key:
        gemini_key_input = st.text_input(
            "Gemini API key",
            value="",
            type="password",
            placeholder="Pega tu API key de Gemini",
        )
        if st.button("Guardar API key", use_container_width=True):
            if not gemini_key_input.strip():
                st.error("Pega una API key antes de guardar.")
            else:
                save_local_env(
                    {
                        "LLM_PROVIDER": "gemini",
                        "LLM_MODEL": "",
                        "GEMINI_API_KEY": gemini_key_input.strip(),
                        "ANTHROPIC_API_KEY": "",
                    }
                )
                st.success("API key guardada. Ya no se va a mostrar en la pantalla principal.")
                st.rerun()

if generate_clicked:
    if not saved_gemini_key:
        st.error("Primero guarda tu API key de Gemini.")
    elif not requirement_text.strip():
        st.error("Escribi o pega un requerimiento antes de generar.")
    else:
        with st.spinner("Generando documentacion..."):
            try:
                save_local_env(
                    {
                        "LLM_PROVIDER": "gemini",
                        "LLM_MODEL": "",
                        "GEMINI_API_KEY": saved_gemini_key,
                        "ANTHROPIC_API_KEY": "",
                    }
                )
                data = generate_test_cases(requirement_text, provider_name="gemini", model=None)
                report_path = save_report(data, project_name.strip())
                markdown_path = save_markdown_report(data, report_path)
                st.session_state["last_data"] = data
                st.session_state["last_report_path"] = str(report_path)
                st.session_state["last_markdown_path"] = str(markdown_path)
                st.session_state["last_project_name"] = project_name.strip() or "proyecto"
                st.success("Documento generado correctamente.")
            except QAAgentError as e:
                st.error(str(e))
            except Exception as e:
                st.error(
                    "No se pudo completar la generacion. "
                    f"Detalle tecnico: {e}"
                )

if "last_data" in st.session_state:
    with st.container(border=True):
        _render_results(st.session_state["last_data"])

st.caption(f"Reportes locales: {REPORTS_DIR}")
