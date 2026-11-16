#!/usr/bin/env python3
"""Copy a figure's artwork (every drawing path) and its text colours out of the source PDF.

The handbook's PDF draws its figures as vectors. `pdftocairo -svg` writes the
page in PDF points; this script keeps every drawing path that lies inside the
figure's region, in drawing order and with its own fill and stroke, and the
colour of each printed line (who-iris vector-labels.json) read from the glyphs
the PDF draws for it. Text glyphs are not copied: the generator writes the
words as SVG <text> from the figure's data, checked against the printed lines.

usage: extract_pdf_artwork.py <as-drawn figure data .json>
       Reads `source.pdf`, `source.page`, `source.region`, `source.labels`;
       writes the file named by `artwork`.
usage: extract_pdf_artwork.py --pictograms <figure data .json>
       Reads `pictograms` ({file, pdf, page, tiles: {id: [x0,y0,x1,y1]}}) and
       writes, per tile, the paths drawn on it (not the tile itself), so a
       generator can place the original's pictogram in its own tile.
"""
import collections
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

SVG = "{http://www.w3.org/2000/svg}"
STYLE = ("fill", "fill-rule", "fill-opacity", "stroke", "stroke-width", "stroke-linecap",
         "stroke-linejoin", "stroke-miterlimit", "stroke-opacity", "stroke-dasharray")


def matrix(t):
    if not t:
        return (1, 0, 0, 1, 0, 0)
    m = re.match(r"matrix\(([^)]*)\)", t.strip())
    if not m:
        raise SystemExit(f"unsupported transform {t!r}")
    return tuple(float(v) for v in re.split(r"[ ,]+", m.group(1).strip()))


def mul(a, b):
    a0, a1, a2, a3, a4, a5 = a
    b0, b1, b2, b3, b4, b5 = b
    return (a0 * b0 + a2 * b1, a1 * b0 + a3 * b1, a0 * b2 + a2 * b3, a1 * b2 + a3 * b3,
            a0 * b4 + a2 * b5 + a4, a1 * b4 + a3 * b5 + a5)


def bounds(d, m):
    nums = [float(v) for v in re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", d)]
    pts = [(m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]) for x, y in zip(nums[::2], nums[1::2])]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


def fmt(m):
    return "matrix(" + ",".join(f"{v:.6g}" for v in m) + ")"

XLINK = "{http://www.w3.org/1999/xlink}href"


def colour(c):
    m = re.match(r"rgb\(([\d.]+)%, ([\d.]+)%, ([\d.]+)%\)", c or "")
    if not m:
        return c
    return "#" + "".join(f"{round(float(v) * 2.55):02X}" for v in m.groups())


def main(data_path):
    data = json.load(open(data_path))
    src = data["source"]
    x0, y0, x1, y1 = src["region"]
    with tempfile.TemporaryDirectory() as tmp:
        svg = f"{tmp}/page.svg"
        subprocess.run(["pdftocairo", "-svg", "-f", str(src["page"]), "-l", str(src["page"]), src["pdf"], svg],
                       check=True, stderr=subprocess.DEVNULL)
        root = ET.parse(svg).getroot()
    paths, glyphs = [], []

    def walk(node, m, fill):
        for ch in node:
            if ch.tag == SVG + "defs":
                continue
            cm = mul(m, matrix(ch.get("transform")))
            f = ch.get("fill", fill)
            if ch.tag == SVG + "g":
                walk(ch, cm, f)
            elif ch.tag == SVG + "use":
                x, y = float(ch.get("x", 0)), float(ch.get("y", 0))
                glyphs.append((cm[0] * x + cm[2] * y + cm[4], cm[1] * x + cm[3] * y + cm[5], colour(f)))
            elif ch.tag == SVG + "path":
                b = bounds(ch.get("d"), cm)
                if b[0] >= x0 - 1 and b[1] >= y0 - 1 and b[2] <= x1 + 1 and b[3] <= y1 + 1:
                    p = {a: ch.get(a) for a in STYLE if ch.get(a) is not None}
                    for a in ("fill", "stroke"):
                        if a in p:
                            p[a] = colour(p[a])
                    p["d"] = ch.get("d").strip()
                    if cm != (1, 0, 0, 1, 0, 0):
                        p["transform"] = fmt(cm)
                    paths.append(p)

    walk(root, (1, 0, 0, 1, 0, 0), None)
    page = next(p for p in json.load(open(src["labels"]))["pages"] if p.get("page") == src["page"])
    lines = []
    for l in page["labels"]:
        a, b, c, d = l["bbox"]
        if not (a >= x0 - 1 and b >= y0 - 1 and c <= x1 + 1 and d <= y1 + 1):
            continue
        # the line's own glyphs: bboxes of adjacent lines overlap, so keep the
        # glyphs whose baseline is near where this line's baseline must be
        expect = b + 0.76 * (d - b)
        mine = [g for g in glyphs if a - 0.5 <= g[0] <= c + 0.5 and abs(g[1] - expect) <= 0.2 * (d - b)]
        if not mine:
            raise SystemExit(f"no glyphs found for printed line {l['text']!r}")
        ys = collections.Counter(round(g[1], 2) for g in mine)
        first = min(mine, key=lambda g: g[0])
        lines.append({"text": l["text"], "bbox": l["bbox"], "fonts": l["fonts"], "size": l["sizes"][0],
                      "baseline": ys.most_common(1)[0][0], "colour": first[2]})
    out = {
        "$schema": "pdf-artwork/v1",
        "$comment": f"The PDF's own drawing paths inside the figure's region and the colour of each printed line, copied by scripts/figures/extract_pdf_artwork.py {data_path}. Not hand-edited.",
        "source": {"pdf": src["pdf"], "page": src["page"], "region": src["region"], "units": "PDF points on the page"},
        "paths": paths,
        "lineColours": lines,
    }
    with open(data["artwork"], "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{data['artwork']}: {len(paths)} paths, {len(lines)} printed lines")


