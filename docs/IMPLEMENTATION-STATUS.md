# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 1.8**.

Latest verified live character checkpoint: `ef74ca9eabb2a242c02d35d72c55377ee9b5529c` — Lula's corrected production package passed mobile playtesting after the front-camera-only placement fix aligned her hands with The Verdant Hart steering wheel. Her portrait, kart, transparent sprite package, consistent skin tone, all six driver states, orientation, AI identity, and runtime behavior are accepted. Lula now supersedes Toph as the latest verified live character checkpoint.

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
- Lula / The Verdant Hart — AA-03
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

- Broader AI pace and difficulty tuning remains pending; racing-line and overtaking behavior now passes live testing.
- Numerical player-roster balance remains pending after the accepted acceleration and surface-transition correction. No driver statistics changed in that correction.
- Continue Slice 3 one-character-at-a-time intake and approval for remaining roster slots.
- Complete any still-unrecorded desktop/mobile acceptance checks for other integrated production characters as required by `docs/TESTING.md`.
- Items and AI item use remain Slice 5.
- Final HUD/audio/post-processing/optimization remain Slice 6.

## Player speed/acceleration coupling correction: live speed ceiling accepted

- Live evidence showed an inverted result: Kraken (Speed 6) reached 73 km/h and Lula (Speed 5) reached 80 km/h, while Accu (Speed 8) and Krios (Speed 10) each stalled near 35 km/h without boost.
- An isolated flat-asphalt regression reproduced the underlying coupling: Accu and Krios settled near 78.6 km/h while Kraken reached 101.6 km/h and Lula reached 97.7 km/h.
- Root cause: the controller applied engine acceleration and its Speed-defined clamp before Rapier's passive linear damping and collider friction. Those later losses made Acceleration determine whether a driver could reach the Speed cap.
- The branch correction makes the arcade controller the sole owner of longitudinal deceleration, lateral grip, and surface behavior. Passive linear damping and kart-ground friction are disabled; the existing explicit coasting, grip, off-road, drift, and boost logic remains in place.
- Automated coverage now verifies that every manifest profile sustains its Speed-defined asphalt maximum and that two profiles with the same Speed but different Acceleration have different early pace yet converge to the same maximum.
- `npm run validate` passes: strict typecheck, zero-warning lint, 58 tests across 14 files, runtime asset verification, and production build.
- Scope is limited to player physics coupling. Driver statistics, tuning curves, boost behavior, and AI pace were not rebalanced.
- PR #45 passed CI, merged to `main` at `f13f7f1cdf5b03f7d143d25691b9a5d54c35cea4`, and passed main validation and Pages deployment in run `33313727924`.
- Manny confirmed on 2026-08-30 that the corrected top speeds feel right. The Speed ceiling portion of the checkpoint is live accepted.

## Gameplay balance follow-up: live accepted

- Manny's follow-up test found that Acceleration 4 heavyweights reached full speed too similarly to Acceleration 8 featherweights, dirt and grass applied their reduced cap in one frame, AI racers cut through inside grass, and blocked AI racers queued bumper-to-bumper instead of passing.
- The Acceleration curve now uses the PRD formula `4.0 + 0.55 × Acceleration`, plus the documented high-speed taper. In isolated full-throttle simulation, Krios and Accu require roughly 7.7 and 7.2 seconds to reach 99% of their maximums; Lavi and Lula require roughly 4.7 seconds.
- Dirt and grass retain their Traction-defined sustained caps, but excess asphalt speed now decays toward those caps over time. The first off-road frame no longer clamps velocity directly to the surface maximum.
- AI lookahead now uses the PRD's 5–14 meter range. The prior implementation treated 20–30 spline samples as lookahead, producing approximately 50–70 meter chords that cut across the inside of curves.
- AI lane targets remain inside the road with a kart-width margin. Nearby-racer awareness scores clear lanes, commits to a pass with hysteresis, and reduces speed only when a close blocker still occupies the selected lane.
- Automated evidence covers the PRD Acceleration curve, a meaningful same-Speed acceleration gap, progressive dirt and grass slowdown, all seven AI profiles completing three laps with less than 2% grass time, road-bounded lateral travel, and a faster AI changing lanes to pass a slower racer.
- `npm run validate` passes: strict typecheck, zero-warning lint, 62 tests across 14 files, 81.1% statement coverage, runtime verification of 27 GLBs and 28 PNGs, and production build.
- Scope excludes driver-stat changes, Speed ceilings, boost values, items, AI item use, and final AI difficulty tuning.
- PR #46 merged and deployed at `60bd87b4ce83b45c7b9bd3ce2b61dbe1953f437e`.
- Manny confirmed on 2026-08-30 that the revised AI is substantially more believable and the gameplay correction feels much better.
- Status: **LIVE ACCEPTED — ACCELERATION, SURFACE TRANSITION, AND AI LANE CORRECTION COMPLETE.**

## Weight-driven collision speed loss: live accepted

