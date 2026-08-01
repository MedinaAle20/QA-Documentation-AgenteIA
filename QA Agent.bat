@echo off
REM Lanzador de QA Agent (app de escritorio).
REM Doble clic para abrir la app sin tocar la terminal.
REM Si algo falla, esta ventana se queda abierta mostrando el error.

cd /d "%~dp0"
python desktop_app.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Hubo un error al iniciar QA Agent. Revisa el mensaje de arriba.
    pause
)
