# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art pass on 2026-09-03 under the existing track/rendering requirements. This does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Candidate 1 visual release: PR **#78**
- Candidate 1 merge: `4453cd8867078a31c837b6a7c8c9c5a768d46d9c`
- Candidate 1 deployment record: PR **#79**
- Current `main`: `4b47cea4027999676c23eb749bf96fcd1280da68`
- Latest main CI / Pages run: **33798472639**
- Result: validation **passed**; Pages deploy **passed**

## Circuit Alpha environment-art Candidate 1 — deployed, corrections requested

Manny's direction remains: **give Circuit Alpha a major 3D environment-art pass without changing the track layout or gameplay.**

The deployed Candidate 1 environment treatment is positively accepted in overall direction. Manny specifically called out the start/finish structure and overall visual punch-up as successful, while requesting three bounded corrections before final acceptance:

1. lower both chase and rear-view camera heights;
2. add a pre-race camera move that cranes down from above the track into the final chase position;
3. correct the Crest Ramp visual so its long axis runs parallel to the track rather than perpendicular to it.

The supplied live screenshots show the elevated race camera allowing the 4.6 m start/finish crossbar to sit between camera and racer, and show the Crest Ramp's longer dimension spanning across the road.

## Active correction candidate

Branch: `polish/circuit-alpha-camera-ramp`

Pull request: **#80 — Lower race cameras and align Crest Ramp**

Validated code checkpoint before this status update: `6a7afb5f7edbe860c85b67f13e1ca683d0ad9745`.

### Camera presentation

`src/game/camera/ChaseCamera.ts` now uses:

- chase distance: **7.4 m**
- chase height: **3.15 m**
- rear-view distance: **7.0 m**
- rear-view height: **3.05 m**
- look target height: **1.15 m**

The previous race camera height was 5.2 m.

For the first **2.85 seconds** of the race camera lifetime, the camera begins approximately 16 m above the track and 2.2 m behind the player, then uses smoothstep easing to crane down into the final lower chase position. This aligns with the existing three-second countdown without altering `RaceDirector`, countdown timing, simulation, controls, physics, or AI.

The intro presentation ignores rear-view framing until the crane completes; normal chase/rear input behavior resumes afterward through the unchanged `ChaseCamera.update` call contract.

### Crest Ramp orientation

The existing gameplay ramp trigger remains at progress 0.5 and `CircuitAlpha.ts` remains unchanged.

Only visual geometry changed:

- former deck: 9.0 m track-local X × 5.75 m track-local Z
- corrected deck: **5.75 m X × 9.0 m Z**
- side rails now run 9.1 m along local Z and sit at ±2.62 m local X
- the deck is named `crest-ramp-deck` for regression inspection

Because the ramp group already rotates its local Z axis to the track tangent, the corrected longer Z dimension now runs parallel to the roadway.

## Protected gameplay contract

The following remain unchanged by PR #80:

- `src/game/track/CircuitAlpha.ts`
- all 384 canonical track samples and Catmull-Rom topology
- loop length and road width
- twelve checkpoints / three-lap validation
- asphalt, dirt, grass, boost, and ramp gameplay classification
- ramp trigger location and ramp boost behavior
- player and AI physics/tuning
- kart collisions
- AI pathing/race logic
- countdown timing
- roster statistics / character assets
- item scope

The camera framing itself is intentionally changed under Manny's explicit live-review request.

## Automated regression evidence

New `tests/chase-camera.test.ts` verifies:

- the first race view begins elevated above 12 m;
- the camera cranes into a chase height between 2.9 and 3.4 m;
- the settled chase camera remains behind the kart;
- the rear-view camera uses the corresponding low height and moves ahead of the kart to look backward.

`tests/track-scene.test.ts` now also verifies that `crest-ramp-deck` is longer along its track-local forward/depth axis than its width axis.

Existing topology, surface, physics, AI, roster, runtime-asset, and gameplay regressions remain intact.

PR #80 head run **33801880713** passed on 2026-09-03:

- repository checkout
- Git LFS runtime-asset verification
- Node setup / lockfile install
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

No automated defect is currently recorded against the camera/ramp correction candidate.

The existing production-build large-chunk warning remains known and non-blocking.

The new camera height, start crane, gantry clearance, ramp orientation, and frame pacing have not yet been evaluated in the deployed game. Automated camera-coordinate tests do not substitute for live visual judgment.

## Deferred work

- Publication and live acceptance of PR #80 remain pending Manny approval.
- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB is introduced here.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this pass.

## Next recommended action

**Stop at the publication gate after the exact PR #80 head passes CI.**

If Manny approves publication, merge PR #80, verify the resulting main validation and Pages deployment, then conduct live desktop/mobile review of:

- start crane composition and smoothness during 3 / 2 / 1;
- final chase height and kart visibility;
- rear-view height and readability;
- start/finish crossbar clearance;
- Crest Ramp orientation and approach readability;
- eight-racer frame pacing and mobile performance.

## Approval state

**Circuit Alpha camera/ramp correction: AUTOMATED VALIDATION PASSED / PUBLICATION PENDING.**

Candidate 1 remains deployed; final Circuit Alpha visual acceptance is pending these corrections and a subsequent live playtest.
