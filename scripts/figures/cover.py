#!/usr/bin/env python3
"""Write folio/dth-phc/media/cover.svg: page 1 (the cover) of the WHO handbook, as the
PDF's own vectors (`pdftocairo -svg`), so the document opens on the cover of the
publication it transcribes. The PDF is the L1 source the who-iris mount holds; the
block cites it (ISBN, IRIS) as the original, like the figure crops. Owner card
2026-11-16 (Q3 = A): the original cover, unchanged and cited.

Usage: cover.py [--check]   (--check needs pdftocairo; without it, it checks the file exists)
"""
import shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PDF = ROOT / "who-iris/uploads/9789240093362-eng/9789240093362-eng.pdf"
OUT = ROOT / "folio/dth-phc/media/cover.svg"
TITLE = ("Cover of Digital transformation handbook for primary health care: optimizing person-centred "
         "point of service systems (WHO, 2024; ISBN 978-92-4-009336-2), page 1 of the PDF")


def render() -> str:
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "p1.svg"
        subprocess.run(["pdftocairo", "-svg", "-f", "1", "-l", "1", str(PDF), str(p)], check=True, stderr=subprocess.DEVNULL)
        svg = p.read_text()
    i = svg.index(">", svg.index("<svg")) + 1
    return svg[:i].replace("<svg ", '<svg role="img" aria-label="' + TITLE + '" ', 1) + f"\n<title>{TITLE}</title>" + svg[i:]


def main() -> None:
    if "--check" in sys.argv:
        if not OUT.exists():
            raise SystemExit(f"{OUT.relative_to(ROOT)} is missing: run scripts/figures/cover.py")
        if shutil.which("pdftocairo") and PDF.exists() and OUT.read_text() != render():
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale: run scripts/figures/cover.py")
        print(f"{OUT.relative_to(ROOT)}: up to date")
        return
    OUT.write_text(render())
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
