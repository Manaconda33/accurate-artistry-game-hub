# Toph — Production Character Record

## Approval state

- Character lock: Approved by Manny, 2026-08-28
- Definitive visual authority: Supplied Toph racing reference
- Transformation rights: Confirmed by Manny, 2026-08-28
- Kart lock: The Grave Shift, approved by Manny, 2026-08-28
- Balance mapping: AA-08 Turbo Bruiser, approved by Manny, 2026-08-28
- 2D design package: Portrait, front, rear, steer-left, steer-right, hit, and corrected victory approved by Manny, 2026-08-28
- 3D kart geometry: Candidate 2 approved by Manny, 2026-08-28
- Runtime activation: Live accepted by Manny, 2026-08-28
- Front-action package: Four candidates approved by Manny, 2026-09-02; live deployed with playtesting pending

## Character lock

Toph is a stylish young man with shaggy blond hair, pale teal eyes, rectangular black glasses, black ear gauges, and a fitted black beanie decorated with small purple, silver, and bronze pins. He wears an oversized black hoodie carrying an original purple thorn-like graphic. His presentation is relaxed, confident, alternative, and slightly mischievous.

## Kart lock

The Grave Shift is a low, aggressive street-racer kart with dark bronze framing, black and deep-purple bodywork, exposed mechanical construction, wide tires, purple exhaust energy, and a prominent thorned-skull nose shield. The design may draw on the broad language of colorful kart-racing games but may not reproduce a specific commercial kart.

## Balance mapping

AA-08 Turbo Bruiser — Speed 7 / Acceleration 5 / Weight 7 / Handling 4 / Mini-Turbo 8 / Traction 5.

The profile gives Toph substantial road presence and rewards drift chains with strong turbo exits. Lower acceleration and handling make missed lines costly and distinguish him from Kraken's lighter AA-05 Drift Specialist.

## Runtime asset contract

- Portrait: 256 × 256 transparent sRGBA PNG
- Front, rear, steer-left, steer-right, hit, victory, front-steer-left, front-steer-right, front-hit, and front-victory: 512 × 512 transparent sRGBA PNG
- Driver layers contain no kart, seat, or steering-wheel geometry
- The corrected victory frame keeps the pelvis and lower body facing race-forward while the upper torso turns toward the chase camera
- Front-action direction follows commanded kart steering: left leans toward the viewer's right and right leans toward the viewer's left.
- Runtime revision: `toph-runtime-20260902-2`. Candidate 2 produced deterministic LOD0/LOD1/LOD2 at 8,604 / 4,452 / 2,344 triangles with 13 required nodes and `extras.forward: "-Z"`. The front-action revision deployed through PR #68 and main run `33661819292`; bundle and deployed-byte verification passed. Product-owner camera/action playtesting remains open.

## Live acceptance

PR #39 merged the production package. PRs #40 and #41 added and finalized Toph's front-camera-only sprite placement so his hands align with The Grave Shift steering wheel without moving any other driver state. Manny confirmed the corrected live deployment passes all tests on 2026-08-28. Toph's production checkpoint is complete.

The 2026-09-02 front-action expansion does not change that accepted base package or placement. Its separate live-acceptance gate remains open until the deployed package passes both steering directions, hit, victory, chase restoration, transparency, cockpit placement, and single-wheel presentation on desktop/mobile.
