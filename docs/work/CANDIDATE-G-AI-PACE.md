# Candidate G — AI Pace Correction

## Trigger

Candidate F passed simulation and was deployed for product-owner live playtest. Manny's live test on 2026-09-03 found that the shared Handling slowdown felt correct, but every tested player-controlled racer could establish an early lead that the AI had no realistic chance to close.

Candidate F therefore does **not** pass the live acceptance gate.

## Diagnosis

The shared kart controller applies Handling-based physical corner-speed retention to both player and AI racers. AI racers additionally compute an anticipatory corner target through `aiCornerTargetSpeed`.

Under Candidate F, that AI-only anticipatory target used a 34–48% full-demand corner penalty before the shared Handling limit. A human player experiences the shared Handling limit but not that additional AI-only reduction. The PRD-governed trailing top-speed allowance remains capped at 4%, so it cannot recover the resulting corner-time deficit.

## Candidate G scope

Candidate G changes only the AI anticipatory corner-speed target:

- full-demand AI anticipation is reduced to a 4–10% range based on AI pace;
- Handling still has a small effect on AI judgment, but the shared physical Handling limit remains the primary corner-speed mechanism;
- higher-pace AI remains slightly faster through equivalent corners;
- the existing 4% trailing allowance is unchanged.

Protected behavior remains unchanged:

- Candidate F 3.0 m/s Speed 1–10 spread;
- every individual racer stat allocation;
- shared Handling corner-speed retention for player and AI;
- Mini-Turbo thresholds, tiers, and boost values;
- Weight collision retention;
- Traction and surface behavior;
- boost pads and ramp/stunt boost;
- Circuit Alpha geometry/checkpoints;
- roster sampling and starting grid;
- assets and item scope.

## Validation gate

Before Candidate G can be deployed:

1. Typecheck, lint, full Vitest/coverage, runtime-asset verification, and production build must pass.
2. All 12 manifest profiles must complete all seven runtime AI profiles over valid three-lap Rapier simulations.
3. Grass exposure and road-boundary regressions must remain within the existing limits.
4. Candidate G three-lap AI times must show a material pace improvement versus Candidate F rather than merely passing unit tests.
5. Character ordering must not collapse into a new single-stat runaway.
6. Candidate G remains draft-only until Manny authorizes another deployed live playtest.

## Approval state

**Candidate F live gate: FAILED — AI unable to challenge a competent player.**

**Candidate G: EXPERIMENT / AUTOMATED VALIDATION REQUIRED.**
