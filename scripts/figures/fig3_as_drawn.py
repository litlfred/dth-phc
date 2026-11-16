#!/usr/bin/env python3
"""Write folio/dth-phc/media/fig-3-phc-digital-ecosystem-as-drawn.svg: Fig. 3 of the
PHC handbook ("Primary health care digital ecosystem") as the original draws it,
generated from the overlay's ArchiMate view.

figure-rebuild, "a pictured figure keeps its pictures": the ArchiMate view
"PHC digital ecosystem (Fig. 3)" in archimate/0.1.0-draft.1/dth-phc-overlay.archimate
stays the source of record and is drawn by archimate-pages in ArchiMate notation.
This script draws the same elements the way the handbook does:

- the words are the model's (each element's name, and its documentation for a
  component), and the script fails unless they equal the lines printed on PDF
  page 17 (who-iris vector-labels.json), which give the line breaks and places;
- the layers, the frame and every pictogram are the PDF's own vector paths
  (archimate/fig-3-pictograms.json, written by extract_pdf_pictograms.py);
- every element is a link to its page in the overlay's ArchiMate site, and the
  note links to the view.

Usage: fig3_as_drawn.py [--check]
"""
import json
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "figure-data/fig-3-as-drawn.json"
OUT = ROOT / "folio/dth-phc/media/fig-3-phc-digital-ecosystem-as-drawn.svg"
FONT = "'Source Sans Pro','Source Sans 3','Open Sans','Segoe UI',Helvetica,Arial,sans-serif"
XSI_TYPE = "{http://www.w3.org/2001/XMLSchema-instance}type"
SCALE = 2  # the crop vfig-p017.png is drawn at 2 px per PDF point; so is this
BASELINE = {"Black": 1.06, "Regular": 1.007}  # baseline below the label's top, in font sizes (measured on page 17)


def esc(s: str) -> str:
    return escape(s, {'"': "&quot;"})


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().casefold()


def model_elements(path: Path) -> dict:
    root = ET.fromstring(zipfile.ZipFile(path).read("model.xml"))
    out = {}
    for e in root.iter("element"):
        doc = e.find("documentation")
        out[e.get("id")] = {"type": e.get(XSI_TYPE, "").split(":")[-1], "name": e.get("name") or "",
                            "documentation": doc.text if doc is not None and doc.text else ""}
    return out


def page_labels(path: Path, page: int) -> list:
    pages = json.load(open(path))["pages"]
    return next(p for p in pages if p.get("page") == page)["labels"]


def inside(label: dict, box: list) -> bool:
    x0, y0, x1, y1 = label["bbox"]
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    return box[0] <= cx <= box[2] and box[1] <= cy <= box[3]


def lines_in(labels: list, box: list) -> list:
    got = [l for l in labels if inside(l, box)]
    return sorted(got, key=lambda l: (round(l["bbox"][1], 0), l["bbox"][0]))


def expected(item: dict, el: dict, view: dict) -> tuple:
    """The model's words for an item, and how the printed lines must match them."""
    m = item["match"]
    if m == "equal":
        return el["name"], "equal"
    if m == "name-and-documentation":
        return el["name"] + " " + el["documentation"], "equal"
    if m == "documentation-prefix":
        return el["documentation"], "prefix"
    if m == "view-documentation-suffix":
        return view["documentation"], "suffix"
    raise SystemExit(f"unknown match {m!r}")


def check_words(what: str, printed: str, model: str, how: str) -> None:
    p, w = norm(printed), norm(model)
    ok = {"equal": p == w, "prefix": w.startswith(p), "suffix": w.endswith(p)}[how]
    if not ok:
        raise SystemExit(f"{what}: the printed words do not match the model ({how})\n  printed: {printed}\n  model:   {model}")


