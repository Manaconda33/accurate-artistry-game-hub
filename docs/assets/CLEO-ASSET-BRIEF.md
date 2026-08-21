# Cleo production asset brief

## Package identity

- Character: Cleo
- Runtime ID: `aa-06`
- Balance profile: AA-06 Grip Specialist
- Kart: The Gilded Stitch
- Package status: approved production package prepared; live verification pending

## Canonical character lock

Use the approved racing reference and approved runtime art as Cleo's definitive likeness. Preserve her green eyes, tortoiseshell glasses, gold drop earrings, brown braided high bun, navy floral blouse, and tailored navy trousers. Her expression is composed in neutral states, startled in the hit state, and warmly confident in victory.

Driver art and kart art remain separate runtime layers. Driver PNGs must not contain a steering wheel, cockpit wall, kart body, or wheel geometry.

## Runtime PNG contract

| Path                                                    | Size      | Use                                 |
| ------------------------------------------------------- | --------- | ----------------------------------- |
| `public/assets/characters/aa-06/portrait.png`           | 256 x 256 | Character Select portrait           |
| `public/assets/characters/aa-06/driver/front.png`       | 512 x 512 | Camera facing the front of the kart |
| `public/assets/characters/aa-06/driver/rear.png`        | 512 x 512 | Neutral chase-camera state          |
| `public/assets/characters/aa-06/driver/steer-left.png`  | 512 x 512 | Chase-camera left steering          |
| `public/assets/characters/aa-06/driver/steer-right.png` | 512 x 512 | Chase-camera right steering         |
| `public/assets/characters/aa-06/driver/hit.png`         | 512 x 512 | Chase-camera impact reaction        |
| `public/assets/characters/aa-06/driver/victory.png`     | 512 x 512 | Chase-camera victory turn           |

Every file must remain sRGB RGBA with non-opaque alpha and transparent corner pixels. Runtime art belongs in normal Git under ADR-012. High-resolution masters do not belong at these paths.

## Driver-state behavior

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

The production model must declare `extras.forward: "-Z"` and use the shared `NEGATIVE_Z_KART_VISUAL_YAW` runtime transform. The sewing-machine head and control assembly belong ahead of Cleo; spool and drive details must read consistently in chase and front-camera checks.

## Current verification

- Portrait: 256 x 256, sRGB RGBA, transparent
- Six driver frames: 512 x 512, sRGB RGBA, transparent
- Every runtime PNG has alpha spanning fully transparent to fully opaque and a fully transparent corner pixel
- Approved art contains no steering wheel or kart geometry
- Runtime PNGs resolve to normal Git rather than Git LFS
- Manny approved LOD0 Candidate 3 on 2026-08-21 after direct interactive GLB review. Candidate 3 uses a rear-biased cockpit, one connected steering wheel, a front sewing-machine pillar and overhanging arm, an exposed needle/presser-foot assembly, non-clipping wooden spool wheels, and continuous attached gold side inlays.
- Runtime paths: `public/assets/characters/aa-06/{kart,kart-lod1,kart-lod2}.glb`.
- Triangle counts: LOD0 12,812; LOD1 10,396; LOD2 4,780.
- All three files use four opaque materials, the exact thirteen-node hierarchy, meters, and `extras.forward: "-Z"`.
- SHA-256/LFS object IDs: LOD0 `453ebc42da5745f7f5251323cd7a38a79add6538ee39dc9e512570c1c9905150`; LOD1 `a9013591726b3bbb43b102d3707fe9da24f2e1e8de24c929bbc6405e28357002`; LOD2 `3578b62d3c9fa332adb2b1ae7addb1d2b56201c7c8491a1075e847ff18caa79e`.
- Runtime driver placement: Cleo uses character-specific sprite position `[0, 0.9, -0.72]` in the kart group. Runtime kart-forward is positive Z, so the negative-Z offset moves her rearward into The Gilded Stitch's approved cockpit and leaves its steering wheel ahead of her. The same placement applies to player and AI instances.

## Integration gate

The approved package is prepared under controlled revision `cleo-runtime-20260821-1`. Do not merge the production manifest activation until the three GLBs are materialized through Git LFS and repository CI passes. Live selection, orientation, driver-state, and unique-opponent checks remain required after deployment.
