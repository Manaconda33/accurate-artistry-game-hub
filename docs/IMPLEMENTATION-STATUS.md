# Implementation Status

## Current slice

**Slice 3 - Character Selection & Avatar Ingestion: Krios driver-art production in progress**

## Slice 3 Krios intake and driver-art checkpoint

- Manny approved Krios's definitive character lock, The Hornbreaker's definitive kart design, source transformation rights, and AA-10 Straight-Line Heavy mapping on 2026-08-22.
- Krios uses he/him pronouns and is locked to AA-10: 10 / 4 / 9 / 3 / 4 / 6. `aa-10` is uniquely allocated in `docs/ROSTER-MAPPING.md`.
- The approved character record and production brief are `docs/avatars/KRIOS.md` and `docs/assets/KRIOS-ASSET-BRIEF.md`.
- Manny approved the definitive portrait and the separately composed front driver frame.
- Runtime derivatives are stored at `public/assets/characters/aa-10/`. The portrait is 256 x 256 and the front frame is 512 x 512. Both are sRGB RGBA PNGs with genuine transparency and transparent corner pixels.
- The front frame contains no kart or steering-wheel geometry and preserves a seated, two-handed neutral driving pose.
- Rear, steer-left, steer-right, hit, victory, kart GLBs, manifest activation, CI, deployment, and live verification remain pending.
- Status: **IN PROGRESS — PORTRAIT AND FRONT FRAME APPROVED.**

## Slice 3 Cleo intake and driver-art checkpoint

- Manny confirmed the supplied racing sheet as Cleo's definitive game likeness and The Gilded Stitch as the definitive kart design on 2026-08-21. He confirmed that he created or controls the reference and authorized its transformation into game assets.
- Cleo uses she/her pronouns and is locked to AA-06 Grip Specialist: 6 / 6 / 5 / 7 / 5 / 7. `aa-06` is uniquely allocated in `docs/ROSTER-MAPPING.md`.
- The approved character record and production brief are `docs/avatars/CLEO.md` and `docs/assets/CLEO-ASSET-BRIEF.md`.
- Manny approved the portrait, front driver frame, neutral chase frame, steer-left, steer-right, hit, and chase-camera victory art.
- Runtime derivatives are stored at `public/assets/characters/aa-06/`. The portrait is 256 x 256; all six driver frames are 512 x 512. Every file is an sRGB RGBA PNG with alpha spanning transparent to opaque and a transparent corner pixel.
- Driver frames contain no kart or steering-wheel geometry. Chase-camera states preserve a seated lower body; the victory frame turns Cleo toward the viewer without becoming a front-facing driving frame.
- Manny approved The Gilded Stitch LOD0 Candidate 3 after direct interactive GLB review. The approved design moves Cleo's cockpit rearward, uses one connected steering wheel, exposes the front needle and presser-foot assembly, clears all four wooden spool wheels from the chassis, and replaces floating decorative dots with continuous gold inlays attached to the navy side panels.
- The deterministic builder is `tools/assets/build_cleo_gilded_stitch.py`. LOD0/1/2 contain 12,812 / 10,396 / 4,780 triangles, four opaque materials, the required thirteen-node hierarchy, and negative-Z forward metadata.
- GLB object IDs: LOD0 `453ebc42da5745f7f5251323cd7a38a79add6538ee39dc9e512570c1c9905150`; LOD1 `a9013591726b3bbb43b102d3707fe9da24f2e1e8de24c929bbc6405e28357002`; LOD2 `3578b62d3c9fa332adb2b1ae7addb1d2b56201c7c8491a1075e847ff18caa79e`.
- The branch-scoped Actions bridge rebuilt all three approved hashes, preserved their committed pointers, uploaded only those object IDs, and completed fetch-back verification. A clean `git lfs fetch origin agent/cleo-gilded-stitch` followed by `git lfs fsck` passed before the temporary workflow was removed.
- AA-06 is prepared as a production manifest entry with Cleo's approved portrait and six driver states, The Gilded Stitch, Grip Specialist statistics, front-camera frame, and controlled revision `cleo-runtime-20260821-1`.
- Repository CI, deployment, and product-owner live visual checks remain approval-gated.
- Manny's first live check passed Cleo's selection data, kart loading, race-forward needle apparatus, all driver states, and unique AI appearance. It failed cockpit integration: the generic sprite position placed Cleo ahead of the rear-biased cockpit, making the steering wheel appear behind her.
- Correction: AA-06 now declares kart-group driver position `[0, 0.9, -0.72]`. Runtime kart-forward is positive Z, so this negative-Z offset moves Cleo rearward. Player and AI sprite creation both consume the character-specific mount, placing her in the cockpit while keeping the steering wheel ahead. No kart geometry, orientation, physics, camera, or approved art changed.
- Manny confirmed the corrected live build on 2026-08-21. Cleo now sits inside The Gilded Stitch's rear cockpit with the steering wheel ahead of her. Together with the first live check, selection data, production kart loading, race-forward orientation, front/rear/steering/hit/victory states, and unique AI appearance all pass.
- Status: **LIVE ACCEPTED — CLEO PRODUCTION INTEGRATION COMPLETE.**

