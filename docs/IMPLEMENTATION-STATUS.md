# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.0**.

Latest verified live deployment checkpoint: `ac39b1ad490999007429713a3f5b82aca274f1dc`. The Lavi and Toph front-action batch is live accepted under `lavi-runtime-20260902-5` and `toph-runtime-20260902-2`.

Current deployment checkpoint: PR #70 deployed Lavi's placement-only correction at `ac39b1ad490999007429713a3f5b82aca274f1dc`. The live bundle maps Lavi's five camera-facing states to `[0, 0.9, -0.12]` and preserves Toph at `[0, 0.45, -0.12]`. Manny accepted Lavi's corrected live placement on 2026-09-03. Lula and Accu are the authorized final candidate batch.

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

## Front-facing action-state parity — in progress

- Manny approved closing the rear-camera action-state gap on 2026-09-01. The target package adds front-steer-left, front-steer-right, front-hit, and front-victory without replacing any approved chase or neutral-front art.
- Nine active production drivers require four camera-facing action states each. Kraken, Manaconda, Krios, Keeg, McFleurdel, Lavi, and Toph have live-accepted packages. Lula and Accu's final eight candidates are visually approved and locally integrated; publication remains gated.
- Rollout normally remains one character at a time. Kraken was the pilot; after its live acceptance, Manny authorized two drivers per batch for the remaining rollout.
- Runtime infrastructure may use the approved neutral front frame as a rollout fallback. No new raster enters a runtime path and no character revision changes until Manny approves that character's candidate package.
- Manny approved Kraken's front-steer-left, front-steer-right, and front-hit candidates on 2026-09-01. They are integrated with the unchanged approved front-victory frame under controlled revision `kraken-runtime-20260901-2`.
- The runtime gate now decodes all four Kraken front-action PNGs, enforces 512 x 512 non-interlaced RGBA data, and rejects non-transparent corners.
- Local `npm run validate` passed on 2026-09-01: strict typecheck, zero-warning lint, 16 Vitest files / 83 tests, 83.14% statement coverage, 27 materialized GLBs, 40 decoded runtime PNGs, and a production Vite build.
- PR #59 head CI run `33464307463` passed. The PR merged to `main` at `6bb689d6b3b6511e601d8445088ec011388a0497`; main run `33464380102` passed validation and GitHub Pages deployment.
- The live page serves bundle `index-DwfeHgzB.js`, which references `kraken-runtime-20260901-2` and the three new front-action paths. SHA-256 checks against the four deployed camera-facing action responses match the approved local files: left `6c35c015d1208dbfb922b1a7986bf81002497bbed7d8d73c882de094ca5cfa34`, right `f6404831ebdb3ea8619d0e15f43c0430dc3e6042652b7eb37bd47bbb735b5dd8`, hit `5f1c4abe842599e2d4fddc4fa9529e24acc0008914228b0fca86fa793eef7666`, victory `4e77db3a622b6fc472bbd031329e9cc80bc3c119dbeab427a9ccf97cbc596609`.
- Manny reported the requested live test passed on 2026-09-01. Kraken's four camera-facing action states, return to chase-facing actions, alpha edges, seated placement, and single-wheel presentation all pass.
- Status: **LIVE ACCEPTED — KRAKEN FRONT-ACTION PILOT COMPLETE; NEXT DRIVER UNLOCKED.**

### Manaconda and Krios batch — live accepted

