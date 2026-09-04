# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

The project roadmap remains at Slice 3. Items remain Slice 5 work and are not authorized. The previously approved Circuit Alpha environment/camera pass remains **LIVE ACCEPTED / CLOSED**. Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

Dragon Queen / The Sovereign Wyrm is now **PUBLISHED / DEPLOYED / LIVE ACCEPTANCE OPEN**. Product-owner desktop and mobile confirmation is the remaining gate before this character checkpoint can be called live accepted.

## Dragon Queen publication and deployment

Manny approved Dragon Queen's character lock, definitive visual reference, transformation rights, The Sovereign Wyrm design/name, AA-06 Grip Specialist mapping, portrait Candidate 2, all ten driver states, and Sovereign Wyrm geometry Candidate 2 before publication.

Publication was completed through:

- Feature branch: `feature/dragon-queen-intake`
- Original completed local/publication checkpoint: `3b7f694e5afcbc668c1eada7e133e61f98adc899`
- Reconciliation checkpoint preserving current-main rollback authority: `4de46328f085e8a279c81f6330e2b30b6f7b7751`
- Pull request: **#89 — Integrate Dragon Queen and The Sovereign Wyrm**
- PR CI run: **33867452643** — passed
- Merge commit: `aef3d92be1ee50d7c4bb6313886b56f8b6478ffe`
- Main CI / Pages run: **33868111838** — validation passed and deployment passed
- GitHub Pages artifact: **9934780648**
- Pages artifact digest: `sha256:3ad70be1f0a5094b05e0cb1a61c5dcb4001d40c89ed34c4cbde02237d2472382`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Runtime asset revision: `dragon-queen-runtime-20260904-1`

The branch originally diverged from accepted pre-balance checkpoint `a706f01f43f07d9b31d05ce38e3e4b67c396894c`. Before merge, current `main` was merged into the feature branch and the current rollback-closeout implementation-status record was explicitly retained. The resulting PR changed no kart physics, AI behavior, track topology, camera geometry, or competitive-balance tuning.

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
- Camera-facing driver position: `[0, 0.95, -0.12]`

The Sovereign Wyrm production geometry is locked at:

- LOD0: 12,164 triangles — SHA-256 `57b3f4b248ed96cd19b0c2b233aec4462fde73b102ad9acde8941550bf69e305`
- LOD1: 7,268 triangles — SHA-256 `31bdd684fb764fdb4d6e04726971e0bf3f34ee4f36aefbf652fcdf3b133053c3`
- LOD2: 3,620 triangles — SHA-256 `124ec43e1ada192d67a3d4fe6bb6c3ec1cdd3f9df6b6c22b1af05b25762197de`

All ten action states are active: rear, front, steer-left, steer-right, hit, victory, front-steer-left, front-steer-right, front-hit, and front-victory. Each approved frame keeps both wings visible, contains exactly one long tail, and contains no baked kart or steering-control geometry. The kart supplies the single modeled steering control.

Cleo / The Gilded Stitch remains archived and inactive. Her former AA-06 package is preserved byte-for-byte at `public/assets/archive/characters/cleo-aa-06/`; archive regression checks pin the approved portrait, six driver frames, and three Gilded Stitch GLBs to their recorded hashes. Dragon Queen does not load any Cleo archive asset.

## Dragon Queen validation evidence

Local pre-publication validation passed with:

- strict TypeScript typecheck;
- ESLint with zero warnings;
- 18 Vitest files / 91 tests;
- 89.7% statement coverage;
- 33 materialized runtime GLBs;
- 94 decoded runtime PNGs;
- production Vite build;
- brand guard;
- `git lfs fsck`.

The deterministic Dragon Queen cockpit review matched across two runs at SHA-256 `7ee269aec57cd1cc95aaa17d66aedeaf2ffe20ccee460f56e7e91c82d6a8f917`.

PR run **33867452643** repeated the repository CI gate on reconciled head `4de46328...` and passed Git LFS runtime verification, dependency installation, typecheck, lint, tests, and production build.