## Slice 3 Kraken intake and locks

- Manny confirmed the supplied racing sheet as Kraken's definitive game likeness and The Abyssal Drifter as the definitive kart design on 2026-08-21.
- Kraken is locked to AA-05 Drift Specialist: 6 / 7 / 5 / 6 / 9 / 3. `aa-05` is uniquely allocated in `docs/ROSTER-MAPPING.md`.
- The approved character record and production brief are `docs/avatars/KRAKEN.md` and `docs/assets/KRAKEN-ASSET-BRIEF.md`.
- Manny approved the portrait, front driver frame, neutral chase frame, steer-left, steer-right, hit, chase-camera victory, and front-view victory art.
- Runtime derivatives are stored at `public/assets/characters/aa-05/`. The portrait is 256 x 256; all seven driver frames are 512 x 512. Every file is an sRGB RGBA PNG with genuine transparency.
- Driver frames contain no kart or steering-wheel geometry. Chase-camera states preserve a forward-facing seated lower body; the victory frame turns Kraken's torso toward the viewer without rotating his hips into a full about-face.
- Manny approved The Abyssal Drifter LOD0 Candidate 3 after direct interactive GLB review. The final steering assembly clears the shell and places its connected column on the nose-facing side of the wheel.
- The deterministic builder is `tools/assets/build_kraken_abyssal_drifter.py`. LOD0/1/2 contain 18,724 / 9,588 / 4,376 triangles, four opaque materials, the required thirteen-node hierarchy, and negative-Z forward metadata.
- GLB object IDs: LOD0 `4a28349e51b0f6936a67bc8160d1b627fb9f77144ab063368e863d644e64a5c9`; LOD1 `c000af29a53fa79810d759b460f7a6a3b72c2f1605b9ff300245c080a95a8bfe`; LOD2 `ca73a74e96ff58769abc83db3b8662b498445144f28497b58213d71022e13546`.
- The branch-scoped Actions bridge rebuilt the three approved hashes, preserved their committed pointers, uploaded only those object IDs, and fetched them back. Follow-up CI run `32514042610` checked out LFS, passed `git lfs fsck`, verified all twelve runtime GLBs, ran 50 tests, and completed the production build. The temporary workflow was then removed before merge.
- AA-05 is staged as a production manifest entry with Kraken's approved art, The Abyssal Drifter, Drift Specialist statistics, front-camera frame, and controlled revision `kraken-runtime-20260821-1`.
- Manny completed the live product-owner acceptance check on 2026-08-21. Kraken was selectable with the correct portrait and stats; The Abyssal Drifter loaded instead of the fallback; its maw and orange eyes faced race-forward; rear, front, steering, hit, and victory frames rendered correctly; and Kraken appeared no more than once as an AI opponent when not selected.
- Status: **LIVE ACCEPTED — KRAKEN PRODUCTION INTEGRATION COMPLETE.**

## Mobile finish-state correction

- Manny's mobile completion screenshot showed the desktop-centered standings card covering the play field and Accu's victory pose while obsolete HUD and touch-driving controls remained visible.
- The finished game shell now retires driving HUD and controls, docks a compact results card to the top of portrait viewports, constrains standings to an internal scroll region, and preserves the lower chase-camera area for the victory frame.
- Automated validation covers the required `is-finished` state. Deployment and product-owner mobile confirmation remain pending.

## August 20 roster-grid and finish-presentation amendment

- PRD amendment 1.6 adds a separately approved 512 x 512 `front.png` to every production character package for camera views facing the front of the kart. Existing approved art remains unchanged; front candidates for Lavi, Manaconda, and Accu are pending.
- The AI grid now samples seven unique manifest identities after excluding the player. Production selections load their approved kart and rear driver frame; unfinished selections retain the governed fallback.
- The finish panel is docked to the right, reduced in size, and partially translucent so the live kart and victory pose remain visible. All eight standings remain scrollable.
- Local validation passed on 2026-08-20: strict TypeScript, ESLint with zero warnings, 48 Vitest tests across 14 files, nine materialized runtime GLBs, and the Vite production build. Desktop/mobile live confirmation remains required before this amendment can pass.

