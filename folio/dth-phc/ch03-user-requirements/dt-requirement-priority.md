# Requirement prioritization decision table (section 3.8 and Annex 13)

Formal DMN 1.5 decision table (`Decision_RequirementPriority`, `hitPolicy="FIRST"`) encoding the three-tier requirement prioritization criteria in section 3.8 (`sec-019`) and Annex 13 (*Requirements prioritization worksheet*, `sec-045`), evaluated at gateway `GW_RequirementPriority` in [`understand-user-requirements.bpmn`](../../../processes/understand-user-requirements.bpmn).

## Alignment with RFC 2119 / RFC 8174 and CRDM

As established in `litlfred/dth-phc#1` §3f:
- **`"High"` (`MVP`, `SHALL`):** Essential for core clinical safety, regulatory compliance or MVP operation; without it the PCPOSS cannot be safely deployed (`Must have`).
- **`"Medium"` (`Version 1`, `SHOULD`):** Important for workflow efficiency, reporting completeness or user experience, but has a viable temporary workaround for MVP (`Should have`).
- **`"Low"` (`Version 2`, `MAY`):** Desirable enhancement (`Nice to have`) scheduled for future iterations once MVP and Version 1 are stable.
