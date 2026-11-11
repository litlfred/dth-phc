#!/usr/bin/env python3
"""Write folio/dth-phc/media/fig-1-paper-to-digital.svg: Fig. 1 of the PHC handbook
("From paper to digital: a transformational journey"), drawn from data.

Two sources, each word in one place:
- figure-data/fig-1-paper-to-digital.json: the staircase (four stages, the step labels
  between them, the two axes) and each stage's glossary term;
- the table block folio/dth-phc/ch01-introduction/t-ch01-fig-1.md: the five comparison
  rows (Definition, Examples, Benefits, Challenges, Dependencies) under the staircase.

Positions follow the PDF page 15 drawing (who-iris vector-labels.json), scaled by 2.
Every label is SVG text; each stage heading and column header links to its glossary term.

Usage: fig1_paper_to_digital.py [--check]
  --check  exit 1 if the committed SVG differs from what the sources draw.
"""
import json
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "figure-data/fig-1-paper-to-digital.json"
OUT = ROOT / "folio/dth-phc/media/fig-1-paper-to-digital.svg"

INK, NAVY, BLUE, PAGE = "#1A1A1A", "#16294D", "#1A8FD6", "#E6E7E8"
FONT = "'Source Sans Pro','Source Sans 3','Open Sans','Segoe UI',Helvetica,Arial,sans-serif"
W = 960
FS, LH = 13.5, 16.5        # table text size and line height
CHAR = 0.53 * FS         # average glyph width used for wrapping


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def read_rows(md_path: Path, columns: list[str]) -> list[tuple[str, dict[str, list[str]]]]:
    """Read the comparison rows from the table block: [(row label, {column: [items]})]."""
    lines = [l for l in md_path.read_text(encoding="utf-8").splitlines() if l.startswith("|")]
    header = [c.strip() for c in lines[0].strip("|").split("|")]
    if header[1:] != columns:
        sys.exit(f"{md_path}: columns {header[1:]} do not match the figure's stages {columns}")
    rows = []
    for line in lines[2:]:
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        label = re.sub(r"\*\*(.*)\*\*", r"\1", cells[0])
        items = {}
        for col, cell in zip(columns, cells[1:]):
            items[col] = [re.sub(r"^•\s*", "", part).strip() for part in cell.split("<br>")]
        bullets = any(cell.startswith("•") for cell in cells[1:])
        rows.append((label, items, bullets))
    return rows


def wrap(text: str, width: float) -> list[str]:
    limit = max(8, int(width / CHAR))
    out, cur = [], ""
    for word in text.split():
        if cur and len(cur) + 1 + len(word) > limit:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    if cur:
        out.append(cur)
    return out


def icon(kind: str, x: float, y: float, s: float) -> str:
    """A plain white pictogram in an s-by-s stage box (the original's icons are artwork)."""
    c = 'fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"'
    m = s * 0.25
    x0, y0, x1, y1 = x + m, y + m, x + s - m, y + s - m
    if kind == "document":
        return (f'<path d="M{x0} {y0}H{x1 - 10}L{x1} {y0 + 10}V{y1}H{x0}Z" {c}/>'
                + "".join(f'<path d="M{x0 + 7} {y0 + 14 + i * 8}H{x1 - 7}" {c}/>' for i in range(3)))
    if kind == "scan":
        k = 9
        corners = (f'M{x0 - 6} {y0 - 6 + k}V{y0 - 6}H{x0 - 6 + k} M{x1 + 6 - k} {y0 - 6}H{x1 + 6}V{y0 - 6 + k} '
                   f'M{x1 + 6} {y1 + 6 - k}V{y1 + 6}H{x1 + 6 - k} M{x0 - 6 + k} {y1 + 6}H{x0 - 6}V{y1 + 6 - k}')
        return (f'<path d="{corners}" {c}/><rect x="{x0 + 5}" y="{y0 + 2}" width="{x1 - x0 - 10}" height="{y1 - y0 - 4}" {c}/>'
                + "".join(f'<path d="M{x0 + 10 + i * 6} {y1 - 8}V{y1 - 14 - i * 4}" {c}/>' for i in range(3)))
    if kind == "network":
        cx = (x0 + x1) / 2
        return (f'<rect x="{cx - 12}" y="{y0}" width="24" height="14" rx="4" {c}/>'
                f'<path d="M{cx} {y0 + 14}V{y0 + 22} M{x0 + 6} {y0 + 30}V{y0 + 22}H{x1 - 6}V{y0 + 30}" {c}/>'
                f'<rect x="{x0 - 2}" y="{y0 + 30}" width="16" height="11" rx="2" {c}/>'
                f'<rect x="{x1 - 14}" y="{y0 + 30}" width="16" height="11" rx="2" {c}/>')
    # hub: a gear-like circle with spokes out to nodes
    cx, cy, r = x0 + 12, (y0 + y1) / 2, 12
    spokes = "".join(
        f'<path d="M{cx + r} {cy + dy}H{x1 - 6}"  {c}/><circle cx="{x1 - 2}" cy="{cy + dy}" r="3.5" {c}/>'
        for dy in (-12, 0, 12))
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" {c}/><circle cx="{cx}" cy="{cy}" r="4" {c}/>{spokes}'


