# Implementation Status

## Current slice

**Slice 3 — Character Selection & Avatar Ingestion**

PRD baseline: **v1.1, working implementation amendment 2.1**.

The roadmap remains at Slice 3. Competitive Slice 4 systems exist because they were implemented early under the documented sequencing correction. Items remain Slice 5 and are not authorized by the current work.

## Current balance work

A bounded Circuit Alpha balance pass is active.

Candidate F passed automated validation and a 250,000-race simulation, then was deployed for product-owner live playtest. Manny's live test on **2026-09-03** found:

- the new Handling behavior is directionally correct — lower-Handling racers visibly lose more speed while turning;
- however, with every tested player-controlled racer, Manny could establish an early lead that the AI had no realistic chance to close.

Therefore:

**Candidate F live balance gate: FAILED / NOT ACCEPTED.**

Do not treat Candidate F as final production balance merely because it remains the currently deployed build.

## Latest verified deployed checkpoint

- Repository: `Manaconda33/manacondas-minigame-mayhem`
- Live URL: `https://manaconda33.github.io/manacondas-minigame-mayhem/`
- Candidate F balance PR: **#86**
- Candidate F runtime merge: `faedd84e6e86ab7adca1d5f8ed06742d6ab70920`
- Deployment-record commit: `c56781d9d3ee4878c5ef47a09fcfc2d7535099dc`
- Main CI / Pages run: **33820024902** — validation passed and deployment passed
- Product-owner state: **LIVE BALANCE REJECTED — AI PACE TOO LOW**

The prior Circuit Alpha environment/camera pass remains separately **LIVE ACCEPTED / CLOSED**.

## Candidate F behavior retained as useful

Candidate F introduced the following shared balance behavior:

- Speed 7 remains anchored at **29.5 m/s**;
- Speed 1–10 sustained-asphalt spread is **3.0 m/s**;
- Handling contributes to shared physical corner-speed retention for both player and AI;
- Circuit Alpha AI corner demand uses normalized lookahead-angle geometry;
- Mini-Turbo-aware AI seeks valid drift opportunities and observes governed drift tiers;
- Weight collision retention, Traction, surfaces, boost pads, ramp behavior, Circuit Alpha geometry, roster sampling, individual racer stat allocations, assets, and item scope remain unchanged.

Manny's live feedback explicitly supports retaining the shared Handling slowdown. The failed gate concerns AI competitiveness, not the concept that low Handling should cost more speed while turning.

## Candidate F automated evidence

Candidate F source checkpoint: `0fce4d2be4c41ff2f7fddf69d13d74306a78f106`.

PR CI and final documented-head validation passed with:

- Git LFS verification;
- strict TypeScript typecheck;
- ESLint with zero warnings;
- **20/20 test files and 102/102 tests**;
- all 12 manifest profiles completing all seven runtime AI profiles over valid three-lap Rapier simulations;
- all 84 diagnostic racer/profile runs recording **0% grass time**;
- runtime asset verification;
- production Vite build.

The final Candidate F 250,000-race moderate-variance Monte Carlo produced these conditional win rates:

- Keeg — **19.54%**
- Krios — **18.56%**
- McFleurdel — **18.12%**
- Lavi — **14.21%**
- Manaconda — **13.70%**
- Jennifer — **11.76%**
- Racer 06 — **11.28%**
- Kraken — **10.36%**
- Racer 01 — **8.68%**
- Lula — **8.18%**
- Accu — **7.88%**
- Toph — **7.74%**

Those results remain useful for character-vs-character balance, but the live gate proved that AI-vs-player execution was not represented strongly enough by the simulation model.

## Candidate G — active experiment

Draft PR **#87 — Candidate G: restore competitive AI corner pace** is the bounded follow-up.

Diagnosis: the shared kart controller already applies Handling-based corner-speed loss to both player and AI, but Candidate F also gave AI an anticipatory target that could impose roughly **34–48%** full-demand corner slowdown. A player did not receive that second AI-only penalty. The PRD-governed trailing top-speed allowance is capped at **4%**, so it could not make up the resulting corner-time loss.

Candidate G changes only that AI anticipatory target:

- full-demand anticipation becomes a modest **4–10%** range based on AI pace;
- shared Handling physics remains the primary corner-speed limiter;
- higher-pace AI remains slightly faster through equivalent corners;
- the existing 4% trailing allowance remains unchanged.

Protected behavior remains unchanged:

- Candidate F 3.0 m/s Speed spread;
- every racer stat allocation;
- shared Handling slowdown;
- Mini-Turbo thresholds/tiers/boosts;
- Weight collision behavior;
- Traction/surfaces;
- boost pads and ramp/stunt boost;
- Circuit Alpha geometry/checkpoints;
- starting grid and roster sampling;
- assets and item scope.

Candidate G branch: `experiment/candidate-g-ai-pace`.

Candidate G draft PR: **#87**.

Current Candidate G head at the time this status was written: `64023b76e8fe1be6469aec7bb73ea184519fcbe6`.

Candidate G is **not deployed and not approved**. Automated validation is required before another live playtest can be proposed.

## Candidate G validation gate

Before deployment:

1. typecheck, lint, full Vitest/coverage, runtime-asset verification, and production build must pass;
2. all 12 manifest profiles must complete all seven runtime AI profiles over valid three-lap Rapier simulations;
3. grass exposure and road-boundary regressions must stay within existing limits;
4. AI three-lap times must improve materially versus Candidate F;
5. character ordering must not collapse into a new single-stat runaway;
6. Manny must authorize another live playtest checkpoint before Candidate G is merged/deployed.

At the time this status was written, GitHub Actions run **33821294439** was stalled in `npm ci` before typecheck/test execution, and superseding run **33821749308** was pending. This is not passing evidence and is not recorded as a Candidate G code failure.

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

- **Balance blocker:** deployed Candidate F AI cannot currently challenge a competent player after the player establishes an early lead.
- Candidate G automated evidence is not yet complete.
- The existing production-build large-chunk warning remains known and non-blocking.

## Deferred work

- AA-01 and AA-06 remain unfilled.
- Items remain Slice 5 work.
- No new track, asset, Weight, Traction, or individual-stat rebalance is authorized by Candidate G.

## Next recommended action

**Validate Candidate G, compare its seven-profile Rapier times against Candidate F, then stop at Manny's approval gate before any new deployment.**

The next live test, if approved, should specifically ask whether AI racers can remain within striking distance of a competent player and exploit the 4% trailing allowance without feeling like obvious rubber-band cheating.

## Approval state

**Candidate F simulation gate: APPROVED.**

**Candidate F live balance gate: FAILED / NOT ACCEPTED.**

**Candidate G: DRAFT EXPERIMENT / AUTOMATED VALIDATION REQUIRED.**

**Circuit Alpha environment-art / camera polish: LIVE ACCEPTED / CLOSED.**
