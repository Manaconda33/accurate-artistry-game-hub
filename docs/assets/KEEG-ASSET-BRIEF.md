# Keeg production asset brief

## Package identity

- Character: Keeg
- Runtime ID: `aa-04`
- Balance profile: AA-04 Balanced Racer
- Kart: The Mycelial Majesty
- Package status: **2D art approved; kart and runtime integration pending**

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
- Kart GLBs, deterministic LODs, runtime URLs, manifest activation, CI deployment, and live manual verification remain pending.

## Next gate

Build and approve The Mycelial Majesty. Do not activate AA-04 as a production manifest identity until all three GLBs pass the negative-Z orientation contract, LFS materialization, runtime-asset gate, repository validation, deployment, and Manny's live confirmation.
