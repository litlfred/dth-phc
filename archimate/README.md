# dth-phc ArchiMate overlay

A DTH builds an **overlay** on the smart-ra (DPI-H RA) ArchiMate model and does not add to that model (owner, 2026-11-01, card Q-RA1 A; [dth-phc#8](https://github.com/litlfred/dth-phc/issues/8)). The one exception is a real conflict between a DTH and smart-ra terms or models: then an issue goes to smart-ra and to the DTH, as with "Health worker" ([smart-ra#201](https://github.com/litlfred/smart-ra/issues/201), [dth-phc#10](https://github.com/litlfred/dth-phc/issues/10)).

| Version | File | Overlays smart-ra |
|---|---|---|
| 0.1.0-draft.1 | [`0.1.0-draft.1/dth-phc-overlay.archimate`](0.1.0-draft.1/dth-phc-overlay.archimate) | 0.3.0-draft.1 |

Each element carries one of two tags:

- `overlay:base`: a reference copy of a smart-ra element, under the same id, with its smart-ra IRI as the value. It is there only so the overlay's views can draw it.
- `overlay:owner` = `dth-phc`: an element this DTH adds. The folio links it with a `https://litlfred.github.io/dth-phc/archimate/<version>/…` IRI.

`overlay:shared-candidate` marks the shared DTH roles, whose home is open ([dth-phc#9](https://github.com/litlfred/dth-phc/issues/9)).

`bun run check:archimate-links` fails when a copy names something smart-ra does not hold, when an owned element is already in smart-ra, or when a folio link does not resolve in the pinned model. `scripts/archimate/extract_overlay.py` built 0.1.0-draft.1 from the PHC work that was once in smart-ra#182.