- Manny approved Manaconda's four camera-facing action frames on 2026-09-01. Each frame preserves the approved front footprint, Driftwood Crest, Paprika, and exactly one sprite-owned steering wheel for the wheel-free Wayfinder.
- Manny approved Krios's four camera-facing action frames on 2026-09-01 after the enclosed pale matte between his horns was cleared to transparency. Krios's frames contain no wheel or kart geometry because The Hornbreaker supplies the modeled steering control.
- The approved runtime derivatives are 512 x 512 non-interlaced sRGBA PNGs with transparent corners. Krios's steering and victory frames retain two substantial enclosed transparent horn apertures as a build-time regression contract.
- Controlled revisions are `manaconda-runtime-20260901-3` and `krios-runtime-20260901-2`.
- Runtime SHA-256 values: Manaconda left `20216cef593ac6fe564cbbaefaffa9264a2ee6211bcece1c567099378163901e`, right `888049aa7be403254a2d0b632da5692ab7b30251826524bc5f2abbcd44137feb`, hit `35097ef795d91497482d2da62ca5dffe70301cc10e5fc13d33327e7d2f3d976e`, victory `969016a528b01b65a2ff541397b134c70feb6679225493006e6222ef2bb47127`; Krios left `5ed347c6c873dbdcdc17e537862b276789b3a761dca2a7733141dcea6ca58a0d`, right `c04e7edb9093f520b57e2f02e85de7aebf1f133f5ca02bb9196ae1522ec51789`, hit `e5743a6e1f62d02ea50dcb3d0afcfb5c6b2d39440122ce93e887f1028d24e127`, victory `a2e7a50042d22583d96570fe0354dbf1ae272f5b022dad99f8f82127e13b061f`.
- Clean local validation passed on 2026-09-01: `npm ci`, strict typecheck, zero-warning lint, 16 Vitest files / 83 tests, 83.14% statement coverage, 27 materialized runtime GLBs, 48 decoded runtime PNGs, Krios horn-aperture verification, and a production Vite build.
- PR #62 head CI run `33507676888` passed. The PR merged to `main` at `7b58fdff7ca3c0d67a4ca70c1df0f6ddf287889f`; main run `33507775105` passed validation and GitHub Pages deployment.
- The live page serves bundle `index-BTjqiGYl.js`, which references both controlled revisions and all eight new front-action paths. SHA-256 checks against every deployed PNG response match the approved local hashes recorded above.
- Manny confirmed the live playtest on 2026-09-01 against deployed checkpoint `2ca852b47f16b8221275ee2b5542650d609b9a0d`. Both steering directions, hit, victory, chase-state restoration, transparency, cockpit placement, and steering-control ownership pass. Manaconda shows exactly one wheel. Krios uses The Hornbreaker's modeled wheel with no duplicate, and the areas between his horns remain transparent.
- Status: **LIVE ACCEPTED — MANACONDA AND KRIOS FRONT-ACTION BATCH COMPLETE; NEXT TWO-DRIVER BATCH UNLOCKED.**

### Keeg and McFleurdel batch — live accepted

- Manny approved Keeg's four camera-facing action frames on 2026-09-01. The steering frames use opposite camera-side leans and distinct arm positions. All four remain free of wheel and kart geometry because The Mycelial Majesty supplies the modeled steering control.
- Manny approved McFleurdel's four camera-facing action frames on 2026-09-01 after rejecting residual white matte in both steering frames. The approved cleanup makes the black-hair curl interiors and arm gaps transparent while preserving the white hair and silver costume details.
- Controlled revisions are `keeg-runtime-20260901-3` and `mcfleurdel-runtime-20260901-2`.
- Runtime SHA-256 values: Keeg left `907140e23dc8d41e566d2ab013baa95c2a1d553bb3c5c56ea541a3136397f9a2`, right `75009c11ab0628999d9530e8c5846e3ca48f4979a72395a6f0478b5ba36c5e06`, hit `6d6b61d687525a2bfb63a575fba95d113bcbf9072dcf76d8585b9bff6f89304d`, victory `dcdfc3ca451660e61db013b9699029f12ef2242008556c3b9355a2a53b8f790b`; McFleurdel left `d69dc042efab13389fd259bfcee8556328657bda3e06ce1cbcdb155f4ab62a41`, right `e2c99f93a3f33fb627967de88852cfe49289f0fe6fffc007beda1c1aa079ce7b`, hit `440b48865114ac4fc2c6acde6f5133c001c3a4c18ccb5fc72772791e874f1c21`, victory `cb5be9ae847303aa8edf74204e809a1bb690754784d671f145243eb1b195f36f`.
- The runtime PNG gate now covers all eight new files. McFleurdel's two steering frames also fail validation if a connected pale matte component of 30 pixels or more reappears in the approved hair or arm gaps.
- Local `npm run validate` passed on 2026-09-01: strict typecheck, zero-warning lint, 16 Vitest files / 83 tests, 83.14% statement coverage, 27 materialized runtime GLBs, 56 decoded runtime PNGs, the McFleurdel matte regression check, and a production Vite build.
- PR #65 head CI run `33563640441` passed. The PR merged to `main` at `8a63a2de5aaffc1b605d9afc0a6e448615b03755`; main run `33563732551` passed validation and GitHub Pages deployment.
- The live page serves `assets/index-CmnuEd5x.js` and `assets/KartTimeTrial-C3p-RRyJ.js`. The game bundle references both controlled revisions, and SHA-256 checks against every deployed PNG response match the approved hashes recorded above.
- PR #66 recorded the deployment evidence and merged at `f8a2ed8be0d72fde62c9403dae4b15e94222f7da`; main run `33564231150` passed validation and GitHub Pages deployment.
- Manny confirmed the live playtest on 2026-09-01 against deployed checkpoint `f8a2ed8be0d72fde62c9403dae4b15e94222f7da`. Both steering directions, hit, victory, chase-state restoration, transparency, cockpit placement, and steering-control ownership pass. Keeg and McFleurdel each show exactly one modeled wheel with no sprite duplicate, and McFleurdel's reviewed hair and arm gaps remain transparent.
- Status: **LIVE ACCEPTED — KEEG AND MCFLEURDEL FRONT-ACTION BATCH COMPLETE; LAVI AND TOPH BATCH APPROVED.**

