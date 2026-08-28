# Toph — Production Character Record

## Approval state

- Character lock: Approved by Manny, 2026-08-28
- Definitive visual authority: Supplied Toph racing reference
- Transformation rights: Confirmed by Manny, 2026-08-28
- Kart lock: The Grave Shift, approved by Manny, 2026-08-28
- Balance mapping: AA-08 Turbo Bruiser, approved by Manny, 2026-08-28
- 2D design package: Portrait, front, rear, steer-left, steer-right, hit, and corrected victory approved by Manny, 2026-08-28
- 3D kart geometry: Candidate 2 approved by Manny, 2026-08-28
- Runtime activation: Staged pending merge, deployment, and live acceptance

## Character lock

Toph is a stylish young man with shaggy blond hair, pale teal eyes, rectangular black glasses, black ear gauges, and a fitted black beanie decorated with small purple, silver, and bronze pins. He wears an oversized black hoodie carrying an original purple thorn-like graphic. His presentation is relaxed, confident, alternative, and slightly mischievous.

## Kart lock

The Grave Shift is a low, aggressive street-racer kart with dark bronze framing, black and deep-purple bodywork, exposed mechanical construction, wide tires, purple exhaust energy, and a prominent thorned-skull nose shield. The design may draw on the broad language of colorful kart-racing games but may not reproduce a specific commercial kart.

## Balance mapping

AA-08 Turbo Bruiser — Speed 7 / Acceleration 5 / Weight 7 / Handling 4 / Mini-Turbo 8 / Traction 5.

The profile gives Toph substantial road presence and rewards drift chains with strong turbo exits. Lower acceleration and handling make missed lines costly and distinguish him from Kraken's lighter AA-05 Drift Specialist.

## Runtime asset contract

- Portrait: 256 × 256 transparent sRGBA PNG
- Front, rear, steer-left, steer-right, hit, and victory: 512 × 512 transparent sRGBA PNG
- Driver layers contain no kart, seat, or steering-wheel geometry
- The corrected victory frame keeps the pelvis and lower body facing race-forward while the upper torso turns toward the chase camera
- Runtime revision: `toph-runtime-20260828-1`. Candidate 2 produced deterministic LOD0/LOD1/LOD2 at 8,604 / 4,452 / 2,344 triangles with 13 required nodes and `extras.forward: "-Z"`. AA-08 activation is staged pending merge, deployment, and live acceptance.
