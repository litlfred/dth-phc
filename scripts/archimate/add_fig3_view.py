#!/usr/bin/env python3
"""Add the handbook's Fig. 3 (PHC digital ecosystem) to the dth-phc overlay as an ArchiMate view.

Owner card Q-PHC-R4 A (2026-11-01 10:54Z): Fig. 3 is rebuilt as an ArchiMate
view in the dth-phc overlay, not in smart-ra. Labels and descriptions are the
figure's own words (who-iris library/9789240093362-eng figures/vfig-p017.png,
page 17). Idempotent: running it again replaces what it added.

usage: add_fig3_view.py <overlay .archimate>
"""
import hashlib, sys, zipfile
import xml.etree.ElementTree as ET

XSI = "http://www.w3.org/2001/XMLSchema-instance"
ARC = "http://www.archimatetool.com/archimate"
ET.register_namespace("xsi", XSI)
ET.register_namespace("archimate", ARC)
T = f"{{{XSI}}}type"
TAG = "fig-3"
SRC = "WHO 9789240093362, Fig. 3 (p. 17)"

def iid(*parts):
    return "id-" + hashlib.md5(("dth-phc/fig-3/" + "/".join(parts)).encode()).hexdigest()

# (layer label, who it serves, [(component, description)])
LAYERS = [
    ("Defining a target population and understanding their needs", "Policy Makers", [
        ("Civil registration & vital statistics", "To provide a population profile (birth rate extent and causes of mortality)"),
        ("Disease surveillance", "Digital tools to understand population risk profile"),
    ]),
    ("Selection, design and planning of services", "Health System Decision Makers", [
        ("Dashboard", "(with geolocated data on disease prevalence, service gaps, etc) To support decision making for universal health service coverage, programme monitoring"),
        ("Management information systems", "To provide canonical record of system inputs"),
    ]),
    ("Organization and management", "Primary care providers", [
        ("Clinical job aids", "To ensure quality of clinical service delivery"),
        ("AI risk assessment", "To flag at risk patients for early intervention"),
        ("Referral & coordination", "Tools to ensure coordination between different provider types"),
        ("An electronic health record", "A longitudinal record of patient care seeking"),
    ]),
    ("Community linkages and engagement", "Community Health Workers, Care Seekers", [
        ("Patient portal", "To help support patient self care and self management"),
        ("Targeted messaging", "Chatbot, SMS, etc. to give targeted health information to patients"),
        ("CHW job aid", "To help community health workers improve coverage"),
        ("Self monitoring devices", "To support patient monitoring and self care"),
        ("Capacity building", "Video-based support and supervision to expand knowledge and skills of providers"),
    ]),
]
CENTRE = ("Centered around the needs of the care seeker",)
NOTE = ("Notes: The different information systems and digital solutions can cover more than one layer of the figure, "
        "or domain, as they are cross-cutting. However, for illustrative purposes, they have been allocated to only layer.")

path = sys.argv[1]
z = zipfile.ZipFile(path)
root = ET.fromstring(z.read("model.xml"))
folders = {f.get("type"): f for f in root.findall("folder")}

# drop anything this script added before
for f in root.iter("folder"):
    for e in list(f):
        if e.tag == "element" and any(p.get("key") == "overlay:figure" and p.get("value") == TAG for p in e.findall("property")):
            f.remove(e)

def el(folder, typ, name, eid, doc=None):
    e = ET.SubElement(folders[folder], "element", {T: f"archimate:{typ}", "name": name, "id": eid})
    if doc:
        ET.SubElement(e, "documentation").text = doc
    ET.SubElement(e, "property", {"key": "overlay:owner", "value": "dth-phc"})
    ET.SubElement(e, "property", {"key": "overlay:figure", "value": TAG})
    ET.SubElement(e, "property", {"key": "source", "value": SRC})
    return e

view = el("diagrams", "ArchimateDiagramModel", "PHC digital ecosystem (Fig. 3)", iid("view"),
          "Fig. 3. Delivering an integrated ecosystem of information systems and digital health solutions supports the PHC approach. " + NOTE)
rels = []
def place(parent, eid, x, y, w, h):
    c = ET.SubElement(parent, "child", {T: "archimate:DiagramObject", "id": eid + "-v", "archimateElement": eid})
    ET.SubElement(c, "bounds", {"x": str(x), "y": str(y), "width": str(w), "height": str(h)})
    return c

# Each layer nests inside the one before, as in the figure: the layer's
# stakeholder top left, its components in a column on the right, the next
# layer below the stakeholder. Bounds are relative to the parent box.
parent, x0, y0, w, h = view, 20, 20, 1240, 900
for li, (layer, who, comps) in enumerate(LAYERS):
    last = li == len(LAYERS) - 1
    g = el("other", "Grouping", layer, iid("layer", str(li)))
    s = el("motivation", "Stakeholder", who, iid("who", who), f"Served by the layer '{layer}' in {SRC}.")
    gv = place(parent, g.get("id"), x0, y0, w, h)
    place(gv, s.get("id"), 20, 30, 360 if last else 240, 50)
    rels.append(("Association", s.get("id"), g.get("id")))
    for ci, (cname, cdoc) in enumerate(comps):
        c = el("application", "ApplicationComponent", cname, iid("comp", cname), cdoc)
        place(gv, c.get("id"), w - 240, (90 if last else 30) + ci * 70, 220, 55)
        rels.append(("Aggregation", g.get("id"), c.get("id")))
    if last:
        centre = el("motivation", "Stakeholder", "Care seeker", iid("centre"), CENTRE[0] + f" ({SRC}).")
        place(gv, centre.get("id"), 20, 100, 130, 70)
    parent, x0, y0, w, h = gv, 20, 100, w - 280, h - 120

for typ, s, t in rels:
    r = ET.SubElement(folders["relations"], "element", {T: f"archimate:{typ}Relationship", "id": iid("rel", typ, s, t), "source": s, "target": t})
    ET.SubElement(r, "property", {"key": "overlay:owner", "value": "dth-phc"})
    ET.SubElement(r, "property", {"key": "overlay:figure", "value": TAG})

ET.indent(root)
xml = b'<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="utf-8")
with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as out:
    zi = zipfile.ZipInfo("model.xml", date_time=(1980, 1, 1, 0, 0, 0))
    zi.compress_type = zipfile.ZIP_DEFLATED
    out.writestr(zi, xml)
print(f"{path}: Fig. 3 view {view.get('id')} with {sum(len(c) for _,_,c in LAYERS)} components, {len(LAYERS)} layers")
