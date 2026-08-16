# Implementation Status

## Current slice

**Slice 3 - Character Selection & Avatar Ingestion: Lavi asset preparation**

Manny manually confirmed Slice 1 lap counting, boost pads, grass slowdown, recovery, reverse-lap rejection, rear camera, and other checks on 2026-08-16. He approved the Slice 1 corrections and authorized Slice 2.

## Slice 1 gap-close completed

- Corrected forward chase-camera controls so A/Left steers visually left and D/Right steers visually right.
- Replaced the black upper viewport with a rendered dusk gradient sky and coordinated horizon fog.
- Added sustained playable speed floors of 8.5 m/s on grass and 11.5 m/s on dirt while throttle is held; both remain slower than asphalt.
- Converted dirt from a full-width forced section to an optional partial-width inside lane using signed lateral track projection.
- Shortened Circuit Alpha from approximately 1.45 km to approximately 0.90 km while preserving three laps and twelve ordered checkpoints.
- Recorded the approved changes in PRD amendment 1.3 and ADR-008.

## Slice 2 completed requirements

- DRIFT-001: Space plus steering at valid speed initiates a short Rapier hop and locks drift direction.
- DRIFT-002: drift charge exposes Blue, Orange, and Purple tiers with HUD meter, rear-wheel glow, and escalating Web Audio tones.
- DRIFT-003: releasing Space applies the highest achieved tier rather than a lower tier.
- DRIFT-004: Mini-Turbo modifies charge thresholds and boost durations; tier speed-cap multipliers are 1.08, 1.12, and 1.16.
- Drift reduces lateral grip, increases yaw response, retains player steering, and cancels on release, low speed, or extended airborne state.
- Boost pads continue to apply visible Blue boost feedback.
- The ramp surface now launches the kart; a successful landing grants an automatic short stunt boost.
- Dirt and grass remain Traction-driven and measurably distinct while preserving the approved playable floors.
- The drift HUD reports charge, tier, active boost, and airborne state without requiring the player to read during normal driving.

## Work in progress

