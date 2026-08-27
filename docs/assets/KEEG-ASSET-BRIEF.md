# Keeg production asset brief

## Package identity

- Character: Keeg
- Runtime ID: `aa-04`
- Balance profile: AA-04 Balanced Racer
- Kart: The Mycelial Majesty
- Package status: **2D art and kart approved; LFS verified; manifest activation staged pending CI**

## Canonical character lock

Use the Manny-supplied Keeg racing reference as definitive visual authority and the approved portrait as the production likeness. Preserve the well-trimmed beard, dark-brown hair, tall broad-brimmed purple witch hat with silver trim and lavender gemstone, layered luminous purple/lavender/silver robes, jeweled details, theatrical pose language, sophisticated magical presence, and restrained mushroom affinity.

Driver art and kart art remain separate runtime layers. Driver PNGs contain no steering wheel, cockpit wall, kart body, tires, exhaust, or other vehicle geometry.

## Runtime PNG contract

| Path | Size | Use | SHA-256 |
| --- | --- | --- | --- |
| `public/assets/characters/aa-04/portrait.png` | 256 x 256 | Character Select portrait | `6bd31eef364f7d5bba3020f0fa2559c69ea3becd6a4132692faadd60b981dd66` |
| `public/assets/characters/aa-04/driver/front.png` | 512 x 512 | Front-facing race camera | `6fdd0263ba10f5cf4b50fce1870bcf2647de251ad8d22fcf59d2f2410df81fee` |
| `public/assets/characters/aa-04/driver/rear.png` | 512 x 512 | Neutral chase-camera state | `6a84ddc834ceb670ee04401559a9360638be08f39cb52236caf7756a86f93c51` |
| `public/assets/characters/aa-04/driver/steer-left.png` | 512 x 512 | Chase-camera left steering | `43f3df67361be5bf7db6d53267a56e3caa7c9684dcf8bddfd4900269547fedd5` |
| `public/assets/characters/aa-04/driver/steer-right.png` | 512 x 512 | Chase-camera right steering | `5b6288894fc2ccd6029c245920c8987cbc1b5a67e4fcd9416fce22e618a0b499` |
| `public/assets/characters/aa-04/driver/hit.png` | 512 x 512 | Chase-camera impact reaction | `30c44e3ad74dd6219a403365ac55a54470967e37f3e7c0288b901ee4c87aa7ff` |
| `public/assets/characters/aa-04/driver/victory.png` | 512 x 512 | Chase-camera victory turn | `bde98ae1841c061baf92966df8909a817af63b2d03f6c1a443e7b0dac7d56540` |

Every approved file is sRGB RGBA with alpha spanning fully transparent to fully opaque and four fully transparent corner pixels. Runtime PNGs belong in normal Git under ADR-012.

## Driver-state behavior

- Rear is the visible fallback if another state fails.
- Front is independently approved and is not a mirrored rear frame.
- Rear, front, steer-left, steer-right, and hit preserve a stable seated footprint.
- Steering states keep both hands in a believable driving position without wheel geometry.
- Hit shows a sharp magical recoil while Keeg remains seated.
- Victory keeps the lower body race-forward while Keeg turns toward the chase camera and presents restrained mushroom magic.

## Definitive kart direction

The supplied racing reference is definitive. Preserve the low wide enchanted grand-tourer chassis, rounded shield-like nose, open cockpit, sculpted side pods, physically connected conventional wheels with violet arcane rim energy, royal-purple bodywork, blackened secondary surfaces, attached silver filigree, lavender glow, and integrated mushroom emblem/fixtures.

## Verification evidence

- Manny approved the portrait and all six driver states on 2026-08-26.
- Initial validation found baked checkerboard RGB backgrounds in all six driver frames; those files were rejected before repository ingestion.
- Corrected outputs were independently checked for exact dimensions, sRGBA channels, alpha range 0–1, and fully transparent corner pixels.
- SHA-256 values above identify the approved normalized runtime files.
- Manny approved Candidate 3 Revision 6 on 2026-08-26 after tire clearance and the angled, chassis-mounted steering assembly were verified in an external GLB viewer.
- The approved deterministic builder is `tools/assets/build_keeg_mycelial_majesty.py`.

| Runtime path | LOD | Triangles | Materials | Nodes | SHA-256 |
| --- | --- | ---: | ---: | ---: | --- |
| `public/assets/characters/aa-04/kart.glb` | LOD0 | 20,260 | 4 | 13 | `70cd099091108ddc6bd6b5182161a52b17e8f3f501c4c8b8ef8b78e7e9eca99c` |
| `public/assets/characters/aa-04/kart-lod1.glb` | LOD1 | 11,652 | 4 | 13 | `18b65676d1a643b34b8bb7e6065032ac28b39867521c5598b1fb982399c2688f` |
| `public/assets/characters/aa-04/kart-lod2.glb` | LOD2 | 4,404 | 4 | 13 | `6ee137d9a8e1a2bc8b05e76638dee04ec6dd81af964d71e79364926a9eb12528` |

All three files use meters, declare `extras.forward: "-Z"`, and contain the required kart root, chassis, accent, steering, four wheel, two exhaust, driver mount, and two item mount nodes. Runtime URLs, manifest activation, CI deployment, and live manual verification remain pending.
- LFS publication bridge run `33015135969` rebuilt and matched all three approved hashes, uploaded only those object IDs, deleted its local cache, fetched the branch objects back, and passed `git lfs fsck`. The temporary workflow was removed before review.
- Pre-activation PR CI run `33015347165` passed LFS materialization, `git lfs fsck`, typecheck, lint, tests, and production build.
- Runtime repair revision: `keeg-runtime-20260826-2`.

The initial live publication corrupted the seven normal-Git PNG payloads while leaving plausible PNG headers and dimensions. The repair restores the exact approved source exports and adds full zlib/scanline decoding to the production asset gate. No artwork was regenerated or visually changed.

The live cockpit check found the generic driver mount placed Keeg's hands above the steering-wheel center. AA-04 therefore uses the character-specific runtime mount `[0, 0.72, -0.12]`; sprite scale, depth, approved artwork, and kart geometry remain unchanged.

## Next gate

Validate the staged AA-04 manifest identity in PR CI, then merge and perform desktop/mobile live checks before closing production acceptance.
