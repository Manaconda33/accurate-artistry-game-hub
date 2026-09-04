# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

The project roadmap remains at Slice 3. Items remain Slice 5 work and are not authorized. The previously approved Circuit Alpha environment/camera pass remains **LIVE ACCEPTED / CLOSED**. Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

**Dragon Queen / The Sovereign Wyrm is LIVE ACCEPTED / CLOSED.** Manny approved the deployed rear-view correction on 2026-09-04 after retesting neutral, steering-left, steering-right, hit, and victory camera-facing states. The final Dragon Queen acceptance defect is closed.

## Dragon Queen publication, correction, and final acceptance

Manny approved Dragon Queen's character lock, definitive visual reference, transformation rights, The Sovereign Wyrm design/name, AA-06 Grip Specialist mapping, portrait Candidate 2, all ten driver states, and Sovereign Wyrm geometry Candidate 2 before publication.

Initial publication completed through:

- Feature branch: `feature/dragon-queen-intake`
- Original completed local/publication checkpoint: `3b7f694e5afcbc668c1eada7e133e61f98adc899`
- Reconciliation checkpoint preserving current-main rollback authority: `4de46328f085e8a279c81f6330e2b30b6f7b7751`
- Pull request: **#89 — Integrate Dragon Queen and The Sovereign Wyrm**
- PR CI run: **33867452643** — passed
- Merge commit: `aef3d92be1ee50d7c4bb6313886b56f8b6478ffe`
- Main CI / Pages run: **33868111838** — validation and deployment passed
- Pages artifact: **9934780648**
- Pages artifact digest: `sha256:3ad70be1f0a5094b05e0cb1a61c5dcb4001d40c89ed34c4cbde02237d2472382`
- Runtime asset revision: `dragon-queen-runtime-20260904-1`

Live playtest passed every item except camera-facing foreclaw-to-steering-control placement. The approved correction retained chase-facing placement at `[0, 0.95, -0.12]`, lowered neutral / steer-left / hit / victory camera-facing placement to `[0, 0.84, -0.12]`, and lowered only front-steer-right to `[0, 0.80, -0.12]` because that approved raster carries its foreclaws slightly higher.

Correction publication completed through:

