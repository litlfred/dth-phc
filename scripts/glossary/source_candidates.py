#!/usr/bin/env python3
"""Build glossary/source-candidates.glossary.json (dth-phc#6, option A).

For handbook terms with no definition in the handbook text, each entry here
quotes a definition from another cited WHO publication in who-iris. Quotes are
cut from the L1 section text between a start and an end phrase, so they are
verbatim (line breaks joined). A candidate is never the handbook's definition;
dth-phc.glossary.json links to it with a SKOS match and an editor adopts one.

Usage: python3 -I scripts/glossary/source_candidates.py [--who-iris PATH] [--check]
"""
import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "glossary" / "source-candidates.glossary.json"

DOCS = {
    "diig": ("9789240010567-eng", "Digital implementation investment guide (DIIG): integrating digital interventions into health programmes. Geneva: World Health Organization; 2020."),
    "daki": ("9789240099456-eng", "Digital adaptation kit for immunizations: operational requirements for implementing WHO recommendations in digital systems. Geneva: World Health Organization; 2024."),
    "cdisah": ("9789240081949-eng", "Classification of digital interventions, services and applications in health: a shared language to describe the uses of digital technology for health, 2nd ed. Geneva: World Health Organization; 2023."),
    "anc": ("9789241549912-eng", "WHO recommendations on antenatal care for a positive pregnancy experience. Geneva: World Health Organization; 2016."),
    "dthpc": ("9789240116191-eng", "Digital transformation handbook for health product catalogue. Geneva: World Health Organization; 2024."),
}

# (id, prefLabel, doc, section file, where, start phrase, end phrase)
CANDIDATES = [
    ("antenatal-care--who-anc-2016", "Antenatal care (ANC)", "anc", "sec-003-1-introduction.md", "Chapter 1, Introduction",
     "Antenatal care (ANC) can be defined as", "during pregnancy."),
    ("digital-health-ecosystem--who-diig-2020", "Digital health ecosystem", "diig", "page-138.md", "Annex 1.1 Glossary",
     "The combined set of digital health components", "in a given context or country."),
    ("enterprise-architecture--who-diig-2020", "Enterprise architecture", "diig", "page-140.md", "Annex 1.1 Glossary",
     "A blueprint of business processes, data, systems and technologies used to help", "such as a health system."),
    ("funder--who-diig-2020", "Funder", "diig", "page-140.md", "Annex 1.1 Glossary",
     "Private foundation, NGO, bilateral or multilateral agency", "digital health investments or projects."),
    ("health-information-system--who-diig-2020", "Health information system", "diig", "page-140.md", "Annex 1.1 Glossary",
     "A system that integrates data collection, processing, reporting, and", "all levels of health services."),
    ("health-management-information-system--who-diig-2020", "Health management information system", "diig", "page-140.md", "Annex 1.1 Glossary",
     "An information system specially designed to assist in", "as opposed to delivery of care."),
    ("standard--who-diig-2020", "Standard", "diig", "page-141.md", "Annex 1.1 Glossary",
     "In software, a standard is a", "independent of a particular application."),
    ("health-information-system--who-dak-immz-2024", "Health information system (HIS)", "daki", "sec-front-matter.md", "Glossary",
     "A system that integrates data collection, processing, reporting and use", "all levels of health services (6)."),
    ("health-management-information-system--who-dak-immz-2024", "Health management information system (HMIS)", "daki", "sec-front-matter.md", "Glossary",
     "An information system specifically designed to assist", "as opposed to delivery of care (6)."),
    ("terminologies--who-dak-immz-2024", "Terminologies", "daki", "sec-front-matter.md", "Glossary",
     "For clinical care, terminologies are structured vocabularies", "consistent and standard way (8)."),
    ("health-interventions-and-recommendations--who-dak-immz-2024", "Health interventions and recommendations", "daki", "sec-002-components-of-a-digital-adaptation-kit.md", "Table 1, component 1",
     "Overview of the health interventions and WHO", "compiled by WHO (22)."),
    ("user-scenarios--who-dak-immz-2024", "User scenarios", "daki", "sec-002-components-of-a-digital-adaptation-kit.md", "Table 1, component 3",
     "Narratives that describe how the different", "an idea of a typical workflow."),
    ("generic-business-processes-and-workflows--who-dak-immz-2024", "Generic business processes and workflows", "daki", "sec-002-components-of-a-digital-adaptation-kit.md", "Table 1, component 4",
     "A business process is a set of related activities", "performed within the business process (1,23)."),
    ("indicators-and-performance-metrics--who-dak-immz-2024", "Indicators and performance metrics", "daki", "sec-002-components-of-a-digital-adaptation-kit.md", "Table 1, component 7",
     "Core set of indicators that need to be", "rather than survey-based tools."),
    ("functional-and-non-functional-requirements--who-dak-immz-2024", "Functional and non-functional requirements", "daki", "sec-002-components-of-a-digital-adaptation-kit.md", "Table 1, component 8",
     "A high-level list of core functions and", "tasks within the business process."),
    ("scheduling-logic--who-dak-immz-2024", "Scheduling logic", "daki", "sec-004-how-to-use-this-digital-adaptation-kit.md", "Section 6.3",
     "scheduling logic to facilitate the digital tracking of clients", "according to clinical protocols."),
    ("point-of-service--who-cdisah-2023", "Point of service", "cdisah", "page-050.md", "Services and application types, category A",
     "Systems that facilitate the provision and delivery of healthcare services", "interactively communicate with them."),
    ("electronic-medical-record-systems--who-cdisah-2023", "Electronic medical record systems", "cdisah", "page-051.md", "Services and application types, A5",
     "A secure, online system that holds information about people", "managed by healthcare providers."),
    ("personal-health-records--who-cdisah-2023", "Personal health records", "cdisah", "page-051.md", "Services and application types, A7",
     "Digital personal health record is a record", "over which the person has agency."),
    ("terminology-and-classification-systems--who-cdisah-2023", "Terminology and classification systems", "cdisah", "page-055.md", "Services and application types, C11",
     "A central authority to uniquely identify the clinical activities", "SNOMED and others.(1,4)"),
    ("data-interchange-and-interoperability--who-cdisah-2023", "Data interchange and interoperability", "cdisah", "page-056.md", "Services and application types, D2",
     "Provides software capabilities to support managed data exchange", "across the digital health enterprise.(1)"),
    ("health-management-information-systems--who-cdisah-2023", "Health Management Information systems (HMIS)", "cdisah", "page-057.md", "Services and application types, D6",
     "Stores routinely collected aggregate healthcare data", "improving the quality of health services.(1,4)"),
    ("open-standards--who-dth-product-catalogue-2024", "Open standards", "dthpc", "page-008.md", "Glossary",
     "Standards that are documented and made freely available", "intended for widespread adoption."),
]


