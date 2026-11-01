import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:starting-scenario",
  title: "Starting-scenario classification decision table (section 2.1)",
  decisionId: "Decision_StartingScenario",
  companions: { dmn: "dt-starting-scenario.dmn" },
  uses: ["prose:ch02-sec-007-readiness-scenarios"],
  meta: {"title": "Starting-scenario classification decision table (section 2.1)", "decisionId": "Decision_StartingScenario", "canonicalDmn": "processes/decisions/starting-scenario.dmn", "dmnSpec": "omg-2024-dmn-1-5", "source": {"library": "9789240093362-eng", "sections": ["sec-007"], "pdfPages": [17, 18], "method": "p4b-dmn-formalization", "file": "who-iris/library/9789240093362-eng/sections/sec-007-21-targeted-scenarios-of-digital-readiness.md", "section": "sec-007-21-targeted-scenarios-of-digital-readiness", "issue": "litlfred/dth-phc#1"}, "relatedBlocks": ["pers:implementing-team", "pers:public-health-authority"], "code": "PHC-DT-01", "dmnFile": "dt-starting-scenario.dmn", "archimate": {"model": "smart-ra 0.3.0-draft.1", "basis": "agent-proposed by name, for working-group review (dth-phc#1)", "elements": [{"iri": "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.1/elements/id-808925f4d2075d7b95e0651ebae00fcf.jsonld", "name": "Point-of-service application", "type": "ApplicationComponent"}], "views": [{"iri": "https://litlfred.github.io/smart-ra/archimate/0.3.0-draft.1/views/id-bcf04de52bb05c3a932bbfdd36d7ae4f.jsonld", "name": "Person-centred point of service (PCPOSS)"}]}, "glossaryTerms": ["https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/person-centred-point-of-service-system", "https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/digitization", "https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/digitalization"]},
});
