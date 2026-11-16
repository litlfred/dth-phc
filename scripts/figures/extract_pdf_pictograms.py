#!/usr/bin/env python3
"""Copy a figure's pictograms out of the source PDF's own vector paths.

figure-rebuild ("pictograms come from the original, traced, not redrawn"):
the handbook's PDF draws every pictogram as vector paths, so they need no
tracing at all. `pdftocairo -svg` writes the page as SVG in PDF points; this
script keeps every drawing path (not the text glyphs) whose bounds fall inside
a pictogram's box, and writes them, with their own fill and stroke, to a
`pictograms/v1` JSON file next to the model. The boxes come from
the regions file (PDF points on the page).

usage: extract_pdf_pictograms.py <as-drawn figure data .json>
       Reads `source.pdf`, `source.page`, `shapes` (each a path whose own
       bounds are `box`, within 1 pt) and `items[].icon` (every path inside the
       box), and writes the file the data names in `pictograms`.

The PDF and pdftocairo are only needed to (re)extract; the generators read
the JSON it writes.
"""
import json, re, subprocess, sys, tempfile
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


def main(data_path):
    data = json.load(open(data_path))
    spec = {"pdf": data["source"]["pdf"], "page": data["source"]["page"], "regions": {}}
    for k, v in data["shapes"].items():
        spec["regions"][k] = {"box": v["box"], "exact": True}
    for it in data["items"]:
        if "icon" in it:
            spec["regions"][it["element"]] = {"box": it["icon"]}
    out_path = data["pictograms"]
    with tempfile.TemporaryDirectory() as tmp:
        svg = f"{tmp}/page.svg"
        subprocess.run(["pdftocairo", "-svg", "-f", str(spec["page"]), "-l", str(spec["page"]), spec["pdf"], svg],
                       check=True, stderr=subprocess.DEVNULL)
        root = ET.parse(svg).getroot()
    found = {k: [] for k in spec["regions"]}

    def walk(node, m):
        for ch in node:
            if ch.tag == SVG + "defs":
                continue
            cm = mul(m, matrix(ch.get("transform")))
            if ch.tag == SVG + "g":
                walk(ch, cm)
            elif ch.tag == SVG + "path":
                b = bounds(ch.get("d"), cm)
                for k, r in spec["regions"].items():
                    x0, y0, x1, y1 = r["box"]
                    if r.get("exact"):
                        hit = max(abs(b[0] - x0), abs(b[1] - y0), abs(b[2] - x1), abs(b[3] - y1)) <= 1
                    else:
                        hit = b[0] >= x0 and b[1] >= y0 and b[2] <= x1 and b[3] <= y1
                    if hit:
                        p = {a: ch.get(a) for a in STYLE if ch.get(a) is not None}
                        p["d"] = ch.get("d").strip()
                        if cm != (1, 0, 0, 1, 0, 0):
                            p["transform"] = fmt(cm)
                        found[k].append(p)
                        break

    walk(root, (1, 0, 0, 1, 0, 0))
    out = {
        "$schema": "pictograms/v1",
        "$comment": f"The PDF's own vector paths, copied by scripts/figures/extract_pdf_pictograms.py {data_path}; keyed by the element (pictograms) or shape id. Not hand-edited.",
        "source": {"pdf": spec["pdf"], "page": spec["page"], "units": "PDF points on the page",
                   "method": "pdftocairo -svg; drawing paths inside each box (scripts/figures/extract_pdf_pictograms.py)"},
        "pictograms": {},
    }
    for k, r in spec["regions"].items():
        if not found[k]:
            raise SystemExit(f"{k}: no paths inside {r['box']}")
        out["pictograms"][k] = {"box": r["box"], "paths": found[k]}
    with open(out_path, "w") as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write("\n")
    for k in found:
        print(f"{k}: {len(found[k])} paths")


if __name__ == "__main__":
    main(*sys.argv[1:])
