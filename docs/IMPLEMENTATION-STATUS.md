# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

The roadmap remains at Slice 3. Competitive Slice 4 systems exist because they were implemented early under the documented sequencing correction. Items remain Slice 5 and are not authorized by the current work.

## Balance rollback decision

On **2026-09-03**, Manny ended the Circuit Alpha rebalance experiment after live playtesting showed that the Candidate F balance model did not preserve competitive player-vs-AI racing. Candidate F's Handling behavior was directionally useful, but the overall rebalance exercise is **ABANDONED / ROLLED BACK** rather than accepted or iterated further.

The game is being restored to the last accepted gameplay checkpoint from immediately before the balance exercise:

- pre-balance source checkpoint: `a706f01f43f07d9b31d05ce38e3e4b67c396894c`;
- Candidate F PR #86 is historical only and must not be treated as accepted balance;
- Candidate G PR #87 is abandoned and must not be merged;
- the 250,000-race Candidate F simulation remains analysis history only and is not an active gameplay specification.

The rollback restores the pre-experiment versions of:

- `src/config/kartTuning.ts`;
- `src/game/ai/AiDriver.ts`;
- `src/game/physics/KartController.ts`;
- the pre-balance AI/controller/tuning tests;
- removal of the temporary balance diagnostic and speed-sweep integration tests.

No character stat allocations, assets, Circuit Alpha environment/camera work, roster membership, or rebrand work are being reverted.

## Latest accepted gameplay checkpoint to restore

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Target gameplay source checkpoint: `a706f01f43f07d9b31d05ce38e3e4b67c396894c`
- Circuit Alpha environment/camera presentation remains **LIVE ACCEPTED / CLOSED**.
- Jennifer / The Hearthwarden and the Manaconda's Minigame Mayhem rebrand remain **LIVE ACCEPTED / CLOSED**.

## Active production roster state

- Lavi / Potato — AA-02
- Lula / The Verdant Hart — AA-03
- Keeg / The Mycelial Majesty — AA-04
- Kraken / The Abyssal Drifter — AA-05
- McFleurdel / The Fleur de Nuit — AA-07
- Toph / The Grave Shift — AA-08
- Manaconda / The Wayfinder — AA-09
- Krios / The Hornbreaker — AA-10
- Accu / Pink Precision — AA-11
- Jennifer / The Hearthwarden — AA-12

Cleo / The Gilded Stitch remains archived and inactive. AA-01 and AA-06 remain governed placeholders.

## Known defects / unresolved issues

- The existing production-build large-chunk warning remains known and non-blocking.
- No balance candidate is currently active.

## Deferred work

- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work.
- Further competitive balance work is deferred until Manny explicitly reopens it.

## Next recommended action

**Return to normal gameplay/roster development from the restored pre-balance runtime.**

Do not resume Candidate F/G tuning or introduce new balance formulas unless Manny explicitly asks to reopen balance work.

## Approval state

**Balance experiment: ABANDONED / ROLLBACK AUTHORIZED BY MANNY.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**

The project roadmap remains at Slice 3.
