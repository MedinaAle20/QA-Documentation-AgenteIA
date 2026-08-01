#!/usr/bin/env python3
"""
QA Agent — App de escritorio
-------------------------------
Envuelve streamlit_app.py en una ventana nativa (sin pestaña de navegador),
usando pywebview. Levanta el servidor de Streamlit en un proceso en segundo
plano, en un puerto libre, y abre una ventana apuntando a esa URL. Al cerrar
la ventana, el servidor se apaga solo.

Uso:
    python desktop_app.py

Para armar un acceso directo de doble clic en Windows, ver el .bat de
ejemplo en README.md (sección "App de escritorio").
"""

import socket
import subprocess
import sys
import time
import urllib.request

try:
    import webview
except ImportError:
    print("Falta instalar pywebview. Corré: pip install -r requirements.txt")
    sys.exit(1)


APP_TITLE = "QA Documentation IA Agent"
STARTUP_TIMEOUT = 20.0


def _free_port() -> int:
    """Busca un puerto TCP libre en localhost para no chocar con otras apps."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


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


def main():
    port = _free_port()
    url = f"http://127.0.0.1:{port}"

    proc = subprocess.Popen(
        [
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", str(port),
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false",
            "--server.address", "127.0.0.1",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    try:
        print("Iniciando QA Documentation IA Agent...")
        if not _wait_for_server(url, STARTUP_TIMEOUT):
            print(
                f"Error: el servidor no respondió después de {STARTUP_TIMEOUT:.0f}s. "
                "Revisá que 'pip install -r requirements.txt' se haya corrido bien."
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
        # Al cerrar la ventana (o si algo falla), apagamos el servidor.
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()


if __name__ == "__main__":
    main()