### Lavi and Toph batch — live accepted

- Manny approved both four-frame candidate sheets on 2026-09-02. Lavi's front actions preserve the native generated alpha. Toph's reviewed derivatives remove the opaque checkerboard and one-pixel edge fringe from the generated previews.
- Both steering pairs follow commanded kart direction: left leans toward the viewer's right and right leans toward the viewer's left. Both packages are free of wheel and kart geometry because Potato and The Grave Shift supply modeled steering controls.
- Controlled revisions are `lavi-runtime-20260902-5` and `toph-runtime-20260902-2`. Toph retains the accepted front placement `[0, 0.45, -0.12]`. Lavi's deployed `[0, 0.45, -0.12]` placement failed live review because Potato's tall body hides the torso and leaves the head too low behind the wheel.
- Runtime SHA-256 values: Lavi left `1a8f3594fe94da9f85d62a390862f6ba043057549d129e03fb8dd4f6a6d50ba6`, right `25d25b7896844651a559521afd5b0a1be69d3cb6b5d3326e69892770a7c9f958`, hit `05303e58b4f79b0369edfd8f9b8b6e9168156d49de9236307309880384da2719`, victory `b08725190e2234c0014151db0073ee7522ac94c508d4a99654d333046d0f6c8c`; Toph left `d2842af32df5e92c10454497b8da3cba92591e52324df571f67bd0ebf7c4f39b`, right `663c18ef0a5fbcbb0cffc796bcd9c209675941a95fc082903360a536b9a33f48`, hit `bf2411404f6311bcb648966ca64f5c5f06a4ce4e3b728ca75fd3f0d56323691d`, victory `96ee0fcf6a8ca14e12db258ba58797d8161ca463e33d6c86a19db4bbe2beea9c`.
- Clean local validation passed on 2026-09-02: `npm ci`, strict typecheck, zero-warning lint, 16 Vitest files / 83 tests, 83.14% statement coverage, 27 materialized runtime GLBs, 64 decoded runtime PNGs, and a production Vite build.
- The built bundle references both controlled revisions and all eight new runtime paths. Every copied `dist/` PNG hash matches its approved source hash.
- Review sheets, discarded candidates, temporary generated files, and Python cache files remain outside the repository.
- PR #68 head CI run `33661673756` passed. The PR merged to `main` at `842778422b6be45b6e4c5da5f4a0b7772e030b74`; main run `33661819292` passed validation and GitHub Pages deployment.
- The live page serves `assets/index-BLnZQ_xQ.js`. The bundle references both controlled revisions and all eight action paths, and SHA-256 checks against every deployed PNG response match the approved hashes recorded above.
- Manny confirmed Toph passes the live camera/action matrix on 2026-09-02. Toph's placement, steering directions, hit, victory, chase restoration, transparency, and single-wheel presentation are accepted.
- Lavi's correction raises only the five camera-facing states to `[0, 0.9, -0.12]`. Sprite bytes, chase-facing placement, Potato, modeled-wheel ownership, camera behavior, physics, stats, and Toph remain unchanged.
- Fresh correction validation passed on 2026-09-02: `npm ci`, strict typecheck, zero-warning lint, 16 Vitest files / 83 tests, 83.14% statement coverage, 27 materialized runtime GLBs, 64 decoded runtime PNGs, and a production Vite build.
- PR #70 head CI run `33664237133` passed. The PR merged to `main` at `ac39b1ad490999007429713a3f5b82aca274f1dc`; main run `33664361276` passed validation and GitHub Pages deployment.
- The live page serves `assets/index-CjbkWPH8.js`. The bundle maps Lavi to `[0, 0.9, -0.12]`, preserves Toph at `[0, 0.45, -0.12]`, and retains both controlled revisions and all eight approved action paths.
- PR #71 recorded the placement deployment evidence and merged at `cd9dad3013208e973421616d90b534c3bbfc4e77`; main run `33664925678` passed validation and GitHub Pages deployment.
- Manny approved Lavi's corrected live cockpit presentation on 2026-09-03. Lavi and Toph now both pass steering-left, steering-right, hit, victory, chase restoration, transparency, cockpit placement, and single-wheel presentation.
- Status: **LIVE ACCEPTED — LAVI AND TOPH FRONT-ACTION BATCH COMPLETE; LULA AND ACCU BATCH STARTED.**

