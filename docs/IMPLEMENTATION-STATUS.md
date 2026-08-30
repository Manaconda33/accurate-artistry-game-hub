# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 1.6**.

Latest verified live character checkpoint: `a8fea24b309e3123115e9a04c3aee0614085bdc1` — PR #42 recorded Toph's completed live production acceptance after the front-view hand-to-wheel correction passed manual testing. Toph's portrait, The Grave Shift, all six driver states, orientation, AI identity, and runtime behavior are accepted. PR #44 subsequently integrated and deployed Lula at main checkpoint `7822ba05dd5e81b0da40b6038596c6fc12095c5f`, but mobile playtesting exposed sprite-alpha and chase-camera skin-palette defects. Their local corrections remain uncommitted pending a playable test build and Manny's confirmation, so Lula does not supersede Toph as the latest verified live character checkpoint.

The prior detailed implementation-status snapshot is preserved verbatim at `docs/history/IMPLEMENTATION-STATUS-through-2026-08-22.md`.

## Active production roster state

Production character packages currently represented in `characterManifest`:

- Lavi / Potato — AA-02
- Kraken / The Abyssal Drifter — AA-05
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- Keeg / The Mycelial Majesty — AA-04
- McFleurdel / The Fleur de Nuit — AA-07
- Toph / The Grave Shift — AA-08
- Lula / The Verdant Hart — AA-03 (staged; not yet live accepted)
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

## Lula production status — deployed; corrective playtest pending

- Manny approved Lula's character lock, definitive authority, transformation rights, AA-03 Feather Dirt Ace mapping, The Verdant Hart, all seven transparent 2D designs, and 3D Candidate 4 on 2026-08-29.
- Candidate 4 resolves the rejected candidates' floating components through open-ended root tubes buried within overlapping organic joints. Dedicated foliage geometry renders recognizable green leaf clusters consistently across viewers.
- Deterministic production GLBs: LOD0 21,948 triangles / LOD1 8,954 / LOD2 4,746. Each has five materials, 13 required nodes, and `extras.forward: "-Z"`.
- Locked SHA-256 object IDs: LOD0 `6842eecf711117d8ca521ebd9620926268452193f5c3b9e2ba7ad9aba090c26c`; LOD1 `b9a267a6a41d14a674771cc0137d1b0445e1a264bfa8b2c5acc7c6685ab399cd`; LOD2 `3a062ee6bee2502bdd3914063cc549a08e4de151ebf5bcfc3a52fe9658eb57f0`.
- AA-03 activation now uses corrected revision `lula-runtime-20260830-2`, all six driver states, approved stats, The Verdant Hart, and `NEGATIVE_Z_KART_VISUAL_YAW`.
- Runtime verification covers all three GLBs and all seven PNGs.
- The branch-scoped LFS bridge regenerated and uploaded only the three locked object IDs. PR #44 CI run `33266092639` then materialized them in a clean checkout, passed `git lfs fsck`, typecheck, lint, 56 tests, runtime asset verification, and the production build.
- The temporary write-enabled workflow was removed before PR #44 merged at `7822ba05dd5e81b0da40b6038596c6fc12095c5f` and deployed to GitHub Pages. Live acceptance is withheld.
- Live mobile testing after PR #44 exposed opaque white background islands and hair-edge ribbons in all seven Lula PNGs. The original validation had checked dimensions, decoding, alpha range, and transparent corners but not enclosed neutral background components. The local repair regenerates the full package with component-based alpha cleanup and adds a CI regression gate that reconstructs PNG scanlines and rejects neutral-white pixels outside protected face/eye regions.
- Side-by-side review then exposed a second package-wide defect: rear, steer-left, steer-right, hit, and victory used a saturated orange skin palette inconsistent with the approved portrait/front authority. `tools/assets/repair_lula_skin_tone.py` applies an idempotent spatially constrained palette normalization; automated comparison confirms zero changes outside reviewed skin masks and zero alpha changes. Both corrections remain uncommitted pending a playable test build and Manny's desktop/mobile confirmation.

## Toph production status — complete

- Manny approved Toph's character lock, definitive authority, rights, AA-08 Turbo Bruiser mapping, The Grave Shift, all seven 2D designs, and corrected victory pose on 2026-08-28.
- Manny rejected Candidate 1 because its rounded pale nose construction read as a clown face and did not match the definitive purple armored design.
- Manny approved rebuilt Candidate 2 on 2026-08-28: purple-dominant armored body, bronze perimeter, flat trapezoidal skull shield, angular integrated thorn crown, low splitter, enclosed sidepods, enclosed rear engine, and twin violet exhausts.
- Deterministic production GLBs: LOD0 8,604 triangles / LOD1 4,452 / LOD2 2,344. Each has 13 required nodes and `extras.forward: "-Z"`.
- Locked SHA-256 object IDs: LOD0 `87db250bcacbbbe93afdee0e4a346ff3c5aaca7fbb90668af383b1772154c953`; LOD1 `1d3b62f715e6288b01447eafe2a81a07b09fe676019b1849ff3b5b78ad9c4d23`; LOD2 `2c38dd14a334443fff3f872fc618210642f51dfc8b612bf1f075b347a5a65be7`.
- The authorized temporary LFS workflow rebuilt the locked bytes. A subsequent clean CI checkout materialized the objects and passed `git lfs fsck`; the temporary write-enabled workflow was removed before review.
- AA-08 activation uses controlled revision `toph-runtime-20260828-1`, all six driver states, The Grave Shift, the approved stats, and `NEGATIVE_Z_KART_VISUAL_YAW`.
- Runtime verification covers all three GLBs and all seven PNGs.
- PR #39 merged the approved production package at `edf9cf54dce39d968497ffc9f72f87329cfb1ac6`.
- Live testing found the front driver frame above the steering wheel. PR #40 introduced a front-only placement override, and PR #41 applied the verified full correction at merge commit `3353109944c3975e0bbbbac4dffbcc24f07bc58b` without moving chase, steering, hit, victory, or AI rear states.
- Manny confirmed on 2026-08-28 that the corrected live deployment passes all tests. Toph's portrait, The Grave Shift, all six driver states, front hand-to-wheel alignment, orientation, AI identity, and runtime behavior are accepted.
- Status: **LIVE ACCEPTED — TOPH PRODUCTION CHECKPOINT COMPLETE.**

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

Continue with the next approved Slice 3 character package. Do not begin Slice 5 or reorder the PRD roadmap without Manny approval.

## Approval gate

No approval remains pending for Toph, Krios, Cleo, or McFleurdel. The next character intake remains separately approval-gated.
