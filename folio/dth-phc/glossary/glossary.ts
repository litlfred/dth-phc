import { chapter, section } from "../../schema/builders";

/** Back matter: the glossary, then its acronyms (each a term's SKOS notation). */
export default chapter({
  title: "Glossary",
  label: "chap:glossary",
  tabLabel: "G",
  sections: [
    section({
      title: "Glossary",
      label: "sec:fm-glossary",
      blocks: ["t-fm-glossary"],
    }),
    section({
      title: "Abbreviations",
      label: "sec:fm-abbreviations",
      blocks: ["t-fm-abbreviations"],
    }),
  ],
});