The approved Lavi package is now connected to a twelve-slot Character Select scaffold. Lavi is the default production entry; all other slots deliberately retain monogram portraits, fallback karts, and unassigned community identities until their one-at-a-time approval gates are complete.

## Slice 3 Accu intake and locks

- Manny supplied Accu's canonical game references and confirmed he created them and permits their transformation into game assets.
- Accu's character lock, Pink Precision kart direction, original heart-bullseye emblem, and AA-11 Collision Tank mapping are approved.
- `aa-11` is uniquely allocated to Accu in `docs/ROSTER-MAPPING.md`. Her intake and production brief are `docs/avatars/ACCU.md` and `docs/assets/ACCU-ASSET-BRIEF.md`.
- Manny approved the portrait and all five driver-state PNGs on 2026-08-20. Runtime derivatives are stored at `public/assets/characters/aa-11/`.
- Portrait is 256 x 256; rear, steer-left, steer-right, hit, and victory are 512 x 512. All six are sRGB RGBA PNGs with genuine transparency and transparent corner pixels.
- Manny approved Pink Precision Candidate 1 on 2026-08-20. The deterministic production package preserves that model as LOD0 and derives LOD1 and LOD2 with 4,156 / 2,700 / 1,804 triangles, four opaque materials, the required 13-node hierarchy, and negative-Z forward metadata.
- Approved GLB object IDs: LOD0 `6e3f8cb6d1bdee7f5b315a7c154bd45fd0f4d6ac9b2e6445b9d85d81959ff958`; LOD1 `9f481cf854d47ec330e5909d5003353376c471cd37562d79410c20e3f824f9c7`; LOD2 `792b8f8bf1d359b3ae464003f0fa9432de5c391d8bd18ac8f84535593d9ba820`.
- GitHub Actions run `32429947766` rebuilt all three approved GLBs, matched their object IDs, proved pointer stability, uploaded only those objects, deleted the runner's local LFS cache, fetched the branch objects back, and passed `git lfs fsck`.
- Manifest/runtime integration, deployment, and live verification remain pending.
- The runtime integration maps AA-11 to Accu, Pink Precision, the 8 / 4 / 10 / 3 / 5 / 6 profile, and all five approved driver frames under controlled revision `accu-runtime-20260820-1`.
- Manny's first live mobile chase-camera test found Pink Precision reversed: the cannon and heart-bullseye nose faced the chase camera. The earlier zero-yaw interpretation was incorrect.
- Pink Precision now uses the shared `NEGATIVE_Z_KART_VISUAL_YAW` (`Math.PI`) correction. All production kart GLBs must declare `extras.forward: "-Z"`; the manifest validator rejects any production kart that does not use the shared correction, and the runtime-asset gate rejects missing or conflicting forward metadata.
- Local validation on 2026-08-20 passed typecheck, ESLint with zero warnings, 44 Vitest tests across 13 files, the nine-GLB runtime signature gate, and the Vite production build. The existing large gameplay-chunk advisory remains non-blocking.
- Deployment and product-owner desktop/mobile verification remain pending.
- Status: **RUNTIME INTEGRATION PREPARED — automated validation and deployment next.**

## Slice 3 Manaconda intake and locks

