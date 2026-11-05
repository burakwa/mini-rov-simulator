"""Mini ROV Ground Station - Main entry point."""

from __future__ import annotations

import sys
from .application import ROVApp


def main() -> None:
    app = ROVApp()
    app.run()


if __name__ == "__main__":
    main()