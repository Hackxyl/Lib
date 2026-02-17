# scripts/run-dev.ps1
# Run the Django development server using the project's venv python
Push-Location (Split-Path -Parent $MyInvocation.MyCommand.Path)
$venvPython = Join-Path .. '.venv2\Scripts\python.exe'
if (-Not (Test-Path $venvPython)) {
    Write-Error "Virtualenv python not found at $venvPython. Create the venv (.venv2) or update this script to point to your python.";
    Pop-Location; exit 1
}
& $venvPython '..\src\manage.py' runserver
Pop-Location
