# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 1.6**.

Current `main` before this bounded cleanup: `962ccf994fb488e8da64068d5b4a739a3c090bcb` — Cleo archived from active production through PR #31. Main CI run `32996219644` passed validation and GitHub Pages deployment.

The prior detailed implementation-status snapshot is preserved verbatim at `docs/history/IMPLEMENTATION-STATUS-through-2026-08-22.md`.

## Active production roster state

Production character packages currently represented in `characterManifest`:

- Lavi / Potato — AA-02
- Kraken / The Abyssal Drifter — AA-05
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- Accu / Pink Precision — AA-11

Cleo / The Gilded Stitch is archived and inactive. AA-06 is a governed placeholder and available for future approved assignment. The twelve-slot Character Select architecture remains intact.

## Cleo archive status — complete

PR #31 merged Cleo's reversible production retirement on 2026-08-26.

- Cleo is absent from active `characterManifest` and cannot be selected or sampled into the AI grid.
- AA-06 renders as a generic placeholder with no Cleo or Gilded Stitch production copy.
- Cleo's complete approved asset package, deterministic builder, GLB object IDs, runtime revision, technical records, and historical acceptance evidence remain preserved under the character archive contract.
- Main CI run `32996219644` passed LFS verification, typecheck, lint, tests, production build, and Pages deployment for merge commit `962ccf994fb488e8da64068d5b4a739a3c090bcb`.
- Manny manually confirmed the live deployment on 2026-08-26: **Cleo is gone from the live game.**
- Status: **LIVE ACCEPTED — CLEO ARCHIVE COMPLETE.**

## Krios production closure — 2026-08-26

A continuity review following the Cleo archive confirmed that Krios's gameplay/asset integration had succeeded before a prior usage-limit interruption, but the final repository continuity work was incomplete.

Verified existing implementation truth:

- Krios is active in `characterManifest` as production AA-10 Straight-Line Heavy.
- The approved portrait and all six driver states are wired to controlled Krios runtime URLs.
- The Hornbreaker production kart is wired to the manifest with the shared negative-Z visual orientation contract.
- Automated manifest coverage already verifies Krios identity, kart path, all six driver-state URLs, orientation yaw, and 10 / 4 / 9 / 3 / 4 / 6 statistics.
- PR #30 merged the complete Hornbreaker production package to `main` at commit `ddbb2dea9e7f5e558cb8d5e76501b99219416f65`.
- Main CI run `32591411527` passed for that merge.
- Manny confirmed on 2026-08-26 that **Krios is in the live game and all assets load as intended.**

Continuity gap found:

- `tools/verify-runtime-assets.mjs` still contained the pre-Krios active-GLB list and therefore did not require the three AA-10 Hornbreaker GLBs during future production builds.
- `docs/avatars/KRIOS.md` and `docs/assets/KRIOS-ASSET-BRIEF.md` still described PR #30/live verification as pending even though the merge, deployment, and live behavior had already succeeded.
- `docs/TESTING.md` lacked a Krios-specific production regression matrix.

Bounded closure on branch `agent/close-krios-production-records`:

- Added `public/assets/characters/aa-10/kart.glb`, `kart-lod1.glb`, and `kart-lod2.glb` to the active runtime signature/orientation gate.
- Updated Krios's character record to **LIVE ACCEPTED — KRIOS PRODUCTION INTEGRATION COMPLETE**.
- Updated the Krios asset brief to record the merged/deployed/live-accepted state and make all three AA-10 GLBs mandatory build-gate inputs.
- Added a Krios / Hornbreaker manual regression matrix and generalized the testing contract: every active production character with GLB LODs must be represented in `tools/verify-runtime-assets.mjs`.

This closure changes no Krios artwork, model geometry, stats, physics, orientation, gameplay behavior, or live runtime URLs. It repairs verification and repository continuity only.

## Validation gate for Krios closure

Before merge, the branch must pass:

1. Git LFS materialized checkout and `git lfs fsck`.
2. Runtime signature/orientation verification for all active production GLBs, now including all three AA-10 Hornbreaker LODs.
3. Strict TypeScript typecheck.
4. ESLint with zero warnings.
5. Full Vitest CI suite.
6. Vite production build.
7. GitHub Actions success on the final PR head.

No new manual gameplay acceptance is required for this documentation/gate-only closure because Manny has already confirmed the current live Krios package loads as intended. A post-merge Pages deployment should still complete successfully.

## Known defects / deferred work

- Slice 4 AI competitiveness remains intentionally weak; previously accepted at the current vertical-slice stage.
- Continue Slice 3 one-character-at-a-time intake and approval for remaining roster slots.
- Complete any still-unrecorded desktop/mobile acceptance checks for other integrated production characters as required by `docs/TESTING.md`.
- Items and AI item use remain Slice 5.
- Final HUD/audio/post-processing/optimization remain Slice 6.

## Next recommended action

Merge the Krios continuity closure after CI passes, confirm the main Pages deployment succeeds, then continue with the next approved Slice 3 character package. Do not begin Slice 5 or reorder the PRD roadmap without Manny approval.

## Approval gate

Krios's original package is already approved and live accepted. This bounded cleanup requires no new product decision; it closes missed repository verification and documentation work caused by the prior interrupted session.