### Lula and Accu batch — locally integrated; publication pending

- Manny authorized Lula and Accu as the final two-driver front-action batch on 2026-09-03.
- Prepare Lula first, then Accu, using each driver's approved neutral front frame and existing character record as the visual authority.
- Manny approved Lula's front-steer-left, front-steer-right, front-hit, and front-victory review set on 2026-09-03, then approved Accu's four-frame set and authorized local integration.
- Accu's steering pair uses opposite camera-side arm emphasis, hit reads as a forward collision recoil, and victory retains the forward seated lower body. Checkerboard removal produced transparent cutouts, and a detached 13-pixel artifact in the hit candidate was cleared before approval.
- Each driver requires front-steer-left, front-steer-right, front-hit, and front-victory. Direction names follow commanded kart direction: left leans toward the viewer's right, and right leans toward the viewer's left.
- Lula's candidates must preserve her approved front complexion, leaf forehead mark, green hair, seated footprint, wheel-free art, and `[0, 0.45, -0.12]` front placement contract. The Verdant Hart owns the modeled wheel.
- Accu's candidates must preserve the pink-hat silhouette, two-tone pink hair, heart-pattern top, seated orientation, and front placement `[0, 0.9, 0.22]`. Pink Precision owns the modeled front wheel; candidate art must not add a duplicate.
- The eight approved 512 x 512 sRGBA frames are locally integrated under `lula-runtime-20260903-3` and `accu-runtime-20260903-3`. The manifest supplies all ten driver states for both characters while preserving Lula's `[0, 0.45, -0.12]` and Accu's `[0, 0.9, 0.22]` camera-facing placements.
- Runtime SHA-256 values: Lula left `4d4efdacb0d38c924b356d2a32ace046ac744a2ec6da0329a8c60a49e545a0ff`, right `6a400c0d2745b2e3fbe13e100fb3b99d09d404ea98e95c6dc995788aee0376ea`, hit `3e99891c712310ff8018b9db9258e8f9a77be949b7403bd28d7a6b8fd679f444`, victory `5c6b662f0449a811319b89396a8053c6e58dc9b0f4916162e37ad5a06434f453`; Accu left `374dc4d70effbfb31b149d8479c206ca147ea3247d2479a519ccca4a04aba91a`, right `c14a5e45c2d89858c2b1b0ef925f738a46bf7198fb21dad7023baaf6640b682c`, hit `21d05413adcbd711f1f47b43a685b1cf7b528cbf8603680805f3936fa2920c37`, victory `f35804907230bb1db0623c84622a34ac5be8a30fb8183186c14f3ab38e8524eb`.
- The runtime gate now decodes all 72 production PNGs, checks the eight new files for 512 x 512 non-interlaced RGBA data and transparent corners, and retains Lula's neutral-white background rejection. Eight near-transparent white fringe pixels in Lula's hit frame and fourteen in victory were cleared before the gate passed.
- Local `npm run validate` passed on 2026-09-03: strict typecheck, zero-warning lint, 16 Vitest files / 83 tests, 83.14% statement coverage, 27 materialized runtime GLBs, 72 decoded runtime PNGs, and a production Vite build. The built bundle references both new revisions and all eight action paths. Every built PNG hash matches its approved source file.
- Review sheets, discarded generations, temporary files, and Python caches remain outside the repository. No kart GLB, gameplay logic, physics, stats, camera geometry, or previously accepted asset changed.
- Approval gate: local integration is complete. Publishing the branch, opening and merging the PR, deploying Pages, and recording live acceptance require Manny's next approval.
- Status: **VALIDATED LOCALLY — PUBLICATION APPROVAL REQUIRED.**

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
- Remaining HUD elements, audio, post-processing, and optimization remain Slice 6; the shared-topology race minimap is now implemented on its validation branch.

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