- Kart contact now measures closing speed before applying its arcade impulse. Non-impact overlap below 0.75 m/s does not reduce forward speed.
- The governed retention curve combines impact severity, the racer's Weight, and a bounded opposing-Weight modifier. Full-severity retention remains between 65% and 96%.
- Accu at Weight 10 retains approximately 85.9% of forward speed in a severe collision with a Weight 2 racer, while the Weight 2 racer retains approximately 67.1%. Accu therefore has a measurable advantage while still losing roughly 14.1% speed.
- Retention affects only positive forward velocity. Existing lateral displacement remains mass-driven and is preserved after the reduction.
- Driver stats, Speed ceilings, Acceleration, surfaces, walls, items, and AI decision-making are unchanged.
- `npm run validate` passes: strict typecheck, zero-warning lint, 66 tests across 14 files, 81.6% statement coverage, runtime verification of 27 GLBs and 28 PNGs, and production build.
- PR #47 passed branch CI run `33338189709`, merged to `main` at `92415a50007fa80b327bcdce87896992733449ae`, and passed main validation and GitHub Pages deployment in run `33338245594`.
- Manny confirmed on 2026-08-31 that the collision work is successful and directed continued gameplay balancing.
- Status: **LIVE ACCEPTED — WEIGHT-DRIVEN KART COLLISION SPEED LOSS COMPLETE.**

## AI Speed-stat authority correction: branch validated; live acceptance pending

- Live testing found that AI racers consistently appeared unable to reach the unboosted maximum available to player-controlled versions of the same roster.
- Root cause: AI desired speed used an absolute grid-profile range of roughly 20.5–26.0 m/s rather than the selected character's Speed-derived `maxSpeed`. In the circuit regression, the first AI profile peaked at 24.1 m/s against a 29.7 m/s cap.
- Each AI now receives its selected character's kart maximum. On clear straights, neutral desired speed equals that maximum; profile pace instead controls how much speed the AI carries through curvature.
- Leading AI no longer receives a hidden top-speed reduction. Trailing top-speed allowance is explicit and bounded to 4%.
- Focused AI, controller, circuit, and overtaking regressions pass. Every configured pace profile reaches at least 98% of the tested character maximum while retaining valid laps, road bounds, grass limits, and stat-driven passing.
- Roster stats, player behavior, Acceleration, collision response, lane selection, surfaces, and items are unchanged.
- `npm run validate` passes: strict typecheck, zero-warning lint, 68 tests across 14 files, 81.6% statement coverage, runtime verification of 27 GLBs and 28 PNGs, and production build.
- Status: **BRANCH VALIDATED — PUBLICATION, DEPLOYMENT, AND LIVE PRODUCT-OWNER ACCEPTANCE REMAIN REQUIRED.**

## Lula production status — complete

- Manny approved Lula's character lock, definitive authority, transformation rights, AA-03 Feather Dirt Ace mapping, The Verdant Hart, all seven transparent 2D designs, and 3D Candidate 4 on 2026-08-29.
- Candidate 4 resolves the rejected candidates' floating components through open-ended root tubes buried within overlapping organic joints. Dedicated foliage geometry renders recognizable green leaf clusters consistently across viewers.
- Deterministic production GLBs: LOD0 21,948 triangles / LOD1 8,954 / LOD2 4,746. Each has five materials, 13 required nodes, and `extras.forward: "-Z"`.
- Locked SHA-256 object IDs: LOD0 `6842eecf711117d8ca521ebd9620926268452193f5c3b9e2ba7ad9aba090c26c`; LOD1 `b9a267a6a41d14a674771cc0137d1b0445e1a264bfa8b2c5acc7c6685ab399cd`; LOD2 `3a062ee6bee2502bdd3914063cc549a08e4de151ebf5bcfc3a52fe9658eb57f0`.
- AA-03 activation now uses corrected revision `lula-runtime-20260830-2`, all six driver states, approved stats, The Verdant Hart, and `NEGATIVE_Z_KART_VISUAL_YAW`.
- Runtime verification covers all three GLBs and all seven PNGs.
- The branch-scoped LFS bridge regenerated and uploaded only the three locked object IDs. PR #44 CI run `33266092639` then materialized them in a clean checkout, passed `git lfs fsck`, typecheck, lint, 56 tests, runtime asset verification, and the production build.
- The temporary write-enabled workflow was removed before PR #44 merged at `7822ba05dd5e81b0da40b6038596c6fc12095c5f` and deployed to GitHub Pages.
- Live mobile testing after PR #44 exposed opaque white background islands and hair-edge ribbons in all seven Lula PNGs. The original validation had checked dimensions, decoding, alpha range, and transparent corners but not enclosed neutral background components. The local repair regenerates the full package with component-based alpha cleanup and adds a CI regression gate that reconstructs PNG scanlines and rejects neutral-white pixels outside protected face/eye regions.
- Side-by-side review then exposed a second package-wide defect: rear, steer-left, steer-right, hit, and victory used a saturated orange skin palette inconsistent with the approved portrait/front authority. `tools/assets/repair_lula_skin_tone.py` applies an idempotent spatially constrained palette normalization; automated comparison confirms zero changes outside reviewed skin masks and zero alpha changes.
- Main checkpoint `514113e448c264c210cdb8cb1dced33cfc31d092` deployed both sprite corrections after CI run `33286572927` passed validation and GitHub Pages deployment. Manny confirmed the transparency and skin tone during mobile playtesting.
- That playtest exposed one remaining acceptance defect: Lula's front-facing hands rendered above The Verdant Hart steering wheel. Main checkpoint `ef74ca9eabb2a242c02d35d72c55377ee9b5529c` applied the same front-camera-only placement mechanism proven by Toph, using `[0, 0.45, -0.12]`; The Verdant Hart and The Grave Shift place their wheels at effectively the same vertical mount. All non-front driver states remained unchanged. CI run `33286891380` passed validation and GitHub Pages deployment.
- Manny confirmed the corrected live mobile deployment on 2026-08-30. Lula's portrait, The Verdant Hart, transparent sprite package, corrected skin tone, all six driver states, front hand-to-wheel alignment, orientation, AI identity, and runtime behavior pass. Lula's AA-03 production checkpoint is complete.

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
