# Roster profile allocation

This ledger is the source of truth for mapping approved Accurate Artistry characters to the twelve fixed PRD balance profiles. Each AA profile may be assigned to one active production character only. An assigned profile is unavailable to every later character unless Manny explicitly approves a remap or retires the assigned character from production.

## Allocation rules

- Every active production character must use one AA-01 through AA-12 profile.
- Each profile may be assigned once among active production characters.
- Each active production character may hold one profile.
- Character appearance or personality may inform discussion but cannot determine a mapping without an approved driving-feel decision.
- A locked mapping records the character, kart, rationale, approval date, and governing decision.
- When Manny retires a character from production, the profile returns to `Available` unless he explicitly reserves it. Historical mapping and package details remain in `docs/CHARACTER-ARCHIVE.md` and the character records.
- The manifest validator must reject duplicate profile IDs or duplicate active production-character assignments.
- Remapping a locked active profile requires Manny's approval and updates to this ledger, the affected avatar records, `docs/DECISIONS.md`, and implementation evidence.

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

| Profile | Archetype           | Class         | Stats                  | Status    | Character  | Kart                 | Approval          |
| ------- | ------------------- | ------------- | ---------------------- | --------- | ---------- | -------------------- | ----------------- |
| AA-01   | Feather Sprinter    | Featherweight | 6 / 9 / 2 / 8 / 7 / 4  | Available | -          | -                    | -                 |
| AA-02   | Feather Technician  | Featherweight | 5 / 8 / 2 / 9 / 8 / 4  | Assigned  | Lavi       | Potato               | Manny, 2026-08-16 |
| AA-03   | Feather Dirt Ace    | Featherweight | 5 / 8 / 3 / 7 / 6 / 7  | Available | -          | -                    | -                 |
| AA-04   | Balanced Racer      | Medium        | 7 / 7 / 5 / 7 / 5 / 5  | Assigned  | Keeg       | The Mycelial Majesty | Manny, 2026-08-26 |
| AA-05   | Drift Specialist    | Medium        | 6 / 7 / 5 / 6 / 9 / 3  | Assigned  | Kraken     | The Abyssal Drifter  | Manny, 2026-08-21 |
| AA-06   | Grip Specialist     | Medium        | 6 / 6 / 5 / 7 / 5 / 7  | Available | -          | -                    | -                 |
| AA-07   | High-Speed Cruiser  | Cruiser       | 8 / 6 / 7 / 5 / 4 / 6  | Assigned  | McFleurdel | The Fleur de Nuit    | Manny, 2026-08-27 |
| AA-08   | Turbo Bruiser       | Cruiser       | 7 / 5 / 7 / 4 / 8 / 5  | Available | -          | -                    | -                 |
| AA-09   | Technical Cruiser   | Cruiser       | 7 / 6 / 6 / 6 / 6 / 5  | Assigned  | Manaconda  | The Wayfinder        | Manny, 2026-08-16 |
| AA-10   | Straight-Line Heavy | Heavyweight   | 10 / 4 / 9 / 3 / 4 / 6 | Assigned  | Krios      | The Hornbreaker      | Manny, 2026-08-22 |
| AA-11   | Collision Tank      | Heavyweight   | 8 / 4 / 10 / 3 / 5 / 6 | Assigned  | Accu       | Pink Precision       | Manny, 2026-08-20 |
| AA-12   | All-Surface Heavy   | Heavyweight   | 8 / 5 / 8 / 4 / 4 / 7  | Available | -          | -                    | -                 |

## Locked mapping rationale

### AA-07: McFleurdel / The Fleur de Nuit

McFleurdel's intended driving identity is elegant, deliberate, and fast rather than twitchy or boost-dependent. Speed 8 and Weight 7 give The Fleur de Nuit strong momentum and substantial road presence. Acceleration 6 and Traction 6 keep it controlled, while Handling 5 and Mini-Turbo 4 make committed lines and anticipation more important than rapid corrections or drift chaining. Manny approved the mapping on 2026-08-27.

### AA-02: Lavi / Potato

Lavi's intended driving identity is nimble, responsive, and technical. Acceleration 8, Handling 9, and Mini-Turbo 8 reward quick reactions, precise lines, and controlled drifting. Speed 5, Weight 2, and Traction 4 keep the profile distinct: Lavi gives up collision resistance, off-road forgiveness, and top-end speed in exchange for immediate control. Manny approved the mapping on 2026-08-16.

### AA-04: Keeg / The Mycelial Majesty

Keeg's intended driving identity is versatile, responsive, technically capable, and expressive without becoming a pure specialist. Speed 7, Acceleration 7, and Handling 7 create a broadly competent racer that rewards deliberate control. Weight 5 gives The Mycelial Majesty enough presence for its substantial enchanted grand-tourer form without turning Keeg into a heavyweight. Mini-Turbo 5 preserves Kraken's dedicated drift-specialist role, while Traction 5 leaves meaningful consequences for poor lines and off-road mistakes. Manny approved the mapping on 2026-08-26.

### AA-09: Manaconda / The Wayfinder

Manaconda is a prepared, heavily equipped explorer whose driving identity is composed route-reading rather than twitchy reflexes or brute force. Speed 7 preserves journeying momentum; the four middle values at 6 reward deliberate all-round competence; Weight 6 gives the equipped field vehicle substance without making it a heavyweight; and Traction 5 retains a real off-road weakness. Manny approved the mapping on 2026-08-16.

### AA-11: Accu / Pink Precision

Accu's compact tank-inspired kart is the roster's collision specialist. Weight 10 and Handling 3 reward committed lines and contact rather than quick corrections. Speed 8 keeps Pink Precision threatening once it builds momentum, while Acceleration 4 makes mistakes costly. Mini-Turbo 5 and Traction 6 preserve basic race usability without weakening the heavyweight identity. Manny approved the mapping on 2026-08-20.

### AA-05: Kraken / The Abyssal Drifter

Kraken is the roster's dedicated drift specialist. Mini-Turbo 9 rewards deliberate drift chains and repeated boost conversion. Acceleration 7 helps him recover momentum between corners, while Speed 6, Weight 5, and Handling 6 keep the profile controlled rather than twitchy. Traction 3 is the defining weakness: poor lines and off-road mistakes cost meaningful time. Manny approved the mapping on 2026-08-21.

### AA-10: Krios / The Hornbreaker

Krios is the roster's straight-line heavyweight bully. Speed 10 and Weight 9 give The Hornbreaker dominant momentum and collision presence. Acceleration 4 and Handling 3 make recovery and tight corrections deliberately costly, while Mini-Turbo 4 prevents overlap with drift-focused racers. Traction 6 keeps the kart usable without turning Krios into the all-surface heavy. Manny approved the mapping on 2026-08-22.

## Historical archived mappings

### AA-06: Cleo / The Gilded Stitch

Manny approved Cleo for AA-06 on 2026-08-21. Handling 7 and Traction 7 supported her precision-craft, stable-line identity while moderate remaining values kept her distinct from the drift and heavyweight specialists. Manny retired Cleo from production on 2026-08-26 while preserving her complete approved package for possible restoration. AA-06 is therefore available again. See `docs/CHARACTER-ARCHIVE.md` for the durable archive and restoration gate.
