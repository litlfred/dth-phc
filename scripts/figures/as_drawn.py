#!/usr/bin/env python3
"""Draw a handbook figure as the original draws it, from its data file.

figure-rebuild, "the redraw keeps the original's layout": the data file
(`dth-phc-figure-as-drawn/v1`, under figure-data/) holds the figure's content
as parts, each with its words, its role and, where a part names a glossary
concept or a model element, a link. The drawing is the PDF's own artwork
(every path in the figure's region, copied by extract_pdf_artwork.py into the
file the data names in `artwork`), so shapes, colours and places are the
original's. The words are written as SVG <text> at the printed places, and the
script fails unless:

- each part's words equal the printed lines inside its box (who-iris
  vector-labels.json, through the artwork file), and
- every printed line in the region belongs to a part, so nothing is dropped.

Usage: as_drawn.py <figure-data/....json> [--check]
       as_drawn.py --all [--check]   (every figure-data/*.json of this schema)
"""
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
SCHEMA = "dth-phc-figure-as-drawn/v1"
FONT = "'Source Sans Pro','Source Sans 3','Open Sans','Segoe UI',Helvetica,Arial,sans-serif"
SCALE = 2  # the who-iris crops are 2 px per PDF point; so is the SVG's default size
WEIGHT = {"Black": 900, "Bold": 700, "Semibold": 600, "Regular": 400, "Light": 300}


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def norm(s: str) -> str:
    s = s.replace("•", " ").replace("\t", " ")
    s = re.sub(r"\s+", " ", s).strip()
    return re.sub(r"(\w)- (\w)", r"\1-\2", s)  # a word the print hyphenates across lines


def style(fonts: list) -> tuple:
    """(weight, italic) of a printed line, from its first font, e.g. SourceSansPro-BoldIt."""
    face = fonts[0].split("-")[-1]
    italic = face.endswith("It") and len(fonts) == 1
    face = face[:-2] if face.endswith("It") else face
    return WEIGHT.get(face or "Regular", 400), italic


def inside(bbox: list, box: list) -> bool:
    cx, cy = (bbox[0] + bbox[2]) / 2, (bbox[1] + bbox[3]) / 2
    return box[0] <= cx <= box[2] and box[1] <= cy <= box[3]


def text(line: dict, anchor: str) -> str:
    x0, _, x1, _ = line["bbox"]
    w, it = style(line["fonts"])
    x = {"start": x0, "middle": (x0 + x1) / 2, "end": x1}[anchor]
    a = "" if anchor == "start" else f' text-anchor="{anchor}"'
    i = ' font-style="italic"' if it else ""
    words = line["text"].replace("\t", " ")
    return (f'<text x="{x:.2f}" y="{line["baseline"]:.2f}"{a} font-size="{line["size"]}" font-weight="{w}"{i} '
            f'fill="{line["colour"]}" textLength="{x1 - x0:.2f}" lengthAdjust="spacingAndGlyphs" '
            f'xml:space="preserve">{esc(words)}</text>')


def resolve(href: str) -> str:
    """`glossary:<id>` is this folio's term, at the IRI base dth-phc.json declares."""
    if href.startswith("glossary:"):
        base = json.load(open(ROOT / "dth-phc.json"))["iriBase"].rstrip("/") + "/"
        return f"{base}v0/ns/glossary/dth-phc/{href[len('glossary:'):]}"
    return href


def draw(d: dict) -> str:
    art = json.load(open(ROOT / d["artwork"]))
    x0, y0, x1, y1 = d["source"]["region"]
    w, h = x1 - x0, y1 - y0
    lines = art["lineColours"]
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w:.2f} {h:.2f}" '
           f'width="{w * SCALE:.0f}" height="{h * SCALE:.0f}" font-family="{FONT}" role="img" '
           f'aria-label="{esc(d["title"])}">\n<title>{esc(d["title"])}</title>\n<g class="artwork">']
    for p in art["paths"]:
        attrs = " ".join(f'{k}="{esc(v)}"' for k, v in p.items() if k != "d")
        out.append(f'<path {attrs} d="{p["d"]}"/>')
    out.append("</g>\n")
    used = set()
    for part in d["parts"]:
        mine = [i for i, l in enumerate(lines) if inside(l["bbox"], part["box"]) and i not in used]
        mine.sort(key=lambda i: (round(lines[i]["baseline"]), lines[i]["bbox"][0]))
        if not mine:
            raise SystemExit(f"{d['figure']} part {part['id']}: no printed line inside {part['box']}")
        printed = norm(" ".join(lines[i]["text"] for i in mine))
        if printed != norm(part["words"]):
            raise SystemExit(f"{d['figure']} part {part['id']}: the printed words differ from the data\n"
                             f"  printed: {printed}\n  data:    {norm(part['words'])}")
        used.update(mine)
        body = "".join(text(lines[i], part.get("anchor", "start")) for i in mine)
        title = f"<title>{esc(part.get('title', norm(part['words'])))}</title>"
        if part.get("href"):
            body = f'<a href="{esc(resolve(part["href"]))}" target="_top">{title}{body}</a>'
        out.append(f'<g class="{esc(part["role"])}" data-part="{esc(part["id"])}">{body}</g>\n')
    left = [lines[i]["text"] for i in range(len(lines)) if i not in used]
    if left:
        raise SystemExit(f"{d['figure']}: printed lines no part holds: {left}")
    out.append("</svg>\n")
    return "".join(out)


def run(path: Path, check: bool) -> None:
    d = json.load(open(path))
    if d.get("$schema") != SCHEMA:
        raise SystemExit(f"{path}: not {SCHEMA}")
    svg, out = draw(d), ROOT / d["out"]
    if check:
        if not out.exists() or out.read_text() != svg:
            raise SystemExit(f"{d['out']} is stale: run scripts/figures/as_drawn.py {path.relative_to(ROOT)}")
        print(f"{d['out']}: up to date")
    else:
        out.write_text(svg)
        print(f"wrote {d['out']}")


def main() -> None:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    if "--all" in sys.argv:
        args = [str(p) for p in sorted((ROOT / "figure-data").glob("*.json"))
                if json.load(open(p)).get("$schema") == SCHEMA]
    for a in args:
        run(Path(a).resolve(), check)


if __name__ == "__main__":
    main()