def page_paths(pdf, page):
    """Every drawing path on a PDF page, with its bounds and its transform."""
    with tempfile.TemporaryDirectory() as tmp:
        svg = f"{tmp}/page.svg"
        subprocess.run(["pdftocairo", "-svg", "-f", str(page), "-l", str(page), pdf, svg], check=True,
                       stderr=subprocess.DEVNULL)
        root = ET.parse(svg).getroot()
    out = []

    def walk(node, m):
        for ch in node:
            if ch.tag == SVG + "defs":
                continue
            cm = mul(m, matrix(ch.get("transform")))
            if ch.tag == SVG + "g":
                walk(ch, cm)
            elif ch.tag == SVG + "path":
                p = {a: ch.get(a) for a in STYLE if ch.get(a) is not None}
                for a in ("fill", "stroke"):
                    if a in p:
                        p[a] = colour(p[a])
                p["d"] = ch.get("d").strip()
                if cm != (1, 0, 0, 1, 0, 0):
                    p["transform"] = fmt(cm)
                out.append((bounds(ch.get("d"), cm), p))

    walk(root, (1, 0, 0, 1, 0, 0))
    return out


def pictograms(data_path):
    spec = json.load(open(data_path))["pictograms"]
    paths = page_paths(spec["pdf"], spec["page"])
    out = {"$schema": "pictograms/v1",
           "$comment": f"The pictograms the PDF draws on each tile, copied by scripts/figures/extract_pdf_artwork.py --pictograms {data_path}. Not hand-edited.",
           "source": {"pdf": spec["pdf"], "page": spec["page"], "units": "PDF points on the page"},
           "pictograms": {}}
    for k, (x0, y0, x1, y1) in spec["tiles"].items():
        tile = [p for b, p in paths if max(abs(b[0] - x0), abs(b[1] - y0), abs(b[2] - x1), abs(b[3] - y1)) <= 1]
        mine = [p for b, p in paths if b[0] >= x0 - 0.5 and b[1] >= y0 - 0.5 and b[2] <= x1 + 0.5 and b[3] <= y1 + 0.5
                and p not in tile]
        if not tile or not mine:
            raise SystemExit(f"{k}: no tile or no pictogram at {[x0, y0, x1, y1]}")
        out["pictograms"][k] = {"box": [x0, y0, x1, y1], "tile": tile[0].get("fill"), "paths": mine}
    with open(spec["file"], "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"{spec['file']}: " + ", ".join(f"{k} {len(v['paths'])} paths" for k, v in out["pictograms"].items()))


if __name__ == "__main__":
    if sys.argv[1] == "--pictograms":
        pictograms(sys.argv[2])
    else:
        main(*sys.argv[1:])
