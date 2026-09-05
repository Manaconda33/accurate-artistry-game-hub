from pathlib import Path

path = Path('docs/IMPLEMENTATION-STATUS.md')
text = path.read_text()

old_header = '**Slice 5 - Item Boxes, Weapons & Position-Based Distribution - FOUNDATION CI PASSED / MANNY REVIEW PENDING**'
new_header = '**Slice 5 - Item Boxes, Weapons & Position-Based Distribution - VISIBLE ITEM BOXES IMPLEMENTED / PR #98 CI PASSED / MANNY REVIEW PENDING**'
if old_header not in text:
    raise SystemExit('Current-slice header anchor not found')
text = text.replace(old_header, new_header, 1)

old_paragraph = "Slice 3 Character Selection & Avatar Ingestion is **COMPLETE / LIVE ACCEPTED**. The already-completed out-of-order Slice 4 AI/grid checkpoint remains retained. Manny approved the reconciled Slice 5 item-system implementation contract and exit checklist on 2026-09-05. The approved design is `docs/SLICE-5-ITEM-SYSTEM-DESIGN.md` and ADR-061. Slice 5 implementation has begun on `feature/slice-5-items-foundation`. The first bounded increment adds typed item configuration, weighted selection/restriction logic, one-slot inventory, and item-box lifecycle state; race-scene item boxes and item effects are not yet integrated."
new_paragraph = "Slice 3 Character Selection & Avatar Ingestion is **COMPLETE / LIVE ACCEPTED**. The already-completed out-of-order Slice 4 AI/grid checkpoint remains retained. Manny approved the reconciled Slice 5 item-system implementation contract and exit checklist on 2026-09-05. The approved design is `docs/SLICE-5-ITEM-SYSTEM-DESIGN.md` and ADR-061. PR #97 merged the first bounded Slice 5 foundation increment to `main` at `5d3466edf9fa6ed8b3380cdfbf0c352e5d70a61f`. PR #98 on `feature/slice-5-item-boxes` now adds the second bounded increment: visible Circuit Alpha item boxes, player/AI collection triggers, selection lock at collection time, shared-world lifecycle presentation, and cleanup. Roulette/HUD/item-use behavior and all item effects remain unimplemented."
if old_paragraph not in text:
    raise SystemExit('Foundation summary paragraph anchor not found')
text = text.replace(old_paragraph, new_paragraph, 1)

old_gate = '**Approval gate:** Slice 5 gameplay implementation is authorized on a dedicated feature branch. Slice 6 remains locked until Slice 5 is fully validated, deployed, and live accepted by Manny.'
new_gate = '**Approval gate:** PR #98 is CI-green and awaits Manny review. Do not merge PR #98 or begin the roulette/HUD/item-use increment until Manny approves this checkpoint. Slice 6 remains locked until Slice 5 is fully validated, deployed, and live accepted by Manny.'
if old_gate not in text:
    raise SystemExit('Approval gate anchor not found')
text = text.replace(old_gate, new_gate, 1)

checkpoint = '''

## Slice 5 visible item-box checkpoint

PR #97 — **Start Slice 5 item-system foundation** — merged to `main` at `5d3466edf9fa6ed8b3380cdfbf0c352e5d70a61f`. Post-merge main CI / Pages run **33999548615** passed validation and deployment.

PR #98 — **Add visible Slice 5 item boxes** — is open on `feature/slice-5-item-boxes` at reviewed head `a30c6161ebb8ba097a3f39f2b7ad0d8cda96ff86` before this status-only record update. Its bounded implementation provides:

- 32 original procedural pickup prisms in four rows of eight at approximately 9%, 34%, 62%, and 89% lap progress;
- legal Circuit Alpha corridor placement across eight lateral lanes per row;
- proximity pickup for the player and seven AI racers;
- one-slot inventory eligibility and rank/gap-weighted item selection locked at collection time;
- Hyper-Drive prerequisite filtering and the initial Apex global-selection cooldown gate;
- shared-world successful collection behavior: pop, immediate non-collectibility, disappearance, fade-back, then collectibility at approximately 4.5 seconds;
- nearest-box matching that prevents one racer from double-triggering overlapping adjacent pickup radii in the same simulation step;
- pause-safe lifecycle timing through the fixed-step race simulation; and
- explicit geometry/material cleanup on disposal.

PR #98 CI run **33999886686** passed after CI exposed and the branch corrected two real implementation defects: strict lint findings in the initial presentation/cleanup code, and an overlapping-radius double-pickup edge case. Final validation passed LFS verification, `npm ci`, strict typecheck, zero-warning lint, **20 Vitest files / 107 tests**, **90.21% overall statement coverage**, **93.64% `game/items` statement coverage**, runtime-asset verification, and the production Vite build. The existing large-chunk warning remains non-blocking.

This checkpoint is **not deployed** because PR #98 remains intentionally unmerged pending Manny review. Because roulette/HUD/item-use is outside this increment, a racer that successfully acquires an item keeps the one-slot inventory occupied and therefore cannot collect another box yet. This is the real inventory contract, not a temporary bypass.

**Review target:** approve the implementation checkpoint for merge/deployment, then perform live visual acceptance of all four rows, pickup readability, the collection pop, disappearance, approximately 4.5-second refresh, and fade-back. Roulette/HUD/item-use remains the next bounded increment only after this gate passes.
'''
anchor = new_gate + '\n'
text = text.replace(anchor, anchor + checkpoint, 1)

# Correct stale approval language if it still exists later in the historical status file.
text = text.replace(
    '**Slice 5 implementation: AUTHORIZED; NOT YET BEGUN / NOT COMPLETE.**',
    '**Slice 5 implementation: IN PROGRESS; FOUNDATION MERGED / VISIBLE ITEM-BOX PR #98 AWAITING MANNY REVIEW.**',
)
text = text.replace(
    '- Items remain Slice 5 work and are not authorized by this checkpoint.',
    '- Remaining Slice 5 work includes roulette/HUD/input, item activation and effects, AI item-use policy, interaction/counter validation, soak/performance evidence, deployment, and live acceptance.',
)

old_next = "Merge the approved Slice 5 documentation checkpoint after CI is healthy. Then create a dedicated Slice 5 implementation branch and implement only the bounded item-system contract in `docs/SLICE-5-ITEM-SYSTEM-DESIGN.md`: configuration/selection first, then inventory/item boxes, shared effects and lifecycle, item families/counters, AI item policy, HUD/mobile input, soak/performance evidence, deployment, and product-owner live acceptance."
new_next = "Manny reviews PR #98. If approved, merge and deploy the visible item-box checkpoint, then complete live visual acceptance of placement/readability and the pop/disappear/fade-back lifecycle. Only after that acceptance should the next bounded Slice 5 increment add roulette, held-item HUD, and desktop/mobile item-use input."
if old_next in text:
    text = text.replace(old_next, new_next, 1)

path.write_text(text)
