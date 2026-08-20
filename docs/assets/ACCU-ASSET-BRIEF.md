# Accu asset brief

## Authority and source

- Accu, Pink Precision, and AA-11 Collision Tank were approved by Manny on 2026-08-20.
- Manny created the supplied references and approved transforming them into production game assets.
- The pink-hat portrait is the canonical game appearance. The tank collage supplies the compact pink armored-kart concept, not licensed branding.
- Keep original source files unchanged; approved runtime derivatives have separate repository paths.

## Production style

- Polished, colorful, high-contrast Accurate Artistry arcade presentation.
- Anime-inspired 2D driver art paired with a stylized 3D kart.
- Original visual language with no Hello Kitty imagery, copied marks, or licensed-character branding.

## Locked character identity

- Long vivid pink hair with pale-pink streaks; pink-magenta eyes.
- Broad pink brimmed hat with darker band and side bow.
- Pink long-sleeved top patterned with darker hearts.
- Friendly, composed, precise confidence.
- Small-scale read: hat and bow, two-tone hair, pink eyes, heart-pattern top.

## Pink Precision

- Compact tank-inspired kart with working treads and cannon, scaled and shaped for racing rather than presented as a full-size tank.
- Pink armored construction with a cute-versus-heavy visual contrast.
- Original heart-shaped bullseye emblem with a central four-point sparkle.
- Steering controls must sit in front of Accu. Cannon, tread housings, cockpit, and driver mount must not clip.
- Prohibited: Hello Kitty imagery, licensed mascots, copied labels, full-size military proportions, conventional exposed tires, or a nonfunctional decorative tread treatment.

## Required production deliverables

| Asset                                           | Format                                          | Approval                         |
| ----------------------------------------------- | ----------------------------------------------- | -------------------------------- |
| Portrait                                        | 256 x 256 transparent PNG, sRGB, straight alpha | Approved and prepared 2026-08-20 |
| Rear / steer-left / steer-right / hit / victory | 512 x 512 transparent PNG, sRGB                 | Approved and prepared 2026-08-20 |
| Pink Precision                                  | GLB with PRD hierarchy and LOD budgets          | Candidate pending                |

## Approved driver-art checkpoint

- Runtime paths: `public/assets/characters/aa-11/portrait.png` and `public/assets/characters/aa-11/driver/{rear,steer-left,steer-right,hit,victory}.png`.
- Portrait is 256 x 256; each driver state is 512 x 512.
- All six files are sRGB RGBA PNGs with genuine transparency, alpha spanning 0 to 1, and transparent corner pixels.
- Victory keeps Accu's seated driving orientation while she turns naturally over her shoulder toward the viewer; it does not use a full-body about-face.
- The driver art contains steering wheels where required by the approved compositions. Runtime integration must verify that these do not conflict visually with the future 3D steering control.

## Runtime delivery requirements

- Manifest URLs use a controlled base-aware revision whenever stable runtime bytes change.
- Pages materializes LFS, passes `git lfs fsck`, and rejects an LFS pointer or invalid glTF binary signature before deployment.
- Runtime preloads all five driver states and retains rear as the safe fallback.
- Chase and rear cameras must confirm Pink Precision's nose, cannon, controls, and treads face the correct direction. Any axis correction applies only to the visual root and is recorded.
- Acceptance requires desktop and mobile confirmation of Accu's portrait, production kart, all five driver states, and orientation.