- Manny supplied Manaconda's written character description and reference on 2026-08-16. The intake is recorded at docs/avatars/MANACONDA.md.
- Manaconda's character lock, original The Wayfinder kart, AA-09 Technical Cruiser profile, and source-transformation permission are approved. The green kart in the supplied image is an example, not the final direction.
- aa-09 is uniquely allocated to Manaconda in docs/ROSTER-MAPPING.md. The production brief is docs/assets/MANACONDA-ASSET-BRIEF.md.
- Manny approved the production portrait and all five driver-state PNGs on 2026-08-20. The prepared runtime derivatives are stored at `public/assets/characters/aa-09/`.
- Portrait is 256 x 256; rear, steer-left, steer-right, hit, and victory are 512 x 512. All six are sRGB RGBA PNGs with genuine transparency and transparent corner pixels.
- Manny approved the wheel-free Wayfinder LOD0, LOD1, and LOD2 package on 2026-08-20. Its empty `SteeringWheel` node preserves the required hierarchy without duplicating the visible wheel already included in every approved driver frame.
- The deterministic builder is `tools/assets/build_manaconda_wayfinder.py`. The approved models use four materials, negative-Z forward metadata, the exact thirteen-node hierarchy, and remain below all LOD triangle limits.
- Wayfinder SHA-256/LFS object IDs: LOD0 `5498567abf25339b2a9f876f2bb81079d263c80afeea4a7c1b0181a36fdfd446`; LOD1 `9465ca4cb7d75c9a80c30ac09414c94bf35c95e82a26784735376df736191390`; LOD2 `4a2e2a43c147bd7fca0ae07edd7fbf612ac067e47f185b87431290de36e45fe0`.
- LFS materialization checkpoint: GitHub Actions run `32428889465` rebuilt all three approved GLBs, matched their object IDs, proved pointer stability, uploaded 3/3 objects, deleted its local LFS cache, fetched the branch objects, and passed `git lfs fsck`. Follow-up CI run `32428954493` materialized LFS and passed the full repository validation.
- AA-09 is now staged as a production manifest entry named Manaconda with the approved portrait, Wayfinder, five driver states, Technical Cruiser statistics, and controlled `manaconda-runtime-20260820-1` revision.
- Runtime visual yaw is character-specific. Lavi retains Potato's documented 180-degree visual-only correction. Wayfinder also requires 180 degrees: its metadata suggested native negative-Z forward, but Manny's deployed chase-camera test proved the grille/navigation core faced backward at zero yaw.
- Character Select labels AA-09 as Manaconda and The Wayfinder. The runtime asset signature gate now requires all three AA-09 GLBs.
- Merge commit `63f2af05ba4a8631594786f2d4ea171b5278778a` deployed through successful Actions run `32429960640`. Manny's mobile test passed selection, portrait, production kart loading, duplicate-wheel removal, and left/right driver frames; orientation failed because the navigation grille faced the chase camera.
- The orientation hotfix rotates only Wayfinder's visual root by 180 degrees. Physics, controls, checkpoints, camera coordinates, and driver sprites remain unchanged.
- Orientation hotfix merge `b88eb635bf928e52a5e34ad218b938fcd7610cfc` deployed through successful Actions run `32430647474`. Manny confirmed the corrected live mobile view: the navigation grille faces race-forward and the satchel/exhausts remain behind Manaconda.
- Live mobile acceptance is complete for selection, portrait, production kart loading, duplicate-wheel removal, left/right driver states, and orientation. Separate desktop evidence remains unrecorded.
- Status: **MOBILE PRODUCTION PASS — accepted; desktop confirmation pending when tested.**

## Slice 3 Lavi production checkpoint

- Character Select now sits between the Hub and Grand Prix and renders exactly twelve roster slots on desktop and mobile layouts.
- `src/characters/manifest.ts` owns the typed manifest, twelve distinct 36-point profiles, validation, stable IDs, asset state, portrait/kart URLs, and safe unknown-ID fallback.
- Lavi is stable ID `aa-02`, maps to the approved Feather Technician profile, displays the approved portrait, and passes their selected statistics into `KartController` tuning.
- Lavi loads the approved `kart.glb` Potato model at race startup, normalizes it to the current race scale, enables mesh shadows, and mounts the approved state-selected driver sprite. Drift feedback remains attached to the runtime kart group.
- The eleven not-yet-approved roster identities use visible `AA` monograms and the existing procedural fallback kart. No placeholder assigns or implies a community identity.
- Missing portraits replace themselves with the correct monogram. A missing production kart is caught and replaced by the fallback kart without changing the selected physics profile or crashing race startup.
- Strict TypeScript and ESLint passed on 2026-08-16. Vitest passed 13 files and 42 tests with 76.72% statements, 72.16% branches, 82.55% functions, and 79.00% lines.
- Vite `8.2.1` production build passed. The title/menu package is 14.91 kB gzip and the lazy Three.js/Rapier gameplay package is 1.256 MB gzip, inside the PRD download budget. The built public asset tree contains the materialized 358,036-byte Potato GLB rather than an LFS pointer.
- Pages materializes LFS during checkout, runs `git lfs fsck`, and invokes `tools/verify-runtime-assets.mjs`; the three Potato GLBs must begin with the binary `glTF` signature or the production build fails. Lavi runtime URLs include the controlled `lavi-runtime-20260816-3` revision query to defeat stale pointer responses at stable public paths.
- The runtime preloads rear, steer-left, steer-right, hit, and victory. Steering selects the matching frame; collision and finish states override it; rear remains visible if an optional frame fails to load.
- Potato's model root rotates 180 degrees around local Y only, aligning its visual positive-Z authoring with the race runtime’s negative-Z forward. Physics, camera, checkpoints, mounts, and input stay unchanged.
- GitHub Pages run `31986673349` successfully deployed final orientation correction commit `660e42d85a618e8f27eaea3a91a0c4f1fcc9c699` on 2026-08-16.
- Manny manually confirmed the final live mobile checkpoint: Potato loaded, Lavi's steering frames worked, and the steering wheel faced forward of Lavi. His acceptance was recorded as “Perfect.”
- Status: **PASS — Lavi production checkpoint accepted.** Slice 3 remains active because eleven identities and their one-at-a-time approval packages are still incomplete; this acceptance does not authorize the next PRD slice.

