Run the project locally

Preferred behavior:
- Activate the project's venv (recommended):

  PowerShell (one-time allow if needed):

  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  . .venv2\Scripts\Activate.ps1
  python src\manage.py runserver

- Or run using the venv python directly (no activation required):

  C:\Users\hackx\OneDrive\Desktop\Lib\.venv2\Scripts\python.exe src\manage.py runserver

Convenience scripts:
- PowerShell: `scripts/run-dev.ps1` (dot-run or run in PowerShell).
- CMD: `scripts/run-dev.bat`.

Quick local `python` shim:
- `python.cmd` at the project root forwards any `python` calls to the project's `.venv2` python. If you run `python manage.py runserver` from the project root, it will use the venv python. Note: this shim is intended for local convenience only.

Security note:
- The `python.cmd` wrapper executes an executable from your repository root — remove it if you don't want repository-local binaries to be run by the shell.
