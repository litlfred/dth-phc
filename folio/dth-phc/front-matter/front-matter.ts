import { chapter, section } from "../../schema/builders";

export default chapter({
  title: "Front matter, acknowledgements, abbreviations and glossary",
  label: "chap:front-matter",
  sections: [
    section({
      title: "Publication metadata and contents",
      label: "sec:fm-metadata",
      lead: true,
      blocks: ["p-fm-publication-metadata"],
    }),
    section({
      title: "Acknowledgements",
      label: "sec:fm-acknowledgements",
      blocks: ["p-fm-acknowledgements"],
    }),
    section({
      title: "Abbreviations",
      label: "sec:fm-abbreviations",
      blocks: ["t-fm-abbreviations"],
    }),
    section({
      title: "Glossary",
      label: "sec:fm-glossary",
      blocks: ["t-fm-glossary"],
    }),
  ],
});