def text_lines(lines: list, colour: str, centre: bool) -> str:
    out = []
    for l in lines:
        x0, y0, x1, _ = l["bbox"]
        weight = l["fonts"][0].split("-")[-1]
        size = l["sizes"][0]
        y = y0 + BASELINE.get(weight, 1.0) * size
        x, anchor = ((x0 + x1) / 2, ' text-anchor="middle"') if centre else (x0, "")
        fw = 900 if weight == "Black" else 400
        out.append(f'<text x="{x:.2f}" y="{y:.2f}"{anchor} font-size="{size}" font-weight="{fw}" fill="{colour}" '
                   f'textLength="{x1 - x0:.2f}" lengthAdjust="spacingAndGlyphs">{esc(l["text"])}</text>')
    return "".join(out)


def paths(p: dict) -> str:
    out = []
    for q in p["paths"]:
        attrs = " ".join(f'{k}="{esc(v)}"' for k, v in q.items() if k != "d")
        out.append(f'<path {attrs} d="{q["d"]}"/>')
    return "".join(out)


def draw(d: dict) -> str:
    src = d["source"]
    els = model_elements(ROOT / d["model"]["file"])
    view = els[d["model"]["view"]]
    labels = page_labels(ROOT / src["labels"], src["page"])
    pics = json.load(open(ROOT / d["pictograms"]))["pictograms"]
    iri_base = json.load(open(ROOT / "dth-phc.json"))["iriBase"].rstrip("/") + "/"
    model_iri = f"{iri_base}archimate/{d['model']['modelId']}"
    x0, y0, x1, y1 = src["region"]
    w, h = x1 - x0, y1 - y0

    def link(eid: str, body: str, title: str) -> str:
        return (f'<a href="{model_iri}/element/{eid}" target="_top"><title>{esc(title)}</title>{body}</a>')

    out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0} {y0} {w:.2f} {h:.2f}" '
           f'width="{w * SCALE:.0f}" height="{h * SCALE:.0f}" font-family="{FONT}" role="img" '
           f'aria-label="{esc(d["title"])}">\n',
           f'<title>{esc(d["title"])} (as drawn; generated from the ArchiMate view "{esc(view["name"])}")</title>\n']
    # the frame and the nested layers, each layer linking to its grouping
    out.append(paths(pics["frame"]) + "\n")
    for key in ("layer-0", "layer-1", "notch-1", "layer-2", "notch-2", "layer-3", "notch-3"):
        eid = d["shapes"][key]["element"]
        out.append(link(eid, paths(pics[key]), els[eid]["name"]) + "\n")
    used = set()
    for it in d["items"]:
        el = els[it["element"]]
        lines = lines_in(labels, it["text"])
        if not lines:
            raise SystemExit(f"{el['name']}: no printed line inside {it['text']}")
        used.update(id(l) for l in lines)
        words, how = expected(it, el, view)
        check_words(el["name"], " ".join(l["text"] for l in lines), words, how)
        body = (paths(pics[it["element"]]) if "icon" in it else "") + text_lines(lines, it["colour"], it["kind"] == "centre")
        tip = el["name"] + (f": {el['documentation']}" if el["documentation"] and it["kind"] == "component" else "")
        out.append(f'<g class="{it["kind"]}">' + link(it["element"], body, tip) + "</g>\n")
    note = d["note"]
    lines = lines_in(labels, note["text"])
    words, how = expected(note, {}, view)
    check_words("note", " ".join(l["text"] for l in lines), words, how)
    out.append(f'<a href="{model_iri}/view/{d["model"]["view"]}" target="_top"><title>{esc(view["name"])}</title>'
               + text_lines(lines, note["colour"], False) + "</a>\n")
    # every printed line in the figure is drawn, so nothing is silently dropped
    left = [l["text"] for l in labels if inside(l, src["region"]) and id(l) not in used and l not in lines]
    if left:
        raise SystemExit(f"printed lines not placed: {left}")
    out.append("</svg>\n")
    return "".join(out)


def main() -> None:
    svg = draw(json.load(open(DATA)))
    if "--check" in sys.argv:
        if not OUT.exists() or OUT.read_text() != svg:
            raise SystemExit(f"{OUT.relative_to(ROOT)} is stale: run scripts/figures/fig3_as_drawn.py")
        print(f"{OUT.relative_to(ROOT)}: up to date")
        return
    OUT.write_text(svg)
    print(f"wrote {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
