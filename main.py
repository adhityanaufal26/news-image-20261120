# Entry program for make.fun competition news-image-20261120.
# Copies the entry.png beside this file to /output/entry.png
# (MAKEFUN_OUTPUT_DIR stands in for /output outside the grader).
# Standard library only.

import os
import shutil
from pathlib import Path


def main() -> None:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, out_dir / "entry.png")


if __name__ == "__main__":
    main()
