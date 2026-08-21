# Kraken production asset brief

## Package identity

- Character: Kraken
- Runtime ID: `aa-05`
- Balance profile: AA-05 Drift Specialist
- Kart: The Abyssal Drifter
- Package status: driver art approved; kart production pending

## Canonical character lock

Use the approved racing reference as the definitive likeness. Kraken has an angular masculine face, vivid green eyes, short cropped dark hair with closely cut sides, two pointed ears, and a burgundy collared shirt. Do not restore earlier long or tousled hairstyles, ornate coats, blood effects, facial tentacles, or a transformed Cthulhu head.

Driver art and kart art remain separate runtime layers. Driver PNGs must not contain a steering wheel, cockpit wall, kart body, or wheel geometry.

## Runtime PNG contract

| Path                                                      | Size      | Use                                 |
| --------------------------------------------------------- | --------- | ----------------------------------- |
| `public/assets/characters/aa-05/portrait.png`             | 256 x 256 | Character Select portrait           |
| `public/assets/characters/aa-05/driver/front.png`         | 512 x 512 | Camera facing the front of the kart |
| `public/assets/characters/aa-05/driver/rear.png`          | 512 x 512 | Neutral chase-camera state          |
| `public/assets/characters/aa-05/driver/steer-left.png`    | 512 x 512 | Chase-camera left steering          |
| `public/assets/characters/aa-05/driver/steer-right.png`   | 512 x 512 | Chase-camera right steering         |
| `public/assets/characters/aa-05/driver/hit.png`           | 512 x 512 | Chase-camera impact reaction        |
| `public/assets/characters/aa-05/driver/victory.png`       | 512 x 512 | Chase-camera victory turn           |
| `public/assets/characters/aa-05/driver/front-victory.png` | 512 x 512 | Front-facing victory presentation   |

Every file must remain sRGB RGBA with non-opaque alpha and transparent corner pixels. Runtime art belongs in normal Git under ADR-012. High-resolution masters do not belong at these paths.

## Driver-state behavior

- Rear is the visible fallback if another frame fails.
- Steer-left and steer-right preserve the same hip anchor, scale, and seated footprint as rear.
- Hit takes precedence over steering and shows Kraken recoiling while his hips remain forward.
- Chase victory keeps his hips and legs facing the kart while his torso turns back toward the viewer. It must not read as a full-body 180-degree about-face.
- Front and front-victory are separate approved views. Neither may be inferred by mirroring a rear frame.

## Definitive kart direction

The supplied kart reference is definitive. Preserve:

- orange eyes and toothed front maw
- indigo and purple living shell
- cyan bioluminescent markings
- copper trim
- tentacle bodywork
- turbine-like wheel language
- a clear cockpit that does not clip through Kraken

The production model must declare `extras.forward: "-Z"` and use the shared `NEGATIVE_Z_KART_VISUAL_YAW` runtime transform. The maw and eyes are the front. Exhaust and rear propulsion details belong behind the driver. Chase- and front-facing camera checks are mandatory before the kart is accepted.

## Current verification

- Portrait: 256 x 256, sRGB RGBA, transparent
- Seven driver frames: 512 x 512, sRGB RGBA, transparent
- Approved art contains no steering wheel or kart geometry
- Kart GLB, LODs, triangle counts, hierarchy, LFS object IDs, and live orientation: pending

## Integration gate

Do not mark `aa-05` as a production manifest entry until The Abyssal Drifter is approved, its three GLBs are materialized through Git LFS, the runtime asset gate passes, and desktop/mobile selection and race checks confirm the approved kart rather than the fallback.
