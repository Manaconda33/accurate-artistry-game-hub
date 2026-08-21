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
| Pink Precision                                  | GLB with PRD hierarchy and LOD budgets          | Approved and prepared 2026-08-20 |

## Approved Pink Precision model checkpoint

- Candidate 1 is the approved production silhouette: low armored hull, continuous tread loops, compact cockpit, forward cannon, rear antennae and exhausts, and the original heart-bullseye nose emblem.
- The approved LOD0 geometry is frozen byte-for-byte in the deterministic builder. LOD1 and LOD2 reduce curved segments, tread pads, and internal road wheels without changing the locked silhouette or mount layout.
- All three GLBs use negative Z as forward, four opaque materials, and the required 13-node kart hierarchy.
- LOD0: 4,156 triangles, SHA-256 `6e3f8cb6d1bdee7f5b315a7c154bd45fd0f4d6ac9b2e6445b9d85d81959ff958`.
- LOD1: 2,700 triangles, SHA-256 `9f481cf854d47ec330e5909d5003353376c471cd37562d79410c20e3f824f9c7`.
- LOD2: 1,804 triangles, SHA-256 `792b8f8bf1d359b3ae464003f0fa9432de5c391d8bd18ac8f84535593d9ba820`.
- The SHA-256 values are also the Git LFS object IDs and must match during publication and fetch-back verification.

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

## Runtime integration checkpoint

- Controlled asset revision: `accu-runtime-20260820-1`.
- The character manifest selects Accu's approved portrait, Pink Precision LOD0, and all five driver frames for AA-11.
- Pink Precision declares negative-Z authored forward and therefore uses the runtime's enforced `NEGATIVE_Z_KART_VISUAL_YAW` (`Math.PI`). The transform affects only the model root; physics, checkpoints, controls, driver sprites, and cameras remain unchanged.
- The production signature gate includes all three Pink Precision GLBs. A pointer or invalid GLB at any required path fails the build.
- Deployment and product-owner desktop/mobile confirmation remain required before the integration checkpoint can pass.