def section_text(who_iris: Path, doc_dir: str, fname: str) -> str:
    raw = (who_iris / "library" / doc_dir / "sections" / fname).read_text(encoding="utf-8")
    raw = re.sub(r"^---\n.*?\n---\n", "", raw, count=1, flags=re.S)
    raw = raw.replace("​", "")
    return re.sub(r"\s+", " ", raw).strip()


def build(who_iris: Path) -> dict:
    terms, errors = [], []
    for cid, label, doc, fname, where, start, end in CANDIDATES:
        doc_dir, cited = DOCS[doc]
        text = section_text(who_iris, doc_dir, fname)
        i = text.find(start)
        j = text.find(end, i + len(start)) if i >= 0 else -1
        if i < 0 or j < 0:
            errors.append(f"{cid}: quote not found in {doc_dir}/{fname}")
            continue
        quote = text[i : j + len(end)]
        if len(quote) > 1200:
            errors.append(f"{cid}: quote too long ({len(quote)} chars), check the phrases")
            continue
        terms.append({
            "id": cid,
            "prefLabel": label[0].upper() + label[1:],
            "definition": quote,
            "scopeNote": f"Cited as: {cited} {where}. Quoted verbatim from the L1 text (line breaks joined). A candidate from another WHO publication, never the handbook's own definition.",
            "source": f"who-iris/library/{doc_dir}/sections/{fname}",
            "status": "candidate",
        })
    if errors:
        sys.exit("\n".join(errors))
    return {
        "$schema": "folio-glossary/v1",
        "id": "source-candidates",
        "title": "Candidate definitions from other WHO publications",
        "description": "Definitions quoted from WHO publications other than the handbook, for terms the handbook uses but does not define (dth-phc#6, option A). One entry per concept and source. dth-phc.glossary.json links each handbook term to its candidates with a SKOS match; a candidate becomes the term's definition only when an editor adopts it. Generated by scripts/glossary/source_candidates.py; do not hand-edit.",
        "source": "who-iris/library",
        "terms": terms,
        "modified": "2026-11-01",
        "license": "CC-BY-NC-SA-3.0-IGO",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--who-iris", default=str(ROOT / "who-iris"))
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    out = json.dumps(build(Path(a.who_iris)), indent=2, ensure_ascii=False) + "\n"
    if a.check:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != out:
            sys.exit(f"{OUT.relative_to(ROOT)} is stale: re-run scripts/glossary/source_candidates.py")
        print(f"OK: {OUT.relative_to(ROOT)} up to date")
        return
    OUT.write_text(out, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(CANDIDATES)} candidates)")


if __name__ == "__main__":
    main()
