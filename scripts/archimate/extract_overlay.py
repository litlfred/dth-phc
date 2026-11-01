#!/usr/bin/env python3
"""Build the dth-phc ArchiMate overlay from the PHC work once held in smart-ra#182.

Owner rule (2026-11-01 08:13Z, card Q-RA1 A): a DTH builds an overlay on the
smart-ra model and does not add to it. This script copies the overlay's views,
and every element and relationship they draw or that the folio links to, out of
a source model (the #182 branch file). Items smart-ra already has become
reference copies tagged `overlay:base` with the smart-ra IRI; the rest are
owned by dth-phc and tagged `overlay:owner`.

usage: extract_overlay.py <source model.xml> <smart-ra base model.xml>
                          <smart-ra version> <out .archimate> <folio dir>
"""
import copy, glob, re, sys, zipfile
import xml.etree.ElementTree as ET

XSI = "http://www.w3.org/2001/XMLSchema-instance"
ARC = "http://www.archimatetool.com/archimate"
ET.register_namespace("xsi", XSI)
ET.register_namespace("archimate", ARC)
T = f"{{{XSI}}}type"
VIEWS = ["Person-centred point of service (PCPOSS)", "Shared DTH Roles and Actors"]
SHARED_VIEW = "Shared DTH Roles and Actors"

src_path, base_path, base_ver, out_path, folio = sys.argv[1:6]
src = ET.parse(src_path).getroot()
base_ids = set(re.findall(r'\bid="([^"]+)"', open(base_path, encoding="utf-8").read()))

top_type, by_id = {}, {}
for top in src.findall("folder"):
    for el in top.iter("element"):
        by_id[el.get("id")] = el
        top_type[el.get("id")] = top.get("type")

views = [by_id[i] for i, e in by_id.items() if e.get(T) == "archimate:ArchimateDiagramModel" and e.get("name") in VIEWS]
assert len(views) == len(VIEWS), [v.get("name") for v in views]

want, shared = set(), set()
for v in views:
    want.add(v.get("id"))
    for n in v.iter():
        for a in ("archimateElement", "archimateRelationship"):
            if n.get(a):
                want.add(n.get(a))
                if v.get("name") == SHARED_VIEW:
                    shared.add(n.get(a))
for f in glob.glob(f"{folio}/**/*.ts", recursive=True):
    # folio links to smart-ra's own items stay smart-ra links; only the rest come here
    want |= set(re.findall(r"smart-ra/archimate/[^/]+/(?:elements|views)/([^/\"]+)\.jsonld", open(f).read())) - base_ids
# a relationship needs both ends
for i in list(want):
    e = by_id.get(i)
    if e is not None and e.get("source"):
        want |= {e.get("source"), e.get("target")}
missing = sorted(i for i in want if i not in by_id)
assert not missing, missing

model = ET.Element(f"{{{ARC}}}model", {"name": "DTH-PHC overlay on the DPI-H reference architecture",
                                       "id": "id-dthphc-overlay-0-1-0-draft-1", "version": "5.0.0"})
doc = ET.SubElement(model, "purpose")
doc.text = (f"Overlay of dth-phc on smart-ra ArchiMate {base_ver}. Elements tagged overlay:base are reference "
            "copies of smart-ra elements (the IRI names the original); elements tagged overlay:owner=dth-phc are "
            "added by this DTH and are not part of smart-ra. Built by scripts/archimate/extract_overlay.py.")
folders = {}
for top in src.findall("folder"):
    f = ET.SubElement(model, "folder", {"name": top.get("name"), "id": top.get("id"), "type": top.get("type")})
    folders[top.get("type")] = (f, ET.SubElement(f, "folder", {"name": "smart-ra (base, reference copies)",
                                                               "id": top.get("id") + "-base"}))
counts = {"owned": 0, "base": 0}
for i in sorted(want, key=lambda i: (by_id[i].get(T), by_id[i].get("name") or "", i)):
    e = copy.deepcopy(by_id[i])
    owned_f, base_f = folders[top_type[i]]
    is_base = i in base_ids
    props = [ET.Element("property", {"key": "overlay:base", "value":
              f"https://litlfred.github.io/smart-ra/archimate/{base_ver}/{'views' if e.get(T).endswith('DiagramModel') else 'elements'}/{i}.jsonld"})] \
        if is_base else [ET.Element("property", {"key": "overlay:owner", "value": "dth-phc"})]
    if not is_base and i in shared:
        props.append(ET.Element("property", {"key": "overlay:shared-candidate", "value": "shared DTH roles (dth-phc#9)"}))
    pos = next((k for k, c in enumerate(list(e)) if c.tag == "property"), len(list(e)))
    for k, p in enumerate(props):
        e.insert(pos + k, p)
    (base_f if is_base else owned_f).append(e)
    counts["base" if is_base else "owned"] += 1
for f, b in folders.values():
    if len(b) == 0:
        f.remove(b)
ET.indent(model)
xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(model, encoding="utf-8")
with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
    zi = zipfile.ZipInfo("model.xml", date_time=(1980, 1, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    z.writestr(zi, xml)
print(f"{out_path}: {counts['owned']} owned, {counts['base']} smart-ra reference copies, views {[v.get('name') for v in views]}")