def draw(data: dict, rows: list) -> str:
    stages = data["stages"]
    out = []
    a = out.append

    # ---- staircase (PDF page 15 positions x2) ----
    box = 84
    boxes = [(92, 258), (330, 202), (562, 130), (810, 58)]       # top-left of each stage box
    pills = [(198, 252, 110, 42), (428, 192, 110, 58), (678, 108, 120, 74)]  # step labels
    # axes
    a(f'<path d="M57 400V44" stroke="{INK}" stroke-width="1.6" stroke-dasharray="1.5 3" fill="none" marker-end="url(#tip)"/>\n')
    a(f'<path d="M60 410H350 M640 410H928" stroke="{INK}" stroke-width="1.6" stroke-dasharray="1.5 3" fill="none"/>\n')
    a(f'<path d="M926 403L936 410L926 417Z" fill="{INK}"/>\n')
    y_ax = data["axes"]["y"]
    a(f'<rect x="34" y="236" width="48" height="50" fill="{PAGE}"/>\n')
    for i, t in enumerate(y_ax["label"]):
        a(f'<text x="57" y="{257 + i * 20}" text-anchor="middle" font-weight="700" font-size="17" fill="{BLUE}">{esc(t)}</text>\n')
    for i, t in enumerate(y_ax["high"]):
        a(f'<text x="63" y="{78 + i * 18}" font-size="14.5" fill="{INK}">{esc(t)}</text>\n')
    for i, t in enumerate(y_ax["low"]):
        a(f'<text x="63" y="{365 + i * 18}" font-size="14.5" fill="{INK}">{esc(t)}</text>\n')
    a(f'<text x="495" y="416" text-anchor="middle" font-weight="700" font-size="17" fill="{BLUE}">{esc(data["axes"]["x"]["label"])}</text>\n')

    # connectors: out of a box's right side, along to the pill, up through it, on to the next box
    for i, (px, py, pw, ph) in enumerate(pills):
        bx, by = boxes[i]
        nx, ny = boxes[i + 1]
        mid = px + pw / 2
        a(f'<path d="M{bx + box} {by + box - 18}H{mid}V{py + ph}" fill="none" stroke="{NAVY}" stroke-width="1.6"/>\n')
        a(f'<path d="M{mid} {py}V{ny + 30}H{nx - 6}" fill="none" stroke="{NAVY}" stroke-width="1.6" marker-end="url(#arrow)"/>\n')
    for i, s in enumerate(stages[1:]):
        px, py, pw, ph = pills[i]
        a(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="{min(ph / 2, 20)}" fill="{NAVY}"/>\n')
        n = len(s["step"])
        for j, t in enumerate(s["step"]):
            ty = py + ph / 2 + (j - (n - 1) / 2) * 16 + 5
            a(f'<text x="{px + pw / 2}" y="{ty}" text-anchor="middle" font-size="14.5" fill="#FFFFFF">{esc(t)}</text>\n')
    for s, (bx, by) in zip(stages, boxes):
        open_a = f'<a href="{esc(s["glossary"])}">' if s.get("glossary") else ""
        close_a = "</a>" if open_a else ""
        a(f'<g id="stage-{s["id"]}">{open_a}\n')
        a(f'<rect x="{bx}" y="{by}" width="{box}" height="{box}" rx="8" fill="{s["colour"]}"/>\n')
        a(icon(s["icon"], bx, by, box) + "\n")
        n = len(s["heading"])
        for j, t in enumerate(s["heading"]):
            a(f'<text x="{bx + box / 2}" y="{by - 10 - (n - 1 - j) * 18}" text-anchor="middle" font-weight="700" '
              f'font-size="17" fill="{s["colour"]}">{esc(t)}</text>\n')
        a(f"{close_a}</g>\n")

    # ---- comparison table, read from the table block ----
    lab_x, lab_w = 10, 34
    xs = [44, 237, 454, 678, 934]
    top = 428
    a(f'<g id="comparison">\n')
    for s, x0, x1 in zip(stages, xs, xs[1:]):
        open_a = f'<a href="{esc(s["glossary"])}">' if s.get("glossary") else ""
        a(f'{open_a}<rect x="{x0}" y="{top}" width="{x1 - x0}" height="32" fill="{s["colour"]}"/>'
          f'<text x="{(x0 + x1) / 2}" y="{top + 22}" text-anchor="middle" font-weight="700" font-size="18" fill="#FFFFFF">'
          f'{esc(s["column"])}</text>{"</a>" if open_a else ""}\n')
    y = top + 32
    for label, items, bullets in rows:
        blocks = []
        for s, x0, x1 in zip(stages, xs, xs[1:]):
            lines = []
            for item in items[s["column"]]:
                wrapped = wrap(item, x1 - x0 - (36 if bullets else 24))
                lines += [(k == 0 and bullets, t) for k, t in enumerate(wrapped)]
                if bullets:
                    lines.append(None)                       # small gap between bullets
            while lines and lines[-1] is None:
                lines.pop()
            blocks.append(lines)
        text_h = max(sum(LH if l else 6 for l in b) for b in blocks)
        h = max(text_h + 22, len(label) * 9 + 30)
        a(f'<g id="row-{label.lower()}">\n')
        a(f'<rect x="{lab_x}" y="{y}" width="{lab_w}" height="{h}" fill="#EEF3F8"/>\n')
        a(f'<text transform="translate({lab_x + 23} {y + h / 2}) rotate(-90)" text-anchor="middle" font-weight="700" '
          f'font-size="17" fill="{BLUE}">{esc(label)}</text>\n')
        for s, x0, x1, lines in zip(stages, xs, xs[1:], blocks):
            a(f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="{h}" fill="{s["tint"]}"/>\n')
            ty = y + 18
            for l in lines:
                if l is None:
                    ty += 6
                    continue
                first, t = l
                tx = x0 + (24 if bullets else 16)
                if first:
                    a(f'<text x="{x0 + 10}" y="{ty}" font-size="{FS}" fill="{INK}">•</text>')
                a(f'<text x="{tx}" y="{ty}" font-size="{FS}" fill="{INK}">{esc(t)}</text>\n')
                ty += LH
        a(f'<path d="M{lab_x} {y + h}H{xs[-1]}" stroke="{BLUE}" stroke-width="1"/>\n</g>\n')
        y += h
    a("</g>\n")
    height = y + 12

    head = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        "<!-- Generated by scripts/figures/fig1_paper_to_digital.py from figure-data/fig-1-paper-to-digital.json "
        "and folio/dth-phc/ch01-introduction/t-ch01-fig-1.md. Do not edit; re-run the script. -->\n",
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height}" width="{W}" height="{height}" '
        f'font-family="{FONT}" role="img" aria-labelledby="t">\n',
        f'<title id="t">{esc(data["title"])}</title>\n',
        f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0L10 5L0 10Z" fill="{NAVY}"/></marker>'
        f'<marker id="tip" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto">'
        f'<path d="M0 0L10 5L0 10Z" fill="{INK}"/></marker></defs>\n',
        f'<rect width="{W}" height="{height}" fill="{PAGE}"/>\n',
    ]
    return "".join(head + out) + "</svg>\n"


def main() -> None:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    rows = read_rows(ROOT / data["rows"], [s["column"] for s in data["stages"]])
    svg = draw(data, rows)
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != svg:
            sys.exit(f"{OUT.relative_to(ROOT)} is out of date: run scripts/figures/fig1_paper_to_digital.py")
        print(f"{OUT.relative_to(ROOT)} is up to date")
        return
    OUT.write_text(svg, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
