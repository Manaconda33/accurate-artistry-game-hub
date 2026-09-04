# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art/camera polish pass under the existing track/rendering requirements. That pass remains **LIVE ACCEPTED / CLOSED** and does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

## Balance rollback — final closeout

Manny ended the Circuit Alpha rebalance experiment on **2026-09-03** after live playtesting showed that the experimental balance candidates did not preserve the desired player-vs-AI race competitiveness. The exercise is **ABANDONED / ROLLED BACK** rather than accepted or iterated further.

The runtime and related tests have been restored exactly to the accepted pre-balance source checkpoint `a706f01f43f07d9b31d05ce38e3e4b67c396894c`.

- Rollback PR: **#88 — Restore pre-balance gameplay**
- Rollback merge: `f8eb2dca1e32fe803b436793edae59b0b01b55ff`
- PR CI run: **33822797898** — validation passed
- Main CI / Pages run: **33822922732** — validation passed and deployment passed
- Candidate F PR #86 remains historical analysis only and is not an accepted balance specification.
- Candidate G PR #87 was closed without merge and is abandoned.
- The 250,000-race Candidate F simulation remains analysis history only.

The rollback restored the exact pre-balance blobs for `src/config/kartTuning.ts`, `src/game/ai/AiDriver.ts`, `src/game/physics/KartController.ts`, and their pre-balance AI/controller/tuning tests, while removing the two temporary balance diagnostic suites. A direct comparison against `a706f01...` confirmed that the runtime/test content matches the pre-balance checkpoint exactly; only this implementation-status record intentionally differs.

No character stat allocations, assets, Circuit Alpha environment/camera work, roster membership, Jennifer work, or rebrand work were reverted. Further competitive-balance work is deferred until Manny explicitly reopens it.

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Current runtime rollback release: PR **#88 — Restore pre-balance gameplay**
- PR #88 merge: `f8eb2dca1e32fe803b436793edae59b0b01b55ff`
- Main CI / Pages run: **33822922732** — validation passed and deployment passed
- Restored gameplay source authority: `a706f01f43f07d9b31d05ce38e3e4b67c396894c`

The prior Circuit Alpha environment/camera release remains separately accepted:

- PR **#83 — Finish at gantry and tighten race camera framing**
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

The later balance experiment was fully rolled back by PR #88, so the gameplay contract above is again the active production behavior.

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

Rollback PR #88 head `156bdc85030f27afc69bef4f24b82fcbf9ab0d80` passed PR run **33822797898**. Merged rollback commit `f8eb2dca1e32fe803b436793edae59b0b01b55ff` passed main run **33822922732** with successful GitHub Pages deployment.

Regression coverage verifies that:

- environment construction does not mutate canonical track samples;
- the gantry is staged ahead of the starting grid;
- the visible gantry matches the lap finish crossing;
- the Crest Ramp is a forward-rising wedge aligned to course-forward;
- player and AI checkpoint detection use the same lap checkpoint positions;
- seven-profile AI simulation completes three valid laps under the restored pre-balance implementation;
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

## Known defects / unresolved issues

No new defect was introduced by the rollback. No balance candidate is active.

The existing production-build large-chunk warning remains known and non-blocking.

## Deferred work

- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB was introduced in the bounded Circuit Alpha pass.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this closeout.
- Further competitive-balance work is deferred until Manny explicitly reopens it.

## Next recommended action

**Return to normal Slice 3 gameplay/roster development from the restored pre-balance runtime.**

Circuit Alpha environment-art/camera work requires no further acceptance action. The balance experiment is closed and should not be resumed implicitly.

The next implementation action must be selected explicitly by Manny, for example:

- begin another Slice 3 character intake using AA-01 or AA-06; or
- approve a different PRD-defined bounded scope.

Do not silently advance to Slice 5, Slice 6, reopen Candidate F/G tuning, or materially reorder the roadmap.

## Approval state

**Balance experiment: ABANDONED / ROLLED BACK / CLOSED.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

The project roadmap remains at Slice 3.
