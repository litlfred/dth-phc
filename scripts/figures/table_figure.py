#!/usr/bin/env python3
"""Draw the handbook's table-shaped figures (Figs. 2, 9, 11, 13) as SVG from their table
blocks, so each word has one source: the block's markdown table. The style per figure
(column widths and colours, taken from the PDF page) is in STYLES below; the words are
never here.

What a block holds and how it is drawn:
- lines before the table (other than the "Fig. N" caption line) are drawn above it;
- the table: header row, then body rows; `<br>` breaks a cell, `•` and `»` start bullets,
  `*italic*` and `**bold**` keep their style; `[text](url "note")` is a link whose
  note shows on hover;
- lines after the table (the "Source: ..." line) are drawn below it.

Usage: table_figure.py [--check] [fig ...]   (default: every figure in STYLES)
"""
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
FOLIO = ROOT / "folio/dth-phc"
FONT = "'Source Sans Pro','Source Sans 3','Open Sans','Segoe UI',Helvetica,Arial,sans-serif"
INK, PAGE = "#1A1A1A", "#E6E7E8"

STYLES = {
    "2": {
        "table": "ch01-introduction/t-ch01-fig-2.md", "out": "media/fig-2-who-2019-recommendation-8.svg",
        "title": "Fig. 2. The 2019 WHO guideline: recommendations on digital interventions for health system strengthening",
        "widths": [170, 180, 430], "head_fill": "#0B8FD2", "head_ink": "#FFFFFF", "head_size": 16,
        "fills": [["#C3C27A", "#EEEEDC", "#FFFFFF"]], "inks": ["#1A1A1A", "#1B4F72", "#1A1A1A"],
        "sizes": [18, 18, 15.5], "grid": "#FFFFFF",
    },
    "9": {
        "table": "ch03-user-requirements/t-ch03-fig-9.md", "out": "media/fig-9-fp-business-process-matrix.svg",
        "title": "Fig. 9. Example business process matrix from family planning DAK",
        "widths": [28, 92, 112, 132, 222, 300], "head_fill": "#FAC98C", "head_ink": "#1A1A1A", "head_size": 14.5,
        "first_row_fill": "#FDE1C0", "fills": [["#FFFFFF"] * 6, ["#DCDDDE"] * 6], "sizes": [13.5] * 6,
        "grid": "#2B9BD8",
    },
    "11": {
        "table": "ch03-user-requirements/t-ch03-fig-11.md", "out": "media/fig-11-workflow-a-notes.svg",
        "title": "Fig. 11. Notes and annotations for Workflow A: Registration business process",
        "widths": [250, 640], "head_fill": "#FFFFFF", "head_ink": "#0B8FD2", "head_size": 14.5,
        "fills": [["#FFFFFF", "#FFFFFF"]], "sizes": [13.5, 13.5], "grid": "#C9CED6", "lead_ink": "#0B8FD2",
    },
    "13": {
        "table": "ch03-user-requirements/t-ch03-fig-13.md", "out": "media/fig-13-hiv-decision-logic-matrix.svg",
        "title": "Fig. 13. Example decision-support logic matrix from DAK for HIV",
        "widths": [150, 82, 118, 540], "head_fill": "#E8263F", "head_ink": "#FFFFFF", "head_size": 14,
        "fills": [["#FFFFFF"] * 4], "sizes": [13] * 4, "grid": "#9A9EA6",
    },
}
PAD_X, PAD_Y, LINE = 9, 10, 1.3


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def runs(text: str, href: str = "") -> list[tuple[str, bool, bool, str]]:
    """Split markdown into (text, bold, italic, link) runs; [text](url) becomes a link."""
    out = []
    for m in re.finditer(r'\[([^\]]+)\]\(([^)\s]+)(?: "([^"]*)")?\)|\*\*(.+?)\*\*|\*(.+?)\*|([^*\[]+|[*\[])', text):
        if m.group(1) is not None:
            out += runs(m.group(1), m.group(2) + ("\n" + m.group(3) if m.group(3) else ""))
        elif m.group(4) is not None:
            out += [(t, True, i, h) for t, _, i, h in runs(m.group(4), href)]
        elif m.group(5) is not None:
            out += [(t, b, True, h) for t, b, _, h in runs(m.group(5), href)]
        else:
            out.append((m.group(6), False, False, href))
    return out


def wrap(text: str, width: float, size: float) -> list:
    """Wrap styled text to width. A line is a list of words; a word is a list of styled pieces."""
    words, cur, space = [], [], True
    for t, b, i, h in runs(text):
        for tok in re.split(r"(\s+)", t):
            if not tok:
                continue
            if tok.isspace():
                space = True
                continue
            if space or not cur:
                cur = []
                words.append(cur)
            cur.append((tok, b, i, h))
            space = False
    limit = width / (0.52 * size)
    lines, line, n = [], [], 0.0
    for w in words:
        wl = sum(len(t) * (1.08 if b else 1.0) for t, b, _, _ in w)
        if line and n + 1 + wl > limit:
            lines.append(line)
            line, n = [], 0.0
        line.append(w)
        n += (1 if n else 0) + wl
    if line:
        lines.append(line)
    return lines


