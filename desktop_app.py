#!/usr/bin/env python3
"""
QA Documentation IA Agent - App de escritorio
---------------------------------------------
Abre la app Streamlit dentro de una ventana nativa usando pywebview.
Para facilitar el empaquetado, el servidor Streamlit corre en un segundo
proceso interno del mismo ejecutable.
"""

from pathlib import Path
import socket
import subprocess
import sys
import time
import tempfile
import traceback
import urllib.request


APP_TITLE = "QA Documentation IA Agent"
STARTUP_TIMEOUT = 20.0


def _log_path() -> Path:
    return Path(tempfile.gettempdir()) / "qa_documentation_ia_agent.log"


def _write_log(message: str) -> None:
    with _log_path().open("a", encoding="utf-8") as log_file:
        log_file.write(message.rstrip() + "\n")


def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(getattr(sys, "_MEIPASS"))
    return Path(__file__).resolve().parent


def _free_port() -> int:
    """Busca un puerto TCP libre en localhost para no chocar con otras apps."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind(("127.0.0.1", 0))
        return server_socket.getsockname()[1]


def _wait_for_server(url: str, timeout: float) -> bool:
    """Espera a que el servidor de Streamlit responda antes de abrir la ventana."""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            urllib.request.urlopen(url, timeout=1)
            return True
        except Exception:
            time.sleep(0.3)
    return False


def _run_streamlit_server(port: int) -> None:
    from streamlit.web import bootstrap

    script_path = _app_dir() / "streamlit_app.py"
    if not script_path.exists():
        raise FileNotFoundError(f"No se encontro streamlit_app.py en {script_path}")

    flag_options = {
        "global.developmentMode": False,
        "server.port": port,
        "server.headless": True,
        "server.address": "127.0.0.1",
        "browser.gatherUsageStats": False,
    }
    bootstrap.load_config_options(flag_options)
    bootstrap.run(str(script_path), False, [], flag_options)


def _server_command(port: int) -> list[str]:
    if getattr(sys, "frozen", False):
        return [sys.executable, "--streamlit-server", str(port)]
    return [sys.executable, str(Path(__file__).resolve()), "--streamlit-server", str(port)]


def _start_streamlit(port: int) -> subprocess.Popen:
    creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    log_file = _log_path().open("a", encoding="utf-8")
    return subprocess.Popen(
        _server_command(port),
        stdout=log_file,
        stderr=log_file,
        creationflags=creationflags,
    )


def main() -> None:
    if len(sys.argv) >= 3 and sys.argv[1] == "--streamlit-server":
        try:
            _run_streamlit_server(int(sys.argv[2]))
        except Exception:
            _write_log(traceback.format_exc())
            raise
        return

    try:
        import webview
    except ImportError:
        print("Falta instalar pywebview. Corre: pip install -r requirements.txt")
        sys.exit(1)

    port = _free_port()
    url = f"http://127.0.0.1:{port}"

    print("Iniciando QA Documentation IA Agent...")
    server_process = _start_streamlit(port)
    try:
        if not _wait_for_server(url, STARTUP_TIMEOUT):
            print(
                f"Error: el servidor no respondio despues de {STARTUP_TIMEOUT:.0f}s. "
                "Revisa que 'pip install -r requirements.txt' se haya corrido bien."
            )
            return

        webview.create_window(
            APP_TITLE,
            url,
            width=1150,
            height=820,
            min_size=(800, 600),
        )
        webview.start()
    finally:
        server_process.terminate()
        try:
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server_process.kill()


if __name__ == "__main__":
    main()
