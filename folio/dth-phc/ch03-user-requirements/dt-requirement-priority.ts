import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:requirement-priority",
  title: "Requirement prioritization decision table (section 3.8 and Annex 13)",
  decisionId: "Decision_RequirementPriority",
  companions: { dmn: "dt-requirement-priority.dmn" },
  uses: ["prose:ch03-sec-019-requirements", "tbl:annex-13"],
  meta: {"title": "Requirement prioritization decision table (section 3.8 and Annex 13)", "decisionId": "Decision_RequirementPriority", "canonicalDmn": "processes/decisions/requirement-priority.dmn", "dmnSpec": "omg-2024-dmn-1-5", "source": {"library": "9789240093362-eng", "sections": ["sec-019", "sec-045"], "pdfPages": [47, 48, 100], "method": "p4b-dmn-formalization", "file": "who-iris/library/9789240093362-eng/sections/sec-019-38-gather-and-prioritize-requirements.md", "section": "sec-019-38-gather-and-prioritize-requirements", "issue": "litlfred/dth-phc#1"}, "relatedBlocks": ["pers:business-analyst", "pers:implementing-team", "pers:public-health-authority"], "code": "PHC-DT-03", "dmnFile": "dt-requirement-priority.dmn", "archimate": {"model": "smart-ra 0.3.0-draft.2", "basis": "agent-proposed by name, for working-group review (dth-phc#1)", "elements": [{"iri": "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.2/elements/id-b1a348e9848f50e19a46bf2226dc2f08.jsonld", "name": "Business analyst", "type": "BusinessRole"}], "views": [{"iri": "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.2/views/id-eac6523c694c551b968166656af2b2e6.jsonld", "name": "Shared DTH Roles and Actors"}]}, "glossaryTerms": ["https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/functional-requirements", "https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/non-functional-requirements", "https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/minimum-viable-product"]},
});
