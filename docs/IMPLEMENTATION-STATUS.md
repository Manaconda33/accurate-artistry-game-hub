# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art pass on 2026-09-03 under the PRD's existing track and rendering/polish requirements. This is a visual-polish increment only; it does **not** advance the roadmap to Slice 5 or Slice 6 and does not authorize unrelated gameplay scope.

The Jennifer / The Hearthwarden publication and the product/repository rebrand to **Manaconda's Minigame Mayhem** remain **LIVE ACCEPTED / CLOSED**. Their detailed pre-acceptance record is preserved at `docs/history/IMPLEMENTATION-STATUS-through-2026-09-03-jennifer-rebrand-pre-acceptance.md`.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Current deployed Candidate 1 merge: `4453cd8867078a31c837b6a7c8c9c5a768d46d9c`
- Release PR: **#78 — Build Circuit Alpha environment-art pass**
- Post-merge CI / Pages run: **33798145690**
- Validation result: **passed**
- GitHub Pages deploy: **passed**
- Pages artifact: `github-pages` artifact **9910007986**
- Artifact digest: `sha256:5df814cde851baf4cfc44f18887bceeffc4a11d0cba3ae397bb605064d8ce015`
- Product-owner live visual acceptance: **pending**

## Circuit Alpha environment-art Candidate 1 — deployed

Manny's approved direction is: **give Circuit Alpha a major 3D environment-art pass without changing the track layout or gameplay.**

Candidate 1 is now deployed from `main`. The pass replaces the primitive scene dressing in `src/game/track/createTrackScene.ts` with a deterministic procedural environment treatment:

- richer layered dusk sky shader with controlled sun glow
- distinct PBR road, shoulder, and darker racing-wear layers
- preserved partial-width Split S-Bend dirt lane
- instanced alternating roadside curb blocks
- instanced emissive roadside reflectors
- deterministic instanced trackside forest with 64 trunks and 64 canopy instances
- 36 instanced trackside rocks
- 18 instanced distant mountain silhouettes
- layered rocky/forested center mesa replacing the former single center cylinder
- center-mesa beacon for route orientation
- constructed start/finish gantry
- visual underpass architecture aligned to the PRD underpass section
- upgraded visuals for both existing boost-pad locations
- upgraded Crest Ramp visual at the existing ramp trigger
- 24 instanced checkpoint pylons
- sparse landmark beacons for route readability

Repeated scenery uses `THREE.InstancedMesh` to increase environmental density without hundreds of independent submissions. No external texture, GLB, audio, or other binary asset was introduced.

## Protected gameplay contract

`src/game/track/CircuitAlpha.ts` is unchanged by Candidate 1.

The following remain protected and unchanged:

- the 384 canonical track samples and Catmull-Rom course topology
- approximately 0.90 km loop length
- road width and signed surface projection
- twelve ordered checkpoints and three-lap validation
- asphalt, dirt, grass, boost, and ramp gameplay classification
- player and AI physics/tuning
- kart collision behavior
- AI pathing and race logic
- camera coordinates and controls
- roster statistics and character assets
- item scope

## Validation evidence

PR #78 candidate validation passed before publication. The exact merged `main` checkpoint then passed run **33798145690** with:

- Git LFS runtime-asset materialization and verification
- Node setup and lockfile install
- strict TypeScript typecheck
- ESLint with zero warnings
- full Vitest CI suite
- `tests/track-scene.test.ts` topology-preservation and environment-composition regression
- existing `tests/circuit-alpha.test.ts` loop/checkpoint/surface regression
- production Vite build
- GitHub Pages configuration
- Pages artifact upload
- successful GitHub Pages deployment

The new environment regression verifies that scene construction does not mutate the 384 canonical samples, required landmarks remain present, the two boost-pad visuals and crest-ramp visual remain represented, and repeated scenery remains instanced with deterministic counts.

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

Cleo / The Gilded Stitch remains archived and inactive. AA-01 and AA-06 remain governed placeholders. The twelve-slot Character Select architecture remains intact.

## Known defects / unresolved issues

No automated defect is recorded against Candidate 1.

The existing production-build large-chunk warning remains known and non-blocking.

The deployed environment has not yet passed product-owner visual/performance acceptance. Potential issues such as scale, occlusion, roadside clutter, landmark placement, lighting balance, mobile readability, or runtime frame cost remain open until live testing.

## Deferred work

- Final live acceptance of Circuit Alpha Candidate 1 is pending Manny's desktop/mobile playtest.
- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB is part of Candidate 1.
- AA-01 and AA-06 character assignments remain unfilled.
- Items remain Slice 5 work and are not authorized by this pass.
- Other Slice 6 presentation/audio/optimization work remains outside this bounded increment.

## Next recommended action

**Stop at the live visual-acceptance gate.**

Manny should play the deployed Candidate 1 on desktop and mobile and evaluate:

- dusk sky and horizon depth
- road, shoulder, racing-wear, curb, and reflector readability at speed
- vegetation/rock density without obstruction
- center mesa silhouette and route-orientation value
- start/finish gantry scale
- underpass clearance and lighting transition
- boost-pad and Crest Ramp readability
- checkpoint/landmark visual language
- eight-racer frame pacing and any mobile performance regression

If the live result passes, record final acceptance. If it does not, make only bounded visual corrections and repeat the deployment gate.

## Approval state

**Circuit Alpha environment Candidate 1: DEPLOYED / LIVE ACCEPTANCE PENDING.**

The project roadmap remains at Slice 3.