## AI Speed-stat authority correction: live accepted

- Live testing found that AI racers consistently appeared unable to reach the unboosted maximum available to player-controlled versions of the same roster.
- Root cause: AI desired speed used an absolute grid-profile range of roughly 20.5–26.0 m/s rather than the selected character's Speed-derived `maxSpeed`. In the circuit regression, the first AI profile peaked at 24.1 m/s against a 29.7 m/s cap.
- Each AI now receives its selected character's kart maximum. On clear straights, neutral desired speed equals that maximum; profile pace instead controls how much speed the AI carries through curvature.
- Leading AI no longer receives a hidden top-speed reduction. Trailing top-speed allowance is explicit and bounded to 4%.
- Focused AI, controller, circuit, and overtaking regressions pass. Every configured pace profile reaches at least 98% of the tested character maximum while retaining valid laps, road bounds, grass limits, and stat-driven passing.
- Roster stats, player behavior, Acceleration, collision response, lane selection, surfaces, and items are unchanged.
- `npm run validate` passes: strict typecheck, zero-warning lint, 68 tests across 14 files, 81.6% statement coverage, runtime verification of 27 GLBs and 28 PNGs, and production build.
- PR #48 passed branch CI run `33348287518`, merged to `main` at `a9e9739616450a25fd967329ebbada6cd769d532`, and passed main validation and GitHub Pages deployment in run `33348420077`.
- Manny confirmed on 2026-08-31 that the live AI Speed-stat correction passed playtesting.
- Status: **LIVE ACCEPTED — AI SPEED-STAT AUTHORITY CORRECTION COMPLETE.**

## Shared-topology race minimap: live accepted

- The live HUD now includes an SVG minimap derived from Circuit Alpha's same 384 ordered samples used for projection and race progress.
- All eight markers use nearest-neighbor head crops from their approved transparent 2D portraits. The player head is larger, gold-outlined, and rendered last so it remains legible in a cluster.
- Racer markers interpolate normalized track progress; the immutable course path is cached rather than rebuilt during every HUD frame.
- Desktop placement is below the Lap HUD. Mobile uses a reduced upper-left map that remains above the bottom driving controls and away from the right-side Position HUD. The map hides during the compact finish presentation.
- `npm run validate` passes: strict typecheck, zero-warning lint, 72 tests across 15 files, 82.9% statement coverage, runtime verification of 27 GLBs and 28 PNGs, and production build.
- PR #49 passed branch CI run `33350027338`, merged to `main` at `b10308fdbe44025c953145daaf48360d46363b78`, and passed main validation and GitHub Pages deployment in run `33350273528`.
- Manny confirmed on 2026-08-31 that the live minimap looks good and approved its track-agnostic topology model.
- Status: **LIVE ACCEPTED — RESPONSIVE SHARED-TOPOLOGY RACE MINIMAP COMPLETE.**

## Shared player/AI driver-sprite states: live accepted