def tspans(line) -> str:
    """One line of styled words as tspans; linked words are wrapped in <a> and underlined."""
    out, prev = [], ""
    for k, word in enumerate(line):
        for j, (t, b, i, h) in enumerate(word):
            lead = " " if k and not j else ""
            attrs = (' font-weight="700"' if b else "") + (' font-style="italic"' if i else "")
            if h:
                if lead and prev != h:            # a space before a link is not part of it
                    out.append(f"<tspan>{lead}</tspan>")
                    lead = ""
                url, _, note = h.partition("\n")     # a link title becomes a hover note
                tip = f"<title>{esc(note)}</title>" if note else ""
                out.append(f'<a href="{esc(url)}">{tip}<tspan{attrs} text-decoration="underline">{esc(lead + t)}</tspan></a>')
            else:
                out.append(f"<tspan{attrs}>{esc(lead + t)}</tspan>")
            prev = h
    return "".join(out)


def cell_lines(cell: str, width: float, size: float) -> list[tuple[str, list]]:
    """[(bullet, styled line)] for a cell; bullet is '•', '»' or ''."""
    out = []
    for part in cell.split("<br>"):
        part = part.strip()
        bullet = ""
        m = re.match(r"^([•»])\s*(.*)$", part)
        if m:
            bullet, part = m.group(1), m.group(2)
        for k, l in enumerate(wrap(part, width - (14 if bullet else 0), size)):
            out.append((bullet if k == 0 else (" " if bullet else ""), l))
    return out


def read_block(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    first = next(k for k, l in enumerate(lines) if l.startswith("|"))
    last = max(k for k, l in enumerate(lines) if l.startswith("|"))
    split = lambda l: [c.strip() for c in l.strip().strip("|").split(" | ")]
    before = [l.strip() for l in lines[:first] if l.strip() and not re.match(r"^Fig\.\s*\d+", l.strip())]
    after = [l.strip() for l in lines[last + 1:] if l.strip()]
    return before, split(lines[first]), [split(l) for l in lines[first + 2:last + 1]], after


def draw(fig: str) -> tuple[Path, str]:
    st = STYLES[fig]
    before, header, rows, after = read_block(FOLIO / st["table"])
    widths = st["widths"]
    if len(header) != len(widths):
        sys.exit(f"Fig. {fig}: {len(header)} columns in the table block, {len(widths)} in STYLES")
    W = sum(widths) + 40
    x0 = 20
    out, y = [], 20
    a = out.append
    for p in before:                                    # lead text above the table
        size = 15 if p.startswith("**") and p.endswith("**") else 13.5
        ink = st.get("lead_ink", INK) if size == 15 else INK
        for l in wrap(p, W - 40, size):
            y += size * LINE
            a(f'<text x="{x0}" y="{y}" font-size="{size}" fill="{ink}">{tspans(l)}</text>\n')
        y += 8
    if before:
        y += 6
    xs = [x0]
    for w in widths:
        xs.append(xs[-1] + w)

    def row(cells, fills, inks, sizes, bold=False, italic=False):
        nonlocal y
        laid = [cell_lines(f"**{c}**" if bold and c else (f"*{c}*" if italic and c and not c.startswith("*") else c),
                           w - 2 * PAD_X, s) for c, w, s in zip(cells, widths, sizes)]
        h = max(len(l) * s * LINE for l, s in zip(laid, sizes)) + 2 * PAD_Y
        for k, (lines, s) in enumerate(zip(laid, sizes)):
            a(f'<rect x="{xs[k]}" y="{y}" width="{widths[k]}" height="{h}" fill="{fills[k]}" stroke="{st["grid"]}" stroke-width="1"/>\n')
            ty = y + PAD_Y + s
            for bullet, l in lines:
                tx = xs[k] + PAD_X
                if bullet.strip():
                    a(f'<text x="{tx}" y="{ty}" font-size="{s}" fill="{inks[k]}">{esc(bullet)}</text>')
                if bullet:
                    tx += 14
                a(f'<text x="{tx}" y="{ty}" font-size="{s}" fill="{inks[k]}">{tspans(l)}</text>\n')
                ty += s * LINE
        y += h

    n = len(widths)
    row(header, [st["head_fill"]] * n, [st["head_ink"]] * n, [st["head_size"]] * n, bold=True)
    inks = st.get("inks", [INK] * n)
    for r, cells in enumerate(rows):
        if r == 0 and "first_row_fill" in st:
            row(cells, [st["first_row_fill"]] * n, inks, st["sizes"])
            continue
        fills = st["fills"][r % len(st["fills"])]
        row(cells, fills, inks, st["sizes"])
    y += 8
    for p in after:                                     # the source line
        for l in wrap(p, W - 40, 13):
            y += 13 * LINE
            a(f'<text x="{x0}" y="{y}" font-size="13" fill="{INK}">{tspans(l)}</text>\n')
    height = y + 18
    head = [
        '<?xml version="1.0" encoding="UTF-8"?>\n',
        f"<!-- Generated by scripts/figures/table_figure.py from folio/dth-phc/{st['table']}. "
        "Do not edit; re-run the script. -->\n",
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {height:.0f}" width="{W}" height="{height:.0f}" '
        f'font-family="{FONT}" role="img" aria-labelledby="t">\n',
        f'<title id="t">{esc(st["title"])}</title>\n',
        f'<rect width="{W}" height="{height:.0f}" fill="{PAGE}"/>\n',
    ]
    return FOLIO / st["out"], "".join(head + out) + "</svg>\n"


def main() -> None:
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    check = "--check" in sys.argv
    bad = False
    for fig in args or list(STYLES):
        path, svg = draw(fig)
        rel = path.relative_to(ROOT)
        if check:
            if not path.exists() or path.read_text(encoding="utf-8") != svg:
                print(f"{rel} is out of date: run scripts/figures/table_figure.py {fig}")
                bad = True
            else:
                print(f"{rel} is up to date")
        else:
            path.write_text(svg, encoding="utf-8")
            print(f"wrote {rel}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
