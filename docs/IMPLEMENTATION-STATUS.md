# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art/camera polish pass under the existing track/rendering requirements. This work does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Deployed correction release: PR **#82 — Correct Circuit Alpha ramp wedge and start gantry staging**
- PR #82 merge: `89febd6c9349dbb37b86923010957bff6039b9e0`
- Main CI / Pages run: **33805574683** — validation passed and deployment passed
- Deployment-record checkpoint: `d885f04825228d62dd3d1da9577219007ec81217`
- Deployment-record run: **33805725831** — validation passed and deployment passed

## Latest product-owner live review

Manny tested the deployed PR #82 build and recorded:

- start/finish gantry ahead of the grid during countdown/start — **PASS**
- racers drive toward and pass under the gantry — **PASS**
- Crest Ramp presents the short low edge first and rises down-track — **PASS**
- pre-race crane-down camera — **PASS**
- settled chase-camera height/angle — **PASS**
- rear-view height/angle — **PASS**
- mobile frame pacing — **PASS**

The overall Circuit Alpha environment-art direction, gantry staging, ramp wedge, crane movement, camera heights, and mobile pacing are therefore accepted.

Two final corrections remain before closing the pass:

1. **Finish-line timing:** racers currently complete lap 3 at the old checkpoint-0 loop origin before reaching the visible gantry.
2. **Camera framing:** chase and rear views should move roughly 25% closer to better showcase the driver/kart, without changing the accepted height, FOV, look target, or angle.

## Active correction candidate

Branch: `polish/circuit-alpha-finish-camera`

Pull request: **#83 — Finish at gantry and tighten race camera framing**

Validated runtime/test head before this documentation update: `cd72eb3d39c6f452105f3ddd15ac3e7b5aaf853d`.

PR CI run: **33808571518** — passed.

### Finish-line alignment

The starting grid remains unchanged at the original checkpoint-0 origin plus 8 m along the opening tangent.

`CircuitAlpha` now separates the grid origin from the lap-completion crossing:

- `checkpointPosition(0)` remains the original geometric origin used by the starting grid;
- `startFinishDistance` is **22 m** along the course from that origin;
- `lapCheckpointPosition(0)` resolves to that 22 m point, matching the already-approved visible gantry;
- `lapCheckpointPosition(1..11)` remains identical to the existing checkpoint positions;
- player and AI checkpoint-overlap detection now use `lapCheckpointPosition`.

Result: the third-lap finish is intended to register under the visible gantry instead of roughly 22 m before it. Track spline, road width, surfaces, AI pathing, physics, grid placement, and checkpoint order remain unchanged.

### Tighter race-camera framing

The accepted camera heights, look targets, FOV, smoothing, and crane timing remain unchanged.

Only longitudinal camera distance changes:

- chase distance: **7.4 m → 5.6 m** (about 24.3% closer)
- rear-view distance: **7.0 m → 5.3 m** (about 24.3% closer)
- chase height remains **3.15 m**
- rear-view height remains **3.05 m**
- look target height remains **1.15 m**
- PerspectiveCamera FOV remains **62°**
- crane duration remains **2.85 s**

This targets the requested Mario Kart-like kart prominence while preserving the approved viewing angle.

## Protected gameplay / presentation contract

PR #83 does not change:

- the 384 canonical Circuit Alpha samples or Catmull-Rom topology
- loop length or road width
- checkpoints 1–11 or checkpoint ordering
- player/AI starting grid positions
- asphalt, dirt, grass, boost, and ramp classification
- ramp trigger or ramp boost behavior
- kart physics, tuning, collisions, or AI navigation
- three-lap requirement
- countdown timing
- accepted crane-down motion
- chase/rear camera heights, FOV, look targets, or smoothing
- roster statistics or character assets
- item scope

The intentional behavior change is that checkpoint 0 for lap completion now coincides with the visible start/finish gantry.

## Automated regression evidence

PR #83 runtime/test head `cd72eb3d39c6f452105f3ddd15ac3e7b5aaf853d` passed CI run **33808571518** with:

- repository checkout
- Git LFS runtime-asset verification
- Node setup and lockfile install
- strict TypeScript typecheck
- ESLint with zero warnings
- full Vitest CI suite
- production Vite build

Pages upload/deployment were correctly skipped on the pull-request run.

New/updated regressions verify that:

- the original starting-grid origin remains separate from the 22 m lap finish crossing;
- checkpoints 1–11 retain their existing positions;
- the visible gantry position matches `lapCheckpointPosition(0)`;
- player runtime checkpoint detection uses the lap checkpoint positions;
- the seven-profile three-lap AI integration uses the same lap checkpoint positions and still completes valid races;
- chase/rear camera distances are tighter while the accepted camera heights remain unchanged.

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

## Known defects / unresolved issues

No automated defect is recorded against PR #83.

The two PR #83 changes have not yet been evaluated in a deployed build. Automated checks do not substitute for Manny's visual/gameplay acceptance.

## Deferred work

- Publication and live acceptance of PR #83 remain pending Manny approval.
- Final Circuit Alpha environment-art acceptance remains open until the finish crossing and tighter camera framing pass live review.
- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB is introduced here.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this pass.

## Next recommended action

**Stop at the PR #83 publication gate after the documentation-only head passes CI.**

If Manny approves publication, merge PR #83, verify the resulting `main` validation and Pages deployment, then live-check only:

- lap 3 does not finish before the gantry and registers as the racer crosses beneath it;
- chase framing shows the player kart/driver at the requested larger scale without clipping or reducing road readability;
- rear-view framing is similarly closer without clipping;
- accepted crane movement, camera heights/angles, gantry staging, ramp presentation, and mobile pacing remain regression-free.

## Approval state

**Circuit Alpha finish-line / camera-framing correction: AUTOMATED VALIDATION PASSED / PUBLICATION PENDING.**

The project roadmap remains at Slice 3.
