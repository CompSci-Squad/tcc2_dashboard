"""Atalho `uv run tcc2-dashboard` que sobe o app."""

from __future__ import annotations

import sys
from pathlib import Path

from streamlit.web import cli as stcli


def main() -> None:
    app = Path(__file__).parent / "app.py"
    sys.argv = ["streamlit", "run", str(app), *sys.argv[1:]]
    sys.exit(stcli.main())


if __name__ == "__main__":
    main()
