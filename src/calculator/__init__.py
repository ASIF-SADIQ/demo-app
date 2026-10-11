"""
FX Scientific Calculator Package
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path


def main() -> None:
    """Launches the Streamlit FX Scientific Calculator application."""
    root_dir = Path(__file__).resolve().parent.parent.parent
    app_path = root_dir / "main.py"
    cmd = [sys.executable, "-m", "streamlit", "run", str(app_path)] + sys.argv[1:]
    subprocess.run(cmd)


if __name__ == "__main__":
    main()
