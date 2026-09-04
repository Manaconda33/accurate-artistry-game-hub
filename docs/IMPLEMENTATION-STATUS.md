# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

Manny explicitly authorized a bounded Circuit Alpha environment-art/camera polish pass under the existing track/rendering requirements. That pass is now **LIVE ACCEPTED / CLOSED** and does **not** advance the roadmap to Slice 5 or Slice 6.

Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

A bounded Circuit Alpha balance pass is now active under PR **#86**. Candidate F passed the 250,000-race simulation gate, was approved for live playtest, merged, validated on `main`, and deployed. **Product-owner live playtest acceptance is the remaining gate.**

## Latest verified live checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Candidate F balance PR: **#86 — Candidate F balance playtest checkpoint**
- Candidate F merge: `faedd84e6e86ab7adca1d5f8ed06742d6ab70920`
- Main CI / Pages run: **33819651122** — validation passed and deployment passed
- Product-owner state: **LIVE PLAYTEST REQUIRED**
- Candidate F is not yet final accepted production balance.

The prior fully accepted Circuit Alpha environment/camera release remains PR **#83**, merge `da9275771941e7e112a6153af3d5d1cd97ea2bf2`, with product-owner final live acceptance on 2026-09-03.

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

Final PR documentation checkpoint before merge: `2146d815c69ff26f8d9bb4ed39beac415ae8eafb`.

PR CI run **33819366960** passed on that exact documented head after the simulation approval record was added.

Earlier Candidate F physics CI run **33818180063** passed:

- Git LFS verification;
- strict TypeScript typecheck;
- ESLint with zero warnings;
- **20/20 test files and 102/102 tests**;
- seven runtime AI profiles completing valid three-lap Rapier simulations for every manifest racer;
- all 84 diagnostic racer/profile runs at **0% grass time**;
- runtime asset verification;
- production Vite build.

Merged `main` commit `faedd84e6e86ab7adca1d5f8ed06742d6ab70920` passed run **33819651122** with the same validation plus successful GitHub Pages artifact upload and deployment.

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

Manny approved Candidate F's simulation gate on **2026-09-03**. Deployment is complete; the remaining evidence is Manny's product-owner live playtest. This approval does not yet make Candidate F final accepted production balance.

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

- Candidate F is deployed but still requires live product-owner playtest acceptance.
- The existing production-build large-chunk warning remains known and non-blocking.

## Deferred work

- No external PBR texture set, HDR environment, baked AO asset, post-processing stack, or authored track GLB was introduced in the bounded environment pass.
- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work and are not authorized by this balance checkpoint.

## Next recommended action

**Stop at the product-owner live playtest gate.**

Play the deployed Candidate F build and focus on whether:

- Krios remains recognizably fastest without overwhelming the field;
- high-Handling racers gain corner value without feeling artificially speed-limited;
- Kraken/Toph Mini-Turbo identity is visible in AI behavior;
- Accu still benefits from Weight without becoming either dominant or inert;
- the pack feels competitive over multiple three-lap races;
- existing surface, collision, ramp, boost, checkpoint, camera, mobile, and asset behavior remains intact.

Do not record Candidate F as final accepted balance until Manny explicitly approves the deployed playtest. Do not silently advance to Slice 5 or Slice 6.

## Approval state

**Candidate F balance: DEPLOYED / LIVE PLAYTEST REQUIRED.**

**Candidate F simulation gate: APPROVED.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

The project roadmap remains at Slice 3.
