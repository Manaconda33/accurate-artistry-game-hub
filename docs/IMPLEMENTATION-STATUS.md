# Implementation Status

## Current slice

**Slice 1 - Engine Setup, Basic Kart Physics, Keyboard Controls, Single Track Loop & Time Trial: implementation complete; deployment verification in progress**

Manny approved Slice 1 on 2026-08-16 and added a standing requirement that every slice checkpoint provide a GitHub-hosted manual test URL.

## Completed requirements

- HUB-001: the SPA opens on a title screen without entering gameplay.
- HUB-002: the first user action resumes the Howler/Web Audio context.
- HUB-003: the Main Menu lists Circuit Alpha Time Trial as playable.
- HUB-004: two future games are visibly unavailable and non-activating.
- HUB-005: Controls and Settings are available from the Main Menu.
- PHYS-001: simulation advances through a clamped fixed 60 Hz runner.
- PHYS-002: the Slice 1 driver’s Speed, Acceleration, Weight, Handling, and Traction values affect kart tuning formulas. Mini-Turbo remains assigned to Slice 2.
- PHYS-003 foundational portion: the Rapier collider owns stat-derived mass; player-to-opponent relative-mass response remains deferred because Slice 1 is explicitly player-only.
- PHYS-004: dirt and grass speed, acceleration, and grip use the Traction stat.
- PHYS-005: manual `R` recovery and automatic out-of-bounds recovery return the kart to the last valid track/recovery sample.
- PHYS-006: finite-state guards recover invalid transforms; the 10-minute fixed-step numerical soak remains finite.
- TRACK-001: procedural Circuit Alpha is approximately 1.45 km and includes asphalt, dirt, grass, boost pads, and a ramp marker/blockout.
- TRACK-002: twelve ordered checkpoints prevent shortcut lap completion.
- TRACK-003: reverse finish crossing is rejected and sustained reverse alignment displays `WRONG WAY`.
- A three-lap time trial, timer, speed/surface/lap HUD, chase camera, rear camera, performance overlay, pause input, and finish result are implemented.
- The title/menu bundle is separated from the lazily loaded Three.js/Rapier gameplay bundle.
- GitHub Pages deployment is integrated into CI through the `github-pages` environment.
- PRD working copy amended to require a live GitHub deployment for every Slice 1+ checkpoint; ADR-007 records the decision.

## Work in progress

- Publish the Slice 1 checkpoint candidate.
- Verify GitHub Actions and the GitHub Pages environment.
- Perform deployed smoke validation and provide the live URL for Manny’s manual confirmation.

## Known defects

- None identified by automated validation.
- Manual play confirmation is pending the deployed checkpoint.

## Deferred work

- Drift, hop, mini-turbo tiers, drift VFX/audio, and full multi-surface drift tuning: Slice 2.
- Seven AI racers, relative-mass kart-to-kart collision behavior, ranking, countdown, results placement, and competitive three-lap race: Slice 3.
- Character selection/roster and avatar art pipeline: Slice 4.
- Items and advanced collision responses: Slice 5.
- Final HUD, audio content, post-processing, and optimization: Slice 6.
- Circuit Alpha uses procedural geometry and a visual ramp marker in Slice 1. Full modeled elevation, banked collision geometry, jump/stunt behavior, and production art remain later track/polish work.

## Next recommended action

Manny manually tests the deployed Slice 1 build. Begin Slice 2 only after he explicitly approves this checkpoint.

## Validation evidence

Validated from a clean npm installation on 2026-08-16:

- Environment: Node.js `v24.19.0`, npm `11.9.0`, Git LFS `3.4.1`.
- Clean install: `npm ci --prefer-offline --no-audit --no-fund` passed; 198 packages installed from `package-lock.json`.
- Typecheck: strict TypeScript project build passed with no diagnostics.
- Lint: ESLint passed with zero warnings permitted.
- Tests: 5 files and 11 tests passed under Vitest `4.1.10`.
- Automated evidence includes fixed-step clamping, 10-minute finite numeric soak, stat mapping, surface slowdown ordering, approximately 1.45 km shared track topology, twelve checkpoints, skipped-checkpoint rejection, reverse finish rejection, and three valid laps.
- Coverage: 59.74% statements, 54.21% branches, 57.57% functions, and 62.85% lines across instrumented test targets.
- Production build: Vite `8.2.1` passed; title/menu JavaScript is 12.49 kB gzip and the lazily loaded Three.js/Rapier gameplay package is 1.20 MB gzip, inside the PRD’s download budgets.
- Local production preview served successfully at the configured `/accurate-artistry-game-hub/` base path.
- CI and GitHub Pages: pending checkpoint publication.

## Last verified commit

`745de06d02b36df9560932323d32a7445c56fec7` - approved Slice 0 checkpoint. Slice 1 candidate commit pending publication.
