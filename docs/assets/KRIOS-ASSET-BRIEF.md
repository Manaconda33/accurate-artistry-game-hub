# Krios production asset brief

## Package identity

- Character: Krios
- Runtime ID: `aa-10`
- Balance profile: AA-10 Straight-Line Heavy
- Kart: The Hornbreaker
- Package status: driver-art production in progress

## Canonical character lock

Use the approved portrait as Krios's definitive game likeness. Preserve saturated red skin, immense muscular scale, two black ridged ram horns growing from the temples, swept-back black hair, pointed ears with metal rings, glowing gold eyes, the huge wild black beard with metal-bound braids, rugged dark leather harness, heavy studded bracers, and red flame emblems. His neutral expression is severe, proud, and controlled.

Driver art and kart art remain separate runtime layers. Driver PNGs must not contain a steering wheel, cockpit wall, kart body, tires, exhaust, or other vehicle geometry.

## Runtime PNG contract

| Path                                                    | Size      | Use                                 |
| ------------------------------------------------------- | --------- | ----------------------------------- |
| `public/assets/characters/aa-10/portrait.png`           | 256 x 256 | Character Select portrait           |
| `public/assets/characters/aa-10/driver/front.png`       | 512 x 512 | Camera facing the front of the kart |
| `public/assets/characters/aa-10/driver/rear.png`        | 512 x 512 | Neutral chase-camera state          |
| `public/assets/characters/aa-10/driver/steer-left.png`  | 512 x 512 | Chase-camera left steering          |
| `public/assets/characters/aa-10/driver/steer-right.png` | 512 x 512 | Chase-camera right steering         |
| `public/assets/characters/aa-10/driver/hit.png`         | 512 x 512 | Chase-camera impact reaction        |
| `public/assets/characters/aa-10/driver/victory.png`     | 512 x 512 | Chase-camera victory turn           |

Every file must remain sRGB RGBA with non-opaque alpha and transparent corner pixels. Runtime art belongs in normal Git under ADR-012. High-resolution masters do not belong at these paths.

## Driver-state behavior

- Rear is the visible fallback if another frame fails.
- Front is a separately approved view and must not be inferred by mirroring a rear frame.
- Rear, steer-left, steer-right, and hit preserve the same broad seated footprint so Krios does not jump or resize between states.
- Steering states keep both hands in a believable driving position without including the wheel.
- Hit takes precedence over steering and shows a forceful recoil without making Krios look timid or comedic.
- Victory keeps the lower body seated toward the kart while Krios turns toward the chase camera in a dominant celebration.
- Horns must remain fully readable and must never become ordinary demon spikes, antlers, or additional horn pairs.

## Definitive kart direction

The supplied Krios racing sheet is definitive. Preserve:

- brutal infernal battle-kart / hot-rod construction
- low, broad, aggressive silhouette
- weathered dark steel with red flame graphics
- integrated ram horns at the nose
- open cockpit sized for Krios's heavy build
- oversized rugged studded tires
- twin rear exhausts with visible flame
- dominant straight-line presence rather than a tall armored vehicle

## Current verification

- Portrait: 256 x 256, sRGB RGBA, transparent
- Front driver frame: 512 x 512, sRGB RGBA, transparent
- Both files have alpha spanning fully transparent to fully opaque and a fully transparent corner pixel
- Approved front art contains no steering wheel or kart geometry
- Runtime PNGs resolve to normal Git rather than Git LFS

## Integration gate

Do not activate AA-10 in the production manifest until all six driver frames and The Hornbreaker's required GLB LODs are approved, materialized, and validated. Repository CI, deployed selection and orientation checks, driver-state checks, unique-opponent checks, and Manny's live acceptance remain required.