- Runtime audit found that player sprites already selected rear, optional front, steering, hit, and victory states, while AI production drivers loaded only the neutral rear texture.
- One shared selector now governs player and AI priority: victory, hit, front during rear view, steering, then neutral rear. AI-to-AI and player-to-AI contacts activate hit for every involved production driver.
- Accu's sprite package owns the steering control in chase-oriented states, so Pink Precision's modeled steering wheel is hidden for rear, steering, hit, and victory and remains available only for the neutral front frame.
- Manny approved the missing front views for Lavi, corrected Manaconda, and Accu on 2026-08-31. Deterministic pixel cleanup converted their baked checkerboards to true alpha without generative redraw.
- Accu's approved steer-left, steer-right, and victory wheel apertures now have genuine transparency. Runtime byte revisions were bumped for all three affected character packages.
- Every active production driver package now declares all six states, and the manifest type makes `front` mandatory for production sprite packages.
- `npm run validate` passes: strict typecheck, zero-warning lint, 76 tests across 16 files, 83.0% statement coverage, runtime verification of 27 GLBs and 36 decoded PNGs including transparent-corner and Accu-aperture regression gates, and production build.
- PR #50 passed branch CI run `33376955408`, merged to `main` at `faeff1dc4f2312cdc2f3bbd76e5d8e474fbd2c1a`, and passed main validation and GitHub Pages deployment in run `33377109106`.
- The deployed bundle exposes controlled Lavi, Manaconda, and Accu revisions, and all three new front sprite paths return successfully from Pages.
- PR #52 corrected camera-relative front/rear selection and Accu's cockpit depth. PR #53 then preserved that state selection while allowing a stopped kart to relaunch on supported grass or dirt and suppressing Pink Precision's modeled steering wheel whenever Accu's active sprite already contains one.
- Manny confirmed on 2026-08-31 that the grass relaunch correction passes and that the chase view no longer exposes the modeled steering wheel.
- The same live test rejected Accu's remaining presentation: the rear-camera front frame reads as a floating head behind the cannon, and the chase-camera rear frame has a conspicuously straight lower hair cutoff at the cockpit edge.
- PR #54 is a deployed but visually unapproved test candidate. It lowers chase-oriented states from `[0, 0.95, 0.22]` to `[0, 0.82, 0.22]` so the lower raster edge is buried by the cockpit, and raises only the front-camera frame from `[0, 0.45, 0.22]` to `[0, 0.9, 0.22]` to restore a seated-driver composition. It does not alter physics, camera logic, sprite bytes, or steering-control visibility.
- PR #54 branch CI run `33446381625` passed. It merged to `main` at `87ddf85b1302cc61f62e486c893136be04b84835`; main run `33446473334` passed validation and GitHub Pages deployment. The public build loaded the Accu selection and Pink Precision race handoff, but the available cloud browser disables WebGL, so it could not render the chase/rear-camera frames. Product-owner desktop/mobile visual confirmation remains required.
- Manny's subsequent live screenshots rejected PR #54: moving the chase frame vertically left the same firm horizontal cockpit-occlusion seam, and the improved rear-camera composition still did not expose a readable steering wheel.
- The next candidate changes depth rather than repeating the failed vertical-placement approach. Chase-oriented Accu states move from Z `0.22` to `-0.72`, placing the sprite ahead of the horizontal cockpit collar but behind Pink Precision's rear chassis. The neutral front frame stays at `[0, 0.9, 0.22]`; only while that frame is active, the modeled steering control moves from its authored local Z `0.48` to `-0.46` so the model's enforced PI rotation places the wheel in front of the sprite. Other characters, approved PNG bytes, physics, camera selection, and grass relaunch behavior remain unchanged.
- Local validation passed: typecheck, lint, all 81 tests, production-asset verification, and the production build. No PNG or GLB bytes changed.
- PR #56 CI run `33447987037` passed and merged to `main` at `404c32b05a78a05080c4150dbe4acd3ca7125cbb`. Main run `33448083520` passed both validation and GitHub Pages deployment, and the public page loaded the candidate production bundle `index-C436jMYp.js`. The available cloud browser disables WebGL, so it could not render either acceptance camera.
- Manny approved the deployed correction on 2026-08-31. The chase-camera hair edge, rear-camera seated composition and visible steering wheel, chase-state modeled-wheel suppression, and stopped-on-grass relaunch behavior all pass the product-owner live gate.
- Status: **LIVE ACCEPTED — SHARED DRIVER STATES AND ACCU RUNTIME CORRECTIONS COMPLETE.**

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
- The front-action expansion is merged, deployed, and live accepted under `keeg-runtime-20260901-3`.

## Next recommended action

Retest Lavi's deployed neutral front, steering, hit, victory, chase restoration, cockpit placement, and single modeled wheel. Do not begin the Lula and Accu batch until Lavi passes.

## Approval gate

Toph's front-action expansion is live accepted. Lavi's placement correction is deployed; live acceptance remains gated. Lula and Accu remain gated before candidate creation.
