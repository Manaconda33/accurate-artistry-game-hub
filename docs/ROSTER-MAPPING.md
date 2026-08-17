# Roster profile allocation

This ledger is the source of truth for mapping approved Accurate Artistry characters to the twelve fixed PRD balance profiles. Each AA profile may be assigned to one character only. An assigned profile is unavailable to every later character unless Manny explicitly approves a remap.

## Allocation rules

- Every production character must use one AA-01 through AA-12 profile.
- Each profile may be assigned once.
- Each character may hold one profile.
- Character appearance or personality may inform discussion but cannot determine a mapping without an approved driving-feel decision.
- A locked mapping records the character, kart, rationale, approval date, and governing decision.
- The manifest validator must reject duplicate profile IDs or duplicate production-character assignments.
- Remapping a locked profile requires Manny's approval and updates to this ledger, the affected avatar records, `docs/DECISIONS.md`, and implementation evidence.

## Required review and update sequence

For every new character:

1. Read this ledger before recommending an archetype.
2. Remove every `Assigned` profile from consideration.
3. Compare the character's approved driving feel, strengths, weaknesses, and weight class against the remaining profiles.
4. Present the strongest recommendation and its tradeoffs to Manny for approval.
5. After approval, update the selected ledger row and add its locked-mapping rationale in the same checkpoint.
6. Update the character record, decision log when required, and implementation evidence so all sources agree.

Do not reserve or mark a profile `Assigned` before Manny approves the mapping. If the ledger and an avatar record disagree, stop character implementation until the conflict is resolved.

## Profile ledger

Stat order is Speed / Acceleration / Weight / Handling / Mini-Turbo / Traction.

| Profile | Archetype           | Class         | Stats                  | Status    | Character | Kart   | Approval          |
| ------- | ------------------- | ------------- | ---------------------- | --------- | --------- | ------ | ----------------- |
| AA-01   | Feather Sprinter    | Featherweight | 6 / 9 / 2 / 8 / 7 / 4  | Available | -         | -      | -                 |
| AA-02   | Feather Technician  | Featherweight | 5 / 8 / 2 / 9 / 8 / 4  | Assigned  | Lavi      | Potato | Manny, 2026-08-16 |
| AA-03   | Feather Dirt Ace    | Featherweight | 5 / 8 / 3 / 7 / 6 / 7  | Available | -         | -      | -                 |
| AA-04   | Balanced Racer      | Medium        | 7 / 7 / 5 / 7 / 5 / 5  | Available | -         | -      | -                 |
| AA-05   | Drift Specialist    | Medium        | 6 / 7 / 5 / 6 / 9 / 3  | Available | -         | -      | -                 |
| AA-06   | Grip Specialist     | Medium        | 6 / 6 / 5 / 7 / 5 / 7  | Available | -         | -      | -                 |
| AA-07   | High-Speed Cruiser  | Cruiser       | 8 / 6 / 7 / 5 / 4 / 6  | Available | -         | -      | -                 |
| AA-08   | Turbo Bruiser       | Cruiser       | 7 / 5 / 7 / 4 / 8 / 5  | Available | -         | -      | -                 |
| AA-09   | Technical Cruiser   | Cruiser       | 7 / 6 / 6 / 6 / 6 / 5  | Assigned  | Manaconda | The Wayfinder | Manny, 2026-08-16 |
| AA-10   | Straight-Line Heavy | Heavyweight   | 10 / 4 / 9 / 3 / 4 / 6 | Available | -         | -      | -                 |
| AA-11   | Collision Tank      | Heavyweight   | 8 / 4 / 10 / 3 / 5 / 6 | Available | -         | -      | -                 |
| AA-12   | All-Surface Heavy   | Heavyweight   | 8 / 5 / 8 / 4 / 4 / 7  | Available | -         | -      | -                 |

## Locked mapping rationale

### AA-02: Lavi / Potato

Lavi's intended driving identity is nimble, responsive, and technical. Acceleration 8, Handling 9, and Mini-Turbo 8 reward quick reactions, precise lines, and controlled drifting. Speed 5, Weight 2, and Traction 4 keep the profile distinct: Lavi gives up collision resistance, off-road forgiveness, and top-end speed in exchange for immediate control. Manny approved the mapping on 2026-08-16.


### AA-09: Manaconda / The Wayfinder

Manaconda is a prepared, heavily equipped explorer whose driving identity is composed route-reading rather than twitchy reflexes or brute force. Speed 7 preserves journeying momentum; the four middle values at 6 reward deliberate all-round competence; Weight 6 gives the equipped field vehicle substance without making it a heavyweight; and Traction 5 retains a real off-road weakness. Manny approved the mapping on 2026-08-16.
