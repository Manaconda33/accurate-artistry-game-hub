# Cleo production asset brief

## Package identity

- Character: Cleo
- Historical runtime ID: `aa-06`
- Historical balance profile: AA-06 Grip Specialist
- Kart: The Gilded Stitch
- Package status: **archived / inactive as of 2026-08-26; complete approved package retained**
- Previous live status: accepted by Manny on 2026-08-21

Cleo is no longer part of the active production manifest. This brief remains the durable technical record for her approved package so it can be restored later without reconstructing design, asset, placement, or LFS details.

## Canonical character lock

Use the approved racing reference and approved runtime art as Cleo's definitive likeness. Preserve her green eyes, tortoiseshell glasses, gold drop earrings, brown braided high bun, navy floral blouse, and tailored navy trousers. Her expression is composed in neutral states, startled in the hit state, and warmly confident in victory.

Driver art and kart art remain separate runtime layers. Driver PNGs must not contain a steering wheel, cockpit wall, kart body, or wheel geometry.

## Runtime PNG contract

| Path                                                                 | Size      | Use                                 |
| -------------------------------------------------------------------- | --------- | ----------------------------------- |
| `public/assets/archive/characters/cleo-aa-06/portrait.png`           | 256 x 256 | Archived Character Select portrait  |
| `public/assets/archive/characters/cleo-aa-06/driver/front.png`       | 512 x 512 | Camera facing the front of the kart |
| `public/assets/archive/characters/cleo-aa-06/driver/rear.png`        | 512 x 512 | Neutral chase-camera state          |
| `public/assets/archive/characters/cleo-aa-06/driver/steer-left.png`  | 512 x 512 | Chase-camera left steering          |
| `public/assets/archive/characters/cleo-aa-06/driver/steer-right.png` | 512 x 512 | Chase-camera right steering         |
| `public/assets/archive/characters/cleo-aa-06/driver/hit.png`         | 512 x 512 | Chase-camera impact reaction        |
| `public/assets/archive/characters/cleo-aa-06/driver/victory.png`     | 512 x 512 | Chase-camera victory turn           |

Every file remains sRGB RGBA with non-opaque alpha and transparent corner pixels. Runtime art remains in normal Git under ADR-012. High-resolution masters do not belong at these paths.

These retained files are archive material, not active runtime requirements while Cleo is retired.

## Driver-state behavior

If Cleo is restored:

- Rear is the visible fallback if another frame fails.
- Steer-left and steer-right preserve the same seated footprint as rear while shifting Cleo's shoulders and hands toward the turn.
- Hit takes precedence over steering and shows Cleo recoiling while her lower body remains seated forward.
- Victory keeps Cleo's lower body seated toward the kart while she looks back and celebrates toward the chase camera.
- Front is a separately approved view and must not be inferred by mirroring a rear frame.

## Definitive kart direction

The supplied sewing-machine racing sheet is definitive. Preserve:

- an immediately readable vintage sewing-machine silhouette
- deep navy bodywork with ornate gold floral scrollwork
- warm wooden spool-like wheels
- visible sewing hardware, including a needle-like steering-column motif
- a low rectangular base and clear seated cockpit
- craftsmanship and precision rather than improvised junkyard construction

The approved production model declares `extras.forward: "-Z"` and historically used the shared `NEGATIVE_Z_KART_VISUAL_YAW` runtime transform. The sewing-machine head and control assembly belong ahead of Cleo; spool and drive details must read consistently in chase and front-camera checks.

## Preserved verification evidence

- Portrait: 256 x 256, sRGB RGBA, transparent
- Six driver frames: 512 x 512, sRGB RGBA, transparent
- Every runtime PNG has alpha spanning fully transparent to fully opaque and a fully transparent corner pixel
- Approved art contains no steering wheel or kart geometry
- Runtime PNGs resolve to normal Git rather than Git LFS
- Manny approved LOD0 Candidate 3 on 2026-08-21 after direct interactive GLB review. Candidate 3 uses a rear-biased cockpit, one connected steering wheel, a front sewing-machine pillar and overhanging arm, an exposed needle/presser-foot assembly, non-clipping wooden spool wheels, and continuous attached gold side inlays.
- Retained paths: `public/assets/archive/characters/cleo-aa-06/{kart,kart-lod1,kart-lod2}.glb`.
- Triangle counts: LOD0 12,812; LOD1 10,396; LOD2 4,780.
- All three files use four opaque materials, the exact thirteen-node hierarchy, meters, and `extras.forward: "-Z"`.
- SHA-256/LFS object IDs: LOD0 `453ebc42da5745f7f5251323cd7a38a79add6538ee39dc9e512570c1c9905150`; LOD1 `a9013591726b3bbb43b102d3707fe9da24f2e1e8de24c929bbc6405e28357002`; LOD2 `3578b62d3c9fa332adb2b1ae7addb1d2b56201c7c8491a1075e847ff18caa79e`.
- Historical runtime driver placement: `[0, 0.9, -0.72]` in the kart group. Runtime kart-forward is positive Z, so the negative-Z offset moves Cleo rearward into The Gilded Stitch's approved cockpit and leaves its steering wheel ahead of her.
- Previous controlled revision: `cleo-runtime-20260821-1`.
- Previous live acceptance: selection, production kart loading, race-forward orientation, front/rear/steering/hit/victory states, unique AI appearance, and corrected cockpit placement passed on 2026-08-21.

## Archive gate

As of 2026-08-26:

- Cleo is excluded from `characterManifest`.
- Dragon Queen owns the active AA-06 slot locally; Cleo remains inactive.
- Cleo cannot be sampled into the AI grid.
- Cleo's archived GLBs are outside the active runtime gate.
- The PNGs, three LFS-backed GLBs, builder, hashes, mount, and prior evidence remain untouched for restoration.

Restoration requires Manny's explicit approval, a current balance-profile decision, reactivation in the manifest, fresh LFS/materialization checks, full repository validation, deployment, and live manual verification. See `docs/CHARACTER-ARCHIVE.md`.
