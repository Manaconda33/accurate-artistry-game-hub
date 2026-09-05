from pathlib import Path

DESIGN = Path('docs/SLICE-5-ITEM-SYSTEM-DESIGN.md')
DECISIONS = Path('docs/DECISIONS.md')
STATUS = Path('docs/IMPLEMENTATION-STATUS.md')


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    if old not in text:
        raise RuntimeError(f'Missing expected {label} anchor')
    return text.replace(old, new, 1)


design = DESIGN.read_text(encoding='utf-8')
design = replace_once(
    design,
    '- A successful collection deactivates that specific box for every racer for approximately 4.5 seconds.\n- A racer already carrying an item passes through without consuming or deactivating the box.',
    '- A successful collection deactivates that specific box for every racer for approximately 4.5 seconds.\n- On collection, the box plays a brief visible pop as it disappears; it becomes non-collectible immediately rather than lingering as an active pickup.\n- After the pop, the box is fully absent from the field for the inactive portion of the respawn window.\n- Near the end of the same approximately 4.5-second respawn window, the box fades back into existence while remaining non-collectible; it becomes collectible only when the fade completes.\n- Initial implementation timing uses an approximately 0.12-second pop and 0.45-second fade-back as tunable presentation constants. The required product behavior is pop -> absent -> fade back -> collectible.\n- A racer already carrying an item passes through without consuming or deactivating the box.',
    'item-box presentation',
)
design = replace_once(
    design,
    '- [ ] Item boxes respawn after approximately 4.5 seconds.\n- [ ] Four eight-box rows exist at the approved approximate lap-progress locations and remain in the legal race corridor.',
    '- [ ] Item boxes pop on successful collection, immediately stop being collectible, disappear from the field, then fade back before becoming collectible at approximately 4.5 seconds.\n- [ ] Four eight-box rows exist at the approved approximate lap-progress locations and remain in the legal race corridor.',
    'item-box exit checklist',
)
DESIGN.write_text(design, encoding='utf-8')

decisions = DECISIONS.read_text(encoding='utf-8')
if '## ADR-062: Clarify Slice 5 item-box collection and respawn presentation' not in decisions:
    decisions += '''\n\n## ADR-062: Clarify Slice 5 item-box collection and respawn presentation\n\n- **Date:** 2026-09-05\n- **Status:** Approved for implementation\n- **Context:** After authorizing Slice 5 implementation, Manny clarified the intended shared item-box presentation: a collected box should visibly pop, disappear from the field while unavailable, then fade back into existence when it refreshes.\n- **Decision:** A successful collection makes the box non-collectible immediately, plays a brief pop/disappearance transition, hides the box for the inactive portion of the existing approximately 4.5-second respawn window, then fades it back while it is still non-collectible. The box becomes collectible only after the fade completes. The shared-world lockout and one-slot inventory rules are unchanged.\n- **Initial engineering defaults:** Use approximately 0.12 seconds for the pop and 0.45 seconds for the fade-back. These are configuration values that may be refined without changing the approved pop -> absent -> fade back -> collectible sequence or the approximately 4.5-second total respawn target.\n- **Scope:** Presentation/lifecycle clarification only. This does not change item probabilities, box ownership, row placement, inventory rules, roulette timing, or any item effect.\n- **Approval:** Manny approved Slice 5 implementation and supplied this item-box behavior clarification on 2026-09-05.\n'''
DECISIONS.write_text(decisions, encoding='utf-8')

status = STATUS.read_text(encoding='utf-8')
status = replace_once(
    status,
    '**Slice 5 - Item Boxes, Weapons & Position-Based Distribution - DESIGN APPROVED / IMPLEMENTATION AUTHORIZED**',
    '**Slice 5 - Item Boxes, Weapons & Position-Based Distribution - IMPLEMENTATION STARTED / FOUNDATION REVIEW PENDING**',
    'current Slice 5 status',
)
status = replace_once(
    status,
    'No Slice 5 gameplay code is complete at this checkpoint; `src/game/items/` remains implementation scaffolding until the dedicated feature branch begins.',
    'Slice 5 implementation has begun on `feature/slice-5-items-foundation`. The first bounded increment adds typed item configuration, weighted selection/restriction logic, one-slot inventory, and item-box lifecycle state; race-scene item boxes and item effects are not yet integrated.',
    'foundation start status',
)
if '## Slice 5 foundation implementation checkpoint' not in status:
    status += '''\n\n## Slice 5 foundation implementation checkpoint\n\nManny authorized Slice 5 implementation on 2026-09-05 and clarified the item-box collection presentation under ADR-062. The first bounded feature branch is `feature/slice-5-items-foundation`.\n\nImplemented for review in this increment:\n\n- one typed registry containing all fifteen approved item IDs, display names, charge counts, and the exact eight-rank probability matrix;\n- configuration for the four approved item-box row progress points and eight boxes per row;\n- weighted item selection with the PRD 1.00-1.35 gap factor, Hyper-Drive 45 m eligibility threshold, Apex/runtime availability filtering, and post-filter weighted selection;\n- one-slot inventory with multi-charge consumption;\n- item-box lifecycle state implementing collection pop, immediate non-collectibility, hidden respawn interval, fade-back, and final collectible restoration at the approximately 4.5-second target;\n- focused Vitest coverage for table totals, restrictions, inventory, and the item-box lifecycle.\n\nThe pop/fade implementation begins with approximately 0.12-second pop and 0.45-second fade-back configuration values. These are reversible presentation defaults; the approved sequence is pop -> absent -> fade back -> collectible.\n\nNot yet implemented in this checkpoint: Circuit Alpha box meshes/triggers/row placement, roulette/HUD/input integration, race pickup wiring, projectiles, hazards, buffs/debuffs, AI item use, or any of the fifteen item effects. This increment must pass CI and Manny review before merge or the next implementation increment.\n'''
STATUS.write_text(status, encoding='utf-8')