- Branch: `fix/dragon-queen-rear-view`
- Correction checkpoint: `7426dbfe83205f3a2a1ecac7e4d0c53c20359dd7`
- Pull request: **#90 — Correct Dragon Queen rear-view placement**
- PR CI run: **33883709850** — passed Git LFS verification, typecheck, lint, tests, and production build
- Merge commit: `15cab462d8eb574785427c026c9b199105c68074`
- Main CI / Pages run: **33883816293** — validation passed and deployment passed
- Pages artifact: **9940994630**
- Pages artifact digest: `sha256:945d0565257008fa62b834cf90ee2a6e00ccc706e6e2f798ed93b321cbe50de6`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`

The correction changes no Dragon Queen raster bytes, kart geometry, camera geometry, kart physics, AI behavior, track topology, roster statistics, or competitive-balance authority. `dragon-queen-runtime-20260904-1` remains the controlled asset revision.

## Dragon Queen active production state

Dragon Queen is the active production identity for **AA-06 Grip Specialist**:

- Speed 6
- Acceleration 6
- Weight 5
- Handling 7
- Mini-Turbo 5
- Traction 7
- Kart: **The Sovereign Wyrm**
- Kart orientation: `NEGATIVE_Z_KART_VISUAL_YAW`
- Chase-facing driver position: `[0, 0.95, -0.12]`
- Camera-facing neutral / steer-left / hit / victory position: `[0, 0.84, -0.12]`
- Camera-facing steer-right position: `[0, 0.80, -0.12]`

The Sovereign Wyrm production geometry is locked at:

- LOD0: 12,164 triangles — SHA-256 `57b3f4b248ed96cd19b0c2b233aec4462fde73b102ad9acde8941550bf69e305`
- LOD1: 7,268 triangles — SHA-256 `31bdd684fb764fdb4d6e04726971e0bf3f34ee4f36aefbf652fcdf3b133053c3`
- LOD2: 3,620 triangles — SHA-256 `124ec43e1ada192d67a3d4fe6bb6c3ec1cdd3f9df6b6c22b1af05b25762197de`

All ten driver states are active: rear, front, steer-left, steer-right, hit, victory, front-steer-left, front-steer-right, front-hit, and front-victory. Every approved frame keeps both wings visible, contains exactly one long tail, and contains no baked kart or steering-control geometry. The Sovereign Wyrm supplies the single modeled steering control.

Cleo / The Gilded Stitch remains archived and inactive. Her former AA-06 package is preserved byte-for-byte at `public/assets/archive/characters/cleo-aa-06/`; Dragon Queen does not load any Cleo archive asset.

## Dragon Queen validation and acceptance evidence

Local correction validation passed:

- strict TypeScript typecheck;
- ESLint with zero warnings;
- 18 Vitest files / 92 tests;
- 89.71% statement coverage;
- 33 materialized runtime GLBs;
- 94 decoded runtime PNGs;
- brand guard;
- production Vite build;
- `git lfs fsck`.

The deterministic five-state front-camera review matched across two renders at SHA-256 `1375abc4e30eaecadb1409030e0fea3e6ca3dd793ad8916227e24925a94006b2`. Focused placement tests pin the shared front mount and state-specific steer-right override and verify override precedence.

PR #90 and the post-merge `main` run independently repeated the repository CI gate. The GitHub Pages artifact is tied to merge `15cab462...`, and the deployed artifact contains the corrected `[0, 0.84, -0.12]` shared camera-facing placement plus `[0, 0.80, -0.12]` front-steer-right override.

### Final product-owner live acceptance — PASSED

Manny approved the deployed Dragon Queen correction on 2026-09-04 after the focused rear-view retest. Final accepted states:

- rear-view neutral — PASS
- rear-view steer-left — PASS
- rear-view steer-right — PASS
- rear-view hit — PASS
- rear-view victory — PASS
- modeled steering control placement relative to foreclaws — PASS

The prior Dragon Queen rear-view placement defect is closed. No Dragon Queen acceptance action remains open.

## Balance rollback — final closeout

The Circuit Alpha rebalance experiment remains **ABANDONED / ROLLED BACK / CLOSED**. The accepted gameplay authority remains pre-balance checkpoint `a706f01f43f07d9b31d05ce38e3e4b67c396894c` as restored by PR #88.

- Rollback PR: **#88 — Restore pre-balance gameplay**
- Rollback merge: `f8eb2dca1e32fe803b436793edae59b0b01b55ff`
- PR CI run: **33822797898** — passed
- Main CI / Pages run: **33822922732** — validation and deployment passed
- Candidate F PR #86 remains historical analysis only.
- Candidate G PR #87 was closed without merge and is abandoned.
- Further competitive-balance work remains deferred until Manny explicitly reopens it.

Dragon Queen publication and correction did not reopen or alter this balance decision.

## Circuit Alpha environment-art / camera checkpoint

The bounded Circuit Alpha environment/camera polish remains **LIVE ACCEPTED / CLOSED**.

Accepted final camera / finish values remain:

- chase distance: 5.6 m
- chase height: 3.15 m
- rear-view distance: 5.3 m
- rear-view height: 3.05 m
- look target height: 1.15 m
- PerspectiveCamera FOV: 62°
- crane duration: 2.85 s
- visible start/finish crossing: 22 m from the original checkpoint-0/grid origin

The protected race contract remains unchanged: 384 canonical track samples, course topology, checkpoints 1–11, starting-grid positions, surface classification, ramp behavior, kart physics, AI navigation, three-lap requirement, countdown timing, and item scope.

## Active production roster

- Lavi / Potato — AA-02
- Lula / The Verdant Hart — AA-03
- Keeg / The Mycelial Majesty — AA-04
- Kraken / The Abyssal Drifter — AA-05
- Dragon Queen / The Sovereign Wyrm — AA-06
- McFleurdel / The Fleur de Nuit — AA-07
- Toph / The Grave Shift — AA-08
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- Accu / Pink Precision — AA-11
- Jennifer / The Hearthwarden — AA-12

Cleo / The Gilded Stitch remains archived and inactive. **AA-01 is the only remaining governed placeholder.**

## Known defects / unresolved issues

- The existing production-build large-chunk warning remains known and non-blocking.
- No Dragon Queen code, asset, orientation, placement, or gameplay defect is open.
- No balance candidate is active.

## Deferred work

- AA-01 remains unfilled.
- Items remain Slice 5 work and are not authorized by this checkpoint.
- Further competitive-balance work remains deferred until explicitly reopened.
- External PBR texture sets, HDR environment, baked AO assets, and other larger presentation additions remain outside the Dragon Queen checkpoint.

## Next recommended action

Remain at **Slice 3**. Dragon Queen requires no further work. The next bounded product action is to continue approved Slice 3 avatar intake for the remaining AA-01 placeholder, or another explicitly approved Slice 3 task.

Do not advance to Slice 5, begin new material balance work, or alter protected gameplay scope without Manny's explicit approval.

## Approval state

**Dragon Queen / The Sovereign Wyrm: LIVE ACCEPTED / CLOSED.**

**Balance experiment: ABANDONED / ROLLED BACK / CLOSED.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

**Latest verified Dragon Queen runtime/deployment commit: `15cab462d8eb574785427c026c9b199105c68074`.**

The project roadmap remains at Slice 3.
