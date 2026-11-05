"""Mini ROV Ground Station - Main entry point."""

from __future__ import annotations

from .application import ROVApp


def main() -> None:
    app = ROVApp()
    app.run()


if __name__ == "__main__":
    main()