- Avatar intake and approval contract established for one-at-a-time character development.
- Lavi is the first avatar in intake. Their supplied personality, physical description, and Potato Kart reference are recorded in `docs/avatars/LAVI.md`.
- Lavi's they/them pronouns, racing outfit, situational cheek grime, natural-potato kart body, and hidden-frame construction language are approved. The reference number `1` and `Potato Prix '24` treatment are excluded from canon.
- Lavi's reference-matched light complexion, standard stud earrings, and realistic-yet-whimsical `Potato` art direction are approved.
- Lavi's earrings are teal-blue studs. Their kart's final name is `Potato`, with approved russet skin, shallow eyes, dry soil, light scuffing, and two or three short rear sprouts. Rot, trailing roots, and an anthropomorphic face are prohibited.
- Lavi's muted-green ribbed sweater, white rainbow-accented platform boots, and Potato's practical handmade hardware are approved. Consolidated character and kart lock candidates are ready for final review.
- Manny approved Lavi's complete character and `Potato` kart locks on 2026-08-16, including simplification rules, no emblem, and limited technical adjustments that preserve the natural-potato silhouette.
- Manny assigned AA-02 Feather Technician to Lavi on 2026-08-16: Speed 5, Acceleration 8, Weight 2, Handling 9, Mini-Turbo 8, and Traction 4.
- `docs/ROSTER-MAPPING.md` now reserves AA-02 for Lavi and records all eleven remaining profiles as available. ADR-011 requires one-to-one allocation and duplicate-assignment validation.
- Manny confirmed he created the supplied Lavi reference and permits its transformation into game assets. Production art must follow the PRD's polished, colorful, kinetic, high-contrast arcade style rather than the reference collage's pixel treatment.
- `docs/assets/LAVI-ASSET-BRIEF.md` governs the approved portrait and later production deliverables.
- Manny approved Lavi portrait Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/portrait.png` is the prepared 256 x 256 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- Manny approved Rear Driver Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/rear.png` is the prepared 512 x 512 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- Manny approved Steer-left Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/steer-left.png` is the prepared 512 x 512 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- Manny approved Steer-right Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/steer-right.png` is the prepared 512 x 512 PNG RGBA derivative; transparent alpha and normal-Git runtime treatment are verified.
- PR #1 merged the approved Lavi documentation, portrait, rear frame, steer-left frame, and steer-right frame into `main` at commit `0716d8fc63c192712c96874a60adb2ed12e427c5`.
- Manny approved Hit Candidate 1 on 2026-08-16. `public/assets/characters/aa-02/driver/hit.png` is the prepared 512 x 512 PNG RGBA derivative. Its alpha ranges from fully transparent to fully opaque, the corner pixel is transparent, and normal-Git runtime treatment is verified.
- No Slice 3 character implementation has begun beyond governance and intake preparation.

## Known defects

- Slice 4 AI is intentionally not strongly competitive yet; Manny won easily and accepted that limitation for now.
- The previously reported drift/Blue-pad freeze is resolved. Commit `10864b6eeee84056d01885b74b1b3fe6e97fd7f5` contains and regression-tests the exception-safe Web Audio repair.

## Deferred work

- Remaining Slice 3 work: twelve-slot manifest/schema, validator, selection UI, kart preview, sprite/fallback pipeline, approved roster mapping, and race handoff.
- Items, AI item use, and advanced collision responses: Slice 5. AI-004 is dependency-blocked until then.
- Final HUD, production audio content, post-processing, production track art/elevation, and optimization: Slice 6.

## Next recommended action

Publish the approved hit-frame checkpoint, then prepare the victory-frame candidate.

## Validation evidence

Local validation on 2026-08-16:

- Lavi runtime assets: portrait is 256 x 256; rear, steer-left, steer-right, and hit are 512 x 512. All five are sRGB RGBA PNGs with non-opaque alpha and transparent corner pixels at the PRD paths.
- Hit transparency: source and runtime alpha both range from 0 to 1. The runtime corner pixel is `srgba(0,0,0,0)`, and a checkerboard composite shows the background through the cutout.
- Asset policy: Git attributes resolve the five fixed-size runtime PNGs to normal Git while high-resolution character art, 3D formats, and production audio remain covered by LFS rules.
- Roster ledger: twelve unique profiles are present, every profile totals 36 points, AA-02 is assigned to Lavi, and eleven profiles remain available.
- Lavi publication checkpoint: GitHub CI run `31977857986` passed for remote commit `15c39bd59e6952d41dc603460f4f100fc5ed01cc`; PR #1 merged it into `main` at `0716d8fc63c192712c96874a60adb2ed12e427c5`.
- Typecheck: strict TypeScript project build passed with no diagnostics.
- Lint: ESLint passed with zero warnings permitted.
- Tests: 6 files and 14 tests passed under Vitest `4.1.10`.
- Rapier integration tests achieve Purple charge, release the highest tier, retain finite transforms, and sustain grass speed above the approved floor.
- Configuration tests prove tier ordering, lower thresholds and longer boosts for higher Mini-Turbo, distinct speed multipliers, and dirt/grass floor ordering.
- Track tests prove an approximately 0.90 km loop, twelve checkpoints, asphalt centerline through the dirt segment, optional offset dirt lane, grass, boost, and ramp surfaces.
- Existing tests continue to prove fixed-step clamping, ten-minute finite numeric soak, skipped-checkpoint rejection, reverse finish rejection, and three consecutive valid laps.
- Clean install: `npm ci --prefer-offline --no-audit --no-fund` passed with 198 packages restored from the committed lockfile.
- Coverage: 69.84% statements, 64.60% branches, 66.66% functions, and 72.01% lines across instrumented test targets.
- Production build: Vite `8.2.1` passed; title/menu JavaScript is 12.70 kB gzip and the lazily loaded Three.js/Rapier gameplay package is 1.20 MB gzip, inside PRD download budgets.
- Formatting: Prettier check passed for all governed files.
- Blocking-freeze repair validation: 7 files and 17 tests passed, including missing-context, thrown-Web-Audio, and rejected-resume regression cases. Typecheck, lint, production build, and formatting also passed locally.
- Repair CI: GitHub Actions run `31969384244` passed for commit `10864b6eeee84056d01885b74b1b3fe6e97fd7f5` and published GitHub Pages deployment `5934890606`.
- Product-owner manual acceptance: Manny confirmed on 2026-08-16 that the repaired deployment passed all previously blocked checks, including the first Blue boost pad, all three drift tiers, highest-tier release boost, Mini-Turbo effects, HUD/wheel/tone feedback, and ramp landing stunt boost.
- Evidence checkpoint CI: GitHub Actions run `31969502068` passed for commit `4ff50635d7a4e471f7718b2a910d905d34f5d7f2` and published successful GitHub Pages deployment `5934911724`.
- CI: GitHub Actions run `31968043110` passed for Slice 2 candidate `350248375ce34659b5580878aa34f256045a907b`, including clean install, typecheck, lint, 14 tests, production build, artifact upload, and Pages deployment.
- Deployment: GitHub Pages deployment `5934663031` published candidate `350248375ce34659b5580878aa34f256045a907b` through the `github-pages` environment.
- Live URL: `https://manaconda33.github.io/accurate-artistry-game-hub/` returned HTTPS 200. The HTML and current title/menu JavaScript, CSS, and lazy gameplay JavaScript assets each returned HTTP 200.
- Early Slice 4 local candidate: strict typecheck, ESLint with zero warnings, formatting, and production build passed on 2026-08-16.
- Early Slice 4 tests: 12 files and 25 tests passed with 71.49% statement, 66.38% branch, 74.64% function, and 73.82% line coverage.
- AI route qualification: all seven configured AI profiles independently completed three checkpoint-validated Circuit Alpha laps under Rapier fixed-step simulation without player input and retained finite physics state.
- Early Slice 4 unit evidence covers dynamic spline lookahead, bounded steering, off-line correction, five-percent rubber-band bounds, race countdown, validated-progress ranking, locked finish places, relative-mass collision shares, and mobile coarse-pointer session gating.
- Early Slice 4 production build: Vite `8.2.1` passed; app-shell JavaScript is 13.54 kB gzip and the lazy Three.js/Rapier gameplay package is 1.234 MB gzip, within the PRD download budget.
- Early Slice 4 candidate CI: GitHub Actions run `31970630840` passed for commit `6580cb02618d2809181cd33f99b7357be84b2f34`, including clean lockfile install, typecheck, lint, 25 tests, coverage, and production build.
- Early Slice 4 deployment: GitHub Pages deployment `5935135220` successfully published the candidate through the `github-pages` environment at `https://manaconda33.github.io/accurate-artistry-game-hub/`.
- Product-owner manual acceptance: desktop and mobile checks passed on 2026-08-16. Manny confirmed the AI racers/grid were functional; six AI profiles were observed running the track, and the player won easily. Low AI competitiveness is accepted for now.
- Governance correction: the AI/grid checkpoint is classified as Slice 4 completed early. Slice 3 returns to Character Selection & Avatar Ingestion per PRD section 35.4.

## Last verified commit

`f608b91d63afb406e2fb404829298f3ff4f568db` - validated and deployed early Slice 4 AI/grid evidence checkpoint. The following governance checkpoint restores Slice 3 ordering and adds the avatar intake contract.
