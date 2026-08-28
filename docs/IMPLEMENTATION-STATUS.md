# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 1.6**.

Latest verified implementation checkpoint: `aa24b655d30ba65438f512e0544e313da3fc343e` — PR #37 merged McFleurdel's approved production package. Main CI run `33037485975` passed LFS verification, typecheck, lint, tests, production build, artifact upload, and GitHub Pages deployment.

The prior detailed implementation-status snapshot is preserved verbatim at `docs/history/IMPLEMENTATION-STATUS-through-2026-08-22.md`.

## Active production roster state

Production character packages currently represented in `characterManifest`:

- Lavi / Potato — AA-02
- Kraken / The Abyssal Drifter — AA-05
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- McFleurdel / The Fleur de Nuit — AA-07
- Accu / Pink Precision — AA-11

Cleo / The Gilded Stitch is archived and inactive. AA-06 is a governed placeholder and available for future approved assignment. The twelve-slot Character Select architecture remains intact.

## Cleo archive status — complete

PR #31 merged Cleo's reversible production retirement on 2026-08-26.

- Cleo is absent from active `characterManifest` and cannot be selected or sampled into the AI grid.
- AA-06 renders as a generic placeholder with no Cleo or Gilded Stitch production copy.
- Cleo's complete approved asset package, deterministic builder, GLB object IDs, runtime revision, technical records, and historical acceptance evidence remain preserved under the character archive contract.
- Main CI run `32996219644` passed LFS verification, typecheck, lint, tests, production build, and Pages deployment for merge commit `962ccf994fb488e8da64068d5b4a739a3c090bcb`.
- Manny manually confirmed the live deployment on 2026-08-26: **Cleo is gone from the live game.**
- Status: **LIVE ACCEPTED — CLEO ARCHIVE COMPLETE.**

## Krios production status — complete

Krios's gameplay and asset integration had succeeded before a prior usage-limit interruption, but the final repository continuity work was incomplete. PR #32 closed that gap without altering Krios's visuals, assets, stats, physics, orientation, runtime URLs, or gameplay behavior.

Verified production state:

- Krios is active in `characterManifest` as production AA-10 Straight-Line Heavy.
- The approved portrait and all six driver states use the controlled Krios runtime revision.
- The Hornbreaker production kart uses the enforced negative-Z visual orientation contract.
- Automated manifest coverage verifies Krios identity, kart path, all six driver-state URLs, orientation yaw, and 10 / 4 / 9 / 3 / 4 / 6 statistics.
- PR #30 originally merged the approved Hornbreaker production package at `ddbb2dea9e7f5e558cb8d5e76501b99219416f65`; main CI run `32591411527` passed.
- Manny confirmed on 2026-08-26 that **Krios is in the live game and all assets load as intended.**

Continuity closure completed by PR #32:

- `tools/verify-runtime-assets.mjs` now requires all three active AA-10 Hornbreaker GLBs: `kart.glb`, `kart-lod1.glb`, and `kart-lod2.glb`.
- Future production builds fail if any Hornbreaker GLB is an LFS pointer, malformed binary glTF, or loses `extras.forward: "-Z"`.
- `docs/avatars/KRIOS.md` records the merged, deployed, live-accepted state.
- `docs/assets/KRIOS-ASSET-BRIEF.md` records the completed integration gate and mandatory runtime verification coverage.
- `docs/TESTING.md` includes a Krios / Hornbreaker regression matrix and now requires every active production GLB package to be represented in the runtime verification list.
- PR #32 head CI run `32997599421` passed LFS verification, typecheck, lint, tests, and production build.
- PR #32 merged to `main` at `83545fdb22a8d6ac413a8f1b9ea5a4068eea5b19`.
- Post-merge main CI run `32997706788` passed the expanded runtime gate, typecheck, lint, tests, production build, artifact upload, and GitHub Pages deployment.
- Status: **LIVE ACCEPTED — KRIOS PRODUCTION INTEGRATION AND REPOSITORY CLOSURE COMPLETE.**

## McFleurdel production status — complete

- McFleurdel is active in `characterManifest` as AA-07 High-Speed Cruiser with 8 / 6 / 7 / 5 / 4 / 6 statistics.
- The approved portrait and six driver states use controlled revision `mcfleurdel-runtime-20260827-1`, including the corrected white viewer-left / black viewer-right hair lock.
- The Fleur de Nuit uses a black body, silver fleur-de-lis and trim, plum throne cockpit, ivory candles with violet flames, and the enforced negative-Z orientation contract.
- Temporary LFS bridge run `33037365942` regenerated the three approved GLBs, matched their locked hashes, uploaded only those object IDs, fetched them back, and passed `git lfs fsck`. The workflow was removed before review.
- PR #37 head CI run `33037428270` passed the complete production package.
- PR #37 merged to `main` at `aa24b655d30ba65438f512e0544e313da3fc343e`.
- Post-merge main CI run `33037485975` passed LFS verification, typecheck, lint, 54 tests, production build, artifact upload, and GitHub Pages deployment.
- Manny manually confirmed the live game on 2026-08-27: McFleurdel is selectable and the complete package looks good.
- Status: **LIVE ACCEPTED — MCFLEURDEL PRODUCTION CHECKPOINT COMPLETE.**

