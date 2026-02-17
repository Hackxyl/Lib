@echo off
:: Local python wrapper - forwards to the project's .venv2 python executable
SETLOCAL
SET SCRIPT_DIR=%~dp0
SET VENV_PY=%SCRIPT_DIR%\.venv2\Scripts\python.exe
IF NOT EXIST "%VENV_PY%" (
  echo Virtualenv python not found at %VENV_PY%
  exit /b 1
)
"%VENV_PY%" %*
ENDLOCAL
