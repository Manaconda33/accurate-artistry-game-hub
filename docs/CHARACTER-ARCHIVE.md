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

The complete package is preserved at `public/assets/archive/characters/cleo-aa-06/` so Dragon Queen can use the active AA-06 path without destroying Cleo's approved work:

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

The archive copy was verified byte-for-byte against Cleo's former active package on 2026-09-04. The portrait hash is `1f960402a447078e681f3f4b1b0ed5fcf8dcc1ca10f4a4deec077d758400b2cf`; driver hashes are retained in path order as front `70b6884751897e9f7ccba2fbeb5c37ed0b6c0631fea0fe1dd6788823a18d524e`, rear `af97bb7be383e6bd1f87eae944941e8c60d8fe987c36db53f75a16a635d582d9`, steer-left `7cde1f8bb0e1eec2f217efbcb9ec2592fe8c39c92487964d63615b07f3fc0d95`, steer-right `c6bae3e9e75f6ed28a71a309bcc44f45e7d470193293051850e82b1c1ffecd4a`, hit `ddbdac8788f5095f406eb0199b7324f1e78a073b74e13db948f62140d7562032`, and victory `53d7648dc4e44d150a43b5db7cd3e5ce8dfd4030c2a802f355fffc5675393d21`.

The historical driver mount `[0, 0.9, -0.72]`, shared negative-Z kart visual orientation contract, and all approved art paths are also retained in the exported `archivedCleo` definition in `src/characters/manifest.ts`.

### Active-runtime behavior

Cleo is not included in `characterManifest`. Dragon Queen now owns the active AA-06 slot locally, so:

- Cleo does not appear in Character Select.
- Cleo cannot be selected as the player.
- Cleo cannot be sampled into the seven-racer AI roster.
- No Cleo archive asset is loaded by Dragon Queen's active AA-06 definition.
- The twelve-slot PRD scaffold remains intact.

Dragon Queen's publication remains gated. Cleo's former AA-06 association is historical archive information, not a current reservation.

### Restoration gate

Restoring Cleo requires explicit Manny approval. A restoration checkpoint must:

1. Confirm the desired balance profile and update `docs/ROSTER-MAPPING.md`.
2. Re-add Cleo's approved definition to the active `characterManifest`.
3. Run current runtime-asset and LFS materialization validation rather than relying only on 2026-08-21 evidence.
4. Run typecheck, lint, automated tests, and production build.
5. Deploy the checkpoint and manually verify selection, kart loading/orientation, all driver states, cockpit placement, and unique AI appearance.
6. Update `docs/DECISIONS.md`, `docs/IMPLEMENTATION-STATUS.md`, and this archive record.
