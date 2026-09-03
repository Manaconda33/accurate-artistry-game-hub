# McFleurdel checkerboard outfit refresh

Status: **IN PROGRESS / ASSET REVIEW REQUIRED**

Branch: `art/mcfleurdel-checkerboard-outfit`
Base checkpoint: `a706f01f43f07d9b31d05ce38e3e4b67c396894c`

## Approved change scope

Manny authorized an outfit-only refresh of every McFleurdel (`aa-07`) 2D asset using the supplied black-and-white checkerboard formalwear reference.

Preserve without redesign:

- approved face, makeup, facial expression, and identity;
- approved black/white hair geometry and each frame's governed view-specific hair-color placement;
- approved posture, seated footprint, limb positions, steering hand placement, hit recoil, and victory turn;
- transparent background and exact runtime dimensions;
- wheel-free / kart-free sprite ownership;
- current camera placement and runtime state behavior.

## Outfit lock

Apply consistently across all views:

- sharply tailored black-and-white checkerboard blazer/jacket treatment;
- black waistcoat/shirt core with crisp white shirt front where visible;
- black bow tie;
- coordinated black/checkerboard lower-body treatment where visible;
- studded black waist/belt detail when visible and compatible with the existing pose;
- coordinated checkerboard footwear only where footwear is visible.

Do not transfer the reference subject's face, hair, tattoos, body proportions, pose, room/background, or accessories that are not part of the clothing.

## Batch plan

Batch 1:
1. `portrait.png`
2. `driver/front.png`
3. `driver/front-steer-left.png`
4. `driver/front-steer-right.png`
5. `driver/front-hit.png`

Batch 2:
6. `driver/front-victory.png`
7. `driver/rear.png`
8. `driver/steer-left.png`
9. `driver/steer-right.png`
10. `driver/hit.png`
11. `driver/victory.png`

All generated candidates remain unapproved until Manny reviews them. No manifest revision, runtime activation, or publication should occur until the complete outfit package is approved.