Main run **33868111838** repeated those validation stages on merge `aef3d92...`, successfully configured GitHub Pages, uploaded the Pages artifact, and completed the `github-pages` deployment job successfully.

The existing production-build large-chunk warning remains known and non-blocking.

## Dragon Queen live acceptance matrix — OPEN

Desktop and mobile product-owner acceptance must confirm the deployed release rather than source-only behavior.

Required checks:

- Character Select shows Dragon Queen's approved portrait, `Grip Specialist`, statistics 6 / 6 / 5 / 7 / 5 / 7, and The Sovereign Wyrm.
- `Race as Dragon Queen` loads The Sovereign Wyrm rather than a placeholder, Cleo, The Gilded Stitch, or the procedural fallback kart.
- The dragon shield is at the race-forward nose; the open tail channel remains behind Dragon Queen.
- Chase view correctly presents neutral rear, steer-left, steer-right, hit, and victory states.
- Rear/front-facing camera correctly presents neutral front, front-steer-left, front-steer-right, front-hit, and front-victory states.
- Every displayed state retains both wings and exactly one long tail without checkerboard, white matte, or baked kart/control geometry.
- Dragon Queen remains seated behind the cockpit edge with wings above bodywork and without unacceptable clipping or floating.
- The Sovereign Wyrm supplies one modeled steering control; in front view it sits between Dragon Queen's foreclaws without covering her face.
- Dragon Queen may appear at most once as an AI opponent when another character is selected; Cleo must not appear in the active player or AI roster.
- Desktop/fine-pointer play keeps touch controls hidden and keyboard controls functional.
- Mobile/coarse-pointer play shows the governed touch controls, maintains usable layout without horizontal clipping, and preserves acceptable frame pacing.

A successful deployment is not product-owner acceptance. Record Manny's desktop/mobile result before closing Dragon Queen.

## Balance rollback — final closeout

The Circuit Alpha rebalance experiment remains **ABANDONED / ROLLED BACK / CLOSED**. The accepted gameplay authority remains pre-balance checkpoint `a706f01f43f07d9b31d05ce38e3e4b67c396894c` as restored by PR #88.

- Rollback PR: **#88 — Restore pre-balance gameplay**
- Rollback merge: `f8eb2dca1e32fe803b436793edae59b0b01b55ff`
- PR CI run: **33822797898** — passed
- Main CI / Pages run: **33822922732** — validation and deployment passed
- Candidate F PR #86 remains historical analysis only.
- Candidate G PR #87 was closed without merge and is abandoned.
- Further competitive-balance work is deferred until Manny explicitly reopens it.

Dragon Queen publication did not reopen or alter this balance decision.

## Circuit Alpha environment-art / camera checkpoint

The bounded Circuit Alpha environment/camera polish remains **LIVE ACCEPTED / CLOSED** with no new acceptance action required.

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

- Dragon Queen desktop/mobile live product-owner acceptance is pending.
- The existing production-build large-chunk warning remains known and non-blocking.
- No Dragon Queen code or asset defect has been established by CI/deployment evidence.
- No balance candidate is active.

## Deferred work

- AA-01 remains unfilled.
- Items remain Slice 5 work and are not authorized by this checkpoint.
- Further competitive-balance work remains deferred until explicitly reopened.
- External PBR texture sets, HDR environment, baked AO assets, and other larger presentation additions remain outside this Dragon Queen checkpoint.

## Next recommended action

**Complete Dragon Queen live desktop/mobile product-owner acceptance against the deployed Pages release.**

Do not advance to Slice 5, Slice 6, reopen Candidate F/G tuning, or begin another material roadmap scope until the current Dragon Queen acceptance result is recorded or Manny explicitly changes direction.

## Approval state

**Dragon Queen / The Sovereign Wyrm: PUBLISHED / DEPLOYED / LIVE ACCEPTANCE OPEN.**

**Balance experiment: ABANDONED / ROLLED BACK / CLOSED.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

The project roadmap remains at Slice 3.
