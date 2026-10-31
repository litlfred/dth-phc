/**
 * Re-export of smart-base's DAK block builders (persona, userScenario,
 * functionalRequirement, nonFunctionalRequirement, dataElement, …).
 *
 * The handbook is an L1 document (smart-base document kind `dth`); its
 * structured assets — generic personas, user scenarios, requirements and data
 * elements — use the same block kinds as an L2 DAK, so they can be carried
 * into one without re-authoring. Written once here, like `builders.ts`.
 */

export * from "../../smart-base/schemas/dak-blocks";
