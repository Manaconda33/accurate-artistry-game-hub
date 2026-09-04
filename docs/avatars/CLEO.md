# Cleo avatar record

## Production status

**Archived / inactive as of 2026-08-26.** Manny retired Cleo from the active production roster while explicitly preserving her approved character, kart, runtime assets, deterministic source, and acceptance evidence for possible future restoration.

Cleo is not currently selectable and cannot appear as an AI opponent. Her complete package remains durable in the repository and is indexed by `docs/CHARACTER-ARCHIVE.md`.

## Identity

- Display name: Cleo
- Historical runtime ID: `aa-06`
- Pronouns: she/her
- Selection descriptor: Steady hands. Flawless lines.
- Character lock: Approved by Manny on 2026-08-21

Cleo is a composed craftswoman with green eyes, tortoiseshell glasses, gold drop earrings, and elaborate brown hair gathered into a braided high bun. Her definitive racing outfit is a navy floral blouse with vivid red-orange flowers and tailored navy trousers. The approved portrait and driver frames control her game likeness.

## Kart direction

- Kart name: The Gilded Stitch
- Kart lock: Approved by Manny on 2026-08-21
- Design authority: the supplied Cleo racing sheet is definitive

The Gilded Stitch is a sewing-machine-inspired kart with an ornate navy-and-gold body, engraved floral scrollwork, warm wooden spool wheels, a visible needle-like steering column, and sewing-hardware construction details. Its production 3D interpretation must preserve the recognizable sewing-machine silhouette and decorative craft language without sacrificing cockpit clearance or race readability.

## Historical gameplay mapping

- Former profile: AA-06 Grip Specialist
- Class: Medium
- Stats: Speed 6 / Acceleration 6 / Weight 5 / Handling 7 / Mini-Turbo 5 / Traction 7
- Mapping approved by Manny on 2026-08-21
- Mapping released on archive: 2026-08-26

Cleo rewarded clean, repeatable lines. Handling 7 and Traction 7 made The Gilded Stitch stable and forgiving through ordinary corners and mixed surfaces. Moderate speed, acceleration, weight, and Mini-Turbo kept her from displacing the roster's dedicated sprinters, drifters, or heavyweights.

AA-06 is available for a future approved active character assignment. If Cleo is restored later, her balance profile must be explicitly confirmed at that time rather than assumed from this historical mapping.

## Approved driver art

Manny approved the following art on 2026-08-21:

- `portrait.png`: definitive selectable portrait
- `driver/front.png`: front-facing neutral driving frame
- `driver/rear.png`: neutral chase-camera frame
- `driver/steer-left.png`: chase-camera left-turn frame
- `driver/steer-right.png`: chase-camera right-turn frame
- `driver/hit.png`: chase-camera impact frame
- `driver/victory.png`: chase-camera over-the-shoulder victory frame

All runtime derivatives are sRGB RGBA PNGs with genuine transparency. The portrait is 256 x 256; every driver frame is 512 x 512. Character layers contain no kart or steering-wheel geometry.

## Provenance and transformation

Manny supplied the definitive character-and-kart reference, confirmed that he created or controls it, and authorized its transformation into game assets. Approved generated derivatives preserve Cleo's likeness and were resized into the PRD runtime contract. High-resolution working renders are not stored in the fixed-size runtime paths.

## Historical production acceptance

- Intake: Approved
- Character lock: Approved
- Kart design lock: Approved
- Former balance mapping: Approved, AA-06
- Driver art: Approved
- Runtime PNG preparation: Complete
- Kart GLB: Approved and prepared in three deterministic LODs
- Previous manifest production integration: Complete under controlled revision `cleo-runtime-20260821-1`
- Previous live verification: Accepted by Manny on 2026-08-21

The historical runtime driver sprite position `[0, 0.9, -0.72]` placed Cleo in the rear-biased cockpit with the steering wheel ahead of her rather than behind her back. This integration detail remains preserved in the exported `archivedCleo` definition.

## Archive and restoration

No approved Cleo asset is deleted. The package is preserved at `public/assets/archive/characters/cleo-aa-06/`, The Gilded Stitch builder remains at `tools/assets/build_cleo_gilded_stitch.py`, and the full package inventory and GLB object IDs are recorded in `docs/CHARACTER-ARCHIVE.md`.

Do not reactivate Cleo, reuse her likeness, or treat historical live acceptance as current deployment evidence without Manny's explicit restoration approval and a fresh validation/deployment pass.
