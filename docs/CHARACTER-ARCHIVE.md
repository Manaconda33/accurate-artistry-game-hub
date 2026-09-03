# Character Archive

This archive preserves retired Manaconda's Minigame Mayhem character packages that are intentionally excluded from the active production roster but may be restored later with product-owner approval.

Archived character assets are not deleted, repurposed, or silently reassigned. Their historical approvals, deterministic builders, runtime derivatives, LFS objects, integration notes, and acceptance evidence remain durable in the repository. An archived character must not appear in Character Select or the AI roster unless a future approved change explicitly restores that character to the active manifest.

## Cleo — archived 2026-08-26

- Historical runtime ID: `aa-06`
- Historical balance profile: AA-06 Grip Specialist — 6 / 6 / 5 / 7 / 5 / 7
- Kart: The Gilded Stitch
- Previous production revision: `cleo-runtime-20260821-1`
- Previous live status: accepted by Manny on 2026-08-21
- Archive status: retained, inactive, reversible

### Preserved records

- `docs/avatars/CLEO.md`
- `docs/assets/CLEO-ASSET-BRIEF.md`
- `tools/assets/build_cleo_gilded_stitch.py`
- Historical approval and implementation evidence in `docs/IMPLEMENTATION-STATUS.md`
- Historical product decision ADR-020 in `docs/DECISIONS.md`

### Preserved runtime package

The complete package remains at `public/assets/characters/aa-06/` so no approved binary or runtime art is destroyed:

- `portrait.png`
- `driver/front.png`
- `driver/rear.png`
- `driver/steer-left.png`
- `driver/steer-right.png`
- `driver/hit.png`
- `driver/victory.png`
- `kart.glb`
- `kart-lod1.glb`
- `kart-lod2.glb`

Approved The Gilded Stitch LFS object IDs remain:

- LOD0: `453ebc42da5745f7f5251323cd7a38a79add6538ee39dc9e512570c1c9905150`
- LOD1: `a9013591726b3bbb43b102d3707fe9da24f2e1e8de24c929bbc6405e28357002`
- LOD2: `3578b62d3c9fa332adb2b1ae7addb1d2b56201c7c8491a1075e847ff18caa79e`

The historical driver mount `[0, 0.9, -0.72]`, shared negative-Z kart visual orientation contract, and all approved art paths are also retained in the exported `archivedCleo` definition in `src/characters/manifest.ts`.

### Active-runtime behavior

Cleo is not included in `characterManifest`. The active AA-06 slot is a governed monogram placeholder, so:

- Cleo does not appear in Character Select.
- Cleo cannot be selected as the player.
- Cleo cannot be sampled into the seven-racer AI roster.
- No Cleo runtime assets are required to render the active AA-06 slot.
- The twelve-slot PRD scaffold remains intact.

AA-06 is available for a future approved character assignment. Cleo's former AA-06 association is historical archive information, not a current reservation.

### Restoration gate

Restoring Cleo requires explicit Manny approval. A restoration checkpoint must:

1. Confirm the desired balance profile and update `docs/ROSTER-MAPPING.md`.
2. Re-add Cleo's approved definition to the active `characterManifest`.
3. Run current runtime-asset and LFS materialization validation rather than relying only on 2026-08-21 evidence.
4. Run typecheck, lint, automated tests, and production build.
5. Deploy the checkpoint and manually verify selection, kart loading/orientation, all driver states, cockpit placement, and unique AI appearance.
6. Update `docs/DECISIONS.md`, `docs/IMPLEMENTATION-STATUS.md`, and this archive record.
