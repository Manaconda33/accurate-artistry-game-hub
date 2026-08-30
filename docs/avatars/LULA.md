# Lula — Production Character Record

## Approval state

- Character lock: Approved by Manny, 2026-08-29
- Definitive visual authority: Supplied Lula racing reference
- Transformation rights: Confirmed by Manny, 2026-08-29
- Kart lock: The Verdant Hart, approved by Manny, 2026-08-29
- Balance mapping: AA-03 Feather Dirt Ace, approved by Manny, 2026-08-29
- 2D design package: Portrait, front, rear, steer-left, steer-right, hit, and corrected victory approved by Manny, 2026-08-29
- 3D kart geometry: Candidate 4 approved by Manny, 2026-08-29
- Runtime activation: Prepared; deployment and live acceptance pending

## Character lock

Lula is an elven woodland guardian with long forest-green hair, pointed ears, green eyes, and a symmetrical leaf-shaped forehead marking. Her fitted ranger attire uses layered moss, olive, and bark-brown materials with practical leather bracers and shoulder protection. She is disciplined, agile, protective, and deeply connected to the forest rather than delicate, whimsical, or ornamental.

## Kart lock

The Verdant Hart is a low open-cockpit woodland racer grown from interwoven dark roots and carved timber. A unified stag face forms the nose, with brow-rooted branching antlers, restrained amber-green eyes, embedded green foliage, leaf-inlaid wheels, and subtle woodland magic. The design must read as one physically connected living-wood racing machine.

## Balance mapping

AA-03 Feather Dirt Ace — Speed 5 / Acceleration 8 / Weight 3 / Handling 7 / Mini-Turbo 6 / Traction 7.

The profile gives Lula quick recovery, responsive control, and strong off-road grip. Lower top speed and low collision resistance keep the profile distinct from Lavi's more technical AA-02 package.

## Runtime asset contract

- Portrait: 256 × 256 transparent sRGBA PNG
- Front, rear, steer-left, steer-right, hit, and victory: 512 × 512 transparent sRGBA PNG
- Driver layers contain no kart, seat, or steering-wheel geometry
- Runtime revision: `lula-runtime-20260830-2`
- Candidate 4 produces deterministic LOD0/LOD1/LOD2 at 21,948 / 8,954 / 4,746 triangles
- Every GLB provides 13 required nodes and `extras.forward: "-Z"`

## Live acceptance

The initial live package exposed opaque white background islands and hair-edge ribbons that the original edge-connected checkerboard cleanup had missed. The deterministic `repair_lula_alpha.py` correction removes enclosed neutral background components and neighboring pale spill while protecting small face/eye highlights. Package review also found that the five chase-camera states had drifted to saturated orange skin; `repair_lula_skin_tone.py` constrains their exposed skin to the approved portrait/front complexion with no non-skin or alpha changes. The combined correction remains uncommitted until a playable build passes Manny's desktop/mobile confirmation.
