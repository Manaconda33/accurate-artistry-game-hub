# Alex / The Neon Vector — PRD traceability and release checklist

This is a review checkpoint for AA-01 local integration. It translates the approved Alex decisions and PRD delivery contract into observable evidence. It does not authorize publication, deployment, or live acceptance.

## PRD-to-runtime traceability

| Approved requirement | Runtime implementation | Automated/local evidence | Remaining product-owner gate |
| --- | --- | --- | --- |
| Alex is an approved adult woman, she/her, warm clever competitor | `characterManifest` entry `aa-01`; `docs/avatars/ALEX.md` | Manifest test checks name, descriptor, stats, and production state | Confirm identity and presentation in deployed Character Select and race |
| AA-01 Feather Sprinter mapping | Stats 6 / 9 / 2 / 8 / 7 / 4 in `src/characters/manifest.ts` | `tests/character-manifest.test.ts`; manifest total validation | Confirm displayed stats and driving feel in live build |
| Portrait Option A approved | `public/assets/characters/aa-01/portrait.png` | Runtime verifier checks 256 x 256 RGBA, alpha margins, and decodability | Confirm portrait loads without fallback on desktop/mobile |
| Ten approved driver states | Ten files under `public/assets/characters/aa-01/driver/` | Runtime verifier checks dimensions, RGBA data, transparent corners, and complete decoding | Confirm every state loads and transitions correctly |
| Chase steering uses moderate turn-directed torso rotation and one visible hand | `steer-left.png` and `steer-right.png` | Offline ten-state cockpit sheet; approved package hashes | Confirm both directions in chase camera and restore correctly after rear view |
| Driver art is character-only and wheel-free | Raster package contains no kart/control geometry | Offline review plus single-wheel ownership check | Confirm no duplicate wheel appears in any deployed state |
| Kart name is The Neon Vector | `kartName` and asset metadata | Manifest test and branding/asset checks | Confirm name in Character Select and race HUD where shown |
| Candidate 3 geometry is approved | `kart.glb`, `kart-lod1.glb`, `kart-lod2.glb` | Deterministic rebuilds match approved SHA-256 values; GLB verifier checks signature and `extras.forward` | Confirm visual orientation, attached geometry, and readable conduits in deployed build |
| Production kart forward axis is negative Z | `NEGATIVE_Z_KART_VISUAL_YAW` and GLB `extras.forward: "-Z"` | Runtime verifier and manifest test | Confirm nose/exhaust direction in chase and rear views |
| One modeled steering wheel belongs to the kart | Candidate 3 `SteeringWheel` node; Alex sprite flag remains unset | Geometry validation and offline cockpit review | Confirm wheel remains singular and readable in all ten live states |
| Camera-facing placement preserves hands/wheel relationship | Chase `[0, 0.92, -0.12]`; front `[0, 0.84, -0.12]` | Offline attachment review and manifest placement test | Confirm no high/low hand placement on desktop/mobile |
| Exposed cockpit-to-thruster conduits remain structurally visible | Candidate 3 rear conduit geometry retained in all LODs | Approved geometry preview and offline review evidence | Confirm conduits are visible and not buried/floating in deployed rear three-quarter/profile views |
| Controlled cache revision protects changed asset paths | `alex-runtime-20260905-1` query on manifest URLs | Manifest test checks revisioned URLs | Confirm deployed responses expose the controlled revision |

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
- [ ] Reconcile any validation defect without reopening approved art or geometry.
- [x] Obtain explicit publication approval.

### Publication and CI

- [ ] Push the exact validated feature branch.
- [ ] Open the pull request with this checklist linked.
- [ ] Confirm PR CI passes typecheck, lint, tests, build, branding, runtime assets, and LFS checks.
- [ ] Merge only after CI passes and publication approval is recorded.
- [ ] Confirm the post-merge `main` workflow passes.
- [ ] Confirm the Pages deployment originates from the merged commit and exposes the expected Alex revision.

### Desktop and mobile live acceptance

- [ ] Character Select: Alex portrait, name, descriptor, stats, and The Neon Vector display correctly.
- [ ] Chase neutral: Alex is seated, correctly oriented, and the kart nose leads.
- [ ] Chase steer-left and steer-right: torso turns in the commanded direction; only the intended hand is visible.
- [ ] Chase hit and victory: approved frames load without clipping or fallback.
- [ ] Rear/front neutral: front frame appears when the rear-view camera faces the kart.
- [ ] Rear/front steer-left and steer-right: matching front action frames preserve input direction.
- [ ] Rear/front hit and victory: matching front action frames load and restore correctly.
- [ ] Steering control: exactly one modeled wheel is visible; no sprite wheel appears.
- [ ] Geometry: hood motif is attached, steering area is clean, and no pale/render-white artifacts appear.
- [ ] Rear three-quarter/profile: both cockpit-to-thruster conduits are visible and attached.
- [ ] Desktop matrix passes.
- [ ] Mobile matrix passes.

### Closeout

- [ ] Record deployed commit, workflow run, Pages URL, asset revision, and live-test results in `docs/IMPLEMENTATION-STATUS.md`.
- [ ] Record any defect and its approval state separately; do not silently alter accepted artwork.
- [ ] Mark Alex `LIVE ACCEPTED / CLOSED` only after all required desktop/mobile checks pass.

## Review boundary

The next approval requested from Manny is approval of this traceability/checklist structure. After approval, the next work item is dependency-backed local validation, not publication. Publication remains a separate explicit gate.