### Failed deployment evidence and corrective action

- Manny's 2026-08-16 mobile test showed the purple procedural player kart with no Lavi sprite. This failed the required Lavi/Potato runtime acceptance check.
- Root cause: `.github/workflows/ci.yml` checked out production with `lfs: false`. The Pages build therefore copied the text pointer for `kart.glb` instead of the approved 358,036-byte GLB. `GLTFLoader` rejected the pointer and activated the fallback kart. Lavi's sprite was mounted only after a successful GLB load, so the same failure also removed the driver.
- Correction: production checkout now materializes LFS and runs `git lfs fsck`. The build runs `tools/verify-runtime-assets.mjs` and fails unless all three Potato runtime files begin with the binary glTF signature. Lavi's driver sprite is also mounted when a kart falls back, keeping independent asset failures independent.
- Status remains **FAILED / CORRECTION IN PROGRESS** until a fresh Pages deployment proves Potato and Lavi render on Manny's device.

### Second manual-failure report and corrective action

- Manny's follow-up mobile test on 2026-08-16 still showed the fallback kart. Lavi's clean rear driver frame rendered, but steering never changed the artwork. Victory was not tested.
- The sprite finding is confirmed: the initial runtime integration created only `rear.png`; no code selected `steer-left.png` or `steer-right.png` during gameplay.
- Potato correction: every Lavi runtime URL now includes a controlled asset revision query, preventing a browser or Pages edge cache from reusing an earlier GLB pointer response at the stable public filename. The existing LFS checkout, `git lfs fsck`, and binary-signature build gate remain required.
- Sprite correction: runtime preloads the five approved Lavi frames and selects rear, left, right, collision-hit, or victory texture without allowing an unloaded optional frame to blank the driver.
- Status remains **FAILED / CORRECTION IN PROGRESS** until Manny confirms Potato and steering states on the newly deployed cache-busted checkpoint.

### Third manual-failure report and corrective action

- Manny's next mobile test confirmed Potato now loads and Lavi's state sprites work. The kart visual is reversed: its steering wheel appears behind Lavi from the driving camera.
- Root cause: Potato's approved GLB is visually authored with forward along positive Z, while the game runtime applies its forward direction along negative Z.
- Correction: rotate Potato's visual root 180° around local Y during load. Kart physics, checkpoints, input, camera, mount hierarchy, and Lavi's billboard sprite remain unchanged.
- Final result: resolved by commit `660e42d85a618e8f27eaea3a91a0c4f1fcc9c699`; Manny's live mobile confirmation accepted the corrected visual orientation.

Manny manually confirmed Slice 1 lap counting, boost pads, grass slowdown, recovery, reverse-lap rejection, rear camera, and other checks on 2026-08-16. He approved the Slice 1 corrections and authorized Slice 2.

## Slice 1 gap-close completed

- Corrected forward chase-camera controls so A/Left steers visually left and D/Right steers visually right.
- Replaced the black upper viewport with a rendered dusk gradient sky and coordinated horizon fog.
- Added sustained playable speed floors of 8.5 m/s on grass and 11.5 m/s on dirt while throttle is held; both remain slower than asphalt.
- Converted dirt from a full-width forced section to an optional partial-width inside lane using signed lateral track projection.
- Shortened Circuit Alpha from approximately 1.45 km to approximately 0.90 km while preserving three laps and twelve ordered checkpoints.
- Recorded the approved changes in PRD amendment 1.3 and ADR-008.

## Slice 2 completed requirements

- DRIFT-001: Space plus steering at valid speed initiates a short Rapier hop and locks drift direction.
- DRIFT-002: drift charge exposes Blue, Orange, and Purple tiers with HUD meter, rear-wheel glow, and escalating Web Audio tones.
- DRIFT-003: releasing Space applies the highest achieved tier rather than a lower tier.
- DRIFT-004: Mini-Turbo modifies charge thresholds and boost durations; tier speed-cap multipliers are 1.08, 1.12, and 1.16.
- Drift reduces lateral grip, increases yaw response, retains player steering, and cancels on release, low speed, or extended airborne state.
- Boost pads continue to apply visible Blue boost feedback.
- The ramp surface now launches the kart; a successful landing grants an automatic short stunt boost.
- Dirt and grass remain Traction-driven and measurably distinct while preserving the approved playable floors.
- The drift HUD reports charge, tier, active boost, and airborne state without requiring the player to read during normal driving.

