# Cleo production asset brief

## Package identity

- Character: Cleo
- Runtime ID: `aa-06`
- Balance profile: AA-06 Grip Specialist
- Kart: The Gilded Stitch
- Package status: approved driver-art checkpoint; kart production pending

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

## Integration gate

Do not mark `aa-06` as production in `src/characters/manifest.ts` until The Gilded Stitch has approved LOD0/1/2 GLBs, required hierarchy and negative-Z metadata, LFS materialization evidence, runtime validation, and a controlled asset revision. Live selection, orientation, driver-state, and unique-opponent checks remain required after deployment.
