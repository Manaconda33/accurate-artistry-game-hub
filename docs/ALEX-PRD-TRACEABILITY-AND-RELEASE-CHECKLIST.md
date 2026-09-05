# Alex / The Neon Vector — PRD traceability and release checklist

This is the final AA-01 production traceability record. It translates the approved Alex decisions and PRD delivery contract into observable evidence through local validation, publication, deployment, and Manny's desktop/mobile live acceptance on 2026-09-05.

## PRD-to-runtime traceability

| Approved requirement | Runtime implementation | Automated/local evidence | Final product-owner result |
| --- | --- | --- | --- |
| Alex is an approved adult woman, she/her, warm clever competitor | `characterManifest` entry `aa-01`; `docs/avatars/ALEX.md` | Manifest test checks name, descriptor, stats, and production state | PASS — identity and presentation accepted in deployed Character Select and race |
| AA-01 Feather Sprinter mapping | Stats 6 / 9 / 2 / 8 / 7 / 4 in `src/characters/manifest.ts` | `tests/character-manifest.test.ts`; manifest total validation | PASS — displayed stats and driving identity accepted |
| Portrait Option A approved | `public/assets/characters/aa-01/portrait.png` | Runtime verifier checks 256 x 256 RGBA, alpha margins, and decodability | PASS — controlled portrait loads without fallback on desktop/mobile |
| Ten approved driver states | Ten files under `public/assets/characters/aa-01/driver/` | Runtime verifier checks dimensions, RGBA data, transparent corners, and complete decoding | PASS — all states load and transition correctly |
| Chase steering uses moderate turn-directed torso rotation and one visible hand | `steer-left.png` and `steer-right.png` | Offline ten-state cockpit sheet; approved package hashes | PASS — both directions and chase restoration accepted |
| Driver art is character-only and wheel-free | Raster package contains no kart/control geometry | Offline review plus single-wheel ownership check | PASS — no duplicate wheel appears in any deployed state |
| Kart name is The Neon Vector | `kartName` and asset metadata | Manifest test and branding/asset checks | PASS — production name accepted live |
| Candidate 3 geometry is approved | `kart.glb`, `kart-lod1.glb`, `kart-lod2.glb` | Deterministic rebuilds match approved SHA-256 values; GLB verifier checks signature and `extras.forward` | PASS — orientation, attached geometry, and readable conduits accepted |
| Production kart forward axis is negative Z | `NEGATIVE_Z_KART_VISUAL_YAW` and GLB `extras.forward: "-Z"` | Runtime verifier and manifest test | PASS — nose/exhaust direction accepted in chase and rear views |
| One modeled steering wheel belongs to the kart | Candidate 3 `SteeringWheel` node; Alex sprite flag remains unset | Geometry validation and offline cockpit review | PASS — wheel remains singular and readable in all ten states |
| Camera-facing placement preserves hands/wheel relationship | Chase `[0, 0.92, -0.12]`; front `[0, 0.84, -0.12]` | Offline attachment review and manifest placement test | PASS — desktop/mobile hand placement accepted |
| Exposed cockpit-to-thruster conduits remain structurally visible | Candidate 3 rear conduit geometry retained in all LODs | Approved geometry preview and offline review evidence | PASS — both conduits remain visible and attached |
| Controlled cache revision protects changed asset paths | `alex-runtime-20260905-1` query on manifest URLs | Manifest test checks revisioned URLs | PASS — deployed controlled revision accepted |

## Local release-readiness checklist

### Before publication

- [x] Approved Alex identity, AA-01 mapping, stats, portrait, ten states, kart name, and Candidate 3 geometry recorded.
- [x] Runtime assets placed under AA-01 paths.
- [x] Manifest replaces the AA-01 placeholder with Alex.
- [x] Runtime verifier includes all eleven Alex PNGs and three GLBs.
- [x] Character-manifest and app-shell tests cover Alex selection, URLs, placement, wheel ownership, and stats.
- [x] Deterministic GLB rebuilds match approved bytes.
- [x] Offline ten-state cockpit review completed.
- [x] Branding and Git LFS checks pass.
- [x] Install dependencies with `npm ci` from the lockfile.
- [x] Run `npm run validate` successfully.
- [x] Record test count, coverage, build output, and exact checkpoint SHA.
- [x] No validation defect required reopening approved art or geometry.
- [x] Obtain explicit publication approval.

### Publication and CI

- [x] Publish the validated file tree to `feature/alex-neon-vector-local` through the connected GitHub integration.
- [x] Open PR #92 with the Slice 3 checklist linked.
- [x] Confirm PR CI run `33989589113` passes typecheck, lint, tests, build, branding, runtime assets, and LFS checks.
- [x] Merge only after CI passes and publication approval is recorded; merge `617312394decfcb95af4f8fee6431ee9d339201b`.
- [x] Confirm post-merge `main` run `33989653688` passes.
- [x] Confirm Pages deployment originates from the merged runtime commit and exposes `alex-runtime-20260905-1`.

### Desktop and mobile live acceptance

- [x] Character Select: Alex portrait, name, descriptor, stats, and The Neon Vector display correctly.
- [x] Chase neutral: Alex is seated, correctly oriented, and the kart nose leads.
- [x] Chase steer-left and steer-right: torso turns in the commanded direction; only the intended hand is visible.
- [x] Chase hit and victory: approved frames load without clipping or fallback.
- [x] Rear/front neutral: front frame appears when the rear-view camera faces the kart.
- [x] Rear/front steer-left and steer-right: matching front action frames preserve input direction.
- [x] Rear/front hit and victory: matching front action frames load and restore correctly.
- [x] Steering control: exactly one modeled wheel is visible; no sprite wheel appears.
- [x] Geometry: hood motif is attached, steering area is clean, and no pale/render-white artifacts appear.
- [x] Rear three-quarter/profile: both cockpit-to-thruster conduits are visible and attached.
- [x] Desktop matrix passes.
- [x] Mobile matrix passes.

### Closeout

- [x] Record deployed commit, workflow run, Pages URL, asset revision, and live-test results in `docs/IMPLEMENTATION-STATUS.md`.
- [x] Record every reported defect and its approval state separately; no accepted artwork was silently altered.
- [x] Mark Alex `LIVE ACCEPTED / CLOSED` after all required desktop/mobile checks pass.

## Final state

Alex / The Neon Vector is **LIVE ACCEPTED / CLOSED**. The complete Slice 3 exit checklist passes against deployed acceptance checkpoint `daf1e3127478981e40cca9533300f8617f61004d`. Slice 3 is **COMPLETE / LIVE ACCEPTED**. Slice 5 remains unauthorized pending Manny's explicit direction.
