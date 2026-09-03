# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art/camera polish pass under the existing track/rendering requirements. That pass is now **LIVE ACCEPTED / CLOSED** and does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Final runtime release: PR **#83 — Finish at gantry and tighten race camera framing**
- PR #83 merge: `da9275771941e7e112a6153af3d5d1cd97ea2bf2`
- Main CI / Pages run: **33809002419** — validation passed and deployment passed
- GitHub Pages artifact: **9914060220**
- Pages artifact digest: `sha256:4005c0b896469a02883bd3a83c22cf6c187bfadf5d1310c185d11df440d1f0e3`
- Deployment-record checkpoint before final acceptance: `4d96262919f71ce01bc3b586e037c2046ea45b3e`
- Deployment-record run: **33809192455** — validation passed and deployment passed
- Product-owner final live acceptance: **2026-09-03 — APPROVED**

## Circuit Alpha environment-art / camera pass — final accepted state

The bounded pass materially improved Circuit Alpha presentation while preserving the governed race topology and physics contract.

Accepted visual/environment changes include:

- deeper dusk sky and atmospheric presentation;
- layered asphalt wear and shoulders;
- alternating curbs and reflectors;
- instanced forest, rocks, and distant mountains;
- rebuilt center mesa and additional trackside landmarks;
- start/finish gantry and underpass architecture;
- upgraded boost-pad and checkpoint presentation;
- Crest Ramp rebuilt as a forward-rising wedge aligned to the course;
- pre-race crane-down camera during the 3 / 2 / 1 countdown;
- lower chase and rear-view camera heights;
- tighter final chase/rear framing to emphasize the driver and kart;
- visual start/finish staging in front of the starting grid;
- lap-completion crossing aligned to the visible gantry.

## Final product-owner acceptance matrix

Manny's deployed live review recorded all required presentation gates as passing:

- start/finish gantry is ahead of the grid during countdown/start — **PASS**
- racers launch toward and pass under the gantry — **PASS**
- Crest Ramp presents the short low edge first and rises toward the far/down-track edge — **PASS**
- pre-race crane-down during 3 / 2 / 1 — **PASS**
- lower chase-camera height/angle — **PASS**
- lower rear-view height/angle — **PASS**
- chase framing at the tighter distance — **PASS**
- rear-view framing at the tighter distance — **PASS**
- lap 3 / race finish occurs at the gantry rather than before it — **PASS**
- mobile frame pacing remains acceptable — **PASS**

The Circuit Alpha environment-art/camera polish pass is therefore **LIVE ACCEPTED / CLOSED**.

## Final camera / finish values

- chase distance: **5.6 m**
- chase height: **3.15 m**
- rear-view distance: **5.3 m**
- rear-view height: **3.05 m**
- look target height: **1.15 m**
- PerspectiveCamera FOV: **62°**
- crane duration: **2.85 s**
- start/finish distance from the original checkpoint-0/grid origin: **22 m**
- player spawn remains **8 m** beyond the original checkpoint-0 origin

`checkpointPosition(0)` remains the starting-grid origin. `lapCheckpointPosition(0)` is the 22 m visible gantry crossing used for lap completion. Checkpoints 1–11 retain their prior positions.

## Protected gameplay contract

The accepted Circuit Alpha pass did not change:

- the 384 canonical Catmull-Rom track samples or course topology;
- loop length or road width;
- checkpoints 1–11 or checkpoint order;
- player/AI starting grid positions;
- asphalt, dirt, grass, boost, and ramp gameplay classification;
- ramp trigger or ramp boost behavior;
- kart physics, driver tuning, collision behavior, or AI navigation;
- three-lap requirement;
- countdown timing;
- roster statistics or character assets;
- item scope.

The intentional gameplay-facing correction was limited to making checkpoint 0 for lap completion coincide with the visible start/finish gantry.

No PRD deviation is recorded.

## Validation evidence

