#!/usr/bin/env python3
"""Seed and formalize folio/dth-phc/ from who-iris/library/9789240093362-eng.

Implements Step P4 of litlfred/dth-phc#1 (§3b Narrative):
- Seeds folio/dth-phc/ from who-iris/library/9789240093362-eng across all 48
  L1 sections (Front matter, Ch 1-6, References, and Annexes 1-14).
- Formalizes Chapters 3 and 4 first (phase panels, method steps producing
  smart-base DAK components, BPMN/DMN tables, four architecture domains, four
  interoperability types, five standards categories, prototyping, build & QA),
  then Chapters 1 (PCPOSS definition, four application types, 13 DHIs
  1.1.3-4.1.3, SMART Guidelines layers L1-L5, quoted WHO 2019 digital guideline
  Recommendation 8), 2 (readiness scenarios, target users, DIIG Fig. 1.1.1
  reproduces link, four-step approach mapped to DIIG phases, software choices),
  5 (phase panel, training, UAT & test cases, deployment, maintenance),
  6 (phase panel, readiness to scale, legacy phase-out planning & execution,
  Table 5 objective indicators, monitoring, change management), and Annexes
  1-14 (Principles for Digital Development as external source, worksheets and
  templates mapped to smart-base DAK component kinds, Annex 11 DMN table shape,
  Annex 12 scheduling logic, Annex 14 HL7 FHIR components linked to
  fhir-harness and smart-base L3 kinds).
- Keeps empirical claims, statistics, benefits, tool names, and health-area
  examples as cited L1 source blocks (`meta.sourceOnly`).
- Links every block's `meta.source`, `meta.glossaryTerms`, `meta.archimate`,
  `meta.archimateElements`, and `meta.archimateViews` to
  `who-iris/library/9789240093362-eng`, `glossary/dth-phc.glossary.json`,
  `dpi-h-ra/glossary/dpi-h-ra.glossary.json`, and `dpi-h-ra`'s ArchiMate model
  (including the `Person-centred point of service (PCPOSS)` view
  `id-bcf04de52bb05c3a932bbfdd36d7ae4f` and `Shared DTH Roles and Actors` view
  `id-eac6523c694c551b968166656af2b2e6`).
"""

import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[2]
DOC = "dth-phc"
FOLIO = ROOT / "folio" / DOC
L1_ID = "9789240093362-eng"
L1_DIR = ROOT / "who-iris" / "library" / L1_ID
TITLE = "Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems"

PHC_TERM_NS = "https://litlfred.github.io/dth-phc/v0/ns/glossary/dth-phc/"
RA_TERM_NS = "https://litlfred.github.io/smart-ra/v0/ns/glossary/dpi-h-ra/"
RA_ARCHI_NS = "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.1/"

# Known ArchiMate elements in smart-ra (0.2.0 + 0.3.0-draft.1 from #133)
ARCHI_ELEMENTS = {
    # New PCPOSS elements (dth_phc.py)
    "pos-app": ("id-808925f4d2075d7b95e0651ebae00fcf", "Point-of-service application"),
    "ehr-system": ("id-a9de9d3bebca5852b7b9c55519e7ab2d", "Electronic health record system"),
    "dss": ("id-bc2b3fab70bf5e48a3b043a7245c8f5f", "Decision support system"),
    "chis": ("id-3acafd57e8cc5d4198ffcb29d39c1184", "Community-based information system"),
    "phr": ("id-9a31cf86a4685fb0ae0c460d973e2031", "Personal health record"),
    "health-worker": ("id-54d7e249c99a59c6a2085f17060de254", "Health worker"),
    "health-service-user": ("id-0b80b004c74f5b00b4a5bc56e9c06ac0", "Health service user"),
    "alerts-and-reminders": ("id-9d1f8abfb4905386b6a8ea65f421d115", "Alerts and reminders"),
    "longitudinal-tracking": ("id-74b83b6a6d8e53a99573467ad6f7ae41", "Longitudinal tracking"),
    "care-checklists": ("id-0a635958abe251829d425db426340b00", "Care checklists"),
    "clinical-screening": ("id-5890b78a30f25b1b8502a7fe0c9aac32", "Clinical screening"),
    "indicator-reporting": ("id-ab03b92d0a8355bca5ce336ab2e2bf17", "Indicator reporting"),
    # Shared DTH roles (dth_shared_roles.py)
    "public-health-authority": ("id-18bf324b7b4753e0aeff853e6bcb6adc", "Public health authority"),
    "implementing-team": ("id-95e8f300e2225113a3195b2d6c2afc9b", "Implementing team"),
    "business-analyst": ("id-b1a348e9848f50e19a46bf2226dc2f08", "Business analyst"),
    "health-informatician": ("id-8074acfb0a065da4b9b36ad88fc2a0d5", "Health informatician"),
    "user-researcher": ("id-b003f851903c557fa2b020e234e850e0", "User researcher"),
    "designer": ("id-5d55040d3ed75347b5d30553fda6f40c", "Designer"),
    "solutions-architect": ("id-ffa13a71f7575bd1ab3bf9496433cdcf", "Solutions architect"),
    "software-engineer": ("id-6f87fe9ac64b5deca8c2ed5c96641485", "Software engineer"),
    "technology-partner": ("id-dec0373effd25980b70e45e852f0ff1f", "Technology partner"),
    "me-specialist": ("id-efb44c09bbb251a4a851dbef2bfaf5a2", "Monitoring and evaluation specialist"),
    # Reused 0.2.0 elements
    "patients": ("id-a2320dbc07e6450b94f3f0f3e03bb877", "Patients"),
    "ministry-of-health": ("id-1c5c0bc9234e4282b654dbc71b9da706", "Ministry of Health"),
    "health-workers-sh": ("id-8d3dd8b68d504c2a9fe8cf414b16c127", "Health Workers"),
    "shr": ("id-f180ad44b2e94e2a9ee8523ffc900264", "Shared Health Record"),
    "shr-repo": ("id-0e6d89398fff4f20994a31b4de58e7d7", "SHR Repository"),
    "patient-level-data": ("id-71b2e11df2e348a2b9f8eee36c8e5292", "Patient-level Data"),
    "dse": ("id-539b04ae45f147258d8253ae5cb87402", "Decision Support Engine"),
    "terminology-service": ("id-3f41de2b51c24041b08243bf72b140d1", "Terminology Service"),
    "limr": ("id-c0d39bf67fe64f54b07fbeb9bf37d404", "Logical Information Model Registry"),
    "logical-models": ("id-6e06187bc1764418b58cfe3455df7481", "Logical Information Models"),
    "hwr": ("id-350840520ae44f658b6ad3b3762e382e", "DPI-H Health Workforce Registry (HWR)"),
    "facility-registry": ("id-5f6d9b9678824b37b95952735420ae8d", "Facility registry"),
    "analytics-platform": ("id-3fd92d497ca040c8a436f355c0b68770", "Analytics & Reporting Platform"),
    "client-identity": ("id-788f660553e14f0283b93c2dda3ae441", "Client Identity Management"),
    "interop-component": ("id-80856538cbd44167a37b276e38c994c3", "Interoperability Component"),
    "interop-capability": ("id-4fa548b8175c4937b46f9d11f9e974ae", "Interoperability"),
    "interop-mgmt": ("id-02200ff02be649ada1bf34a0a4d8e594", "Interoperability Management"),
    "info-mediator": ("id-3c5d846710034c4595e206e748d65e36", "DPI-F Information Mediator"),
    "security-consent": ("id-d79aa0eec0584b0792b44bca408afeb6", "DPI-F Security & Consent Module"),
    "smart-l1": ("id-5b55a8ca67864a1a91910347db193e79", "SMART Guidelines L1"),
    "adapted-smart-l1": ("id-b03a09f1177a4bf6bfd1f22c6cea1c94", "Adapted SMART Guidelines L1"),
    "smart-l2-dak": ("id-066e40fefc9e48e4b23e51d9f9bd14d2", "SMART Guidelines L2 (DAK)"),
    "adapted-smart-l2-dak": ("id-2f415a2e0d4245c19663f5821ed02a16", "Adapted SMART Guidelines L2 (DAK)"),
    "testing-platforms": ("id-7c03cebca775460c8481d8c4729b127b", "Testing Platforms"),
    "test-cases": ("id-9410790dc72a4831b7bdd40e85a8158d", "Test Cases"),
    "system-under-test": ("id-f9759d3c33a848cd81ba7cbae9fa2b99", "System Under Test"),
    "test-operator": ("id-abd2da4297944a5ca707a28a400dfb8f", "Test Operator"),
    "hmis": ("id-d626508a7dc55b1fb11bf34f57f8ddd9", "Health Management Information System"),
}

ARCHI_VIEWS = {
    "pcposs": ("id-bcf04de52bb05c3a932bbfdd36d7ae4f", "Person-centred point of service (PCPOSS)"),
    "shared-roles": ("id-eac6523c694c551b968166656af2b2e6", "Shared DTH Roles and Actors"),
    "shr": ("id-cefde7ed0dcd47d3bb214657ac3e5725", "SHR"),
    "cds": ("id-4c98f10e0a244315acddaf5257c7822e", "CDS"),
    "testing": ("id-0e97a3f6a8f545f5bd90e123c11a2545", "Testing"),
    "conformance": ("id-b44f768c54ea493c8b33499e5d2e2d33", "Conformance"),
    "components": ("id-3ad41900b17d47f78129e16d32ed2f38", "Components"),
    "interop-layer": ("id-8c5dd12b8d4e425184f6003d0513d569", "Interoperability Layer"),
    "lmir-overview": ("id-dbcfb8e417294161ac0b1614c2e18cc5", "LMIR Overview"),
    "capabilities-goals": ("id-4e6e25746e8d4398add06fcbc4fb5a4e", "Capabilities-Goals"),
}


def el_refs(*keys):
    out = []
    for k in keys:
        eid, name = ARCHI_ELEMENTS[k]
        out.append({"iri": f"{RA_ARCHI_NS}elements/{eid}.jsonld", "id": eid, "name": name})
    return out


def view_refs(*keys):
    out = []
    for k in keys:
        vid, name = ARCHI_VIEWS[k]
        out.append({"iri": f"{RA_ARCHI_NS}views/{vid}.jsonld", "id": vid, "name": name})
    return out


def term_refs(phc_ids=(), ra_ids=()):
    out = [f"{PHC_TERM_NS}{t}" for t in phc_ids]
    out.extend(f"{RA_TERM_NS}{t}" for t in ra_ids)
    return out


def read_l1_section(sec_file: str):
    path = L1_DIR / "sections" / sec_file
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n*", raw, flags=re.S)
    fm = {}
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                fm[k.strip()] = v.strip().strip('"')
        body = raw[m.end():]
    else:
        body = raw
    pages_str = fm.get("pages", "1-1")
    p_parts = [int(x) for x in pages_str.split("-") if x.strip().isdigit()]
    pdf_pages = list(range(p_parts[0], p_parts[-1] + 1)) if len(p_parts) == 2 else p_parts
    return body.splitlines(), fm, pdf_pages


def slice_lines(lines, start_1based=1, end_1based=None):
    s = max(0, start_1based - 1)
    e = len(lines) if end_1based is None else end_1based
    return "\n".join(lines[s:e]).strip() + "\n"


DOT_LEADER = re.compile(r"(?:\.\s{0,2}){6,}\s*[0-9ivxlc]*\s*$")
TERMINAL = ("." , "”", ")", ".”", ":")


def clean_front_matter(lines):
    """Turn the L1 front-matter section into readable prose.

    The L1 section is the PDF's raw text, one PDF line per line. Three things
    in it are page furniture, not content, and each was rendered as one run-on
    paragraph before this cleaner existed:
      - the cover text, printed twice (front and inside cover);
      - the printed table of contents, with dot leaders and page numbers.
        The site builds its own contents from the document's structure, and
        the L1 entry keeps the printed one in structure.json;
      - hard line wraps inside paragraphs.
    Nothing is reworded: the cleaner drops the cover repeat and the printed
    contents, and joins wrapped lines into paragraphs.
    """
    lines = [l.rstrip() for l in lines]
    # Cover text: everything before the title line that precedes the first ISBN.
    isbn = next((i for i, l in enumerate(lines) if l.startswith("ISBN")), None)
    if isbn:
        title = isbn - 1
        while title > 0 and not lines[title].strip():
            title -= 1
        lines = lines[title:]
    # Printed contents: from a "Contents" line that is followed by dot leaders.
    for i, l in enumerate(lines):
        if l.strip().lower() in ("contents", "table of contents") and any(
            DOT_LEADER.search(x) for x in lines[i + 1 : i + 8]
        ):
            lines = lines[:i]
            break
    # Running page numbers ("iii", "12") on a line of their own.
    lines = [l for l in lines if not re.fullmatch(r"\s*(?:[ivxlc]+|[0-9]+)\s*", l)]
    width = max((len(l) for l in lines), default=0)
    paras = []
    prev = ""
    for l in lines:
        t = l.strip()
        if not t:
            prev = ""
            continue
        p = prev.strip()
        new = (
            not paras
            or not prev
            or t.startswith(("ISBN", "©"))
            or p.startswith(("ISBN", "©"))
            or (p.endswith(TERMINAL) and len(prev) < 0.8 * width)
        )
        if new:
            paras.append(t)
        else:
            paras[-1] += " " + t
        prev = l
    out = []
    for x in paras:
        if x.startswith("ISBN") and out and out[-1].startswith("ISBN"):
            out[-1] += "  \n" + x
        else:
            out.append(x)
    if out:
        out[0] = "**" + out[0] + "**"
    return "\n\n".join(out) + "\n"


def make_meta(
    title: str,
    sec_file: str,
    pdf_pages: list[int],
    method: str = "l1-section-formalized",
    phc_terms=(),
    ra_terms=(),
    elements=(),
    views=(),
    **extra,
):
    sec_id = sec_file.removesuffix(".md")
    meta = {
        "title": title,
        "source": {
            "library": L1_ID,
            "section": sec_id,
            "file": f"who-iris/library/{L1_ID}/sections/{sec_file}",
            "pdfPages": pdf_pages,
            "method": method,
        },
        "glossaryTerms": term_refs(phc_terms, ra_terms),
    }
    if elements or views:
        els = el_refs(*elements)
        vws = view_refs(*views)
        meta["archimateElements"] = els
        meta["archimateViews"] = vws
        meta["archimate"] = {
            "model": "smart-ra 0.3.0-draft.1",
            "basis": "formalized from WHO 9789240093362 (dth-phc#1 §3b/§3c)",
            "elements": [{"iri": x["iri"], "name": x["name"]} for x in els],
            "views": [{"iri": x["iri"], "name": x["name"]} for x in vws],
        }
    meta.update(extra)
    return meta


def write_prose_block(ch_dir: Path, stem: str, label: str, md_text: str, meta: dict, uses=(), defines=()):
    (ch_dir / f"{stem}.md").write_text(md_text.strip() + "\n", encoding="utf-8")
    defines_line = f"  defines: {json.dumps(list(defines))},\n" if defines else ""
    ts = (
        'import { prose } from "../../schema/builders";\n\n'
        "export default prose({\n"
        f"  label: {json.dumps(label)},\n"
        f"  title: {json.dumps(meta['title'])},\n"
        f"  uses: {json.dumps(list(uses))},\n"
        f"{defines_line}"
        f"  meta: {json.dumps(meta, ensure_ascii=False)},\n"
        "});\n"
    )
    (ch_dir / f"{stem}.ts").write_text(ts, encoding="utf-8")
    return stem


def write_table_block(ch_dir: Path, stem: str, label: str, caption: str, md_text: str, meta: dict, uses=()):
    (ch_dir / f"{stem}.md").write_text(md_text.strip() + "\n", encoding="utf-8")
    ts = (
        'import { table } from "../../schema/builders";\n\n'
        "export default table({\n"
        f"  label: {json.dumps(label)},\n"
        f"  title: {json.dumps(meta['title'])},\n"
        f"  caption: {json.dumps(caption)},\n"
        f"  uses: {json.dumps(list(uses))},\n"
        f"  meta: {json.dumps(meta, ensure_ascii=False)},\n"
        "});\n"
    )
    (ch_dir / f"{stem}.ts").write_text(ts, encoding="utf-8")
    return stem


def write_figure_block(ch_dir: Path, stem: str, label: str, file_rel: str, caption: str, page: int, md_text: str, meta: dict, uses=()):
    (ch_dir / f"{stem}.md").write_text(md_text.strip() + "\n", encoding="utf-8")
    ts = (
        'import { figure } from "../../schema/builders";\n\n'
        "export default figure({\n"
        f"  label: {json.dumps(label)},\n"
        f"  title: {json.dumps(meta['title'])},\n"
        f"  file: {json.dumps(file_rel)},\n"
        f"  caption: {json.dumps(caption)},\n"
        f"  page: {page},\n"
        f"  uses: {json.dumps(list(uses))},\n"
        f"  meta: {json.dumps(meta, ensure_ascii=False)},\n"
        "});\n"
    )
    (ch_dir / f"{stem}.ts").write_text(ts, encoding="utf-8")
    return stem


def write_recommendation_block(ch_dir: Path, stem: str, label: str, md_text: str, meta: dict, strength: dict, uses=()):
    (ch_dir / f"{stem}.md").write_text(md_text.strip() + "\n", encoding="utf-8")
    ts = (
        'import { recommendation } from "../../schema/builders";\n\n'
        "export default recommendation({\n"
        f"  label: {json.dumps(label)},\n"
        f"  title: {json.dumps(meta['title'])},\n"
        f"  strength: {json.dumps(strength, ensure_ascii=False)},\n"
        f"  uses: {json.dumps(list(uses))},\n"
        f"  meta: {json.dumps(meta, ensure_ascii=False)},\n"
        "});\n"
    )
    (ch_dir / f"{stem}.ts").write_text(ts, encoding="utf-8")
    return stem


