import { chapter, section } from "../../schema/builders";

export default chapter({
  title: "Front matter and acknowledgements",
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
  ],
});
