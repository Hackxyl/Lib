@echo off
REM scripts\run-dev.bat - Run Django dev server using project's venv python
SET SCRIPT_DIR=%~dp0
SET VENV_PY=%~dp0..\.venv2\Scripts\python.exe
IF NOT EXIST "%VENV_PY%" (
  echo Virtualenv python not found at %VENV_PY%
  exit /b 1
)
"%VENV_PY%" "%~dp0..\src\manage.py" runserver
