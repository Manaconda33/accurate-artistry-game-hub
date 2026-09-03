# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art pass on 2026-09-03 under the PRD's existing track and rendering/polish requirements. This is a visual-polish increment only; it does **not** advance the roadmap to Slice 5 or Slice 6 and does not authorize unrelated gameplay scope.

The Jennifer / The Hearthwarden publication and the product/repository rebrand to **Manaconda's Minigame Mayhem** remain **LIVE ACCEPTED / CLOSED**. Their detailed pre-acceptance record is preserved at `docs/history/IMPLEMENTATION-STATUS-through-2026-09-03-jennifer-rebrand-pre-acceptance.md`.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Current `main`: `90d27523413ca296333bfe13442e7a3e1bcf157a`
- Jennifer/rebrand release PR: **#76 — Publish Jennifer and rebrand as Manaconda's Minigame Mayhem**
- Jennifer/rebrand release merge: `cec008cfb8e1ae12e8985e5d5104c094d2e36148`
- Acceptance closeout PR: **#77 — Record Jennifer and rebrand live acceptance**
- Acceptance closeout merge: `90d27523413ca296333bfe13442e7a3e1bcf157a`
- Latest verified main CI / Pages run: `33795517803`
- Result: validation **passed**; GitHub Pages deploy **passed**

## Active work: Circuit Alpha environment-art pass

### Approved scope

Manny's direction is: **give Circuit Alpha a major 3D environment-art pass without changing the track layout or gameplay.**

The pass is constrained to rendering and environment presentation. The following remain protected and unchanged:

- `src/game/track/CircuitAlpha.ts`
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

### Candidate 1

Branch: `polish/circuit-alpha-environment`

Pull request: **#78 — Build Circuit Alpha environment-art pass**

Validated candidate checkpoint before this status record: `9bea7e91aecb9c61ca68ee87a2562cef34fd309b`.

Candidate 1 replaces the primitive scene dressing in `src/game/track/createTrackScene.ts` with a deterministic procedural environment pass:

- richer layered dusk sky shader with controlled sun glow
- distinct PBR road, shoulder, and darker racing-wear layers
- preserved partial-width Split S-Bend dirt lane
- instanced alternating roadside curb blocks
- instanced emissive roadside reflectors
- deterministic instanced trackside forest with 64 trunks and 64 canopy instances
- 36 instanced trackside rocks
- 18 instanced distant mountain silhouettes
- layered rocky/forested center mesa replacing the former single center cylinder
- center-mesa beacon for mid-course visual orientation
- constructed start/finish gantry
- visual underpass architecture aligned to the PRD underpass section
- upgraded visuals for both existing boost-pad locations
- upgraded Crest Ramp visual at the existing ramp trigger
- 24 instanced checkpoint pylons
- sparse landmark beacons for route readability

Repeated dressing uses `THREE.InstancedMesh` so the visual-density increase does not translate into hundreds of independent draw submissions.

No new external texture, GLB, audio, or other binary asset was introduced in Candidate 1.

### Automated regression guard

`tests/track-scene.test.ts` was added to verify the environment pass independently of gameplay topology.

It confirms that:

- environment construction leaves all 384 canonical `CircuitAlpha.samples` unchanged
- required visual landmarks are present
- both boost-pad visuals and the crest-ramp visual are present at the existing scene contract
- repeated curb, reflector, forest, rock, mountain, and checkpoint dressing remains instanced
- expected deterministic instance counts remain stable

Existing `tests/circuit-alpha.test.ts` continues to guard loop length, twelve checkpoints, and asphalt/dirt/grass/boost/ramp surface projection.

### Validation evidence

PR #78 head run **33797708233** completed successfully on 2026-09-03.

Passed:

- repository checkout
- Git LFS runtime-asset materialization / verification
- Node setup and lockfile install
- strict TypeScript typecheck
- ESLint with zero warnings
- full Vitest CI suite, including the new environment regression
- production Vite build

GitHub Pages configuration, artifact upload, and deployment were correctly skipped because this is still an unmerged pull-request candidate.

The candidate has therefore passed the automated code/build gate but has **not** passed visual or performance acceptance. A production deployment and product-owner desktop/mobile playtest remain required before the environment pass can be called complete.

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

## Completed requirements and acceptance criteria

- Jennifer / The Hearthwarden remains fully live accepted.
- All ten active production drivers retain their complete shared chase-facing and camera-facing action-state contract.
- The Manaconda's Minigame Mayhem product/repository/Pages rebrand remains live accepted.
- Existing live-accepted gameplay, physics, AI, minimap, driver, kart, and surface checkpoints are unchanged by the Circuit Alpha candidate.
- Candidate 1 satisfies its automated visual-scene composition and topology-preservation checks.

## Known defects / unresolved issues

No automated defect is recorded against Candidate 1.

The existing production-build large-chunk warning remains known and non-blocking.

The environment-art pass has not yet been viewed in a deployed race. Potential visual issues such as scale, occlusion, roadside clutter, landmark placement, lighting balance, mobile readability, or runtime frame cost remain unresolved until live testing.

## Deferred work

- Publication and live acceptance of Circuit Alpha Candidate 1 are pending Manny approval.
- No new external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB is part of Candidate 1.
- AA-01 and AA-06 character assignments remain unfilled.
- Items remain Slice 5 work and are not authorized by this pass.
- Other Slice 6 presentation/audio/optimization work remains outside this bounded increment.

## Next recommended action

**Stop at the publication gate.**

If Manny approves Candidate 1 for publication, merge PR #78, verify the resulting `main` validation and GitHub Pages deployment, then conduct desktop/mobile visual and performance playtesting of the live build.

The live review should specifically evaluate:

- dusk sky and horizon depth
- road, shoulder, racing-wear, curb, and reflector readability at speed
- trackside vegetation/rock density without visual obstruction
- center mesa silhouette and route-orientation value
- start/finish gantry scale
- underpass clearance and lighting transition
- boost-pad and Crest Ramp readability
- checkpoint/landmark visual language
- eight-racer frame pacing and any mobile performance regression

Do not declare the environment pass complete from CI alone.

## Approval state

**Circuit Alpha environment Candidate 1: AUTOMATED VALIDATION PASSED / PUBLICATION PENDING.**

The project roadmap remains at Slice 3. PR #78 must not merge until Manny explicitly authorizes publication for live visual playtesting.