Final PR #83 head `3614de78a62cd483ae32dba6923194d8bcfbb1b6` passed PR CI run **33808711461** with:

- Git LFS runtime-asset verification;
- strict TypeScript typecheck;
- ESLint with zero warnings;
- full Vitest CI suite;
- production Vite build.

Merged runtime commit `da9275771941e7e112a6153af3d5d1cd97ea2bf2` passed main run **33809002419** with the same validation plus successful GitHub Pages artifact upload and deployment.

Deployment-record checkpoint `4d96262919f71ce01bc3b586e037c2046ea45b3e` passed main run **33809192455** and deployed successfully.

Regression coverage verifies that:

- environment construction does not mutate canonical track samples;
- the gantry is staged ahead of the starting grid;
- the visible gantry matches the lap finish crossing;
- the Crest Ramp is a forward-rising wedge aligned to course-forward;
- player and AI checkpoint detection use the same lap checkpoint positions;
- seven-profile AI simulation still completes three valid laps;
- closer chase/rear distances preserve accepted heights;
- required environment landmarks and repeated-scenery instancing remain intact.

The existing production-build large-chunk warning remains known and non-blocking.

## Active production roster state

- Lavi / Potato — AA-02
- Lula / The Verdant Hart — AA-03
- Keeg / The Mycelial Majesty — AA-04
- Kraken / The Abyssal Drifter — AA-05
- McFleurdel / The Fleur de Nuit — AA-07
- Toph / The Grave Shift — AA-08
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- Accu / Pink Precision — AA-11
- Jennifer / The Hearthwarden — AA-12

Cleo / The Gilded Stitch remains archived and inactive. AA-01 and AA-06 remain governed placeholders.

## Active McFleurdel outfit candidate

Manny authorized an outfit-only refresh of all eleven McFleurdel 2D assets using the supplied black-and-white checkerboard formalwear reference.

- Branch: `art/mcfleurdel-checkerboard-outfit`
- Pull request: **#85 — Refresh McFleurdel 2D outfit with checkerboard formalwear**
- Candidate package: all eleven `aa-07` 2D PNGs updated on the branch
- Batch 1 generation/validation run: **33811917223 — passed**
- Batch 2 generation/validation run: **33812111707 — passed**
- Temporary branch-only generation workflow: removed after both generated commits
- Detailed scope, candidate SHA-256 values, and review checklist: `docs/work/Mcfleurdel-checkerboard-outfit-refresh.md` and `docs/work/Mcfleurdel-checkerboard-outfit-review.md`

The candidate preserves the exact source alpha channel for every sprite, exact runtime dimensions, existing transparent negative space, approved pose/footprint, and existing hair/face geometry. The controlled production revision and production asset brief remain unchanged pending product-owner visual approval.

## Known defects / unresolved issues

No new defect was reported in Manny's final Circuit Alpha acceptance pass.

The existing production-build large-chunk warning remains known and non-blocking.

McFleurdel's checkerboard outfit package is **candidate-only**. It has not yet received product-owner asset approval, runtime revision update, merge approval, or live deployment approval.

## Deferred work

- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB was introduced in the Circuit Alpha bounded pass.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this closeout.

## Next recommended action

**Stop at the McFleurdel visual asset-review gate.**

Review the eleven checkerboard outfit candidates in PR #85. If approved, update McFleurdel's controlled runtime revision and asset hashes/documentation, run normal CI, publish a live build, and perform the existing McFleurdel state/cockpit/transparency acceptance matrix. If any candidate fails visual review, correct only the outfit treatment while preserving the already-approved face, hair, posture, hand placement, transparency, and sprite-state contract.

Do not silently advance to Slice 5, Slice 6, or materially reorder the roadmap.

## Approval state

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

**McFleurdel checkerboard outfit refresh: CANDIDATE COMPLETE / PRODUCT-OWNER ASSET REVIEW REQUIRED.**

The project roadmap remains at Slice 3.