## Known defects / deferred work

- Slice 4 AI competitiveness remains intentionally weak; previously accepted at the current vertical-slice stage.
- Continue Slice 3 one-character-at-a-time intake and approval for remaining roster slots.
- Complete any still-unrecorded desktop/mobile acceptance checks for other integrated production characters as required by `docs/TESTING.md`.
- Items and AI item use remain Slice 5.
- Final HUD/audio/post-processing/optimization remain Slice 6.

## Toph production status — 2D package approved; kart modeling pending

- Manny approved Toph's character lock, definitive visual authority, and transformation rights on 2026-08-28.
- Toph is locked to AA-08 Turbo Bruiser with The Grave Shift: 7 / 5 / 7 / 4 / 8 / 5.
- Manny approved the portrait, front, rear, steer-left, steer-right, hit, and corrected victory designs on 2026-08-28.
- The initial generated previews contained baked checkerboard pixels despite the transparent-output request. The deterministic preparation step removed the edge-connected checkerboard before resizing rather than accepting opaque runtime files.
- Runtime derivatives are prepared at `public/assets/characters/aa-08/`: portrait at 256 × 256 and six driver states at 512 × 512. Every file is sRGBA, has non-opaque alpha, and has fully transparent corner pixels.
- Dark-background contact-sheet inspection confirms clean silhouettes. The corrected victory pose keeps Toph's lower body race-forward while his upper torso turns toward the viewer.
- Toph is not yet active in `characterManifest`; no fallback slot, live roster, AI grid, or runtime behavior has changed.
- Status: **2D PRE-KART CHECKPOINT PREPARED — THE GRAVE SHIFT GLB APPROVAL GATE PENDING.**

## Keeg production status — kart approved; pre-activation package prepared

- Keeg is locked to AA-04 Balanced Racer with The Mycelial Majesty on `agent/keeg-production`.
- Manny approved the portrait, front, rear, steer-left, steer-right, hit, and victory art on 2026-08-26.
- The first six driver exports were correctly rejected because their checkerboard backgrounds were baked RGB pixels rather than transparency.
- Corrected runtime files now meet the 256/512 size contract, use sRGBA, span alpha 0–1, and have fully transparent corner pixels.
- Manny approved The Mycelial Majesty Candidate 3 Revision 6 on 2026-08-26.
- Deterministic production GLBs are prepared at `public/assets/characters/aa-04/`: LOD0 20,260 triangles, LOD1 11,652, and LOD2 4,404. All use four materials, 13 required nodes, and `extras.forward: "-Z"`.
- `tools/verify-runtime-assets.mjs` now includes all three AA-04 GLBs.
- Temporary branch-scoped LFS bridge run `33015135969` rebuilt all three approved hashes, proved the committed pointers were unchanged, uploaded only the approved object IDs, deleted its runner cache, fetched the objects back, and passed `git lfs fsck`. The workflow was removed at remote commit `6443cb7cf660ae07f87a9f460abcc10bbf43e225`.
- Pre-activation PR CI run `33015347165` passed LFS materialization, `git lfs fsck`, typecheck, lint, tests, and production build.
- Keeg's AA-04 manifest uses controlled repair revision `keeg-runtime-20260826-2`, the approved Balanced Racer descriptor and 7 / 7 / 5 / 7 / 5 / 5 statistics, all six driver states, and the negative-Z visual yaw contract.
- Live acceptance found that the seven published AA-04 PNG payloads were only partially decodable and that Character Select's separate hard-coded kart-name lookup omitted Keeg. The correction restores the exact approved PNG exports, derives the displayed name from the manifest, and adds decode-level PNG verification to CI.
- Manny's subsequent mobile check passed the portrait, kart identity, PNG loading, and remaining runtime behavior but found Keeg's hands above the steering-wheel center. The bounded cockpit correction lowered only AA-04's driver sprite mount to `[0, 0.72, -0.12]`.
- Manny confirmed the corrected live mobile deployment on 2026-08-27. Keeg's portrait, The Mycelial Majesty name/model, all six driver states, cockpit alignment, orientation, and runtime behavior pass. Keeg's AA-04 production checkpoint is complete.
- Active-manifest CI, merge, deployment, and live acceptance remain pending.

## Next recommended action

Continue Toph's Slice 3 pipeline by producing the first reviewable deterministic LOD0 candidate for The Grave Shift. Do not activate AA-08 until the kart, LODs, runtime package, CI, deployment, and live manual checks pass.

## Approval gate

Toph's 2D package is approved. The Grave Shift's 3D geometry remains the next product-owner approval gate. No approval is pending for Krios, Cleo, or McFleurdel.
