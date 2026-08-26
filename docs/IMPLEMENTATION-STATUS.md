# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 1.6**.

Latest verified `main` checkpoint before this work: `ddbb2dea9e7f5e558cb8d5e76501b99219416f65` — Krios / The Hornbreaker production package merged through PR #30. GitHub Actions run `32591411527` passed on that commit.

The prior detailed implementation-status snapshot is preserved verbatim at `docs/history/IMPLEMENTATION-STATUS-through-2026-08-22.md` so historical acceptance and troubleshooting evidence remain durable without obscuring the current state.

## Active production roster state

Production character packages currently represented in `characterManifest`:

- Lavi / Potato — AA-02
- Kraken / The Abyssal Drifter — AA-05
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- Accu / Pink Precision — AA-11

The remaining AA slots are governed placeholders until a character package is approved and activated. The twelve-slot Character Select architecture remains intact.

## Cleo production retirement and archive — 2026-08-26

Manny explicitly directed that Cleo be removed from production while preserving her complete character package for possible future restoration.

Implemented on branch `agent/archive-cleo-production`:

- Cleo is no longer included in active `characterManifest`.
- AA-06 is restored to a generic governed placeholder, so Cleo is not selectable by the player and cannot be sampled into the seven-racer AI grid.
- Character Select no longer hard-codes AA-06 to The Gilded Stitch; the placeholder shows `AA 06`, `Roster placeholder`, and `Fallback prototype` with no Cleo-specific production copy.
- The complete former Cleo production definition remains exported as `archivedCleo`, retaining the approved asset paths, controlled revision, kart orientation, driver-state mapping, AA-06 historical statistics, and character-specific driver mount `[0, 0.9, -0.72]`.
- `public/assets/characters/aa-06/` is intentionally preserved. No Cleo portrait, driver frame, GLB, or LFS object was deleted or moved.
- `tools/assets/build_cleo_gilded_stitch.py` remains the deterministic source for The Gilded Stitch.
- The active runtime-asset signature gate no longer requires Cleo's three AA-06 GLBs, so the production build is not operationally dependent on the archived package.
- AA-06 is marked `Available` again in `docs/ROSTER-MAPPING.md`. Cleo's former mapping is retained as historical archive information rather than a current reservation.
- `docs/CHARACTER-ARCHIVE.md` now indexes the full package, prior GLB object IDs, acceptance history, and explicit restoration gate.
- `docs/avatars/CLEO.md` and `docs/assets/CLEO-ASSET-BRIEF.md` now identify the package as archived/inactive while preserving all prior approvals and technical details.

### Preserved Cleo package

- Portrait: `public/assets/characters/aa-06/portrait.png`
- Driver frames: front, rear, steer-left, steer-right, hit, victory
- GLBs: `kart.glb`, `kart-lod1.glb`, `kart-lod2.glb`
- Deterministic builder: `tools/assets/build_cleo_gilded_stitch.py`
- Historical production revision: `cleo-runtime-20260821-1`
- Historical GLB object IDs:
  - LOD0 `453ebc42da5745f7f5251323cd7a38a79add6538ee39dc9e512570c1c9905150`
  - LOD1 `a9013591726b3bbb43b102d3707fe9da24f2e1e8de24c929bbc6405e28357002`
  - LOD2 `3578b62d3c9fa332adb2b1ae7addb1d2b56201c7c8491a1075e847ff18caa79e`

### Restoration rule

Cleo may return only after explicit Manny approval. Restoration requires a current balance-profile decision, active-manifest reactivation, fresh LFS/materialization checks, repository validation, deployment, and live visual confirmation. Historical 2026-08-21 acceptance is retained as evidence but is not sufficient by itself for a future reactivation.

## Validation status for Cleo retirement checkpoint

Automated contract coverage proves:

- AA-06 is an active placeholder with no Cleo portrait, kart, or driver assets;
- no active manifest identity is named Cleo;
- the archived Cleo definition still resolves the preserved package and cockpit mount;
- Character Select renders AA-06 as a placeholder and does not expose `Cleo` or `The Gilded Stitch` production copy.

PR #31 validation history:

- Initial CI run `32995795985` correctly failed at the test stage. LFS verification, typecheck, and lint had already passed. The failing UI regression exposed a remaining hard-coded AA-06 → The Gilded Stitch label in Character Select.
- That production reference was removed and the app-shell test was updated to require `AA 06`, `Roster placeholder`, and `Fallback prototype`, and to reject visible `Cleo` / `The Gilded Stitch` copy for AA-06.
- Corrected CI run `32996003591` on head `ad060371c5da8de1f1cfa0c992d41fe6850494e2` passed Git LFS runtime verification, strict TypeScript typecheck, ESLint, the Vitest CI suite, and the production build.
- The final documentation-only head after recording this evidence must also receive a green PR check before merge.

After merge, the `main` deployment must be checked to confirm AA-06 presents as a placeholder and Cleo does not appear in Character Select or AI selection. Product-owner manual confirmation remains the final rendered-behavior gate.

## Known defects / discrepancies

- Slice 4 AI competitiveness remains intentionally weak; this was previously accepted for the current vertical-slice stage.
- The historical status file contained stale statements about Krios being only 2D-complete. Repository `main` supersedes those statements: PR #30 activated the approved Krios production package and its CI passed.
- The current `tools/verify-runtime-assets.mjs` list predates Krios activation and does not yet include the AA-10 Hornbreaker GLBs. This is a pre-existing production-gate discrepancy discovered during Cleo retirement review; it is not caused by the archive change and should be corrected in a bounded follow-up before declaring the overall character-production pipeline complete.

## Deferred work

- Continue Slice 3 one-character-at-a-time intake and approval for the remaining active roster slots.
- Complete any still-unrecorded desktop/mobile acceptance checks for already integrated production characters as required by `docs/TESTING.md`.
- Items and AI item use remain Slice 5.
- Final HUD/audio/post-processing/optimization remain Slice 6.

## Next recommended action

Merge PR #31 after its final head CI passes, then validate the deployed Character Select and race AI behavior. Once Manny confirms the live result, continue the next approved Slice 3 character package. Do not begin Slice 5 or otherwise reorder the PRD roadmap without Manny approval.

## Approval gate

Cleo's retirement/archive direction is explicitly approved by Manny on 2026-08-26. The code change may merge after repository CI passes. The deployed rendered result remains subject to Manny's manual confirmation.