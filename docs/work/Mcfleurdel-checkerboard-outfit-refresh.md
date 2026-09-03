# McFleurdel checkerboard outfit refresh

Status: **CANDIDATE COMPLETE / PRODUCT-OWNER ASSET REVIEW REQUIRED**

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

## Candidate batches

Batch 1 generated and committed by branch-only bridge run **33811917223**:

1. `portrait.png`
2. `driver/front.png`
3. `driver/front-steer-left.png`
4. `driver/front-steer-right.png`
5. `driver/front-hit.png`

Batch 2 generated and committed by branch-only bridge run **33812111707**:

6. `driver/front-victory.png`
7. `driver/rear.png`
8. `driver/steer-left.png`
9. `driver/steer-right.png`
10. `driver/hit.png`
11. `driver/victory.png`

The temporary asset bridge workflow was removed after both generated commits. The deterministic builders remain on the branch as review evidence and to make approved corrections reproducible.

## Candidate SHA-256 values

| Runtime path | Candidate SHA-256 |
| --- | --- |
| `public/assets/characters/aa-07/portrait.png` | `ed99ee9506b04e69623a713de79f7986c39c0f7df044eb44ae6e7eaff90c919c` |
| `public/assets/characters/aa-07/driver/front.png` | `1ef810c9a5011f8109e13c118c796c8002ed2ab909870f7826cef57c74c79974` |
| `public/assets/characters/aa-07/driver/front-steer-left.png` | `59e85daad353f0b49383d7b54138cca38f841b8470587697080bb9aee6bb3eab` |
| `public/assets/characters/aa-07/driver/front-steer-right.png` | `3d7d32c81b324f2907573907793c0e3f867ddfdc1f6eaf5c39b813c7a1d6aa85` |
| `public/assets/characters/aa-07/driver/front-hit.png` | `8bc8d8deb65c166f7c6454d1c175d1839b06e881cdcbeaa479df0b4e3e47f4c6` |
| `public/assets/characters/aa-07/driver/front-victory.png` | `252a527eaf62aaf751ae72ad412ed280f14255f99c2c5ed4c2ff98aff952ed88` |
| `public/assets/characters/aa-07/driver/rear.png` | `fdfcc62ac5aa53efc041d4b32aff6f60106a24b490ff7b009b5fdf67db66d165` |
| `public/assets/characters/aa-07/driver/steer-left.png` | `483c6f49f9031e2da0e00d271bbae7e5fad3672a1b7dfa850984d631caa2c74b` |
| `public/assets/characters/aa-07/driver/steer-right.png` | `c83a730b17afd53378688464a54484875f9ace4bd5c3f52af3b260c2ea4bdff3` |
| `public/assets/characters/aa-07/driver/hit.png` | `de5fbfdf275c3246d6dd6f3b2747748012632f575426bed5bcacc5c4dd31c44d` |
| `public/assets/characters/aa-07/driver/victory.png` | `adcaca06b71407d74e1486ae6a338bc822a70aceffe61d3d9a0f66ddd58195df` |

## Automated candidate checks

Both generation runs verified before committing:

- portrait remains exactly **256 × 256**;
- all ten driver states remain exactly **512 × 512**;
- every candidate is RGBA with alpha spanning fully transparent to fully opaque;
- all four corner pixels remain fully transparent;
- the source alpha channel is preserved exactly, so the approved sprite silhouette, posture footprint, hair contour, arm gaps, and transparent negative space cannot move during this outfit-only pass.

## Approval boundary

All eleven candidates remain **unapproved** until Manny reviews them. Do not update the controlled McFleurdel runtime revision, production hashes, `docs/assets/MCFLEURDEL-ASSET-BRIEF.md`, `docs/avatars/MCFLEURDEL.md`, merge to `main`, or publish to Pages before product-owner asset approval.
