#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from pathlib import Path


def _reexec_with_venv_python():
    """If a local virtualenv exists ('.venv2', '.venv', or 'venv'), re-exec this script with that python executable.
    This makes `python manage.py ...` work even when the system python is invoked.
    Uses an env var `MANAGE_PY_REEXEC` to avoid infinite re-exec loops."""
    try:
        # Only attempt re-exec once
        if os.environ.get('MANAGE_PY_REEXEC') == '1':
            return
        base = Path(__file__).resolve().parent.parent  # project root
        candidates = ['.venv2', '.venv', 'venv']
        for c in candidates:
            venv_dir = base / c
            if venv_dir.exists():
                if os.name == 'nt':
                    venv_python = venv_dir / 'Scripts' / 'python.exe'
                else:
                    venv_python = venv_dir / 'bin' / 'python'
                if venv_python.exists():
                    # If we're already running under that python, do nothing
                    try:
                        if Path(sys.executable).samefile(venv_python):
                            return
                    except Exception:
                        pass
                    # Re-exec using the venv python
                    os.environ['MANAGE_PY_REEXEC'] = '1'
                    os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    except Exception:
        # Fail silently and continue with current interpreter
        return


_reexec_with_venv_python()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ruby.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
