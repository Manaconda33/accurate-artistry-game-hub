# Lula / The Verdant Hart Asset Brief

## Governing locks

- Character, definitive reference, and transformation rights: Approved 2026-08-29
- Kart name and design direction: Approved 2026-08-29
- Balance profile: AA-03 Feather Dirt Ace, approved 2026-08-29
- Portrait and six driver-state designs: Approved 2026-08-29
- Kart GLB geometry: Candidate 4 approved 2026-08-29

## Approved 2D package

Runtime derivatives are stored under `public/assets/characters/aa-03/`:

- `portrait.png`: 256 × 256 sRGBA
- `driver/front.png`: 512 × 512 sRGBA
- `driver/rear.png`: 512 × 512 sRGBA
- `driver/steer-left.png`: 512 × 512 sRGBA
- `driver/steer-right.png`: 512 × 512 sRGBA
- `driver/hit.png`: 512 × 512 sRGBA
- `driver/victory.png`: 512 × 512 sRGBA

All seven files have genuine transparency, fully transparent corners, and approved clean silhouettes. Driver layers contain no kart, seat, or steering-wheel geometry.

## Approved 3D package

Candidate 4 preserves the approved low stag-racer silhouette while replacing exposed cylinder endcaps with overlapping organic joints. The stag face, cheek roots, structural antlers, cockpit roots, wheel housings, and wooden outlets form one connected construction. Dedicated foliage geometry and a neutral leaf material keep the embedded leaf clusters visibly green across viewers.

| Runtime path                                   | LOD  | Triangles | SHA-256                                                            |
| ---------------------------------------------- | ---- | --------: | ------------------------------------------------------------------ |
| `public/assets/characters/aa-03/kart.glb`      | LOD0 |    21,948 | `6842eecf711117d8ca521ebd9620926268452193f5c3b9e2ba7ad9aba090c26c` |
| `public/assets/characters/aa-03/kart-lod1.glb` | LOD1 |     8,954 | `b9a267a6a41d14a674771cc0137d1b0445e1a264bfa8b2c5acc7c6685ab399cd` |
| `public/assets/characters/aa-03/kart-lod2.glb` | LOD2 |     4,746 | `3a062ee6bee2502bdd3914063cc549a08e4de151ebf5bcfc3a52fe9658eb57f0` |

All three GLBs provide 13 required nodes and `extras.forward: "-Z"`. The controlled runtime revision is `lula-runtime-20260829-1`. LFS publication, deployment, and live acceptance remain pending.
