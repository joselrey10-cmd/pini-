from __future__ import annotations

import sys

from pini_desktop.app import main as pini_main


def run():
    return pini_main()


if __name__ == "__main__":
    sys.exit(run())