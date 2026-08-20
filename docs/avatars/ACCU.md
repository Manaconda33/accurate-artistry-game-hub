# Avatar intake: Accu

- **Intake date:** 2026-08-20
- **Current phase:** Driver art and Pink Precision production package approved and prepared; runtime integration pending
- **Intake status:** Approved
- **Character lock:** Approved by Manny on 2026-08-20
- **Kart lock:** _Pink Precision_, approved by Manny on 2026-08-20
- **Balance mapping lock:** AA-11 Collision Tank, approved by Manny on 2026-08-20
- **Asset approval:** Portrait and all five driver states approved by Manny on 2026-08-20
- **Kart-model approval:** Pink Precision Candidate 1 approved by Manny on 2026-08-20
- **Implementation verification:** Not started

Manny created the supplied Accu reference art and approved transforming it into production game assets. The attached pink-hat design is Accu's canonical appearance for this game and supersedes earlier descriptions that conflict with it.

## Identity and visual locks

- **Stable internal ID:** `aa-11`
- **Selection descriptor:** Perfect aim. Maximum armor.
- Long vivid pink hair with pale-pink streaks, pink-magenta eyes, a broad pink brimmed hat with a darker band and side bow, and a pink long-sleeved top covered in darker heart motifs.
- Bright, composed confidence; cute presentation paired with disciplined precision and heavyweight durability.
- Preserve the hat-and-bow silhouette, two-tone pink hair, pink eyes, heart-pattern top, and friendly confident expression at small scale.
- Do not revert to the earlier twin-ponytail, green-eye, pleated-skirt, or tactical-vest description for this game.

## Pink Precision: locked kart

- Compact tank-inspired racing kart with working treads and a working cannon; it is not a literal full-size tank.
- Pink armored bodywork balances cute presentation with heavy, purposeful construction.
- Original emblem: a heart-shaped bullseye with a central four-point sparkle.
- No Hello Kitty imagery, licensed-character branding, copied marks, or reference text.
- The final model must keep its steering controls in front of Accu and must read correctly from chase and rear cameras.

## Gameplay and roster mapping

- **Driving feel:** armored collision specialist with strong speed once moving, maximum weight, limited acceleration, and deliberate handling.
- **Assigned profile:** AA-11 Collision Tank — Speed 8 / Acceleration 4 / Weight 10 / Handling 3 / Mini-Turbo 5 / Traction 6.
- **Rationale:** Weight 10 and Handling 3 make contact and commitment central to the character, while Speed 8 preserves racing threat. Acceleration 4 creates a real recovery cost; Mini-Turbo 5 and Traction 6 keep the kart usable without erasing its heavyweight identity.
- **Approval:** Manny approved AA-11 on 2026-08-20.

## Required assets

| Asset                                           | Required format                                 | Status                     |
| ----------------------------------------------- | ----------------------------------------------- | -------------------------- |
| Portrait                                        | 256 x 256 transparent PNG, sRGB, straight alpha | Approved and prepared      |
| Rear / steer-left / steer-right / hit / victory | 512 x 512 transparent PNG, sRGB                 | Approved and prepared      |
| Pink Precision                                  | GLB with PRD hierarchy and LOD budgets          | Approved and prepared      |

## Approval record

- Character lock, kart lock, balance mapping, emblem direction, and source transformation: approved.
- Portrait, rear, steer-left, steer-right, hit, and victory: approved by Manny on 2026-08-20 and prepared at the PRD runtime paths.
- Pink Precision Candidate 1 is the approved production LOD0. Its deterministic LOD package is prepared at `public/assets/characters/aa-11/{kart,kart-lod1,kart-lod2}.glb`.
- Manifest/runtime integration, deployment, and live desktop/mobile verification remain separately pending.

## Next action

Publish and fetch-verify the three Pink Precision LFS objects, then begin the separate runtime-integration checkpoint.
