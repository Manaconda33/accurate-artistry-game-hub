# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art pass under the existing track/rendering requirements. This visual-polish work does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Camera/ramp release PR: **#80 — Lower race cameras and align Crest Ramp**
- PR #80 merge: `c235b2dd647663acd99c75d0dd3fcd0c8f86e059`
- PR #80 main CI / Pages run: **33802245643** — passed validation and deployment
- Deployment-record PR: **#81**
- Current durable `main` checkpoint before the next correction: `27bb99dfa7f3a162d09d02c5ffd74ab5e776a49e`
- PR #81 main run: **33802643628** — passed validation and deployment

## Latest product-owner live review

Manny tested the deployed PR #80 build and recorded:

- pre-race crane-down during 3 / 2 / 1 — **PASS**
- final lower chase-camera framing — **PASS**
- rear-view framing — **PASS**
- mobile frame pacing — **PASS**
- start/finish structure staging — **FAIL / correction required**: the visual gantry is behind the starting racers and therefore disappears from the forward start view
- Crest Ramp direction/approach — **FAIL / correction required**: the deck still reads as a tilted plank rather than a proper forward-facing ramp; the short low edge must face the approaching driver and the high edge must sit farther down the road

The overall Circuit Alpha environment-art direction remains positively accepted. Final visual acceptance is blocked only on the two presentation corrections above.

## Active correction candidate

Branch: `polish/circuit-alpha-ramp-gate`

Pull request: **#82 — Correct Circuit Alpha ramp wedge and start gantry staging**

Current validated runtime/test head: `8092ebe2b2c97d9a816ee9fc48e1ad272faed23a`.

Exact-head CI run: **33804308991** — passed.

### Start/finish gantry staging

The player gameplay spawn remains unchanged at:

`checkpointPosition(0) + checkpointTangent(0) * 8 m`.

The visual gantry previously sat exactly at checkpoint 0, placing it behind the player and much of the grid at race start. PR #82 changes only the visual gantry placement:

- visible gantry position: **22 m along the course from checkpoint 0**
- player spawn remains **8 m** beyond checkpoint 0
- visual gantry therefore sits roughly **14 m ahead of the player's start position** along the opening straight
- checkpoint 0, lap validation, grid spawn, race timing, and track topology are unchanged

This should make the pack launch toward and pass under the start/finish structure.

### Crest Ramp wedge

The gameplay ramp trigger remains at progress **0.5** and `src/game/track/CircuitAlpha.ts` remains unchanged.

PR #82 replaces the tilted rectangular deck with a closed wedge aligned to the track tangent:

- width: **5.0 m**
- length: **9.5 m** along track-local Z / course-forward
- approaching local `-Z` edge: **0.08 m** high
- far local `+Z` edge: **1.30 m** high
- side rails follow the same slope
- named `crest-ramp-approach-edge` remains on the low / approaching side
- no group-level X tilt is used; the wedge geometry itself supplies the rising road surface

The intended visual read is now: short low edge toward the driver, long dimension running with the roadway, and elevated takeoff edge farther down the track.

## Protected gameplay contract

The following remain unchanged by PR #82:

- `src/game/track/CircuitAlpha.ts`
- all 384 canonical track samples and Catmull-Rom topology
- loop length and road width
- twelve checkpoints and three-lap validation
- player and AI starting positions
- asphalt, dirt, grass, boost, and ramp gameplay classification
- ramp trigger location and ramp boost behavior
- player and AI physics/tuning
- kart collisions
- AI pathing and race logic
- countdown timing
- the accepted crane-down, chase-camera, and rear-view coordinates from PR #80
- roster statistics and character assets
- item scope

No PRD deviation is introduced.

## Automated regression evidence

PR #82 now verifies that:

- constructing the environment does not mutate the canonical Circuit Alpha samples
- the visible start/finish gantry sits more than 10 m ahead of the player's starting spawn along the opening tangent
- the Crest Ramp's local Z extent is longer than its local X extent
- the far / `+Z` edge is more than 1 m higher than the near / `-Z` approach edge
- `crest-ramp-approach-edge` remains on local negative Z
- all existing required environment landmarks remain present
- repeated scenery instancing counts remain intact

Two earlier PR runs failed only on redundant TypeScript assertions inside the new regression test. No runtime/typecheck defect was involved. Those assertions were removed.

Exact candidate head `8092ebe2b2c97d9a816ee9fc48e1ad272faed23a` passed CI run **33804308991** with:

- repository checkout
- Git LFS runtime-asset verification
- Node setup and lockfile install
- strict TypeScript typecheck
- ESLint with zero warnings
- full Vitest CI suite
- production Vite build

Pages upload/deployment were correctly skipped on the pull-request run.

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

No automated defect is recorded against the current PR #82 candidate.

The existing production-build large-chunk warning remains known and non-blocking.

The corrected gantry position and rebuilt ramp wedge have not yet been evaluated in the deployed game. Automated geometry tests do not substitute for Manny's live visual judgment.

## Deferred work

- Publication and live acceptance of PR #82 remain pending Manny approval.
- Final Circuit Alpha environment-art acceptance remains open until the corrected gantry and ramp pass desktop/mobile review.
- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB is introduced here.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this pass.

## Next recommended action

**Stop at the PR #82 publication gate after this documentation-only status update passes CI.**

If Manny approves publication, merge PR #82, verify the resulting `main` validation and Pages deployment, then live-check only:

- the start/finish gantry is visible ahead of the grid during the countdown and racers launch toward/pass under it;
- the Crest Ramp presents its short low edge to the approaching driver and rises toward its far edge down-track;
- no regression to the already-passed crane, chase/rear framing, or mobile frame pacing.

## Approval state

**Circuit Alpha gantry/ramp correction: AUTOMATED VALIDATION PASSED / PUBLICATION PENDING.**

The project roadmap remains at Slice 3.
