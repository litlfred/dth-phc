# Digital Transformation Handbook for Primary Health Care (`dth-phc`)

Structured **L2 document and Digital Adaptation Kit (DAK) folio** for the World Health Organization publication:

> *Digital transformation handbook for primary health care: optimizing person-centred point of service systems.* Geneva: World Health Organization; 2024. ISBN 978-92-4-009336-2 ([WHO IRIS `10665/379452`](https://iris.who.int/handle/10665/379452)).

## Architecture & Upstream Dependencies

This repository follows the [`smart-base` S4 L2 DTH layout](docs/l2-wiring.md) (`dth-phc.json` declaring `needs: ["smart-base", "dpi-h-ra"]`):

| Layer | Instance | Role in `dth-phc` |
|---|---|---|
| **L1 Source** | `who-iris` (`library/9789240093362-eng`) | Normalized Markdown sections, figures, and tables from the WHO publication |
| **Reference Architecture** | `dpi-h-ra` (`litlfred/smart-ra`) | WHO/ITU DPI-H Reference Architecture & Full-STAC glossaries and ArchiMate models |
| **DAK Base** | `smart-base` (`litlfred/smart-base`) | WHO SMART Guidelines DAK component schemas, block kinds, and DTH authoring skills |
| **L2 Folio** | `dth-phc` (this repo) | PHC SKOS glossary (`glossary/dth-phc.glossary.json`) and structured folio (`folio/dth-phc/`) |

## Quick Start

```bash
# Materialize remote mounts declared in index.config.json
bun run cat-harness-tools/scripts/remote-mount.ts

# Validate declaration and glossary cross-links to smart-ra and smart-base
bun run check:dth-glossary
```

## Workplan

Tracked in [`litlfred/dth-phc#1`](https://github.com/litlfred/dth-phc/issues/1).