## Work in progress

- Avatar intake and approval contract established for one-at-a-time character development.
- Lavi is the first avatar in intake. Their supplied personality, physical description, and Potato Kart reference are recorded in `docs/avatars/LAVI.md`.
- Lavi's they/them pronouns, racing outfit, situational cheek grime, natural-potato kart body, and hidden-frame construction language are approved. The reference number `1` and `Potato Prix '24` treatment are excluded from canon.
- Lavi's reference-matched light complexion, standard stud earrings, and realistic-yet-whimsical `Potato` art direction are approved.
- Lavi's earrings are teal-blue studs. Their kart's final name is `Potato`, with approved russet skin, shallow eyes, dry soil, light scuffing, and two or three short rear sprouts. Rot, trailing roots, and an anthropomorphic face are prohibited.
- Lavi's muted-green ribbed sweater, white rainbow-accented platform boots, and Potato's practical handmade hardware are approved. Consolidated character and kart lock candidates are ready for final review.
- Manny approved Lavi's complete character and `Potato` kart locks on 2026-08-16, including simplification rules, no emblem, and limited technical adjustments that preserve the natural-potato silhouette.
- Manny assigned AA-02 Feather Technician to Lavi on 2026-08-16: Speed 5, Acceleration 8, Weight 2, Handling 9, Mini-Turbo 8, and Traction 4.
- `docs/ROSTER-MAPPING.md` now reserves AA-02 for Lavi and records all eleven remaining profiles as available. ADR-011 requires one-to-one allocation and duplicate-assignment validation.
- Manny confirmed he created the supplied Lavi reference and permits its transformation into game assets. Production art must follow the PRD's polished, colorful, kinetic, high-contrast arcade style rather than the reference collage's pixel treatment.
- `docs/assets/LAVI-ASSET-BRIEF.md` governs the approved portrait and later production deliverables.
- Manny approved Lavi portrait Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/portrait.png` is the prepared 256 x 256 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- Manny approved Rear Driver Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/rear.png` is the prepared 512 x 512 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- Manny approved Steer-left Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/steer-left.png` is the prepared 512 x 512 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- Manny approved Steer-right Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/steer-right.png` is the prepared 512 x 512 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- PR #1 merged the approved Lavi documentation, portrait, rear frame, steer-left frame, and steer-right frame into `main` at commit `0716d8fc63c192712c96874a60adb2ed12e427c5`.
- Manny approved Hit Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/hit.png` is the prepared 512 x 512 PNG RGBA derivative. Its alpha ranges from fully transparent to fully opaque, the corner pixel is transparent, and normal-Git runtime treatment is verified.
- Hit publication checkpoint: PR #2 passed GitHub CI run `31979696233` for remote commit `f670fa3ec65fea7fdb93f0b5a6fdc6bb0dbfb69a`.
- PR #2 merged the approved hit frame and its evidence into `main` at commit `14a45ca0e4eca11b91715c99c33d8dd60035a3d2` after final CI run `31979774258` passed.
- Manny approved the corrected Victory Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/victory.png` is the prepared 512 x 512 PNG RGBA derivative. Its alpha ranges from fully transparent to fully opaque, the corner pixel is transparent, and normal-Git runtime treatment is verified.
- Lavi's portrait and all five PRD-required driver frames are now approved and prepared.
- Manny approved Potato LOD0 Candidate 4 on 2026-08-16 after direct external-viewer review. The final kart uses a continuous opaque potato body with a sculpted cockpit, embedded eyes and scuffs, three rooted rear sprouts, and four visible axles connecting the wheel hubs.
- Potato's production package is prepared at the PRD character path: `kart.glb` is LOD0 with 9,552 triangles, `kart-lod1.glb` has 5,528, and `kart-lod2.glb` has 3,086. All three use four materials and the required thirteen-node kart hierarchy.
- The three Potato GLBs are governed by Git LFS. `tools/assets/build_lavi_potato.py` preserves the procedural source used to reproduce and validate each level.
- LFS materialization checkpoint: GitHub Actions run `31983718813` rebuilt all three GLBs, matched the approved object IDs, uploaded 3/3 LFS objects, deleted its local object cache, fetched the objects from GitHub, and passed `git lfs fsck`.
- ADR-013 and `docs/LFS-PUBLISHING.md` make this temporary GitHub Actions bridge the default fallback for reproducible LFS assets when a hosted Work shell cannot push directly. Assets without deterministic committed source still require an authenticated external Git/LFS handoff.
- The roster ledger was reviewed for this checkpoint. AA-02 remains uniquely assigned to Lavi / Potato, and the eleven other profiles remain available for later characters.
- Victory publication checkpoint: PR #3 passed GitHub CI run `31980324500` for remote commit `d793263de4cf12a396673974cf6eb0e6af97c514`.
- No Slice 3 character implementation has begun beyond governance and intake preparation.

## Known defects

- Slice 4 AI is intentionally not strongly competitive yet; Manny won easily and accepted that limitation for now.
- The previously reported drift/Blue-pad freeze is resolved. Commit `10864b6eeee84056d01885b74b1b3fe6e97fd7f5` contains and regression-tests the exception-safe Web Audio repair.

## Deferred work

- Remaining Slice 3 work: twelve-slot manifest/schema, validator, selection UI, kart preview, sprite/fallback pipeline, approved roster mapping, and race handoff.
- Items, AI item use, and advanced collision responses: Slice 5. AI-004 is dependency-blocked until then.
- Final HUD, production audio content, post-processing, production track art/elevation, and optimization: Slice 6.

## Next recommended action

Begin Slice 3 manifest/schema and selection-flow implementation using Lavi's complete approved asset package, AA-02 mapping, rotating Potato preview, driver-sprite mounts, and race handoff.

## Validation evidence

- Accu runtime PNG validation on 2026-08-20: portrait is 256 x 256; all five driver states are 512 x 512; every file is sRGB RGBA with alpha spanning transparent to opaque and a fully transparent corner pixel. Manny approved the final six-file package.
- Manaconda runtime PNG validation on 2026-08-20: portrait is 256 x 256; all five driver states are 512 x 512; every file is sRGB RGBA with alpha spanning transparent to opaque and a fully transparent corner pixel. Dark-blue and parchment-gold composites were visually reviewed after checkerboard extraction; Manny approved the final six-file set.

### Local validation on 2026-08-16

- Lavi runtime assets: portrait is 256 x 256; rear, steer-left, steer-right, hit, and victory are 512 x 512. All six are sRGB RGBA PNGs with non-opaque alpha and transparent corner pixels at the PRD paths.
- Hit transparency: source and runtime alpha both range from 0 to 1. The runtime corner pixel is `srgba(0,0,0,0)`, and a checkerboard composite shows the background through the cutout.
- Asset policy: Git attributes resolve the six fixed-size runtime PNGs to normal Git while high-resolution character art, 3D formats, and production audio remain covered by LFS rules.
- Roster ledger: twelve unique profiles are present, every profile totals 36 points, AA-02 is assigned to Lavi, and eleven profiles remain available.
- Lavi publication checkpoint: GitHub CI run `31977857986` passed for remote commit `15c39bd59e6952d41dc603460f4f100fc5ed01cc`; PR #1 merged it into `main` at `0716d8fc63c192712c96874a60adb2ed12e427c5`.
- Lavi hit checkpoint: GitHub CI run `31979696233` passed for remote commit `f670fa3ec65fea7fdb93f0b5a6fdc6bb0dbfb69a` in PR #2.
- Lavi victory checkpoint: GitHub CI run `31980324500` passed for remote commit `d793263de4cf12a396673974cf6eb0e6af97c514` in PR #3.
- Potato GLB validation: LOD0, LOD1, and LOD2 are valid glTF 2.0 binary containers with declared byte lengths matching file size, four opaque materials, meters, negative-Z forward metadata, and the exact thirteen-node PRD hierarchy.
- Potato geometry budgets: LOD0 is 9,552 / 25,000 triangles; LOD1 is 5,528 / 12,000; LOD2 is 3,086 / 5,000.
- Potato construction validation: the LOD0 potato surface retains its complete 5,184-triangle body topology; the cockpit is sculpted into that surface without deleted upper-body faces. Four axle meshes overlap the potato body and wheel hubs.
- Potato asset policy: `git check-attr` resolves all three GLBs to the LFS filter. Runtime avatar PNG exceptions remain in normal Git.
- Potato LFS publication: GitHub Actions run `31983718813` passed every build, SHA-256, pointer-preservation, upload, fetch-back, and `git lfs fsck` step for object IDs `5d3d570e21759d0f77f2bc7cf88085e43b1b8c1be75a3ef0299f8fac83ef0ad2`, `f74cc0e67de68d5b1f06a21dd3b9436521dfa0e7027f94ee9315ab6f107335ce`, and `e1df4c501328d2709fb6793269e6a48a930bf7a7ce75eb0b6152765c46d0e758`.
- Typecheck: strict TypeScript project build passed with no diagnostics.
- Lint: ESLint passed with zero warnings permitted.
- Tests: 6 files and 14 tests passed under Vitest `4.1.10`.
- Rapier integration tests achieve Purple charge, release the highest tier, retain finite transforms, and sustain grass speed above the approved floor.
- Configuration tests prove tier ordering, lower thresholds and longer boosts for higher Mini-Turbo, distinct speed multipliers, and dirt/grass floor ordering.
- Track tests prove an approximately 0.90 km loop, twelve checkpoints, asphalt centerline through the dirt segment, optional offset dirt lane, grass, boost, and ramp surfaces.
- Existing tests continue to prove fixed-step clamping, ten-minute finite numeric soak, skipped-checkpoint rejection, reverse finish rejection, and three consecutive valid laps.
- Clean install: `npm ci --prefer-offline --no-audit --no-fund` passed with 198 packages restored from the committed lockfile.
- Coverage: 69.84% statements, 64.60% branches, 66.66% functions, and 72.01% lines across instrumented test targets.
- Production build: Vite `8.2.1` passed; title/menu JavaScript is 12.70 kB gzip and the lazily loaded Three.js/Rapier gameplay package is 1.20 MB gzip, inside PRD download budgets.
- Formatting: Prettier check passed for all governed files.
- Blocking-freeze repair validation: 7 files and 17 tests passed, including missing-context, thrown-Web-Audio, and rejected-resume regression cases. Typecheck, lint, production build, and formatting also passed locally.
- Repair CI: GitHub Actions run `31969384244` passed for commit `10864b6eeee84056d01885b74b1b3fe6e97fd7f5` and published GitHub Pages deployment `5934890606`.
- Product-owner manual acceptance: Manny confirmed on 2026-08-16 that the repaired deployment passed all previously blocked checks, including the first Blue boost pad, all three drift tiers, highest-tier release boost, Mini-Turbo effects, HUD/wheel/tone feedback, and ramp landing stunt boost.
- Evidence checkpoint CI: GitHub Actions run `31969502068` passed for commit `4ff50635d7a4e471f7718b2a910d905d34f5d7f2` and published successful GitHub Pages deployment `5934911724`.
- CI: GitHub Actions run `31968043110` passed for Slice 2 candidate `350248375ce34659b5580878aa34f256045a907b`, including clean install, typecheck, lint, 14 tests, production build, artifact upload, and Pages deployment.
- Deployment: GitHub Pages deployment `5934663031` published candidate `350248375ce34659b5580878aa34f256045a907b` through the `github-pages` environment.
- Live URL: `https://manaconda33.github.io/accurate-artistry-game-hub/` returned HTTPS 200. The HTML and current title/menu JavaScript, CSS, and lazy gameplay JavaScript assets each returned HTTP 200.
- Early Slice 4 local candidate: strict typecheck, ESLint with zero warnings, formatting, and production build passed on 2026-08-16.
- Early Slice 4 tests: 12 files and 25 tests passed with 71.49% statement, 66.38% branch, 74.64% function, and 73.82% line coverage.
- AI route qualification: all seven configured AI profiles independently completed three checkpoint-validated Circuit Alpha laps under Rapier fixed-step simulation without player input and retained finite physics state.
- Early Slice 4 unit evidence covers dynamic spline lookahead, bounded steering, off-line correction, five-percent rubber-band bounds, race countdown, validated-progress ranking, locked finish places, relative-mass collision shares, and mobile coarse-pointer session gating.
- Early Slice 4 production build: Vite `8.2.1` passed; app-shell JavaScript is 13.54 kB gzip and the lazy Three.js/Rapier gameplay package is 1.234 MB gzip, within the PRD download budget.
- Early Slice 4 candidate CI: GitHub Actions run `31970630840` passed for commit `6580cb02618d2809181cd33f99b7357be84b2f34`, including clean lockfile install, typecheck, lint, 25 tests, coverage, and production build.
- Early Slice 4 deployment: GitHub Pages deployment `5935135220` successfully published the candidate through the `github-pages` environment at `https://manaconda33.github.io/accurate-artistry-game-hub/`.
- Product-owner manual acceptance: desktop and mobile checks passed on 2026-08-16. Manny confirmed the AI racers/grid were functional; six AI profiles were observed running the track, and the player won easily. Low AI competitiveness is accepted for now.
- Governance correction: the AI/grid checkpoint is classified as Slice 4 completed early. Slice 3 returns to Character Selection & Avatar Ingestion per PRD section 35.4.

## Last verified commit

`f608b91d63afb406e2fb404829298f3ff4f568db` - validated and deployed early Slice 4 AI/grid evidence checkpoint. The following governance checkpoint restores Slice 3 ordering and adds the avatar intake contract.