def write_chapter_manifest(ch_dir: Path, ch_slug: str, title: str, sections: list[tuple[str, str, list[str], bool]], number: int | None = None):
    sec_strs = []
    for sec_title, sec_label, blocks, is_lead in sections:
        lead_str = "      lead: true,\n" if is_lead else ""
        b_list = ", ".join(json.dumps(b) for b in blocks)
        sec_strs.append(
            "    section({\n"
            f"      title: {json.dumps(sec_title)},\n"
            f"      label: {json.dumps(sec_label)},\n"
            f"{lead_str}"
            f"      blocks: [{b_list}],\n"
            "    }),"
        )
    num_str = f"  number: {number},\n" if number is not None else ""
    ts = (
        'import { chapter, section } from "../../schema/builders";\n\n'
        "export default chapter({\n"
        f"{num_str}"
        f"  title: {json.dumps(title)},\n"
        f"  label: {json.dumps('chap:' + ch_slug)},\n"
        "  sections: [\n" + "\n".join(sec_strs) + "\n  ],\n"
        "});\n"
    )
    (ch_dir / f"{ch_slug}.ts").write_text(ts, encoding="utf-8")


def build_ch03(folio_dir: Path):
    """Formalize Chapter 3: Understand user requirements (sec-012..sec-019)."""
    ch_slug = "ch03-user-requirements"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    # sec-012: Chapter 3 opener, phase panel, and 3.1 Follow key requirement-gathering methods
    l12, _, p12 = read_l1_section("sec-012-31-follow-key-requirement-gathering-methods.md")
    lead_md = slice_lines(l12, 1, 9)
    panel_md = slice_lines(l12, 10, 15)
    methods_intro_md = slice_lines(l12, 16, 21)
    desk_obs_md = slice_lines(l12, 22, 91)
    interviews_md = slice_lines(l12, 92, 165)
    fig8_caption_md = slice_lines(l12, 166, 213)
    workshops_md = slice_lines(l12, 214, None)

    b_lead = write_prose_block(
        ch_dir,
        "p-ch03-overview",
        "prose:ch03-overview",
        lead_md,
        make_meta(
            "Chapter 3 overview: Understand user requirements",
            "sec-012-31-follow-key-requirement-gathering-methods.md",
            [28],
            phc_terms=["person-centred-point-of-service-system", "requirements", "end-user", "workflow"],
            ra_terms=["point-of-service-applications", "stakeholder"],
            elements=["pos-app", "health-worker", "health-service-user", "public-health-authority", "business-analyst"],
            views=["pcposs", "shared-roles"],
        ),
    )

    b_panel = write_table_block(
        ch_dir,
        "t-ch03-phase-panel",
        "tbl:ch03-phase-panel",
        "Chapter 3 phase panel: Who should be involved, Inputs, Tools and Outputs for understanding user requirements",
        panel_md,
        make_meta(
            "Chapter 3 phase panel (Who should be involved / Inputs / Tools / Outputs)",
            "sec-012-31-follow-key-requirement-gathering-methods.md",
            [28, 29],
            method="l1-phase-panel-formalized",
            phc_terms=[
                "person-centred-point-of-service-system",
                "user-persona",
                "use-case",
                "user-story",
                "business-process",
                "data-dictionary",
                "scheduling-logic",
                "decision-support-logic",
                "indicators-and-performance-metrics",
                "functional-requirements",
                "non-functional-requirements",
                "digital-adaptation-kits",
            ],
            ra_terms=["point-of-service-applications", "interoperability", "enterprise-architecture"],
            elements=[
                "health-worker",
                "health-service-user",
                "business-analyst",
                "health-informatician",
                "user-researcher",
                "software-engineer",
                "public-health-authority",
                "pos-app",
                "smart-l2-dak",
            ],
            views=["pcposs", "shared-roles"],
            phasePanel={
                "phase": 1,
                "chapter": 3,
                "title": "Understand user requirements",
                "diigPhase": 3,
                "roles": [
                    "health-worker",
                    "health-service-user",
                    "business-analyst",
                    "health-informatician",
                    "user-researcher",
                    "software-engineer",
                    "public-health-authority",
                ],
                "inputs": [
                    "National health strategy, digital health strategy, health policies, and PCPOSS strategic scope",
                    "Health information system, privacy, security and data use policies",
                    "Digital health architecture blueprint and interoperability requirements",
                    "Infrastructure readiness assessment",
                    "Unique identifier method",
                    "List of anticipated outcomes",
                    "WHO and national clinical/public health guidelines and SOPs",
                    "Existing paper records and register forms",
                    "End-user and key stakeholder interviews and insights",
                ],
                "tools": [
                    "Observation templates (Annex 3)",
                    "User persona template (Annex 4)",
                    "User stories template (Annex 5)",
                    "Business process matrix template (Annex 6)",
                    "WHO Digital adaptation kits (DAKs)",
                    "Forms inventory template (Annex 7)",
                    "Form data mapping template (Annex 8)",
                    "Aggregate indicator mapping template (Annex 9)",
                    "Decision table and scheduling matrix template (Annex 10)",
                    "Decision table template (Annex 11)",
                    "Service schedule template (Annex 12)",
                    "Prioritization of requirements template (Annex 13)",
                ],
                "outputs": [
                    {"artifact": "User personas", "dakKind": "persona", "smartBaseClass": "smart-base:Persona"},
                    {"artifact": "Use cases", "dakKind": "user-scenario", "smartBaseClass": "smart-base:UserScenario"},
                    {"artifact": "User stories", "dakKind": "user-scenario", "smartBaseClass": "smart-base:UserScenario"},
                    {"artifact": "As-is and to-be business processes", "dakKind": "business-process", "smartBaseClass": "smart-base:BusinessProcess"},
                    {"artifact": "Data dictionary and data model", "dakKind": "data-element", "smartBaseClass": "smart-base:DataElement"},
                    {"artifact": "Documented health service schedule", "dakKind": "scheduling-logic", "smartBaseClass": "smart-base:SchedulingLogic"},
                    {"artifact": "Documented decision logic algorithms", "dakKind": "decision-table", "smartBaseClass": "smart-base:DecisionTable"},
                    {"artifact": "List of indicators and calculation method", "dakKind": "indicator", "smartBaseClass": "smart-base:Indicator"},
                    {"artifact": "Prioritized functional and non-functional requirements", "dakKind": "functional-requirement", "smartBaseClass": "smart-base:FunctionalRequirement"},
                ],
            },
        ),
        uses=["prose:ch03-overview"],
    )

    b_31_methods = write_prose_block(
        ch_dir,
        "p-ch03-sec-012-methods",
        "prose:ch03-sec-012-methods",
        methods_intro_md + "\n" + desk_obs_md,
        make_meta(
            "3.1 Follow key requirement-gathering methods: desk review and observations",
            "sec-012-31-follow-key-requirement-gathering-methods.md",
            [29, 30, 31],
            phc_terms=[
                "collaborative-requirements-development-methodology",
                "requirements",
                "end-user",
                "register",
                "clinical-protocol",
            ],
            ra_terms=["point-of-service-applications"],
            elements=["business-analyst", "user-researcher", "health-informatician", "health-worker"],
            views=["shared-roles", "pcposs"],
            methodStep={
                "stepId": "3.1",
                "title": "Follow key requirement-gathering methods",
                "substeps": ["3.1.1 Desk review", "3.1.2 Observations", "3.1.3 Semi-structured and follow-up interviews", "3.1.4 Requirements-gathering workshops"],
                "templates": ["Annex 2 (sec-035)", "Annex 3 (sec-036)"],
                "methodology": "Collaborative Requirements Development Methodology (CRDM, PHII 2023 ref. 20; PATH 2012 ref. 50)",
            },
        ),
        uses=["tbl:ch03-phase-panel"],
    )

    b_31_interviews = write_prose_block(
        ch_dir,
        "p-ch03-sec-012-interviews-and-workshops",
        "prose:ch03-sec-012-interviews-and-workshops",
        interviews_md + "\n" + workshops_md,
        make_meta(
            "3.1.3–3.1.4 Semi-structured interviews and requirements-gathering workshops",
            "sec-012-31-follow-key-requirement-gathering-methods.md",
            [31, 32, 33],
            phc_terms=["end-user", "health-service-users", "pain-point", "requirements"],
            ra_terms=["stakeholder"],
            elements=["user-researcher", "business-analyst", "health-worker", "health-service-user"],
            views=["shared-roles"],
            sourceOnly="interview and workshop facilitation tips and example prompts: cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["prose:ch03-sec-012-methods"],
    )

    b_fig8 = write_figure_block(
        ch_dir,
        "f-ch03-fig-8",
        "fig:8",
        "media/vfig-p032.png",
        "Fig. 8. Example prompts and questions for starting broad and narrowing down",
        32,
        "![Fig. 8. Example prompts and questions for starting broad and narrowing down](media/vfig-p032.png)\n\n" + fig8_caption_md,
        make_meta(
            "Fig. 8. Example prompts and questions for starting broad and narrowing down",
            "sec-012-31-follow-key-requirement-gathering-methods.md",
            [32],
            method="l1-vector-figure",
            phc_terms=["end-user", "pain-point", "requirements"],
            elements=["user-researcher", "business-analyst"],
            views=["shared-roles"],
            sourceOnly="adapted from Tran 2018 (ref. 35): cited L1 figure per dth-phc#1 §3b",
        ),
        uses=["prose:ch03-sec-012-interviews-and-workshops"],
    )

    # sec-013: 3.2 Get to know the users
    l13, _, p13 = read_l1_section("sec-013-32-get-to-know-the-users.md")
    sec13_personas_md = slice_lines(l13, 1, 98)
    sec13_usecases_md = slice_lines(l13, 99, None)

    b_32_personas = write_prose_block(
        ch_dir,
        "p-ch03-sec-013-personas",
        "prose:ch03-sec-013-personas",
        sec13_personas_md,
        make_meta(
            "3.2.1 Create user personas",
            "sec-013-32-get-to-know-the-users.md",
            [33, 34],
            phc_terms=["user-persona", "end-user", "health-service-users", "pain-point", "workflow"],
            ra_terms=["stakeholder"],
            elements=["health-worker", "health-service-user", "user-researcher", "business-analyst"],
            views=["shared-roles", "pcposs"],
            methodStep={
                "stepId": "3.2.1",
                "title": "Create user personas",
                "producesDakComponents": ["smart-base:Persona"],
                "dakKind": "persona",
                "template": "Annex 4. User persona worksheet (sec-037)",
            },
        ),
        uses=["prose:ch03-sec-012-methods"],
        defines=["user-persona"],
    )

    b_32_usecases = write_prose_block(
        ch_dir,
        "p-ch03-sec-013-use-cases-and-stories",
        "prose:ch03-sec-013-use-cases-and-stories",
        sec13_usecases_md,
        make_meta(
            "3.2.2–3.2.3 Gather use cases and user stories",
            "sec-013-32-get-to-know-the-users.md",
            [34, 35],
            phc_terms=["use-case", "user-story", "user-scenario", "user-persona", "functional-requirements", "non-functional-requirements"],
            ra_terms=["point-of-service-applications"],
            elements=["business-analyst", "user-researcher", "health-worker", "pos-app"],
            views=["shared-roles", "pcposs"],
            methodStep={
                "stepId": "3.2.2-3.2.3",
                "title": "Gather use cases and user stories",
                "producesDakComponents": ["smart-base:UserScenario", "smart-base:FunctionalRequirement", "smart-base:NonFunctionalRequirement"],
                "dakKinds": ["user-scenario", "functional-requirement", "non-functional-requirement"],
                "template": "Annex 5. User stories worksheet (sec-038)",
            },
        ),
        uses=["prose:ch03-sec-013-personas"],
        defines=["use-case", "user-story"],
    )

    # sec-014: 3.3 Map business processes and workflows
    l14, _, p14 = read_l1_section("sec-014-33-map-business-processes-and-workflows.md")
    sec14_intro_md = slice_lines(l14, 1, 31)
    fig9_md = slice_lines(l14, 32, 42)
    sec14_conventions_md = slice_lines(l14, 43, 74)
    tbl1_md = slice_lines(l14, 75, 98)
    sec14_labelling_md = slice_lines(l14, 99, 118)
    fig10_11_md = slice_lines(l14, 119, 268)
    sec14_asis_tobe_md = slice_lines(l14, 269, None)

    b_33_intro = write_prose_block(
        ch_dir,
        "p-ch03-sec-014-workflows",
        "prose:ch03-sec-014-workflows",
        sec14_intro_md + "\n" + sec14_conventions_md + "\n" + sec14_labelling_md + "\n" + sec14_asis_tobe_md,
        make_meta(
            "3.3 Map business processes and workflows (BPMN conventions, annotations, as-is and to-be analysis)",
            "sec-014-33-map-business-processes-and-workflows.md",
            [35, 36, 37, 38, 39],
            phc_terms=[
                "business-process",
                "business-objective",
                "workflow",
                "generic-business-processes-and-workflows",
                "as-is",
                "to-be",
                "trigger-event",
                "input",
                "output",
                "annotation",
                "pain-point",
                "digital-adaptation-kits",
            ],
            ra_terms=["point-of-service-applications"],
            elements=["business-analyst", "health-informatician", "health-worker", "pos-app", "smart-l2-dak"],
            views=["pcposs", "shared-roles"],
            methodStep={
                "stepId": "3.3",
                "title": "Map business processes and workflows",
                "substeps": ["3.3.1 Workflow mapping conventions", "3.3.2 Process labelling and annotations", "3.3.3 As-is and to-be analysis"],
                "producesDakComponents": ["smart-base:BusinessProcess"],
                "dakKind": "business-process",
                "template": "Annex 6. Business process matrix guide (sec-039)",
                "standards": ["omg-2013-bpmn-2-0-2"],
                "sdlcAlignment": {
                    "compareWith": ["smart-base/processes/l2-dak-authoring.bpmn", "cat-harness/processes/crdm-requirements-definition.bpmn"],
                    "normativeSpec": "cat-harness/library/omg-2013-bpmn-2-0-2",
                },
            },
        ),
        uses=["prose:ch03-sec-013-use-cases-and-stories"],
        defines=["business-process", "workflow", "as-is", "to-be", "annotation", "trigger-event"],
    )

    b_tbl1 = write_table_block(
        ch_dir,
        "t-ch03-table-1",
        "tbl:1",
        "Table 1. Key Business Process Model and Notation (BPMN) symbols",
        tbl1_md,
        make_meta(
            "Table 1. Key Business Process Model and Notation (BPMN) symbols",
            "sec-014-33-map-business-processes-and-workflows.md",
            [36, 37],
            method="l1-table-formalized",
            phc_terms=["business-process", "workflow", "trigger-event", "user-persona"],
            elements=["business-analyst", "smart-l2-dak"],
            views=["shared-roles"],
            normativeSpec="cat-harness/library/omg-2013-bpmn-2-0-2",
        ),
        uses=["prose:ch03-sec-014-workflows"],
    )

    b_fig9 = write_figure_block(
        ch_dir,
        "f-ch03-fig-9",
        "fig:9",
        "media/vfig-p035.png",
        "Fig. 9. Example business process matrix from family planning DAK",
        35,
        "![Fig. 9. Example business process matrix from family planning DAK](media/vfig-p035.png)\n\n" + fig9_md,
        make_meta(
            "Fig. 9. Example business process matrix from family planning DAK",
            "sec-014-33-map-business-processes-and-workflows.md",
            [35],
            method="l1-vector-figure",
            phc_terms=["business-process", "business-objective", "user-persona", "digital-adaptation-kits"],
            elements=["smart-l2-dak"],
            views=["pcposs"],
            reproduces={
                "source": "WHO Digital adaptation kit for family planning (2021)",
                "iris": "https://iris.who.int/handle/10665/341997",
                "component": "business-process",
            },
            sourceOnly="reproduced DAK example from WHO Family Planning DAK (ref. 30): linked, never redrawn per dth-phc#1 §3d",
        ),
        uses=["prose:ch03-sec-014-workflows"],
    )

    b_fig10 = write_figure_block(
        ch_dir,
        "f-ch03-fig-10",
        "fig:10",
        "media/vfig-p038.png",
        "Fig. 10. Workflow A: Registration business process",
        38,
        "![Fig. 10. Workflow A: Registration business process](media/vfig-p038.png)\n\n*Source: WHO Digital adaptation kit for antenatal care, 2021 (ref. 29).*",
        make_meta(
            "Fig. 10. Workflow A: Registration business process (from WHO ANC DAK)",
            "sec-014-33-map-business-processes-and-workflows.md",
            [38],
            method="l1-vector-figure",
            phc_terms=["business-process", "workflow", "antenatal-care", "digital-adaptation-kits"],
            elements=["smart-l2-dak", "health-worker", "health-service-user"],
            views=["pcposs"],
            reproduces={
                "source": "WHO Digital adaptation kit for antenatal care (2021)",
                "iris": "https://iris.who.int/handle/10665/339745",
                "processId": "ANC.A",
                "component": "business-process",
            },
            sourceOnly="reproduced BPMN workflow from WHO ANC DAK (ref. 29): linked, never redrawn per dth-phc#1 §3d",
        ),
        uses=["tbl:1"],
    )

    b_fig11 = write_figure_block(
        ch_dir,
        "f-ch03-fig-11",
        "fig:11",
        "media/vfig-p038.png",
        "Fig. 11. Notes and annotations for Workflow A: Registration business process",
        38,
        "![Fig. 11. Notes and annotations for Workflow A: Registration business process](media/vfig-p038.png)\n\n" + fig10_11_md,
        make_meta(
            "Fig. 11. Notes and annotations for Workflow A: Registration business process",
            "sec-014-33-map-business-processes-and-workflows.md",
            [38, 39],
            method="l1-vector-figure",
            phc_terms=["annotation", "business-process", "workflow", "antenatal-care", "digital-adaptation-kits"],
            elements=["smart-l2-dak"],
            views=["pcposs"],
            reproduces={
                "source": "WHO Digital adaptation kit for antenatal care (2021)",
                "iris": "https://iris.who.int/handle/10665/339745",
                "processId": "ANC.A",
                "component": "business-process",
            },
            sourceOnly="reproduced workflow annotations from WHO ANC DAK (ref. 29): linked, never redrawn per dth-phc#1 §3d",
        ),
        uses=["fig:10"],
    )

    # sec-015: 3.4 Streamline data collection and indicator reporting
    l15, _, p15 = read_l1_section("sec-015-34-streamline-data-collection-and-indicator-repo.md")
    sec15_body_md = slice_lines(l15, 1, 169)
    fig12_tbl_md = slice_lines(l15, 170, None)

    b_34_streamline = write_prose_block(
        ch_dir,
        "p-ch03-sec-015-streamline-data-and-indicators",
        "prose:ch03-sec-015-streamline-data-and-indicators",
        sec15_body_md,
        make_meta(
            "3.4 Streamline data collection and indicator reporting",
            "sec-015-34-streamline-data-collection-and-indicator-repo.md",
            [39, 40, 41, 42],
            phc_terms=[
                "data-element",
                "register",
                "indicators-and-performance-metrics",
                "health-management-information-system",
                "person-centred-point-of-service-system",
            ],
            ra_terms=["point-of-service-applications", "data-object"],
            elements=["pos-app", "indicator-reporting", "analytics-platform", "hmis", "shr", "patient-level-data"],
            views=["pcposs", "shr"],
            methodStep={
                "stepId": "3.4",
                "title": "Streamline data collection and indicator reporting",
                "substeps": [
                    "3.4.1 Create an inventory of paper forms",
                    "3.4.2 Map all the data elements used in forms",
                    "3.4.3 Compile aggregate indicators",
                    "3.4.4 Remove duplicated, orphaned or non-essential data elements",
                ],
                "producesDakComponents": ["smart-base:DataElement", "smart-base:Indicator"],
                "dakKinds": ["data-element", "indicator"],
                "templates": [
                    "Annex 7. Form inventory guide (sec-040)",
                    "Annex 8. Form data mapping guide (sec-041)",
                    "Annex 9. Aggregate indicator mapping guide (sec-042)",
                ],
            },
        ),
        uses=["prose:ch03-sec-014-workflows"],
        defines=["register", "indicators-and-performance-metrics"],
    )

    b_tbl_fig12 = write_table_block(
        ch_dir,
        "t-ch03-fig-12",
        "tbl:fig-12",
        "Fig. 12. Is each and every data element collected truly needed? (Decision criteria for keeping or removing a data element)",
        fig12_tbl_md,
        make_meta(
            "Fig. 12 decision matrix: Keep or remove a data element",
            "sec-015-34-streamline-data-collection-and-indicator-repo.md",
            [41, 42],
            method="l1-table-formalized",
            phc_terms=["data-element", "data-dictionary", "indicators-and-performance-metrics"],
            elements=["business-analyst", "health-informatician", "patient-level-data"],
            views=["pcposs"],
            dmnCandidate={
                "table": "Data element retention",
                "section": "3.4.4, Fig. 12",
                "inputs": ["duplicated?", "needed for service delivery or accountability?", "orphaned?"],
                "output": "keep, consolidate, link to workflow, or remove",
            },
        ),
        uses=["prose:ch03-sec-015-streamline-data-and-indicators"],
    )

    b_fig12 = write_figure_block(
        ch_dir,
        "f-ch03-fig-12",
        "fig:12",
        "media/vfig-p042.png",
        "Fig. 12. Is each and every data element collected truly needed?",
        42,
        "![Fig. 12. Is each and every data element collected truly needed?](media/vfig-p042.png)\n\n*Source: WHO, Digital transformation handbook for primary health care, 2024, PDF pages 41–42.*",
        make_meta(
            "Fig. 12. Is each and every data element collected truly needed?",
            "sec-015-34-streamline-data-collection-and-indicator-repo.md",
            [41, 42],
            method="l1-vector-figure",
            phc_terms=["data-element", "data-dictionary"],
            elements=["patient-level-data"],
            views=["pcposs"],
        ),
        uses=["tbl:fig-12"],
    )

    # sec-016: 3.5 Create a data dictionary
    l16, _, p16 = read_l1_section("sec-016-35-create-a-data-dictionary.md")
    sec16_md = slice_lines(l16, 1, None)

    b_35_dd = write_prose_block(
        ch_dir,
        "p-ch03-sec-016-data-dictionary",
        "prose:ch03-sec-016-data-dictionary",
        sec16_md,
        make_meta(
            "3.5 Create a data dictionary (data element definitions and terminology mapping)",
            "sec-016-35-create-a-data-dictionary.md",
            [42, 43, 44],
            phc_terms=[
                "data-dictionary",
                "data-element",
                "metadata",
                "terminologies",
                "classifications",
                "coding-schemes",
                "interoperability-standards",
                "international-classification-of-diseases",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "fast-healthcare-interoperability-resources",
            ],
            ra_terms=[
                "interoperability",
                "fast-healthcare-interoperability-resources",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "snomed-gps",
            ],
            elements=["terminology-service", "limr", "logical-models", "patient-level-data", "health-informatician"],
            views=["pcposs", "lmir-overview"],
            methodStep={
                "stepId": "3.5",
                "title": "Create a data dictionary",
                "substeps": ["3.5.1 Define data elements for inclusion in the data dictionary", "3.5.2 Map data elements to standardized terminologies"],
                "producesDakComponents": ["smart-base:DataElement"],
                "dakKind": "data-element",
                "template": "Annex 8. Form data mapping guide (sec-041)",
            },
        ),
        uses=["prose:ch03-sec-015-streamline-data-and-indicators"],
        defines=["data-dictionary", "data-element", "metadata"],
    )

    # sec-017: 3.6 Determine decision-support logic
    l17, _, p17 = read_l1_section("sec-017-36-determine-decision-support-logic.md")
    sec17_body_md = slice_lines(l17, 1, 97)
    fig13_md = slice_lines(l17, 98, 109)
    fig14_md = slice_lines(l17, 110, None)

    b_36_decision = write_prose_block(
        ch_dir,
        "p-ch03-sec-017-decision-support-logic",
        "prose:ch03-sec-017-decision-support-logic",
        sec17_body_md,
        make_meta(
            "3.6 Determine decision-support logic",
            "sec-017-36-determine-decision-support-logic.md",
            [44, 45, 46, 47],
            phc_terms=[
                "decision-support-logic",
                "decision-support-table",
                "decision-support-system",
                "clinical-protocol",
                "care-pathway",
                "algorithm",
                "rule",
                "input",
                "output",
                "flag",
                "pop-up-message",
            ],
            ra_terms=["point-of-service-applications"],
            elements=["dss", "dse", "alerts-and-reminders", "care-checklists", "clinical-screening", "smart-l2-dak"],
            views=["pcposs", "cds"],
            methodStep={
                "stepId": "3.6",
                "title": "Determine decision-support logic",
                "substeps": ["3.6.1 Document clinical care pathway decision-support logic"],
                "producesDakComponents": ["smart-base:DecisionTable"],
                "dakKind": "decision-table",
                "templates": [
                    "Annex 10. Decision-support logic and scheduling matrix guide (sec-042)",
                    "Annex 11. Template for a decision-support table (sec-043)",
                ],
                "standards": ["omg-2024-dmn-1-5"],
                "normativeSpec": "cat-harness/library/omg-2024-dmn-1-5",
            },
        ),
        uses=["prose:ch03-sec-016-data-dictionary"],
        defines=["decision-support-logic", "decision-support-table", "rule", "flag", "pop-up-message"],
    )

    b_fig13 = write_figure_block(
        ch_dir,
        "f-ch03-fig-13",
        "fig:13",
        "media/vfig-p045.png",
        "Fig. 13. Example decision-support logic matrix from DAK for HIV",
        45,
        "![Fig. 13. Example decision-support logic matrix from DAK for HIV](media/vfig-p045.png)\n\n" + fig13_md,
        make_meta(
            "Fig. 13. Example decision-support logic matrix from DAK for HIV",
            "sec-017-36-determine-decision-support-logic.md",
            [45],
            method="l1-vector-figure",
            phc_terms=["decision-support-logic", "decision-support-table", "digital-adaptation-kits"],
            elements=["dss", "dse", "smart-l2-dak"],
            views=["cds", "pcposs"],
            reproduces={
                "source": "WHO Digital adaptation kit for HIV, 2nd ed. (2023)",
                "iris": "https://iris.who.int/handle/10665/375230",
                "component": "decision-table",
            },
            sourceOnly="reproduced decision-support matrix from WHO HIV DAK (ref. 31): linked, never redrawn per dth-phc#1 §3d",
        ),
        uses=["prose:ch03-sec-017-decision-support-logic"],
    )

    b_fig14 = write_figure_block(
        ch_dir,
        "f-ch03-fig-14",
        "fig:14",
        "media/vfig-p046.png",
        "Fig. 14. Decision-support logic for a clinical care pathway in the form of a decision tree",
        46,
        "![Fig. 14. Decision-support logic for a clinical care pathway in the form of a decision tree](media/vfig-p046.png)\n\n" + fig14_md,
        make_meta(
            "Fig. 14. Decision-support logic for a clinical care pathway in the form of a decision tree",
            "sec-017-36-determine-decision-support-logic.md",
            [46, 47],
            method="l1-vector-figure",
            phc_terms=["decision-support-logic", "care-pathway", "antenatal-care", "digital-adaptation-kits"],
            elements=["dss", "dse", "clinical-screening"],
            views=["cds", "pcposs"],
            reproduces={
                "source": "WHO Digital adaptation kit for antenatal care (2021)",
                "iris": "https://iris.who.int/handle/10665/339745",
                "component": "decision-table",
            },
            sourceOnly="reproduced ANC HIV-testing decision tree from WHO ANC DAK (ref. 29): linked, never redrawn per dth-phc#1 §3d",
        ),
        uses=["fig:13"],
    )

    # sec-018: 3.7 Map health service schedules
    l18, _, p18 = read_l1_section("sec-018-37-map-health-service-schedules.md")
    sec18_md = slice_lines(l18, 1, None)

    b_37_schedules = write_prose_block(
        ch_dir,
        "p-ch03-sec-018-schedules",
        "prose:ch03-sec-018-schedules",
        sec18_md,
        make_meta(
            "3.7 Map health service schedules",
            "sec-018-37-map-health-service-schedules.md",
            [47],
            phc_terms=["scheduling-logic", "longitudinal-tracking", "care-pathway", "trigger-event", "flag"],
            ra_terms=["point-of-service-applications"],
            elements=["longitudinal-tracking", "alerts-and-reminders", "dss", "pos-app"],
            views=["pcposs", "cds"],
            methodStep={
                "stepId": "3.7",
                "title": "Map health service schedules",
                "producesDakComponents": ["smart-base:SchedulingLogic"],
                "dakKind": "scheduling-logic",
                "templates": [
                    "Annex 10. Decision-support logic and scheduling matrix guide (sec-042)",
                    "Annex 12. Scheduling logic table guide (sec-044)",
                ],
            },
        ),
        uses=["prose:ch03-sec-017-decision-support-logic"],
        defines=["scheduling-logic"],
    )

    # sec-019: 3.8 Gather and prioritize requirements
    l19, _, p19 = read_l1_section("sec-019-38-gather-and-prioritize-requirements.md")
    sec19_md = slice_lines(l19, 1, None)

    b_38_reqs = write_prose_block(
        ch_dir,
        "p-ch03-sec-019-requirements",
        "prose:ch03-sec-019-requirements",
        sec19_md,
        make_meta(
            "3.8 Gather and prioritize functional and non-functional requirements",
            "sec-019-38-gather-and-prioritize-requirements.md",
            [47, 48, 49],
            phc_terms=[
                "requirements",
                "functional-requirements",
                "non-functional-requirements",
                "features",
                "functions",
                "minimum-viable-product",
            ],
            ra_terms=["point-of-service-applications", "capability"],
            elements=["pos-app", "business-analyst", "software-engineer", "security-consent"],
            views=["pcposs", "shared-roles"],
            methodStep={
                "stepId": "3.8",
                "title": "Gather and prioritize requirements",
                "producesDakComponents": ["smart-base:FunctionalRequirement", "smart-base:NonFunctionalRequirement"],
                "dakKinds": ["functional-requirement", "non-functional-requirement"],
                "template": "Annex 13. Prioritization of requirements guide (sec-045)",
                "priorityAlignment": {
                    "High": "Must-have / SHALL (RFC 2119 / RFC 8174)",
                    "Medium": "Should-have / SHOULD (RFC 2119 / RFC 8174)",
                    "Low": "Nice-to-have / MAY (RFC 2119 / RFC 8174)",
                },
            },
            dmnCandidate={
                "table": "Requirement priority",
                "section": "3.8, Annex 13",
                "inputs": ["needed for a complete system?", "strongly advised for uptake and usability?"],
                "output": "High, Medium, or Low",
            },
        ),
        uses=["prose:ch03-sec-018-schedules"],
        defines=["requirements", "functional-requirements", "non-functional-requirements", "features", "functions"],
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Chapter 3. Understand user requirements",
        [
            ("Chapter overview and phase panel", "sec:ch03-lead", [b_lead, b_panel], True),
            ("3.1 Follow key requirement-gathering methods", "sec:3-1", [b_31_methods, b_31_interviews, b_fig8], False),
            ("3.2 Get to know the users", "sec:3-2", [b_32_personas, b_32_usecases], False),
            ("3.3 Map business processes and workflows", "sec:3-3", [b_33_intro, b_tbl1, b_fig9, b_fig10, b_fig11], False),
            ("3.4 Streamline data collection and indicator reporting", "sec:3-4", [b_34_streamline, b_tbl_fig12, b_fig12], False),
            ("3.5 Create a data dictionary", "sec:3-5", [b_35_dd], False),
            ("3.6 Determine decision-support logic", "sec:3-6", [b_36_decision, b_fig13, b_fig14], False),
            ("3.7 Map health service schedules", "sec:3-7", [b_37_schedules], False),
            ("3.8 Gather and prioritize requirements", "sec:3-8", [b_38_reqs], False),
        ],
        number=3,
    )
    return ch_slug


def build_ch04(folio_dir: Path):
    """Formalize Chapter 4: Undertake design and adaptation (sec-020..sec-024)."""
    ch_slug = "ch04-design-and-adaptation"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    # sec-020: Chapter 4 opener, phase panel, and 4.1 Finalize software and vendor selection
    l20, _, p20 = read_l1_section("sec-020-41-finalize-software-and-vendor-selection.md")
    lead_md = slice_lines(l20, 1, 7)
    panel_md = slice_lines(l20, 8, 17)
    vendor_md = slice_lines(l20, 18, None)

    b_lead = write_prose_block(
        ch_dir,
        "p-ch04-overview",
        "prose:ch04-overview",
        lead_md,
        make_meta(
            "Chapter 4 overview: Undertake design and adaptation",
            "sec-020-41-finalize-software-and-vendor-selection.md",
            [50],
            phc_terms=["person-centred-point-of-service-system", "systems-architecture", "prototype", "beta-version"],
            ra_terms=["solution-architecture", "point-of-service-applications"],
            elements=["technology-partner", "software-engineer", "solutions-architect", "implementing-team", "pos-app"],
            views=["pcposs", "shared-roles"],
        ),
    )

    b_panel = write_table_block(
        ch_dir,
        "t-ch04-phase-panel",
        "tbl:ch04-phase-panel",
        "Chapter 4 phase panel: Who should be involved, Inputs, Tools and Outputs for design and adaptation",
        panel_md,
        make_meta(
            "Chapter 4 phase panel (Who should be involved / Inputs / Tools / Outputs)",
            "sec-020-41-finalize-software-and-vendor-selection.md",
            [50, 51],
            method="l1-phase-panel-formalized",
            phc_terms=[
                "person-centred-point-of-service-system",
                "systems-architecture",
                "fast-healthcare-interoperability-resources",
                "terminologies",
                "prototype",
                "beta-version",
                "digital-adaptation-kits",
            ],
            ra_terms=["solution-architecture", "fast-healthcare-interoperability-resources", "interoperability"],
            elements=[
                "software-engineer",
                "solutions-architect",
                "business-analyst",
                "designer",
                "health-informatician",
                "health-worker",
                "health-service-user",
                "technology-partner",
                "terminology-service",
                "pos-app",
            ],
            views=["pcposs", "shared-roles"],
            phasePanel={
                "phase": 2,
                "chapter": 4,
                "title": "Undertake design and adaptation",
                "diigPhase": 4,
                "roles": [
                    "software-engineer",
                    "solutions-architect",
                    "business-analyst",
                    "designer",
                    "health-informatician",
                    "health-worker",
                    "health-service-user",
                    "technology-partner",
                ],
                "inputs": [
                    "Scope for PCPOSS",
                    "Project team governance structure",
                    "Budget, timeline, and risk and mitigations plan",
                    "Digital adaptation kits (DAKs)",
                    "Chapter 3 requirements documentation (user personas, use cases, user stories, as-is/to-be business processes, data dictionary, data model with semantic and syntactic standards, decision logic algorithms, health service schedule, prioritized functional and non-functional requirements)",
                ],
                "tools": [
                    "Design software tools for prototype creation",
                    "Design tools for depicting system architecture",
                    "Concept dictionary or terminology service",
                    "Coding environment",
                ],
                "outputs": [
                    "Selected software and software vendor",
                    "System architecture",
                    "User interface design",
                    "Product documentation",
                    "Beta version of the PCPOSS",
                ],
            },
        ),
        uses=["prose:ch04-overview"],
    )

    b_41_vendor = write_prose_block(
        ch_dir,
        "p-ch04-sec-020-vendor-selection",
        "prose:ch04-sec-020-vendor-selection",
        vendor_md,
        make_meta(
            "4.1 Finalize software and vendor selection",
            "sec-020-41-finalize-software-and-vendor-selection.md",
            [51, 52, 53],
            phc_terms=[
                "reference-software",
                "software-platform",
                "open-source",
                "open-standards",
                "smart-guidelines",
                "technical-debt",
                "interoperability-standards",
            ],
            ra_terms=["point-of-service-applications", "smart-guidelines"],
            elements=["technology-partner", "solutions-architect", "software-engineer", "pos-app"],
            views=["shared-roles", "pcposs"],
            sourceOnly="vendor-selection and contracting advice: cited L1 narrative per dth-phc#1 §3b; SMART Guidelines L4 reference software definition captured formally",
        ),
        uses=["tbl:ch04-phase-panel"],
        defines=["reference-software", "software-platform", "open-source", "open-standards"],
    )

    # sec-021: 4.2 Validate functional requirements
    l21, _, p21 = read_l1_section("sec-021-42-validate-functional-requirements.md")
    sec21_md = slice_lines(l21, 1, None)

    b_42_validate = write_prose_block(
        ch_dir,
        "p-ch04-sec-021-validate-requirements",
        "prose:ch04-sec-021-validate-requirements",
        sec21_md,
        make_meta(
            "4.2 Validate functional requirements",
            "sec-021-42-validate-functional-requirements.md",
            [53],
            phc_terms=["functional-requirements", "non-functional-requirements", "requirements", "minimum-viable-product"],
            ra_terms=["point-of-service-applications"],
            elements=["business-analyst", "software-engineer", "technology-partner", "implementing-team"],
            views=["shared-roles", "pcposs"],
        ),
        uses=["prose:ch04-sec-020-vendor-selection"],
    )

    # sec-022: 4.3 Develop and test prototype design
    l22, _, p22 = read_l1_section("sec-022-43-develop-and-test-prototype-design.md")
    sec22_dev_md = slice_lines(l22, 1, 97)
    fig15_md = slice_lines(l22, 98, 146)
    sec22_test_md = slice_lines(l22, 147, None)

    b_43_proto = write_prose_block(
        ch_dir,
        "p-ch04-sec-022-prototyping",
        "prose:ch04-sec-022-prototyping",
        sec22_dev_md + "\n" + sec22_test_md,
        make_meta(
            "4.3 Develop and test prototype design (wireframes, mock-ups, prototypes and user testing)",
            "sec-022-43-develop-and-test-prototype-design.md",
            [53, 54, 55, 56],
            phc_terms=["wireframes", "mock-up", "prototype", "end-user", "features", "functions"],
            ra_terms=["point-of-service-applications"],
            elements=["designer", "user-researcher", "software-engineer", "health-worker", "health-service-user", "pos-app"],
            views=["shared-roles", "pcposs"],
            prototypeProgression=["wireframes (low-fidelity layout)", "mock-up (mid-to-high-fidelity visual design)", "prototype (interactive testable model)"],
            sourceOnly="prototyping workshop facilitation tips and feedback capture matrix (adapted from Tran 2018 ref. 35): cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["prose:ch04-sec-021-validate-requirements"],
        defines=["wireframes", "mock-up", "prototype"],
    )

    b_fig15 = write_figure_block(
        ch_dir,
        "f-ch04-fig-15",
        "fig:15",
        "media/vfig-p054.png",
        "Fig. 15. Levels of insight gained from different prototypes",
        54,
        "![Fig. 15. Levels of insight gained from different prototypes](media/vfig-p054.png)\n\n" + fig15_md,
        make_meta(
            "Fig. 15. Levels of insight gained from different prototypes",
            "sec-022-43-develop-and-test-prototype-design.md",
            [54],
            method="l1-vector-figure",
            phc_terms=["wireframes", "mock-up", "prototype"],
            elements=["designer", "user-researcher"],
            views=["shared-roles"],
        ),
        uses=["prose:ch04-sec-022-prototyping"],
    )

    # sec-023: 4.4 Design system architecture
    l23, _, p23 = read_l1_section("sec-023-44-design-system-architecture.md")
    sec23_intro_md = slice_lines(l23, 1, 56)
    sec23_441_md = slice_lines(l23, 57, 89)
    tbl2_md = slice_lines(l23, 90, 97)
    sec23_441_post_md = slice_lines(l23, 98, 109)
    sec23_442_md = slice_lines(l23, 110, 122)
    tbl3_md = slice_lines(l23, 123, 130)
    sec23_443_md = slice_lines(l23, 131, 147)
    tbl4_md = slice_lines(l23, 148, None)

    b_44_overview = write_prose_block(
        ch_dir,
        "p-ch04-sec-023-architecture-overview",
        "prose:ch04-sec-023-architecture-overview",
        sec23_intro_md,
        make_meta(
            "4.4 Design system architecture: enterprise architecture, interoperability and SMART Guidelines L3",
            "sec-023-44-design-system-architecture.md",
            [56],
            phc_terms=[
                "systems-architecture",
                "enterprise-architecture",
                "architecture",
                "architecture-building-blocks",
                "interoperability",
                "interoperability-standards",
                "smart-guidelines",
                "fast-healthcare-interoperability-resources",
            ],
            ra_terms=[
                "enterprise-architecture",
                "solution-architecture",
                "reference-architecture",
                "interoperability",
                "fast-healthcare-interoperability-resources",
                "smart-guidelines",
            ],
            elements=[
                "solutions-architect",
                "health-informatician",
                "pos-app",
                "interop-component",
                "interop-capability",
                "terminology-service",
                "limr",
                "shr",
                "dse",
            ],
            views=["pcposs", "interop-layer", "components", "shr", "cds"],
            sourceOnly="visual diagramming tool names (diagrams.net, Lucidchart, PowerPoint, Visio) are illustrative and not endorsed by WHO (dth-phc#1 §3b)",
        ),
        uses=["prose:ch04-sec-022-prototyping"],
        defines=["systems-architecture", "enterprise-architecture"],
    )

    b_441_domains = write_prose_block(
        ch_dir,
        "p-ch04-sec-023-architecture-domains",
        "prose:ch04-sec-023-architecture-domains",
        sec23_441_md + "\n" + sec23_441_post_md,
        make_meta(
            "4.4.1 Types of architecture (TOGAF viewpoints and OpenHIE reference model)",
            "sec-023-44-design-system-architecture.md",
            [56, 57],
            phc_terms=["architecture", "enterprise-architecture", "systems-architecture", "architecture-building-blocks"],
            ra_terms=[
                "enterprise-architecture",
                "reference-architecture",
                "solution-architecture",
                "business-domain",
                "data-object",
                "application-component",
                "digital-infrastructure",
            ],
            elements=["solutions-architect", "pos-app", "shr-repo", "dse", "terminology-service", "hwr", "facility-registry", "client-identity"],
            views=["pcposs", "components", "capabilities-goals"],
            referenceFrameworks={
                "TOGAF": "The Open Group Architecture Framework (refs. 65-67)",
                "OpenHIE": "Open Health Information Exchange reference architecture model (cited external reference model, ref. 72, per dth-phc#1 §3b)",
            },
        ),
        uses=["prose:ch04-sec-023-architecture-overview"],
    )

    b_tbl2 = write_table_block(
        ch_dir,
        "t-ch04-table-2",
        "tbl:2",
        "Table 2. Types of architecture domains",
        tbl2_md,
        make_meta(
            "Table 2. Types of architecture domains (Business, Data, Application, Technology)",
            "sec-023-44-design-system-architecture.md",
            [57],
            method="l1-table-formalized",
            phc_terms=["architecture", "enterprise-architecture", "systems-architecture", "business-process", "data-exchange"],
            ra_terms=["enterprise-architecture", "business-domain", "data-object", "application-component", "digital-infrastructure"],
            elements=["solutions-architect", "pos-app", "shr", "interop-component"],
            views=["pcposs", "components"],
            architectureDomains=[
                {"domain": "Business architecture", "archimateLayer": "Business Layer", "focus": "strategy, governance, organization and health system business processes"},
                {"domain": "Data architecture", "archimateLayer": "Data / Information Objects", "focus": "logical and physical data assets, data management resources, and data standards"},
                {"domain": "Application architecture", "archimateLayer": "Application Layer", "focus": "software applications, interactions, APIs and interoperability standards"},
                {"domain": "Technology architecture", "archimateLayer": "Technology Layer", "focus": "logical software and hardware components, infrastructure, middleware, networks and security"},
            ],
        ),
        uses=["prose:ch04-sec-023-architecture-domains"],
    )

    b_442_interop = write_prose_block(
        ch_dir,
        "p-ch04-sec-023-interoperability",
        "prose:ch04-sec-023-interoperability",
        sec23_442_md,
        make_meta(
            "4.4.2 Types of interoperability in health",
            "sec-023-44-design-system-architecture.md",
            [57],
            phc_terms=["interoperability", "interoperability-standards", "data-exchange", "terminologies", "classifications", "coding-schemes"],
            ra_terms=["interoperability", "health-information-exchange", "data-governance"],
            elements=["interop-capability", "interop-mgmt", "interop-component", "info-mediator", "terminology-service", "security-consent"],
            views=["interop-layer", "pcposs"],
        ),
        uses=["tbl:2"],
        defines=["interoperability"],
    )

    b_tbl3 = write_table_block(
        ch_dir,
        "t-ch04-table-3",
        "tbl:3",
        "Table 3. Types of interoperability in health",
        tbl3_md,
        make_meta(
            "Table 3. Types of interoperability in health (Syntactic, Semantic, Organizational, Legal)",
            "sec-023-44-design-system-architecture.md",
            [57],
            method="l1-table-formalized",
            phc_terms=[
                "interoperability",
                "interoperability-standards",
                "data-exchange",
                "terminologies",
                "classifications",
                "coding-schemes",
                "fast-healthcare-interoperability-resources",
                "international-classification-of-diseases",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
            ],
            ra_terms=[
                "interoperability",
                "fast-healthcare-interoperability-resources",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "snomed-gps",
                "data-governance",
            ],
            elements=["interop-capability", "interop-mgmt", "interop-component", "terminology-service", "limr", "security-consent"],
            views=["interop-layer", "pcposs"],
            interoperabilityTypes=[
                {
                    "id": "syntactic",
                    "name": "Syntactic interoperability",
                    "altName": "Structural interoperability",
                    "definition": "Ability of two or more systems to communicate and exchange structured data using specified data formats and communication protocols (e.g. HL7 FHIR, DICOM).",
                    "archimateElements": ["id-80856538cbd44167a37b276e38c994c3", "id-3c5d846710034c4595e206e748d65e36"],
                },
                {
                    "id": "semantic",
                    "name": "Semantic interoperability",
                    "definition": "Ability of systems to exchange data with unambiguous, shared meaning through standardized data models, terminologies, classifications and coding schemes (e.g. ICD-11, LOINC, SNOMED-GPS).",
                    "archimateElements": ["id-3f41de2b51c24041b08243bf72b140d1", "id-c0d39bf67fe64f54b07fbeb9bf37d404"],
                },
                {
                    "id": "organizational",
                    "name": "Organizational interoperability",
                    "definition": "Coordination of business processes, workflows, responsibilities and expectations across organizations and care levels so information is exchanged in a timely, actionable manner.",
                    "archimateElements": ["id-02200ff02be649ada1bf34a0a4d8e594", "id-18bf324b7b4753e0aeff853e6bcb6adc"],
                },
                {
                    "id": "legal",
                    "name": "Legal interoperability",
                    "definition": "Alignment of legal frameworks, data protection, privacy, consent and regulatory policies enabling lawful cross-organization and cross-border health data exchange.",
                    "archimateElements": ["id-d79aa0eec0584b0792b44bca408afeb6"],
                },
            ],
        ),
        uses=["prose:ch04-sec-023-interoperability"],
    )

    b_443_standards = write_prose_block(
        ch_dir,
        "p-ch04-sec-023-standards",
        "prose:ch04-sec-023-standards",
        sec23_443_md,
        make_meta(
            "4.4.3 Types of standards",
            "sec-023-44-design-system-architecture.md",
            [58],
            phc_terms=[
                "interoperability-standards",
                "open-standards",
                "terminologies",
                "classifications",
                "coding-schemes",
                "fast-healthcare-interoperability-resources",
                "international-classification-of-diseases",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
            ],
            ra_terms=[
                "interoperability",
                "fast-healthcare-interoperability-resources",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "snomed-gps",
            ],
            elements=["terminology-service", "limr", "interop-component", "security-consent", "health-informatician"],
            views=["interop-layer", "lmir-overview", "pcposs"],
        ),
        uses=["tbl:3"],
        defines=["interoperability-standards", "terminologies", "classifications", "coding-schemes"],
    )

    b_tbl4 = write_table_block(
        ch_dir,
        "t-ch04-table-4",
        "tbl:4",
        "Table 4. Types of standards",
        tbl4_md,
        make_meta(
            "Table 4. Types of standards (Semantic, Organizational, Syntactic, Legal)",
            "sec-023-44-design-system-architecture.md",
            [58, 59, 60],
            method="l1-table-formalized",
            phc_terms=[
                "interoperability-standards",
                "terminologies",
                "classifications",
                "coding-schemes",
                "fast-healthcare-interoperability-resources",
                "international-classification-of-diseases",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "smart-guidelines",
                "digital-adaptation-kits",
            ],
            ra_terms=[
                "interoperability",
                "fast-healthcare-interoperability-resources",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "snomed-gps",
                "smart-guidelines",
            ],
            elements=["terminology-service", "limr", "interop-component", "security-consent", "smart-l1", "smart-l2-dak"],
            views=["interop-layer", "lmir-overview", "pcposs"],
            standardsTypes=[
                {"interoperabilityType": "Semantic", "category": "Terminology and Classification Standards", "examples": ["ICD-11", "ICF", "ICHI", "LOINC", "SNOMED-GPS / SNOMED CT"]},
                {"interoperabilityType": "Organizational", "category": "Health Content standards", "examples": ["WHO SMART Guidelines", "WHO Digital Adaptation Kits (DAKs)"]},
                {"interoperabilityType": "Organizational", "category": "Digital health strategies", "examples": ["WHO Global strategy on digital health 2020–2025", "National digital health strategies"]},
                {"interoperabilityType": "Syntactic", "category": "Communication standards", "examples": ["HL7 FHIR", "IHE profiles", "DICOM", "ISO/IEEE 11073"]},
                {"interoperabilityType": "Legal", "category": "Privacy protection", "examples": ["National data protection acts (e.g. HIPAA, Thailand PDPA, Rwanda Data Protection Law)", "EU GDPR"]},
            ],
        ),
        uses=["prose:ch04-sec-023-standards"],
    )

    # sec-024: 4.5 Build and quality assurance
    l24, _, p24 = read_l1_section("sec-024-45-build-and-quality-assurance.md")
    sec24_md = slice_lines(l24, 1, None)

    b_45_build = write_prose_block(
        ch_dir,
        "p-ch04-sec-024-build-and-qa",
        "prose:ch04-sec-024-build-and-qa",
        sec24_md,
        make_meta(
            "4.5 Build and quality assurance",
            "sec-024-45-build-and-quality-assurance.md",
            [60, 61],
            phc_terms=["build", "beta-version", "minimum-viable-product", "devsecops", "technical-debt", "prototype"],
            ra_terms=["point-of-service-applications"],
            elements=["software-engineer", "technology-partner", "testing-platforms", "system-under-test", "test-cases", "test-operator", "pos-app"],
            views=["testing", "conformance", "pcposs", "shared-roles"],
            qaTestCategories=[
                "Installation testing",
                "Stress testing",
                "Security testing",
                "Graphic UI testing",
                "Integration testing",
                "Quality assurance testing",
                "Accessibility testing",
            ],
            sdlcAlignment={
                "compareWith": ["cat-harness/processes/crdm-deliver.bpmn"],
            },
        ),
        uses=["tbl:4"],
        defines=["build", "beta-version", "devsecops"],
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Chapter 4. Undertake design and adaptation",
        [
            ("Chapter overview and phase panel", "sec:ch04-lead", [b_lead, b_panel], True),
            ("4.1 Finalize software and vendor selection", "sec:4-1", [b_41_vendor], False),
            ("4.2 Validate functional requirements", "sec:4-2", [b_42_validate], False),
            ("4.3 Develop and test prototype design", "sec:4-3", [b_43_proto, b_fig15], False),
            ("4.4 Design system architecture", "sec:4-4", [b_44_overview, b_441_domains, b_tbl2, b_442_interop, b_tbl3, b_443_standards, b_tbl4], False),
            ("4.5 Build and quality assurance", "sec:4-5", [b_45_build], False),
        ],
        number=4,
    )
    return ch_slug


def build_ch01(folio_dir: Path):
    """Formalize Chapter 1: Introduction (sec-003..sec-006)."""
    ch_slug = "ch01-introduction"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    l03, _, _ = read_l1_section("sec-003-introduction.md")
    intro_lead_md = slice_lines(l03, 1, 65)
    fig1_tbl_md = slice_lines(l03, 66, 75)
    fig1_axis_md = slice_lines(l03, 76, 100)
    phc_eco_md = slice_lines(l03, 101, 124) + "\n" + slice_lines(l03, 162, 185)
    rec8_md = slice_lines(l03, 125, 161)
    fig3_md = slice_lines(l03, 186, 280)
    clerical_burden_md = slice_lines(l03, 281, None)

    b_intro_lead = write_prose_block(
        ch_dir,
        "p-ch01-sec-003-introduction",
        "prose:ch01-sec-003-introduction",
        intro_lead_md,
        make_meta(
            "Chapter 1. Introduction: From paper-based records to digital transformation at the point of service",
            "sec-003-introduction.md",
            [13, 14, 15],
            phc_terms=[
                "digitization",
                "digitalization",
                "digital-transformation",
                "digital-health",
                "point-of-service",
                "person-centred-point-of-service-system",
                "community-based-information-system",
                "decision-support-system",
                "electronic-health-record-system",
                "electronic-medical-record",
            ],
            ra_terms=["digital-health", "point-of-service-applications"],
            elements=["pos-app", "ehr-system", "dss", "chis", "phr", "health-worker", "health-service-user"],
            views=["pcposs"],
        ),
        defines=["digitization", "digitalization", "digital-transformation", "point-of-service"],
    )

    b_tbl_fig1 = write_table_block(
        ch_dir,
        "t-ch01-fig-1",
        "tbl:fig-1",
        "Fig. 1. From paper to digital: a transformational journey (comparison of Paper, Digitization, Digitalization and Digital transformation)",
        fig1_tbl_md,
        make_meta(
            "Fig. 1 table: From paper to digital: a transformational journey",
            "sec-003-introduction.md",
            [15],
            method="l1-table-formalized",
            phc_terms=[
                "digitization",
                "digitalization",
                "digital-transformation",
                "register",
                "interoperability-standards",
                "enterprise-architecture",
            ],
            ra_terms=["enterprise-architecture", "interoperability", "digital-infrastructure"],
            elements=["pos-app", "interop-capability", "shr"],
            views=["pcposs", "interop-layer"],
        ),
        uses=["prose:ch01-sec-003-introduction"],
    )

    b_fig1 = write_figure_block(
        ch_dir,
        "f-ch01-fig-1",
        "fig:1",
        "media/vfig-p015.png",
        "Fig. 1. From paper to digital: a transformational journey",
        15,
        "![Fig. 1. From paper to digital: a transformational journey](media/vfig-p015.png)\n\n" + fig1_axis_md,
        make_meta(
            "Fig. 1. From paper to digital: a transformational journey",
            "sec-003-introduction.md",
            [15],
            method="l1-vector-figure",
            phc_terms=["digitization", "digitalization", "digital-transformation"],
            elements=["pos-app"],
            views=["pcposs"],
        ),
        uses=["tbl:fig-1"],
    )

    b_rec8 = write_recommendation_block(
        ch_dir,
        "rec-who-2019-digital-tracking-decision-support",
        "rec:who-2019-digital-tracking-decision-support",
        (
            "> **Recommendation 8 (WHO 2019 Guideline on Digital Interventions for Health System Strengthening):** "
            "WHO recommends digital tracking of clients’ health status and services, combined with decision support under these conditions:\n"
            "> - in settings where the health system can support the implementation of these intervention components in an integrated manner; and\n"
            "> - for tasks that are already defined as within the scope of practice for the health worker.\n"
            "> *(Recommended only in specific contexts or conditions)*\n\n"
            "*Source: WHO guideline: recommendations on digital interventions for health system strengthening. Geneva: World Health Organization; 2019 (ref. 2; https://iris.who.int/handle/10665/311941).*"
        ),
        make_meta(
            "WHO 2019 Digital Guideline Recommendation 8: Digital tracking of clients' health status and services combined with decision support",
            "sec-003-introduction.md",
            [14, 16],
            method="l1-quoted-external-recommendation",
            phc_terms=[
                "digital-health-intervention",
                "longitudinal-tracking",
                "decision-support-system",
                "person-centred-point-of-service-system",
            ],
            ra_terms=["point-of-service-applications"],
            elements=["pos-app", "longitudinal-tracking", "dss", "dse", "health-worker", "health-service-user"],
            views=["pcposs", "cds"],
            externalSource={
                "title": "WHO guideline: recommendations on digital interventions for health system strengthening",
                "publisher": "World Health Organization",
                "date": "2019",
                "iris": "https://iris.who.int/handle/10665/311941",
                "recommendationNumber": "Recommendation 8",
                "note": "Quoted, cited recommendation of the 2019 WHO digital guideline, not a new dth-phc normative statement (dth-phc#1 §3b).",
            },
        ),
        strength={
            "list": "grade-recommendation-strength",
            "code": "conditional",
        },
        uses=["prose:ch01-sec-003-introduction"],
    )

    b_fig2 = write_figure_block(
        ch_dir,
        "f-ch01-fig-2",
        "fig:2",
        "media/vfig-p016.png",
        "Fig. 2. The 2019 WHO guideline: recommendations on digital interventions for health system strengthening",
        16,
        "![Fig. 2. The 2019 WHO guideline: recommendations on digital interventions for health system strengthening](media/vfig-p016.png)\n\n" + rec8_md,
        make_meta(
            "Fig. 2. The 2019 WHO guideline: recommendations on digital interventions for health system strengthening",
            "sec-003-introduction.md",
            [16],
            method="l1-vector-figure",
            phc_terms=["digital-health-intervention", "longitudinal-tracking", "decision-support-system"],
            elements=["longitudinal-tracking", "dss"],
            views=["pcposs"],
            reproduces={
                "source": "WHO guideline: recommendations on digital interventions for health system strengthening (2019)",
                "iris": "https://iris.who.int/handle/10665/311941",
            },
        ),
        uses=["rec:who-2019-digital-tracking-decision-support"],
    )

    b_phc_eco = write_prose_block(
        ch_dir,
        "p-ch01-sec-003-phc-digital-ecosystem",
        "prose:ch01-sec-003-phc-digital-ecosystem",
        phc_eco_md,
        make_meta(
            "Primary health care digital ecosystem and workflow-based optimization",
            "sec-003-introduction.md",
            [15, 16, 17],
            phc_terms=[
                "primary-health-care",
                "digital-health-ecosystem",
                "person-centred-point-of-service-system",
                "business-process",
                "workflow",
                "care-pathway",
                "longitudinal-tracking",
                "smart-guidelines",
            ],
            ra_terms=["point-of-service-applications", "smart-guidelines", "health-information-exchange"],
            elements=["pos-app", "ehr-system", "dss", "chis", "phr", "shr", "longitudinal-tracking", "analytics-platform"],
            views=["pcposs", "shr", "cds", "components"],
        ),
        uses=["rec:who-2019-digital-tracking-decision-support"],
    )

    b_fig3 = write_figure_block(
        ch_dir,
        "f-ch01-fig-3",
        "fig:3",
        "media/vfig-p017.png",
        "Fig. 3. Delivering an integrated ecosystem of information systems and digital health solutions supports the PHC approach",
        17,
        "![Fig. 3. Delivering an integrated ecosystem of information systems and digital health solutions supports the PHC approach](media/vfig-p017.png)\n\n" + fig3_md,
        make_meta(
            "Fig. 3. Primary health care digital ecosystem",
            "sec-003-introduction.md",
            [17],
            method="l1-vector-figure",
            phc_terms=["primary-health-care", "digital-health-ecosystem", "electronic-health-record-system", "community-based-information-system"],
            elements=["pos-app", "ehr-system", "dss", "chis", "phr", "analytics-platform"],
            views=["pcposs"],
        ),
        uses=["prose:ch01-sec-003-phc-digital-ecosystem"],
    )

    b_clerical = write_prose_block(
        ch_dir,
        "p-ch01-sec-003-clerical-burden",
        "prose:ch01-sec-003-clerical-burden",
        clerical_burden_md,
        make_meta(
            "Reasons for digitizing paper-based systems (clerical burden, workforce shortage and missed services)",
            "sec-003-introduction.md",
            [18],
            method="l1-source-only",
            phc_terms=["register", "care-pathway", "person-centred-point-of-service-system", "health-service-users"],
            elements=["pos-app", "health-worker", "health-service-user"],
            views=["pcposs"],
            sourceOnly="empirical claims on clerical burden, workforce shortage, and missed services: kept as cited L1 source block and excluded from formal content per dth-phc#1 §3b and §6",
        ),
        uses=["prose:ch01-sec-003-phc-digital-ecosystem"],
    )

    # sec-004: 1.1 Person-centred point of service systems
    l04, _, _ = read_l1_section("sec-004-11-person-centred-point-of-service-systems.md")
    sec04_body_md = slice_lines(l04, 1, 96)
    fig4_md = slice_lines(l04, 97, None)

    b_11_pcposs = write_prose_block(
        ch_dir,
        "p-ch01-sec-004-pcposs",
        "prose:ch01-sec-004-pcposs",
        sec04_body_md,
        make_meta(
            "1.1 Person-centred point of service systems (PCPOSS): four application types and 13 WHO DHI classification codes",
            "sec-004-11-person-centred-point-of-service-systems.md",
            [18, 19],
            phc_terms=[
                "person-centred-point-of-service-system",
                "person-centred",
                "point-of-service",
                "community-based-information-system",
                "decision-support-system",
                "electronic-health-record-system",
                "electronic-medical-record",
                "digital-health-intervention",
                "longitudinal-tracking",
                "interoperability-standards",
                "international-classification-of-diseases",
                "snomed-ct",
                "fast-healthcare-interoperability-resources",
                "technical-debt",
            ],
            ra_terms=[
                "point-of-service-applications",
                "interoperability",
                "fast-healthcare-interoperability-resources",
                "snomed-gps",
            ],
            elements=[
                "pos-app",
                "ehr-system",
                "dss",
                "chis",
                "phr",
                "health-worker",
                "health-service-user",
                "patients",
                "alerts-and-reminders",
                "longitudinal-tracking",
                "care-checklists",
                "clinical-screening",
                "indicator-reporting",
                "shr",
                "shr-repo",
                "dse",
                "terminology-service",
                "analytics-platform",
                "client-identity",
            ],
            views=["pcposs", "shr", "cds"],
            pcpossApplicationTypes=[
                {"id": "chis", "name": "Community-based information system", "archimateId": "id-3acafd57e8cc5d4198ffcb29d39c1184"},
                {"id": "dss", "name": "Decision support system", "archimateId": "id-bc2b3fab70bf5e48a3b043a7245c8f5f"},
                {"id": "ehr-system", "name": "Electronic health record system", "archimateId": "id-a9de9d3bebca5852b7b9c55519e7ab2d"},
                {"id": "phr", "name": "Personal health record", "archimateId": "id-9a31cf86a4685fb0ae0c460d973e2031"},
            ],
            dhiClassifications={
                "scheme": "WHO Classification of digital interventions, services and applications in health (2nd ed., 2023)",
                "iris": "https://iris.who.int/handle/10665/373581",
                "interventions": [
                    {"code": "1.1.3", "title": "Transmit targeted alerts and reminders to health service user(s)", "archimateId": "id-9d1f8abfb4905386b6a8ea65f421d115"},
                    {"code": "2.1.2", "title": "Enrol person(s) for health services/clinical care plan", "archimateId": "id-788f660553e14f0283b93c2dda3ae441"},
                    {"code": "2.2.1", "title": "Longitudinal tracking of a health service user’s health status and services", "archimateId": "id-74b83b6a6d8e53a99573467ad6f7ae41"},
                    {"code": "2.2.2", "title": "Manage person-centred structured clinical records", "archimateId": "id-a9de9d3bebca5852b7b9c55519e7ab2d"},
                    {"code": "2.2.3", "title": "Manage person-centred unstructured clinical records (e.g. notes, images, documents)", "archimateId": "id-0e6d89398fff4f20994a31b4de58e7d7"},
                    {"code": "2.2.4", "title": "Routine health indicator data collection and management", "archimateId": "id-ab03b92d0a8355bca5ce336ab2e2bf17"},
                    {"code": "2.3.1", "title": "Provide prompts and alerts according to protocols", "archimateId": "id-9d1f8abfb4905386b6a8ea65f421d115"},
                    {"code": "2.3.2", "title": "Provide checklists according to protocols", "archimateId": "id-0a635958abe251829d425db426340b00"},
                    {"code": "2.3.3", "title": "Screen persons by risk or other health status", "archimateId": "id-5890b78a30f25b1b8502a7fe0c9aac32"},
                    {"code": "2.5.2", "title": "Communication and performance feedback to health workers", "archimateId": "id-3fd92d497ca040c8a436f355c0b68770"},
                    {"code": "2.7.1", "title": "Identify persons in need of services", "archimateId": "id-5890b78a30f25b1b8502a7fe0c9aac32"},
                    {"code": "4.1.2", "title": "Data storage and aggregation", "archimateId": "id-0e6d89398fff4f20994a31b4de58e7d7"},
                    {"code": "4.1.3", "title": "Data synthesis and visualizations", "archimateId": "id-3fd92d497ca040c8a436f355c0b68770"},
                ],
            },
        ),
        uses=["prose:ch01-sec-003-introduction", "rec:who-2019-digital-tracking-decision-support"],
        defines=[
            "person-centred-point-of-service-system",
            "person-centred",
            "community-based-information-system",
            "decision-support-system",
            "electronic-health-record-system",
            "longitudinal-tracking",
        ],
    )

    b_fig4 = write_figure_block(
        ch_dir,
        "f-ch01-fig-4",
        "fig:4",
        "media/vfig-p019.png",
        "Fig. 4. The added value of “collect once, use for many purposes” principle",
        19,
        "![Fig. 4. The added value of “collect once, use for many purposes” principle](media/vfig-p019.png)\n\n" + fig4_md,
        make_meta(
            "Fig. 4. The added value of “collect once, use for many purposes” principle",
            "sec-004-11-person-centred-point-of-service-systems.md",
            [19],
            method="l1-vector-figure",
            phc_terms=["person-centred-point-of-service-system", "indicators-and-performance-metrics", "decision-support-system", "scheduling-logic"],
            elements=["pos-app", "shr", "indicator-reporting", "analytics-platform"],
            views=["pcposs", "shr"],
        ),
        uses=["prose:ch01-sec-004-pcposs"],
    )

    # sec-005: 1.2 SMART Guidelines
    l05, _, _ = read_l1_section("sec-005-12-smart-guidelines.md")
    sec05_body_md = slice_lines(l05, 1, 36)
    fig5_md = slice_lines(l05, 37, None)

    b_12_smart = write_prose_block(
        ch_dir,
        "p-ch01-sec-005-smart-guidelines",
        "prose:ch01-sec-005-smart-guidelines",
        sec05_body_md,
        make_meta(
            "1.2 SMART Guidelines: five knowledge layers (L1–L5) and country adaptation",
            "sec-005-12-smart-guidelines.md",
            [20],
            phc_terms=[
                "smart-guidelines",
                "digital-adaptation-kits",
                "health-interventions-and-recommendations",
                "reference-software",
                "fast-healthcare-interoperability-resources",
                "interoperability-standards",
            ],
            ra_terms=["smart-guidelines", "fast-healthcare-interoperability-resources", "interoperability"],
            elements=["smart-l1", "adapted-smart-l1", "smart-l2-dak", "adapted-smart-l2-dak", "limr", "dse", "pos-app"],
            views=["cds", "lmir-overview", "pcposs"],
            smartGuidelinesLayers=[
                {"layer": "L1", "name": "Narrative guidelines", "product": "Enhanced evidence-based guidelines and data recommendations"},
                {"layer": "L2", "name": "Operational guidelines", "product": "Digital Adaptation Kits (DAKs): personas, workflows, data dictionary, decision tables, indicators, requirements"},
                {"layer": "L3", "name": "Machine-readable guidelines", "product": "Structured, software-neutral specifications, FHIR Implementation Guides, CQL and terminology bindings"},
                {"layer": "L4", "name": "Executable guidelines", "product": "Reference software and interoperable digital components executing static algorithms"},
                {"layer": "L5", "name": "Dynamic guidelines", "product": "Executable dynamic algorithms and precision health models trained and optimized with advanced analytics"},
            ],
        ),
        uses=["prose:ch01-sec-004-pcposs"],
        defines=["smart-guidelines", "digital-adaptation-kits"],
    )

    b_fig5 = write_figure_block(
        ch_dir,
        "f-ch01-fig-5",
        "fig:5",
        "media/vfig-p020.png",
        "Fig. 5. WHO SMART Guidelines approach",
        20,
        "![Fig. 5. WHO SMART Guidelines approach](media/vfig-p020.png)\n\n" + fig5_md,
        make_meta(
            "Fig. 5. WHO SMART Guidelines approach",
            "sec-005-12-smart-guidelines.md",
            [20],
            method="l1-vector-figure",
            phc_terms=["smart-guidelines", "digital-adaptation-kits", "reference-software"],
            elements=["smart-l1", "adapted-smart-l1", "smart-l2-dak", "adapted-smart-l2-dak"],
            views=["cds", "pcposs"],
        ),
        uses=["prose:ch01-sec-005-smart-guidelines"],
    )

    # sec-006: 1.3 How this handbook was developed
    l06, _, _ = read_l1_section("sec-006-13-how-this-handbook-was-developed.md")
    sec06_md = slice_lines(l06, 1, None)

    b_13_dev = write_prose_block(
        ch_dir,
        "p-ch01-sec-006-how-developed",
        "prose:ch01-sec-006-how-developed",
        sec06_md,
        make_meta(
            "1.3 How this handbook was developed (CRDM, Principles for Digital Development, and country consultations)",
            "sec-006-13-how-this-handbook-was-developed.md",
            [21],
            phc_terms=["collaborative-requirements-development-methodology", "person-centred-point-of-service-system"],
            elements=["business-analyst", "health-worker", "health-service-user"],
            views=["shared-roles", "pcposs"],
            sdlcAlignment={
                "crdmSources": ["PHII 2023 (ref. 20)", "PATH 2012 (ref. 50)"],
                "catHarnessSkills": ["cat-harness/skills/sdlc/crdm/"],
            },
            sourceOnly="country consultation history (Bangladesh, Pakistan, Indonesia) and conflict-of-interest declarations: cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["prose:ch01-sec-005-smart-guidelines"],
        defines=["collaborative-requirements-development-methodology"],
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Chapter 1. Introduction",
        [
            ("Introduction and WHO Digital Guideline Recommendation 8", "sec:1-0", [b_intro_lead, b_tbl_fig1, b_fig1, b_rec8, b_fig2, b_phc_eco, b_fig3, b_clerical], True),
            ("1.1 Person-centred point of service systems", "sec:1-1", [b_11_pcposs, b_fig4], False),
            ("1.2 SMART Guidelines", "sec:1-2", [b_12_smart, b_fig5], False),
            ("1.3 How this handbook was developed", "sec:1-3", [b_13_dev], False),
        ],
        number=1,
    )
    return ch_slug


def build_ch02(folio_dir: Path):
    """Formalize Chapter 2: How to use this handbook (sec-007..sec-011)."""
    ch_slug = "ch02-how-to-use"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    # sec-007: 2.1 Targeted scenarios of digital readiness
    l07, _, _ = read_l1_section("sec-007-21-targeted-scenarios-of-digital-readiness.md")
    sec07_md = slice_lines(l07, 1, None)

    b_21_scenarios = write_prose_block(
        ch_dir,
        "p-ch02-sec-007-readiness-scenarios",
        "prose:ch02-sec-007-readiness-scenarios",
        sec07_md,
        make_meta(
            "2.1 Targeted scenarios of digital readiness (paper-only vs partly digitized)",
            "sec-007-21-targeted-scenarios-of-digital-readiness.md",
            [22, 23],
            phc_terms=[
                "person-centred-point-of-service-system",
                "digitization",
                "digitalization",
                "legacy-system",
                "register",
                "care-pathway",
                "interoperability",
            ],
            ra_terms=["point-of-service-applications", "interoperability"],
            elements=["pos-app", "public-health-authority", "shr"],
            views=["pcposs"],
            readinessScenarios=[
                {
                    "id": "paper-only",
                    "name": "Starting from a paper-only system",
                    "description": "No PCPOSS in place; only paper-based records and registers are used at the point of care for service delivery and reporting.",
                },
                {
                    "id": "partly-digitized",
                    "name": "Starting with some parts of the system already digitized",
                    "description": "Disparate or siloed digital systems exist in parallel with paper records, with limited functionality, health domain coverage, or interoperability.",
                },
            ],
            dmnCandidate={
                "table": "Starting scenario",
                "section": "2.1",
                "inputs": ["any PCPOSS in place?", "comprehensive and interoperable?"],
                "output": "paper-only or partly-digitized, and entry step",
            },
            sourceOnly="narrative framing of readiness scenarios: cited L1 narrative per dth-phc#1 §3b",
        ),
    )

    # sec-008: 2.2 Targeted users
    l08, _, _ = read_l1_section("sec-008-22-targeted-users.md")
    sec08_md = slice_lines(l08, 1, None)

    b_22_users = write_prose_block(
        ch_dir,
        "p-ch02-sec-008-targeted-users",
        "prose:ch02-sec-008-targeted-users",
        sec08_md,
        make_meta(
            "2.2 Targeted users of this handbook",
            "sec-008-22-targeted-users.md",
            [23, 24],
            phc_terms=["end-user", "health-service-users", "person-centred-point-of-service-system", "requirements"],
            ra_terms=["stakeholder", "point-of-service-applications"],
            elements=[
                "business-analyst",
                "health-informatician",
                "public-health-authority",
                "implementing-team",
                "designer",
                "technology-partner",
                "health-worker",
                "health-service-user",
            ],
            views=["shared-roles", "pcposs"],
            targetRoles=[
                {"role": "Business analyst", "scope": "smart-ra shared role", "reuse": "smart-base SGAuthoring.Persona.BusinessAnalyst"},
                {"role": "Health informatician", "scope": "smart-ra shared role"},
                {"role": "Public health authority", "scope": "smart-ra shared actor"},
                {"role": "Implementing team", "scope": "smart-ra shared actor"},
                {"role": "Designer", "scope": "smart-ra shared role"},
                {"role": "Technology partner (software vendor)", "scope": "smart-ra shared role"},
                {"role": "Donors and development partners", "scope": "dth-phc reader only (not a process actor)"},
                {"role": "Health worker", "scope": "end-user consulted throughout"},
                {"role": "Health service user", "scope": "end-user consulted throughout"},
            ],
        ),
        uses=["prose:ch02-sec-007-readiness-scenarios"],
    )

    # sec-009: 2.3 Before using this resource
    l09, _, _ = read_l1_section("sec-009-23-before-using-this-resource.md")
    sec09_pre_md = slice_lines(l09, 1, 36)
    fig6_md = slice_lines(l09, 37, 307)
    sec09_post_md = slice_lines(l09, 308, None)

    b_23_prereq = write_prose_block(
        ch_dir,
        "p-ch02-sec-009-prerequisites",
        "prose:ch02-sec-009-prerequisites",
        sec09_pre_md + "\n" + sec09_post_md,
        make_meta(
            "2.3 Before using this resource: DIIG prerequisites, enterprise architecture and Box 1 Unique identifiers",
            "sec-009-23-before-using-this-resource.md",
            [24, 25, 26],
            phc_terms=[
                "enterprise-architecture",
                "interoperability-standards",
                "registry",
                "register",
                "health-service-users-health-records",
                "person-centred-point-of-service-system",
            ],
            ra_terms=["enterprise-architecture", "registry", "interoperability", "data-governance"],
            elements=["client-identity", "hwr", "facility-registry", "shr", "security-consent", "public-health-authority"],
            views=["pcposs", "shr", "components"],
        ),
        uses=["prose:ch02-sec-008-targeted-users"],
        defines=["registry"],
    )

    b_fig6 = write_figure_block(
        ch_dir,
        "f-ch02-fig-6",
        "fig:6",
        "media/vfig-p024.png",
        "Fig. 6. Planning and implementing a digital health enterprise: phases, steps and resources",
        24,
        "![Fig. 6. Planning and implementing a digital health enterprise: phases, steps and resources](media/vfig-p024.png)\n\n" + fig6_md,
        make_meta(
            "Fig. 6. Planning and implementing a digital health enterprise: phases, steps and resources (reproduced from WHO DIIG Fig. 1.1.1)",
            "sec-009-23-before-using-this-resource.md",
            [24],
            method="l1-vector-figure",
            phc_terms=["enterprise-architecture", "systems-architecture", "interoperability"],
            ra_terms=["enterprise-architecture"],
            elements=["public-health-authority", "implementing-team", "pos-app"],
            views=["pcposs", "shared-roles"],
            reproduces={
                "source": "WHO Digital implementation investment guide (DIIG): integrating digital interventions into health programmes (2020), Fig. 1.1.1",
                "library": "9789240015029-eng",
                "iris": "https://iris.who.int/handle/10665/334306",
                "note": "DIIG Fig. 1.1.1 is linked via reproduces and never redrawn (dth-phc#1 §3b).",
            },
        ),
        uses=["prose:ch02-sec-009-prerequisites"],
    )

    # sec-010: 2.4 The stepwise approaches to digitizing
    l10, _, _ = read_l1_section("sec-010-24-the-stepwise-approaches-to-digitizing.md")
    sec10_body_md = slice_lines(l10, 1, 47) + "\n" + slice_lines(l10, 99, None)
    fig7_md = slice_lines(l10, 48, 98)

    b_24_steps = write_prose_block(
        ch_dir,
        "p-ch02-sec-010-stepwise-approach",
        "prose:ch02-sec-010-stepwise-approach",
        sec10_body_md,
        make_meta(
            "2.4 The stepwise approaches to digitizing (four phases mapped to DIIG and iterative agile MVP loop)",
            "sec-010-24-the-stepwise-approaches-to-digitizing.md",
            [26, 27],
            phc_terms=[
                "person-centred-point-of-service-system",
                "minimum-viable-product",
                "requirements",
                "prototype",
                "user-acceptance-testing",
                "deploy",
            ],
            ra_terms=["point-of-service-applications"],
            elements=["implementing-team", "business-analyst", "technology-partner", "pos-app"],
            views=["pcposs", "shared-roles"],
            phases=[
                {"step": 1, "chapter": 3, "title": "Understand user requirements", "diigPhases": [3], "summary": "Gather user personas, use cases, workflows, data dictionary, decision logic, schedules and prioritized requirements."},
                {"step": 2, "chapter": 4, "title": "Undertake design and adaptation", "diigPhases": [4], "summary": "Select software/vendor, validate requirements, prototype UI, design system architecture and build/test beta MVP."},
                {"step": 3, "chapter": 5, "title": "Conduct training, testing and roll-out", "diigPhases": [5, 6], "summary": "Train users and support teams, conduct UAT with test cases/data, deploy and establish maintenance/feedback loops."},
                {"step": 4, "chapter": 6, "title": "Scale up the system", "diigPhases": [6, 7], "summary": "Assess readiness to scale, plan and execute staged legacy/paper phase-out, monitor objectives and manage change."},
            ],
            sdlcAlignment={
                "structuralMapping": "cat-harness/library/arxiv-2404.04834v4",
                "mvpLoopCompareWith": "cat-harness/processes/crdm-deliver.bpmn",
            },
        ),
        uses=["fig:6"],
        defines=["minimum-viable-product"],
    )

    b_fig7 = write_figure_block(
        ch_dir,
        "f-ch02-fig-7",
        "fig:7",
        "media/vfig-p026.png",
        "Fig. 7. Steps in this handbook to optimize a person-centred point of service system (PCPOSS)",
        26,
        "![Fig. 7. Steps in this handbook to optimize a person-centred point of service system (PCPOSS)](media/vfig-p026.png)\n\n" + fig7_md,
        make_meta(
            "Fig. 7. Steps in this handbook to optimize a PCPOSS (with iterative agile MVP build-and-test loop)",
            "sec-010-24-the-stepwise-approaches-to-digitizing.md",
            [26],
            method="l1-vector-figure",
            phc_terms=["person-centred-point-of-service-system", "minimum-viable-product", "build", "deploy"],
            elements=["pos-app", "implementing-team", "technology-partner"],
            views=["pcposs", "shared-roles"],
        ),
        uses=["prose:ch02-sec-010-stepwise-approach"],
    )

    # sec-011: 2.5 Choices for software and digital applications
    l11, _, _ = read_l1_section("sec-011-25-choices-for-software-and-digital-applications.md")
    sec11_md = slice_lines(l11, 1, None)

    b_25_choices = write_prose_block(
        ch_dir,
        "p-ch02-sec-011-software-choices",
        "prose:ch02-sec-011-software-choices",
        sec11_md,
        make_meta(
            "2.5 Choices for software and digital applications",
            "sec-011-25-choices-for-software-and-digital-applications.md",
            [27],
            phc_terms=["reference-software", "software-platform", "open-source", "open-standards", "interoperability-standards"],
            ra_terms=["point-of-service-applications", "interoperability"],
            elements=["pos-app", "technology-partner"],
            views=["pcposs"],
            sourceOnly="software-choice advice (adapting existing platforms vs bespoke development): cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["prose:ch02-sec-010-stepwise-approach"],
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Chapter 2. How to use this handbook",
        [
            ("2.1 Targeted scenarios of digital readiness", "sec:2-1", [b_21_scenarios], True),
            ("2.2 Targeted users", "sec:2-2", [b_22_users], False),
            ("2.3 Before using this resource", "sec:2-3", [b_23_prereq, b_fig6], False),
            ("2.4 The stepwise approaches to digitizing", "sec:2-4", [b_24_steps, b_fig7], False),
            ("2.5 Choices for software and digital applications", "sec:2-5", [b_25_choices], False),
        ],
        number=2,
    )
    return ch_slug


def build_ch05(folio_dir: Path):
    """Formalize Chapter 5: Conduct training, testing and roll-out (sec-025..sec-028)."""
    ch_slug = "ch05-training-testing-rollout"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    l25, _, _ = read_l1_section("sec-025-51-develop-and-conduct-training.md")
    lead_md = slice_lines(l25, 1, 5)
    panel_md = slice_lines(l25, 6, 11)
    training_md = slice_lines(l25, 12, None)

    b_lead = write_prose_block(
        ch_dir,
        "p-ch05-overview",
        "prose:ch05-overview",
        lead_md,
        make_meta(
            "Chapter 5 overview: Conduct training, testing and roll-out",
            "sec-025-51-develop-and-conduct-training.md",
            [62],
            phc_terms=["person-centred-point-of-service-system", "beta-version", "user-acceptance-testing", "deploy"],
            ra_terms=["point-of-service-applications"],
            elements=["implementing-team", "technology-partner", "health-worker", "pos-app"],
            views=["pcposs", "shared-roles", "testing"],
        ),
    )

    b_panel = write_table_block(
        ch_dir,
        "t-ch05-phase-panel",
        "tbl:ch05-phase-panel",
        "Chapter 5 phase panel: Who should be involved, Inputs, Tools and Outputs for training, testing and roll-out",
        panel_md,
        make_meta(
            "Chapter 5 phase panel (Who should be involved / Inputs / Tools / Outputs)",
            "sec-025-51-develop-and-conduct-training.md",
            [62],
            method="l1-phase-panel-formalized",
            phc_terms=["beta-version", "user-acceptance-testing", "deploy", "person-centred-point-of-service-system"],
            ra_terms=["point-of-service-applications"],
            elements=["implementing-team", "technology-partner", "health-worker", "public-health-authority", "testing-platforms", "test-cases", "pos-app"],
            views=["pcposs", "shared-roles", "testing", "conformance"],
            phasePanel={
                "phase": 3,
                "chapter": 5,
                "title": "Conduct training, testing and roll-out",
                "diigPhases": [5, 6],
                "roles": ["implementing-team", "technology-partner", "health-worker", "public-health-authority"],
                "inputs": ["Beta version of the person-centred point of service system (PCPOSS)"],
                "tools": ["Testing checklist"],
                "outputs": ["Training materials", "A deployed and rolled-out PCPOSS"],
            },
        ),
        uses=["prose:ch05-overview"],
    )

    b_51_training = write_prose_block(
        ch_dir,
        "p-ch05-sec-025-training",
        "prose:ch05-sec-025-training",
        training_md,
        make_meta(
            "5.1 Develop and conduct training (5.1.1 Training on use, 5.1.2 Training on maintenance)",
            "sec-025-51-develop-and-conduct-training.md",
            [62, 63, 64],
            phc_terms=["end-user", "person-centred-point-of-service-system", "workflow"],
            elements=["implementing-team", "technology-partner", "health-worker"],
            views=["shared-roles", "pcposs"],
            sourceOnly="training delivery and curriculum advice: cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["tbl:ch05-phase-panel"],
    )

    # sec-026: 5.2 Test user acceptance and deployment readiness
    l26, _, _ = read_l1_section("sec-026-52-test-user-acceptance-and-deployment-readiness.md")
    sec26_md = slice_lines(l26, 1, None)

    b_52_uat = write_prose_block(
        ch_dir,
        "p-ch05-sec-026-uat",
        "prose:ch05-sec-026-uat",
        sec26_md,
        make_meta(
            "5.2 Test user acceptance and deployment readiness (5.2.1 Test cases and test data)",
            "sec-026-52-test-user-acceptance-and-deployment-readiness.md",
            [64, 65],
            phc_terms=["user-acceptance-testing", "beta-version", "use-case", "user-story", "functional-requirements", "non-functional-requirements"],
            ra_terms=["point-of-service-applications"],
            elements=["testing-platforms", "test-cases", "system-under-test", "test-operator", "health-worker", "implementing-team", "technology-partner"],
            views=["testing", "conformance", "pcposs", "shared-roles"],
            methodStep={
                "stepId": "5.2",
                "title": "Test user acceptance and deployment readiness",
                "substeps": ["5.2.1 Test cases and test data"],
                "producesDakComponents": ["smart-base:TestScenario"],
                "dakKind": "test-scenario",
                "sdlcAlignment": {
                    "catHarnessSkill": "cat-harness/skills/sdlc/sdlc-core/test-plan-execution.md",
                },
            },
        ),
        uses=["prose:ch05-sec-025-training"],
        defines=["user-acceptance-testing"],
    )

    # sec-027: 5.3 Deploy the system
    l27, _, _ = read_l1_section("sec-027-53-deploy-the-system.md")
    sec27_md = slice_lines(l27, 1, None)

    b_53_deploy = write_prose_block(
        ch_dir,
        "p-ch05-sec-027-deploy",
        "prose:ch05-sec-027-deploy",
        sec27_md,
        make_meta(
            "5.3 Deploy the system",
            "sec-027-53-deploy-the-system.md",
            [65],
            phc_terms=["deploy", "person-centred-point-of-service-system", "legacy-system", "register"],
            elements=["implementing-team", "technology-partner", "pos-app", "health-worker"],
            views=["pcposs", "shared-roles"],
            sourceOnly="deployment operational and phased roll-out advice: cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["prose:ch05-sec-026-uat"],
        defines=["deploy"],
    )

    # sec-028: 5.4 Manage feedback and system maintenance
    l28, _, _ = read_l1_section("sec-028-54-manage-feedback-and-system-maintenance.md")
    sec28_md = slice_lines(l28, 1, None)

    b_54_maint = write_prose_block(
        ch_dir,
        "p-ch05-sec-028-maintenance",
        "prose:ch05-sec-028-maintenance",
        sec28_md,
        make_meta(
            "5.4 Manage feedback and system maintenance",
            "sec-028-54-manage-feedback-and-system-maintenance.md",
            [65],
            phc_terms=["deploy", "devsecops", "technical-debt", "person-centred-point-of-service-system"],
            elements=["implementing-team", "technology-partner", "software-engineer", "pos-app"],
            views=["pcposs", "shared-roles"],
        ),
        uses=["prose:ch05-sec-027-deploy"],
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Chapter 5. Conduct training, testing and roll-out",
        [
            ("Chapter overview and phase panel", "sec:ch05-lead", [b_lead, b_panel], True),
            ("5.1 Develop and conduct training", "sec:5-1", [b_51_training], False),
            ("5.2 Test user acceptance and deployment readiness", "sec:5-2", [b_52_uat], False),
            ("5.3 Deploy the system", "sec:5-3", [b_53_deploy], False),
            ("5.4 Manage feedback and system maintenance", "sec:5-4", [b_54_maint], False),
        ],
        number=5,
    )
    return ch_slug


def build_ch06(folio_dir: Path):
    """Formalize Chapter 6: Scale up the system (sec-029..sec-033)."""
    ch_slug = "ch06-scale-up"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    l29, _, _ = read_l1_section("sec-029-61-determine-readiness-for-scaling-up.md")
    lead_md = slice_lines(l29, 1, 7)
    panel_md = slice_lines(l29, 8, 13)
    sec29_body_md = slice_lines(l29, 14, None)

    b_lead = write_prose_block(
        ch_dir,
        "p-ch06-overview",
        "prose:ch06-overview",
        lead_md,
        make_meta(
            "Chapter 6 overview: Scale up the system",
            "sec-029-61-determine-readiness-for-scaling-up.md",
            [66],
            phc_terms=["person-centred-point-of-service-system", "mhealth-assessment-and-planning-for-scale", "legacy-system"],
            ra_terms=["point-of-service-applications"],
            elements=["public-health-authority", "ministry-of-health", "implementing-team", "me-specialist", "pos-app"],
            views=["pcposs", "shared-roles"],
            diigPhase=7,
        ),
    )

    b_panel = write_table_block(
        ch_dir,
        "t-ch06-phase-panel",
        "tbl:ch06-phase-panel",
        "Chapter 6 phase panel: Who should be involved, Inputs, Tools and Outputs for scaling up the system",
        panel_md,
        make_meta(
            "Chapter 6 phase panel (Who should be involved / Inputs / Tools / Outputs)",
            "sec-029-61-determine-readiness-for-scaling-up.md",
            [66],
            method="l1-phase-panel-formalized",
            phc_terms=[
                "person-centred-point-of-service-system",
                "mhealth-assessment-and-planning-for-scale",
                "legacy-system",
                "indicators-and-performance-metrics",
            ],
            ra_terms=["point-of-service-applications", "stakeholder"],
            elements=[
                "public-health-authority",
                "ministry-of-health",
                "implementing-team",
                "technology-partner",
                "me-specialist",
                "health-worker",
                "health-service-user",
                "analytics-platform",
                "pos-app",
            ],
            views=["pcposs", "shared-roles"],
            phasePanel={
                "phase": 4,
                "chapter": 6,
                "title": "Scale up the system",
                "diigPhase": 7,
                "roles": [
                    "public-health-authority",
                    "implementing-team",
                    "technology-partner",
                    "me-specialist",
                    "health-worker",
                    "health-service-user",
                ],
                "inputs": ["Live version of your PCPOSS being used"],
                "tools": [
                    "Monitoring and evaluating digital health interventions (WHO 2016, ref. 99)",
                    "The MAPS toolkit: mHealth assessment and planning for scale (WHO 2015, ref. 100)",
                ],
                "outputs": [
                    "Set of objectives and benchmarks the PCPOSS will need to meet before phasing out paper or legacy systems",
                    "Plan for phasing out paper or legacy systems",
                    "Change management strategy",
                ],
            },
        ),
        uses=["prose:ch06-overview"],
    )

    b_61_readiness = write_prose_block(
        ch_dir,
        "p-ch06-sec-029-readiness-to-scale",
        "prose:ch06-sec-029-readiness-to-scale",
        sec29_body_md,
        make_meta(
            "6.1 Determine readiness for scaling up",
            "sec-029-61-determine-readiness-for-scaling-up.md",
            [66, 67, 68],
            phc_terms=[
                "mhealth-assessment-and-planning-for-scale",
                "person-centred-point-of-service-system",
                "interoperability",
                "enterprise-architecture",
            ],
            ra_terms=["enterprise-architecture", "interoperability", "point-of-service-applications"],
            elements=["public-health-authority", "implementing-team", "me-specialist", "pos-app"],
            views=["pcposs", "shared-roles"],
            dmnCandidate={
                "table": "Scale-up readiness and legacy system phase-out",
                "section": "6.1, 6.2",
                "inputs": ["PCPOSS ready?", "health system ready?", "objectives met?"],
                "output": "proceed with scale-up / legacy phase-out or continue stabilization",
            },
        ),
        uses=["tbl:ch06-phase-panel"],
    )

    # sec-030: 6.2 Plan for phase-out of legacy system(s)
    l30, _, _ = read_l1_section("sec-030-62-plan-for-phase-out-of-legacy-systems.md")
    sec30_body_md = slice_lines(l30, 1, 63)
    tbl5_md = slice_lines(l30, 64, None)

    b_62_plan = write_prose_block(
        ch_dir,
        "p-ch06-sec-030-plan-legacy-phaseout",
        "prose:ch06-sec-030-plan-legacy-phaseout",
        sec30_body_md,
        make_meta(
            "6.2 Plan for phase-out of legacy system(s)",
            "sec-030-62-plan-for-phase-out-of-legacy-systems.md",
            [68, 69, 70],
            phc_terms=[
                "legacy-system",
                "register",
                "person-centred-point-of-service-system",
                "health-service-users-health-records",
                "indicators-and-performance-metrics",
                "data-exchange",
            ],
            ra_terms=["point-of-service-applications", "repository"],
            elements=["pos-app", "shr", "shr-repo", "analytics-platform", "public-health-authority", "me-specialist"],
            views=["pcposs", "shr", "shared-roles"],
        ),
        uses=["prose:ch06-sec-029-readiness-to-scale"],
        defines=["legacy-system"],
    )

    b_tbl5 = write_table_block(
        ch_dir,
        "t-ch06-table-5",
        "tbl:5",
        "Table 5. Key indicators of whether a digital system meets its objectives",
        tbl5_md,
        make_meta(
            "Table 5. Key indicators of whether a digital system meets its objectives",
            "sec-030-62-plan-for-phase-out-of-legacy-systems.md",
            [69, 70],
            method="l1-table-formalized",
            phc_terms=["indicators-and-performance-metrics", "person-centred-point-of-service-system", "legacy-system", "end-user"],
            elements=["me-specialist", "analytics-platform", "indicator-reporting", "pos-app"],
            views=["pcposs", "shared-roles"],
        ),
        uses=["prose:ch06-sec-030-plan-legacy-phaseout"],
    )

    # sec-031: 6.3 Monitor and evaluate progress on objectives
    l31, _, _ = read_l1_section("sec-031-63-monitor-and-evaluate-progress-on-objectives.md")
    sec31_md = slice_lines(l31, 1, None)

    b_63_monitor = write_prose_block(
        ch_dir,
        "p-ch06-sec-031-monitoring",
        "prose:ch06-sec-031-monitoring",
        sec31_md,
        make_meta(
            "6.3 Monitor and evaluate progress on objectives",
            "sec-031-63-monitor-and-evaluate-progress-on-objectives.md",
            [71],
            phc_terms=["indicators-and-performance-metrics", "digital-health-intervention", "person-centred-point-of-service-system"],
            elements=["me-specialist", "analytics-platform", "indicator-reporting", "public-health-authority"],
            views=["pcposs", "shared-roles"],
            sourceOnly="monitoring and evaluation guidance pointer (WHO 2016 ref. 99): cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["tbl:5"],
    )

    # sec-032: 6.4 Phase-out of legacy system(s)
    l32, _, _ = read_l1_section("sec-032-64-phase-out-of-legacy-systems.md")
    sec32_md = slice_lines(l32, 1, None)

    b_64_phaseout = write_prose_block(
        ch_dir,
        "p-ch06-sec-032-execute-legacy-phaseout",
        "prose:ch06-sec-032-execute-legacy-phaseout",
        sec32_md,
        make_meta(
            "6.4 Phase-out of legacy system(s) and emergency paper backup resilience",
            "sec-032-64-phase-out-of-legacy-systems.md",
            [71],
            phc_terms=["legacy-system", "register", "health-service-users-health-records", "person-centred-point-of-service-system"],
            elements=["public-health-authority", "implementing-team", "health-worker", "pos-app"],
            views=["pcposs", "shared-roles"],
        ),
        uses=["prose:ch06-sec-030-plan-legacy-phaseout"],
    )

    # sec-033: 6.5 Adopt change management practices
    l33, _, _ = read_l1_section("sec-033-65-adopt-change-management-practices.md")
    sec33_md = slice_lines(l33, 1, None)

    b_65_change = write_prose_block(
        ch_dir,
        "p-ch06-sec-033-change-management",
        "prose:ch06-sec-033-change-management",
        sec33_md,
        make_meta(
            "6.5 Adopt change management practices and SMART Guidelines Layer 5 (Dynamic guidelines)",
            "sec-033-65-adopt-change-management-practices.md",
            [71, 72],
            phc_terms=["smart-guidelines", "person-centred-point-of-service-system", "legacy-system"],
            ra_terms=["smart-guidelines"],
            elements=["public-health-authority", "implementing-team", "health-worker", "analytics-platform"],
            views=["pcposs", "shared-roles"],
            sourceOnly="change-management advice: cited L1 narrative per dth-phc#1 §3b",
        ),
        uses=["prose:ch06-sec-032-execute-legacy-phaseout"],
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Chapter 6. Scale up the system",
        [
            ("Chapter overview and phase panel", "sec:ch06-lead", [b_lead, b_panel], True),
            ("6.1 Determine readiness for scaling up", "sec:6-1", [b_61_readiness], False),
            ("6.2 Plan for phase-out of legacy system(s)", "sec:6-2", [b_62_plan, b_tbl5], False),
            ("6.3 Monitor and evaluate progress on objectives", "sec:6-3", [b_63_monitor], False),
            ("6.4 Phase-out of legacy system(s)", "sec:6-4", [b_64_phaseout], False),
            ("6.5 Adopt change management practices", "sec:6-5", [b_65_change], False),
        ],
        number=6,
    )
    return ch_slug


def build_front_matter(folio_dir: Path):
    """Build Front matter chapter (sec-front-matter, sec-000, sec-001, sec-002)."""
    ch_slug = "front-matter"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    lfm, _, pfm = read_l1_section("sec-front-matter.md")
    l00, _, p00 = read_l1_section("sec-000-acknowledgements.md")
    l01, _, p01 = read_l1_section("sec-001-abbreviations.md")
    l02, _, p02 = read_l1_section("sec-002-glossary.md")

    b_fm = write_prose_block(
        ch_dir,
        "p-fm-publication-metadata",
        "prose:fm-publication-metadata",
        clean_front_matter(lfm),
        make_meta(
            "Publication metadata and licensing",
            "sec-front-matter.md",
            pfm,
            method="l1-front-matter",
            phc_terms=["primary-health-care", "person-centred-point-of-service-system"],
            ra_terms=["point-of-service-applications"],
            elements=["pos-app"],
            views=["pcposs"],
        ),
    )

    b_ack = write_prose_block(
        ch_dir,
        "p-fm-acknowledgements",
        "prose:fm-acknowledgements",
        slice_lines(l00, 1, None),
        make_meta(
            "Acknowledgements",
            "sec-000-acknowledgements.md",
            p00,
            method="l1-front-matter",
            phc_terms=["special-programme-of-research-in-human-reproduction", "primary-health-care"],
            sourceOnly="contributor and funder acknowledgements: cited L1 front matter",
        ),
    )

    b_abbr = write_table_block(
        ch_dir,
        "t-fm-abbreviations",
        "tbl:abbreviations",
        "Abbreviations",
        slice_lines(l01, 1, None),
        make_meta(
            "Abbreviations (35 acronyms)",
            "sec-001-abbreviations.md",
            p01,
            method="l1-table-formalized",
            phc_terms=[
                "antenatal-care",
                "collaborative-requirements-development-methodology",
                "diastolic-blood-pressure",
                "digital-adaptation-kits",
                "digital-health-intervention",
                "electronic-health-record-system",
                "electronic-medical-record",
                "enterprise-architecture",
                "fast-healthcare-interoperability-resources",
                "health-information-system",
                "health-management-information-system",
                "international-classification-of-diseases",
                "logical-observation-identifiers-names-and-codes",
                "mhealth-assessment-and-planning-for-scale",
                "minimum-viable-product",
                "person-centred-point-of-service-system",
                "point-of-service",
                "primary-health-care",
                "snomed-ct",
                "special-programme-of-research-in-human-reproduction",
                "systolic-blood-pressure",
                "user-acceptance-testing",
            ],
            ra_terms=[
                "enterprise-architecture",
                "fast-healthcare-interoperability-resources",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "snomed-gps",
            ],
        ),
    )

    b_gloss = write_table_block(
        ch_dir,
        "t-fm-glossary",
        "tbl:glossary",
        "Glossary (59 defined terms and 24 glossary references)",
        slice_lines(l02, 1, None),
        make_meta(
            "Glossary and glossary references",
            "sec-002-glossary.md",
            p02,
            method="l1-table-formalized",
            phc_terms=[
                "person-centred-point-of-service-system",
                "register",
                "registry",
                "interoperability",
                "smart-guidelines",
                "digital-adaptation-kits",
                "business-process",
                "data-dictionary",
                "decision-support-logic",
                "scheduling-logic",
                "functional-requirements",
                "non-functional-requirements",
            ],
            ra_terms=[
                "point-of-service-applications",
                "registry",
                "interoperability",
                "smart-guidelines",
                "enterprise-architecture",
            ],
            elements=["pos-app", "ehr-system", "dss", "chis", "phr", "shr", "dse", "terminology-service"],
            views=["pcposs"],
        ),
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Front matter, acknowledgements, abbreviations and glossary",
        [
            ("Publication metadata and contents", "sec:fm-metadata", [b_fm], True),
            ("Acknowledgements", "sec:fm-acknowledgements", [b_ack], False),
            ("Abbreviations", "sec:fm-abbreviations", [b_abbr], False),
            ("Glossary", "sec:fm-glossary", [b_gloss], False),
        ],
        number=None,
    )
    return ch_slug


def build_references(folio_dir: Path):
    """Build References chapter (sec-034-references)."""
    ch_slug = "references"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    l34, _, p34 = read_l1_section("sec-034-references.md")
    b_ref = write_prose_block(
        ch_dir,
        "p-references-main",
        "prose:references-main",
        slice_lines(l34, 1, None),
        make_meta(
            "References (107 numbered references)",
            "sec-034-references.md",
            p34,
            method="l1-references",
            phc_terms=[
                "person-centred-point-of-service-system",
                "smart-guidelines",
                "digital-adaptation-kits",
                "collaborative-requirements-development-methodology",
                "interoperability",
            ],
            ra_terms=["smart-guidelines", "interoperability"],
            ingestedCrossReferences={
                "ref-20": {"citation": "PHII Collaborative Requirements Development Methodology (CRDM)", "bean": "folio-assistant-max2"},
                "ref-47-49": {"citation": "OMG Business Process Model and Notation (BPMN) 2.0.2", "library": "cat-harness/library/omg-2013-bpmn-2-0-2"},
                "ref-50": {"citation": "PATH Common Requirements for Maternal and Child Health Information Systems (2012)", "bean": "folio-assistant-max2"},
                "dmn-3.6": {"citation": "OMG Decision Model and Notation (DMN) 1.5", "library": "cat-harness/library/omg-2024-dmn-1-5"},
                "sdlc-mapping": {"citation": "SDLC phase structural mapping", "library": "cat-harness/library/arxiv-2404.04834v4"},
            },
        ),
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "References",
        [("References", "sec:references-main", [b_ref], True)],
        number=None,
    )
    return ch_slug


def build_annexes(folio_dir: Path):
    """Formalize Annexes 1–14 (sec-035..sec-046) per dth-phc#1 §3b, §3d, §3e."""
    ch_slug = "annexes"
    ch_dir = folio_dir / ch_slug
    ch_dir.mkdir(parents=True, exist_ok=True)

    # sec-035: Annex 1 (lines 1-17) and Annex 2 (lines 18-end)
    l35, _, _ = read_l1_section("sec-035-principles-for-digital-development.md")
    annex1_md = slice_lines(l35, 1, 17)
    annex2_md = slice_lines(l35, 18, None)

    b_a01 = write_prose_block(
        ch_dir,
        "p-annex-01-principles",
        "prose:annex-01-principles",
        annex1_md,
        make_meta(
            "Annex 1. Principles for digital development",
            "sec-035-principles-for-digital-development.md",
            [76],
            method="l1-external-source",
            phc_terms=["digital-health", "digital-transformation", "person-centred"],
            sourceOnly="Principles for Digital Development (United Nations Foundation / digitalprinciples.org, CC BY-SA 4.0): cited as an external source, not formalized per dth-phc#1 §3b",
        ),
    )

    b_a02 = write_table_block(
        ch_dir,
        "t-annex-02-interview-worksheet",
        "tbl:annex-02",
        "Annex 2. Worksheet for semi-structured interviews",
        annex2_md,
        make_meta(
            "Annex 2. Worksheet for semi-structured interviews",
            "sec-035-principles-for-digital-development.md",
            [77, 78, 79],
            method="l1-template-formalized",
            phc_terms=["user-persona", "end-user", "workflow", "pain-point", "collaborative-requirements-development-methodology"],
            elements=["user-researcher", "business-analyst", "health-worker"],
            views=["shared-roles"],
            templateFor={
                "chapterStep": "3.1.3 Semi-structured and follow-up interviews",
                "feedsDakKinds": ["persona", "business-process"],
                "smartBaseClasses": ["smart-base:Persona", "smart-base:BusinessProcess"],
            },
        ),
    )

    # sec-036: Annex 3 Observations worksheet
    l36, _, p36 = read_l1_section("sec-036-observations-worksheet.md")
    b_a03 = write_table_block(
        ch_dir,
        "t-annex-03-observations-worksheet",
        "tbl:annex-03",
        "Annex 3. Observations worksheet",
        slice_lines(l36, 1, None),
        make_meta(
            "Annex 3. Observations worksheet",
            "sec-036-observations-worksheet.md",
            p36,
            method="l1-template-formalized",
            phc_terms=["workflow", "register", "pain-point", "end-user"],
            elements=["user-researcher", "business-analyst", "health-worker"],
            views=["shared-roles"],
            templateFor={
                "chapterStep": "3.1.2 Observations",
                "feedsDakKinds": ["persona", "business-process"],
                "schemaProposalNote": "dth-phc#1 §3e: candidate extension for an observation worksheet schema in smart-base (awaiting architecture group review)",
            },
        ),
    )

    # sec-037: Annex 4 User persona worksheet
    l37, _, p37 = read_l1_section("sec-037-user-persona-worksheet.md")
    b_a04 = write_table_block(
        ch_dir,
        "t-annex-04-user-persona-worksheet",
        "tbl:annex-04",
        "Annex 4. User persona worksheet",
        slice_lines(l37, 1, None),
        make_meta(
            "Annex 4. User persona worksheet",
            "sec-037-user-persona-worksheet.md",
            p37,
            method="l1-template-formalized",
            phc_terms=["user-persona", "end-user", "health-service-users", "pain-point"],
            elements=["user-researcher", "business-analyst", "health-worker", "health-service-user"],
            views=["shared-roles", "pcposs"],
            templateFor={
                "chapterStep": "3.2.1 Create user personas",
                "producesDakKind": "persona",
                "smartBaseClass": "smart-base:Persona",
                "smartBaseStructureDefinition": "http://smart.who.int/base/StructureDefinition/GenericPersona",
            },
        ),
    )

    # sec-038: Annex 5 User stories worksheet
    l38, _, p38 = read_l1_section("sec-038-user-stories-worksheet.md")
    b_a05 = write_table_block(
        ch_dir,
        "t-annex-05-user-stories-worksheet",
        "tbl:annex-05",
        "Annex 5. User stories worksheet",
        slice_lines(l38, 1, None),
        make_meta(
            "Annex 5. User stories worksheet",
            "sec-038-user-stories-worksheet.md",
            p38,
            method="l1-template-formalized",
            phc_terms=["user-story", "use-case", "user-scenario", "user-persona", "functional-requirements", "non-functional-requirements"],
            elements=["business-analyst", "user-researcher", "health-worker"],
            views=["shared-roles"],
            templateFor={
                "chapterStep": "3.2.3 Gather user stories",
                "producesDakKinds": ["user-scenario", "functional-requirement", "non-functional-requirement"],
                "smartBaseClasses": ["smart-base:UserScenario", "smart-base:FunctionalRequirement", "smart-base:NonFunctionalRequirement"],
                "columns": ["As a… (User persona)", "I want to… (Functional / non-functional requirement)", "So that… (Purpose / objective)"],
            },
        ),
    )

    # sec-039: Annex 6 Business process matrix guide
    l39, _, p39 = read_l1_section("sec-039-business-process-matrix-guide.md")
    b_a06 = write_table_block(
        ch_dir,
        "t-annex-06-business-process-matrix",
        "tbl:annex-06",
        "Annex 6. Business process matrix guide",
        slice_lines(l39, 1, None),
        make_meta(
            "Annex 6. Business process matrix guide",
            "sec-039-business-process-matrix-guide.md",
            p39,
            method="l1-template-formalized",
            phc_terms=["business-process", "business-objective", "workflow", "user-persona", "trigger-event", "input", "output"],
            elements=["business-analyst", "smart-l2-dak"],
            views=["shared-roles", "pcposs"],
            templateFor={
                "chapterStep": "3.3 Map business processes and workflows",
                "producesDakKind": "business-process",
                "smartBaseClass": "smart-base:BusinessProcess",
                "smartBaseStructureDefinition": "http://smart.who.int/base/StructureDefinition/BusinessProcessWorkflow",
                "columns": ["Business process number", "Process name", "Objectives", "Key personas", "Trigger event", "Inputs", "Process / activities", "Outputs"],
            },
        ),
    )

    # sec-040: Annex 7 Form inventory guide
    l40, _, p40 = read_l1_section("sec-040-form-inventory-guide.md")
    b_a07 = write_table_block(
        ch_dir,
        "t-annex-07-form-inventory-guide",
        "tbl:annex-07",
        "Annex 7. Form inventory guide",
        slice_lines(l40, 1, None),
        make_meta(
            "Annex 7. Form inventory guide",
            "sec-040-form-inventory-guide.md",
            p40,
            method="l1-template-formalized",
            phc_terms=["register", "data-element", "workflow"],
            elements=["business-analyst", "health-informatician"],
            views=["shared-roles"],
            templateFor={
                "chapterStep": "3.4.1 Create an inventory of paper forms",
                "feedsDakKind": "data-element",
                "smartBaseClass": "smart-base:DataElement",
                "schemaProposalNote": "dth-phc#1 §3e: candidate form-inventory schema (form, register, data elements on it)",
            },
        ),
    )

    # sec-041: Annex 8 Form data mapping guide
    l41, _, p41 = read_l1_section("sec-041-form-data-mapping-guide.md")
    b_a08 = write_table_block(
        ch_dir,
        "t-annex-08-form-data-mapping-guide",
        "tbl:annex-08",
        "Annex 8. Form data mapping guide (Data dictionary template)",
        slice_lines(l41, 1, None),
        make_meta(
            "Annex 8. Form data mapping guide",
            "sec-041-form-data-mapping-guide.md",
            p41,
            method="l1-template-formalized",
            phc_terms=[
                "data-dictionary",
                "data-element",
                "metadata",
                "terminologies",
                "classifications",
                "coding-schemes",
                "international-classification-of-diseases",
                "logical-observation-identifiers-names-and-codes",
                "snomed-ct",
                "fast-healthcare-interoperability-resources",
            ],
            ra_terms=["interoperability", "fast-healthcare-interoperability-resources", "logical-observation-identifiers-names-and-codes", "snomed-ct", "snomed-gps"],
            elements=["terminology-service", "limr", "logical-models", "patient-level-data", "health-informatician"],
            views=["pcposs", "lmir-overview"],
            templateFor={
                "chapterStep": "3.4.2 Map all the data elements used in forms & 3.5 Create a data dictionary",
                "producesDakKind": "data-element",
                "smartBaseClass": "smart-base:DataElement",
                "smartBaseStructureDefinition": "http://smart.who.int/base/StructureDefinition/CoreDataElement",
            },
        ),
    )

    # sec-042: Annex 9 (lines 1-19) and Annex 10 (lines 20-end)
    l42, _, _ = read_l1_section("sec-042-aggregate-indicator-mapping-guide.md")
    annex9_md = slice_lines(l42, 1, 19)
    annex10_md = slice_lines(l42, 20, None)

    b_a09 = write_table_block(
        ch_dir,
        "t-annex-09-indicator-mapping-guide",
        "tbl:annex-09",
        "Annex 9. Aggregate indicator mapping guide",
        annex9_md,
        make_meta(
            "Annex 9. Aggregate indicator mapping guide",
            "sec-042-aggregate-indicator-mapping-guide.md",
            [90],
            method="l1-template-formalized",
            phc_terms=["indicators-and-performance-metrics", "data-element", "data-dictionary", "health-management-information-system"],
            elements=["indicator-reporting", "analytics-platform", "hmis", "me-specialist"],
            views=["pcposs", "shared-roles"],
            templateFor={
                "chapterStep": "3.4.3 Compile aggregate indicators",
                "producesDakKind": "indicator",
                "smartBaseClass": "smart-base:Indicator",
                "smartBaseStructureDefinition": "http://smart.who.int/base/StructureDefinition/ProgramIndicator",
                "columns": [
                    "Indicator ID",
                    "Indicator name",
                    "Definition",
                    "Numerator description",
                    "Numerator computation",
                    "Denominator description",
                    "Denominator computation",
                    "Frequency of reporting",
                    "Disaggregation",
                    "Alerts or targets",
                    "References",
                ],
            },
        ),
    )

    b_a10 = write_table_block(
        ch_dir,
        "t-annex-10-decision-and-scheduling-matrix",
        "tbl:annex-10",
        "Annex 10. Decision-support logic and scheduling matrix guide",
        annex10_md,
        make_meta(
            "Annex 10. Decision-support logic and scheduling matrix guide",
            "sec-042-aggregate-indicator-mapping-guide.md",
            [90, 91],
            method="l1-template-formalized",
            phc_terms=["decision-support-logic", "decision-support-table", "scheduling-logic", "digital-adaptation-kits"],
            elements=["dss", "dse", "smart-l2-dak"],
            views=["cds", "pcposs"],
            templateFor={
                "chapterStep": "3.6 Determine decision-support logic & 3.7 Map health service schedules",
                "producesDakKinds": ["decision-table", "scheduling-logic"],
                "smartBaseClasses": ["smart-base:DecisionTable", "smart-base:SchedulingLogic"],
                "referencedDaks": [
                    {"title": "WHO DAK for Antenatal Care (2021)", "iris": "https://iris.who.int/handle/10665/339745"},
                    {"title": "WHO DAK for Family Planning (2021)", "iris": "https://iris.who.int/handle/10665/341997"},
                    {"title": "WHO DAK for HIV, 2nd ed. (2023)", "iris": "https://iris.who.int/handle/10665/375230"},
                    {"title": "WHO DAK for Tuberculosis (2024)", "iris": "https://iris.who.int/handle/10665/376631"},
                    {"title": "WHO DAK for Child Health in Humanitarian Emergencies (2024)", "iris": "https://iris.who.int/handle/10665/376626"},
                ],
            },
        ),
    )

    # sec-043: Annex 11 Template for a decision-support table
    l43, _, p43 = read_l1_section("sec-043-template-for-a-decision-support-table.md")
    b_a11 = write_table_block(
        ch_dir,
        "t-annex-11-decision-support-table-template",
        "tbl:annex-11",
        "Annex 11. Template for a decision-support table (DMN shape)",
        slice_lines(l43, 1, None),
        make_meta(
            "Annex 11. Template for a decision-support table (DMN hit policy and rule structure)",
            "sec-043-template-for-a-decision-support-table.md",
            p43,
            method="l1-template-formalized",
            phc_terms=["decision-support-table", "decision-support-logic", "rule", "input", "output", "annotation", "trigger-event"],
            elements=["dss", "dse", "smart-l2-dak"],
            views=["cds", "pcposs"],
            templateFor={
                "chapterStep": "3.6 Determine decision-support logic",
                "producesDakKind": "decision-table",
                "smartBaseClass": "smart-base:DecisionTable",
                "smartBaseStructureDefinition": "http://smart.who.int/base/StructureDefinition/DecisionSupportLogic",
                "normativeSpec": "cat-harness/library/omg-2024-dmn-1-5",
            },
            dmnShape={
                "hitPolicies": {
                    "U": "Unique (no overlap; at most one rule matches)",
                    "R": "Rule order (multiple rules may match; outputs returned in rule order)",
                    "F": "First (multiple rules may match; first matching rule wins)",
                },
                "ruleIdPattern": "<process ID>.<activity number>.DT.<rule number>",
                "conjunctionRule": "Inputs on the same row are combined with AND; separate rows represent OR.",
                "columns": ["Rule ID", "Input(s)", "Output", "Action", "Annotation(s)"],
            },
        ),
    )

    # sec-044: Annex 12 Scheduling logic table guide
    l44, _, p44 = read_l1_section("sec-044-scheduling-logic-table-guide.md")
    b_a12 = write_table_block(
        ch_dir,
        "t-annex-12-scheduling-logic-guide",
        "tbl:annex-12",
        "Annex 12. Scheduling logic table guide",
        slice_lines(l44, 1, None),
        make_meta(
            "Annex 12. Scheduling logic table guide",
            "sec-044-scheduling-logic-table-guide.md",
            p44,
            method="l1-template-formalized",
            phc_terms=["scheduling-logic", "trigger-event", "longitudinal-tracking", "antenatal-care", "digital-adaptation-kits"],
            elements=["longitudinal-tracking", "alerts-and-reminders", "dss", "smart-l2-dak"],
            views=["pcposs", "cds"],
            templateFor={
                "chapterStep": "3.7 Map health service schedules",
                "producesDakKind": "scheduling-logic",
                "smartBaseClass": "smart-base:SchedulingLogic",
                "columns": [
                    "Scheduling logic ID",
                    "Service name",
                    "Visit / contact number",
                    "Trigger event",
                    "Timing / due window",
                    "Overdue threshold",
                    "Expiration / cutoff",
                    "Associated decision-support logic",
                    "References",
                ],
            },
            reproduces={
                "example": "Hepatitis B birth dose vaccination schedule",
                "ancDakScheduleReference": "https://iris.who.int/handle/10665/339745",
            },
        ),
    )

    # sec-045: Annex 13 Prioritization of requirements guide
    l45, _, p45 = read_l1_section("sec-045-prioritization-of-requirements-guide.md")
    b_a13 = write_table_block(
        ch_dir,
        "t-annex-13-prioritization-guide",
        "tbl:annex-13",
        "Annex 13. Prioritization of requirements guide",
        slice_lines(l45, 1, None),
        make_meta(
            "Annex 13. Prioritization of requirements guide",
            "sec-045-prioritization-of-requirements-guide.md",
            p45,
            method="l1-template-formalized",
            phc_terms=["requirements", "functional-requirements", "non-functional-requirements", "user-persona", "minimum-viable-product"],
            elements=["business-analyst", "software-engineer", "pos-app"],
            views=["shared-roles", "pcposs"],
            templateFor={
                "chapterStep": "3.8 Gather and prioritize requirements",
                "producesDakKinds": ["functional-requirement", "non-functional-requirement"],
                "smartBaseClasses": ["smart-base:FunctionalRequirement", "smart-base:NonFunctionalRequirement"],
                "smartBaseStructureDefinitions": [
                    "http://smart.who.int/base/StructureDefinition/FunctionalRequirement",
                    "http://smart.who.int/base/StructureDefinition/NonFunctionalRequirement",
                ],
                "columns": ["Requirement ID", "Activity ID and name", "As a (user persona)…", "I want to…", "So that…", "Priority (High / Medium / Low)", "Notes"],
                "priorityLevels": ["High (need-to-have / Must / SHALL)", "Medium (should-have / SHOULD)", "Low (nice-to-have / MAY)"],
            },
        ),
    )

    # sec-046: Annex 14 HL7 FHIR standard components
    l46, _, p46 = read_l1_section("sec-046-hl7-fhir-standard-components.md")
    b_a14 = write_prose_block(
        ch_dir,
        "p-annex-14-fhir-components",
        "prose:annex-14-fhir-components",
        slice_lines(l46, 1, None),
        make_meta(
            "Annex 14. HL7 FHIR standard components (Resources, Implementation Guides, Profiles, Stores, APIs)",
            "sec-046-hl7-fhir-standard-components.md",
            p46,
            method="l1-section-formalized",
            phc_terms=[
                "fast-healthcare-interoperability-resources",
                "interoperability-standards",
                "smart-guidelines",
                "digital-adaptation-kits",
                "data-exchange",
                "metadata",
            ],
            ra_terms=[
                "fast-healthcare-interoperability-resources",
                "interoperability",
                "smart-guidelines",
            ],
            elements=["interop-component", "limr", "terminology-service", "shr-repo", "dse", "pos-app"],
            views=["interop-layer", "lmir-overview", "pcposs"],
            fhirHarnessLinks={
                "harness": "fhir-harness",
                "smartBaseL3Kinds": [
                    "logical-model",
                    "profile",
                    "value-set",
                    "questionnaire",
                    "cql-library",
                    "structure-map",
                    "plan-definition",
                    "measure",
                ],
                "referencedImplementationGuides": [
                    {"title": "WHO Antenatal Care (ANC) FHIR Implementation Guide", "url": "http://build.fhir.org/ig/WorldHealthOrganization/smart-anc/"},
                ],
            },
        ),
    )

    write_chapter_manifest(
        ch_dir,
        ch_slug,
        "Annexes",
        [
            ("Annex 1. Principles for digital development", "sec:annex-01", [b_a01], True),
            ("Annex 2. Worksheet for semi-structured interviews", "sec:annex-02", [b_a02], False),
            ("Annex 3. Observations worksheet", "sec:annex-03", [b_a03], False),
            ("Annex 4. User persona worksheet", "sec:annex-04", [b_a04], False),
            ("Annex 5. User stories worksheet", "sec:annex-05", [b_a05], False),
            ("Annex 6. Business process matrix guide", "sec:annex-06", [b_a06], False),
            ("Annex 7. Form inventory guide", "sec:annex-07", [b_a07], False),
            ("Annex 8. Form data mapping guide", "sec:annex-08", [b_a08], False),
            ("Annex 9. Aggregate indicator mapping guide", "sec:annex-09", [b_a09], False),
            ("Annex 10. Decision-support logic and scheduling matrix guide", "sec:annex-10", [b_a10], False),
            ("Annex 11. Template for a decision-support table", "sec:annex-11", [b_a11], False),
            ("Annex 12. Scheduling logic table guide", "sec:annex-12", [b_a12], False),
            ("Annex 13. Prioritization of requirements guide", "sec:annex-13", [b_a13], False),
            ("Annex 14. HL7 FHIR standard components", "sec:annex-14", [b_a14], False),
        ],
        number=None,
    )
    return ch_slug


def main():
    if FOLIO.exists():
        shutil.rmtree(FOLIO)
    FOLIO.mkdir(parents=True, exist_ok=True)

    # Copy vector figures into folio/dth-phc/media/
    media_dir = FOLIO / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    for fig_path in sorted((L1_DIR / "figures").glob("vfig-p*.png")):
        shutil.copy2(fig_path, media_dir / fig_path.name)

    # Formalize Chapters 3 and 4 first (most structure), then 1, 2, 5, 6, Front matter, References and Annexes
    build_ch03(FOLIO)
    build_ch04(FOLIO)
    build_ch01(FOLIO)
    build_ch02(FOLIO)
    build_ch05(FOLIO)
    build_ch06(FOLIO)
    build_front_matter(FOLIO)
    build_references(FOLIO)
    build_annexes(FOLIO)

    chapter_order = [
        "front-matter",
        "ch01-introduction",
        "ch02-how-to-use",
        "ch03-user-requirements",
        "ch04-design-and-adaptation",
        "ch05-training-testing-rollout",
        "ch06-scale-up",
        "references",
        "annexes",
    ]
    chapter_refs = "\n".join(f'    chapterRef({{ dir: "{c}" }}),' for c in chapter_order)

    doc_ts = (
        'import { paper, chapterRef } from "../schema/builders";\n\n'
        "/**\n"
        f" * {TITLE}\n"
        " *\n"
        " * The document manifest. `chapters` is an ORDERED list: its order is the\n"
        " * reading order, and it is the only place that order is recorded.\n"
        " *\n"
        f" * Seeded from who-iris/library/{L1_ID} and formalized per litlfred/dth-phc#1\n"
        " * §3b by scripts/folio/seed_from_l1.py.\n"
        " */\n"
        "export default paper({\n"
        f"  title: {json.dumps(TITLE)},\n"
        '  authors: ["World Health Organization"],\n'
        '  date: "2024",\n'
        "  meta: {\n"
        '    documentKind: "smart-base:dth",\n'
        '    level: "L1",\n'
        '    targetLevel: "L2",\n'
        '    isbn: "9789240093362",\n'
        '    irisHandle: "https://iris.who.int/handle/10665/378469",\n'
        f'    source: {{ library: "{L1_ID}", repository: "litlfred/who-iris" }},\n'
        '    licence: "CC BY-NC-SA 3.0 IGO",\n'
        '    status: "seeded from L1 and formalized per dth-phc#1 §3b; linked to glossary and smart-ra ArchiMate",\n'
        "  },\n"
        "  chapters: [\n" + chapter_refs + "\n  ],\n"
        "});\n"
    )
    (FOLIO / f"{DOC}.ts").write_text(doc_ts, encoding="utf-8")

    block_count = sum(1 for _ in FOLIO.rglob("*.md"))
    print(f"wrote {FOLIO}: {len(chapter_order)} chapters, {block_count} blocks")


if __name__ == "__main__":
    main()
