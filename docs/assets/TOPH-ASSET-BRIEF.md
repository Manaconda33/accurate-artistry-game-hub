# Toph / The Grave Shift Asset Brief

## Governing locks

- Character, definitive reference, and transformation rights: Approved 2026-08-28
- Kart name and design direction: Approved 2026-08-28
- Balance profile: AA-08 Turbo Bruiser, approved 2026-08-28
- Portrait and six driver-state designs: Approved 2026-08-28
- Kart GLB geometry: Candidate 2 approved 2026-08-28
- Runtime activation: Staged pending merge, deployment, and live acceptance

## Approved 2D package

Runtime derivatives are stored under `public/assets/characters/aa-08/`:

- `portrait.png`: 256 × 256 sRGBA
- `driver/front.png`: 512 × 512 sRGBA
- `driver/rear.png`: 512 × 512 sRGBA
- `driver/steer-left.png`: 512 × 512 sRGBA
- `driver/steer-right.png`: 512 × 512 sRGBA
- `driver/hit.png`: 512 × 512 sRGBA
- `driver/victory.png`: 512 × 512 sRGBA

All files have genuine alpha spanning transparent to opaque and fully transparent corners. Driver layers contain no kart, seat, or steering-wheel geometry. The initial generated previews contained baked light checkerboards; `tools/assets/prepare_toph_2d.py` deterministically removes only edge-connected light-neutral background pixels before square containment and runtime resizing. Dark-background contact-sheet inspection confirms clean silhouettes and no retained checkerboard cells.

## Pending 3D package

The approved kart direction requires a deterministic LOD0/LOD1/LOD2 builder for The Grave Shift. The production model must provide:

- Low aggressive street-racer silhouette
- Dark bronze connected frame and exposed mechanical construction
- Black and deep-purple bodywork
- Four physically connected wide tires
- Open cockpit and chassis-mounted steering assembly sized for the approved driver frames
- Structurally integrated thorned-skull nose shield
- Rear-mounted purple exhaust-energy treatment
- `extras.forward: "-Z"` on every GLB
- `NEGATIVE_Z_KART_VISUAL_YAW` in the future manifest entry

Candidate 2 replaced the rejected rounded/clown-like Candidate 1 with the definitive purple-dominant armored interpretation: a flat trapezoidal skull shield, angular integrated thorn crown, enclosed sidepods, low splitter, and enclosed rear engine with twin violet exhausts.

| Runtime path | LOD | Triangles | SHA-256 |
| --- | --- | ---: | --- |
| `public/assets/characters/aa-08/kart.glb` | LOD0 | 8,604 | `87db250bcacbbbe93afdee0e4a346ff3c5aaca7fbb90668af383b1772154c953` |
| `public/assets/characters/aa-08/kart-lod1.glb` | LOD1 | 4,452 | `1d3b62f715e6288b01447eafe2a81a07b09fe676019b1849ff3b5b78ad9c4d23` |
| `public/assets/characters/aa-08/kart-lod2.glb` | LOD2 | 2,344 | `2c38dd14a334443fff3f872fc618210642f51dfc8b612bf1f075b347a5a65be7` |

All three GLBs have 13 required nodes and `extras.forward: "-Z"`. The controlled runtime revision is `toph-runtime-20260828-1`. LFS publication materialized successfully in CI. Merge, deployment, and live acceptance remain pending.
