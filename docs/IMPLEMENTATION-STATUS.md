# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art/camera polish pass under the existing track/rendering requirements. That pass is now **LIVE ACCEPTED / CLOSED** and does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

A bounded Circuit Alpha balance pass is now active under PR **#86**. Candidate F has passed the simulation gate and is **APPROVED FOR LIVE PLAYTEST**, but is not yet final accepted balance.

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

## Active Candidate F balance checkpoint

Candidate F keeps all existing racer stat allocations unchanged and changes only shared balance behavior:

- Speed 7 remains anchored at **29.5 m/s**;
- the Speed 1–10 sustained-asphalt spread is compressed to **3.0 m/s**;
- Handling now contributes to shared physical corner-speed retention;
- AI receives only a modest additional Handling-aware braking adjustment so Handling is not heavily double-counted;
- Circuit Alpha AI corner demand uses normalized lookahead-angle geometry;
- Mini-Turbo-aware AI seeks valid drift opportunities and respects governed blue/orange/purple tier limits;
- Weight collision retention, Traction, surfaces, boost pads, ramp behavior, Circuit Alpha geometry, roster sampling, individual stat allocations, assets, and item scope remain unchanged.

Candidate F source checkpoint: `0fce4d2be4c41ff2f7fddf69d13d74306a78f106`.

PR CI run **33818180063** passed:

- Git LFS verification;
- strict TypeScript typecheck;
- ESLint with zero warnings;
- **20/20 test files and 102/102 tests**;
- seven runtime AI profiles completing valid three-lap Rapier simulations for every manifest racer;
- all 84 diagnostic racer/profile runs at **0% grass time**;
- runtime asset verification;
- production Vite build.

The final **250,000-race** moderate-variance Monte Carlo produced these conditional win rates when each racer was present in an eight-racer field:

- Keeg — **19.54%**
- Krios — **18.56%**
- McFleurdel — **18.12%**
- Lavi — **14.21%**
- Manaconda — **13.70%**
- Jennifer — **11.76%**
- Racer 06 — **11.28%**
- Kraken — **10.36%**
- Racer 01 — **8.68%**
- Lula — **8.18%**
- Accu — **7.88%**
- Toph — **7.74%**

Compared with Candidate E, Krios fell from **23.81% to 18.56%**, Lula rose from **6.16% to 8.18%**, the best-to-worst win-rate spread fell from **17.65 to 11.80 percentage points**, and field win-rate standard deviation fell by about **24.1%**.

Manny approved Candidate F's simulation gate on **2026-09-03**. The next required evidence is a deployed product-owner playtest. This approval does not yet make Candidate F final accepted production balance.

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

The accepted Circuit Alpha environment pass did not change:

- the 384 canonical Catmull-Rom track samples or course topology;
- loop length or road width;
- checkpoints 1–11 or checkpoint order;
- player/AI starting grid positions;
- asphalt, dirt, grass, boost, and ramp gameplay classification;
- ramp trigger or ramp boost behavior;
- three-lap requirement;
- countdown timing;
- roster statistics or character assets;
- item scope.

The later Candidate F balance checkpoint intentionally changes shared Speed/Handling/AI Mini-Turbo behavior only as described above and remains pending live acceptance.

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

- Candidate F has passed simulation and automated validation but still requires live product-owner playtest acceptance.
- The existing production-build large-chunk warning remains known and non-blocking.

## Deferred work

- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB was introduced in the bounded environment pass.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this balance checkpoint.

## Next recommended action

**Deploy Candidate F and stop at the product-owner live playtest gate.**

The live playtest should focus on whether:

- Krios remains recognizably fastest without overwhelming the field;
- high-Handling racers gain corner value without feeling artificially speed-limited;
- Kraken/Toph Mini-Turbo identity is visible in AI behavior;
- Accu still benefits from Weight without becoming either dominant or inert;
- the pack feels competitive over multiple three-lap races;
- existing surface, collision, ramp, boost, checkpoint, camera, mobile, and asset behavior remains intact.

Do not record Candidate F as final accepted balance until Manny explicitly approves the deployed playtest. Do not silently advance to Slice 5 or Slice 6.

## Approval state

**Candidate F balance simulation gate: APPROVED / LIVE PLAYTEST REQUIRED.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

The project roadmap remains at Slice 3.
