# Toph / The Grave Shift Asset Brief

## Governing locks

- Character, definitive reference, and transformation rights: Approved 2026-08-28
- Kart name and design direction: Approved 2026-08-28
- Balance profile: AA-08 Turbo Bruiser, approved 2026-08-28
- Portrait and six driver-state designs: Approved 2026-08-28
- Kart GLB geometry: Pending
- Runtime activation: Pending

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

No GLB, manifest activation, runtime revision, mount, LFS publication, CI checkpoint, deployment, or live acceptance is approved by this brief.
