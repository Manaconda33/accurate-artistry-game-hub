# Testing and Validation

This file is the operational source of truth for local and CI validation. Update it when commands, environments, or evidence requirements change.

## Supported environment

- Node.js 22 LTS or newer compatible release
- npm from the selected Node.js installation
- Modern Chromium, Firefox, or Safari for manual browser checks
- Git LFS 3.x before adding production binary assets

## Clean local validation

From the repository root:

```bash
npm ci
npm run typecheck
npm run lint
npm run test:ci
npm run build
```

`npm run validate` runs the validation stages after dependencies are installed. `npm run test` starts Vitest in watch mode for development.

## CI validation

GitHub Actions runs `.github/workflows/ci.yml` on pushes and pull requests targeting `main`:

1. Check out the repository.
2. Set up Node.js 22 with npm caching.
3. Install exactly from `package-lock.json` with `npm ci`.
4. Run strict TypeScript checks.
5. Run ESLint with zero warnings allowed.
6. Run Vitest once with coverage evidence.
7. Produce a Vite production build.
8. On a healthy push to `main`, publish `dist/` through the `github-pages` deployment environment.

Any failed stage fails the workflow.

The production checkout must use `lfs: true`, run `git lfs fsck`, and execute the runtime-asset signature gate through `npm run build`. A pointer file in any required runtime GLB path must fail the build rather than silently deploying a fallback kart.

## Restricted Work LFS publication

When direct Git/LFS push is blocked, follow `docs/LFS-PUBLISHING.md`. A valid checkpoint requires:

- A committed deterministic builder and pinned dependencies.
- SHA-256 checks matching every approved LFS object ID.
- An unchanged-pointer check after the runner regenerates and stages the files.
- A successful object-ID-only LFS upload.
- A fetch from GitHub after the runner deletes its local LFS cache.
- A passing `git lfs fsck` after that fetch.
- Removal of the temporary workflow before review or merge.

The bridge is not valid evidence for a binary that cannot be reproduced byte-for-byte from committed source.

## Manual confirmation deployment

Every Slice 1+ checkpoint must provide a live GitHub deployment URL, normally:

`https://manaconda33.github.io/accurate-artistry-game-hub/`

The deployment must originate from the reported checkpoint commit after validation. The product owner uses it for manual confirmation. A passing deployment does not imply approval; the next slice remains locked until explicit approval is recorded.

## Evidence expectations

Every slice done-check must record fresh evidence in `docs/IMPLEMENTATION-STATUS.md`:

- Commands executed and whether each passed.
- Test counts and meaningful coverage or scenario evidence.
- Production build result and generated output summary.
- Manual browser/device evidence when the slice changes rendered behavior.
- GitHub Actions workflow result for the checkpoint commit.
- GitHub deployment environment, live URL, and deployed commit.
- Manual confirmation scenarios appropriate to the slice.
- Known defects, deferred checks, and environmental limitations.
- Exact checkpoint commit SHA.

Code presence alone is not completion evidence.

## Slice 4 AI/grid manual matrix

- Desktop/fine-pointer session: touch controls are absent; keyboard controls remain functional.
- Mobile/coarse-pointer session: touch controls appear only in gameplay and support simultaneous accelerate-plus-steer and drift-plus-steer input.
- Countdown prevents an early start and transitions through 3, 2, 1, and GO.
- Exactly seven visible opponents join the player, live position changes during overtakes, and collisions do not produce sustained vibration.
- The player identity is absent from the AI grid, all seven AI identities are unique, and repeated races vary the sampled roster.
- A sampled production identity displays its approved kart and rear driver frame. A sampled unfinished identity remains an explicit fallback and never borrows another character's art.
- AI racers follow the course, recover after displacement, overtake, and complete validated laps without player involvement.
- Player completion records a placement from first through eighth and presents standings.
- Drift tiers, boost pads, ramp/stunt boost, off-road floors, recovery, rear view, and three-lap validation regressions remain functional.

## Slice 3 Character Select and Lavi manual matrix

- Hub `Start Grand Prix` opens Character Select rather than starting the race immediately.
- Exactly twelve slots render; Lavi displays the approved portrait and all other unfinished identities display intentional monogram placeholders.
- Selecting any slot updates its name, descriptor, six statistics, kart label, selected state, and race button without layout clipping.
- Lavi remains the default selection and `Race as Lavi` loads Potato rather than the procedural fallback kart.
- Potato reads as one opaque natural russet body with a continuous sculpted cockpit, rooted rear sprouts, connected wheels/axles, and no body clipping or translucency.
- Potato's steering wheel sits in front of Lavi, and its intended nose faces the race direction; a rear-camera check confirms the visual alignment is not reversed.
- Lavi's rear driver artwork sits convincingly in the cockpit without floating, clipping, or obscuring the kart silhouette.
- Holding visual left/right steering switches Lavi to the matching approved steer-left/steer-right frame within two rendered frames; releasing steering restores the rear frame.
- Collision impulse selects the approved hit frame briefly, and a completed player race selects the approved victory frame.
- Lavi's AA-02 profile feels nimble and responsive and remains the controlled player kart throughout the race.
- Selecting a placeholder profile starts the same race with a monogram/fallback kart and that profile's statistics; it does not borrow Lavi's identity or final art.
- Simulated missing portrait replaces the image with the correct monogram; simulated missing GLB loads the fallback kart and does not crash or change physics.
- Desktop and mobile layouts expose all twelve slots, detail panel, back action, and race action without horizontal scrolling or controls hidden outside the viewport.

## Required runtime character-asset contract

Run this matrix for every future production character, in addition to its slice-specific checks:

- CI uses an LFS-materialized checkout, passes `git lfs fsck`, and the production build rejects a pointer or bad binary signature at each required kart path.
- The deployed response uses the current controlled asset revision (or changed filename), not a cached response from an earlier object.
- The selected production kart loads in the live deployment; a fallback kart is evidence of a failed delivery check, not a passing degraded experience.
- All six approved driver states are preloaded. Rear is the safe fallback; the reverse camera selects front, visual left/right select the matching steer frame, hit overrides steering briefly, and victory overrides normal driving after the player finishes.
- Chase and rear cameras confirm the kart’s nose and steering wheel face forward of the driver. Any visual-root rotation or other axis correction is recorded in that character’s record and asset brief.
- Every production GLB declares `extras.forward: "-Z"`, and every production manifest entry uses `NEGATIVE_Z_KART_VISUAL_YAW`. Automated checks must fail if either side of this orientation contract changes independently.
- Every active production character with GLB LODs must have all required LOD paths listed in `tools/verify-runtime-assets.mjs`. Manifest activation without corresponding runtime-gate coverage is an incomplete production checkpoint.
- A product-owner test on desktop and mobile confirms the portrait, controlled kart, driver states, and orientation. Record the tested deployment, commit, browser/device result, and limitations in implementation status.

## Keeg / Mycelial Majesty manual matrix

- AA-04 renders Keeg's approved portrait, Balanced Racer descriptor, and 7 / 7 / 5 / 7 / 5 / 5 statistics.
- `Race as Keeg` loads The Mycelial Majesty rather than the fallback kart.
- The approved purple-and-silver grand-tourer body, mushroom crest and fixtures, four connected wheels, open cockpit, and angled chassis-mounted steering assembly load without clipping or floating geometry.
- Keeg sits correctly in the cockpit with the steering wheel forward of the driver.
- Keeg's driving hands align with the steering-wheel center; the wheel must not cross his abdomen or float below his hands in chase view.
- Rear, front, steer-left, steer-right, hit, and victory driver states load from `keeg-runtime-20260826-2`.
- Chase and rear views confirm the mushroom shield is at the race-forward nose and the exhausts remain behind Keeg.
- Keeg appears no more than once as an AI opponent when the player selects another character.
- CI materializes and validates all three AA-04 GLBs; each begins with the binary glTF signature and declares `extras.forward: "-Z"`.
- CI inflates every AA-04 PNG and validates its RGBA dimensions and PNG scanline filters; a header-only or partially decodable image must fail the build.
- Product-owner acceptance is recorded only after the deployed game confirms Keeg is selectable and all approved assets load as intended on desktop and mobile.

## Krios / Hornbreaker manual matrix

- AA-10 renders Krios's approved portrait, Straight-Line Heavy descriptor, and 10 / 4 / 9 / 3 / 4 / 6 statistics.
- `Race as Krios` loads The Hornbreaker rather than the fallback kart.
- The Hornbreaker's low broad chassis, integrated front ram horns, oversized studded tires, open cockpit, and twin rear exhausts load without clipping or detached housings.
- Krios sits correctly in the cockpit without floating or obscuring the kart silhouette.
- Rear, front, steer-left, steer-right, hit, and victory driver states load from the controlled Krios runtime revision.
- Chase and rear views confirm the integrated ram horns remain at the race-forward nose and the rear exhausts remain behind Krios.
- Krios appears no more than once as an AI opponent when the player selects another character.
- CI materializes and validates all three AA-10 GLBs: `kart.glb`, `kart-lod1.glb`, and `kart-lod2.glb`. Each must begin with the binary glTF signature and declare `extras.forward: "-Z"`.
- Product-owner acceptance is recorded only after the deployed game confirms Krios is present and all approved assets load as intended.

## McFleurdel / Fleur de Nuit manual matrix

- AA-07 renders McFleurdel's approved portrait, High-Speed Cruiser descriptor, and 8 / 6 / 7 / 5 / 4 / 6 statistics.
- `Race as McFleurdel` loads The Fleur de Nuit rather than the fallback kart.
- The approved black body, raised silver fleur-de-lis, black nose shield, plum throne cockpit, attached silver trim, four connected wheels, ivory candles, and violet flames load without clipping or floating geometry.
- McFleurdel sits correctly in the cockpit with the steering wheel forward of the driver.
- Rear, front, steer-left, steer-right, hit, and victory states load from `mcfleurdel-runtime-20260827-1`.
- Chase and rear views confirm the fleur-de-lis shield is at the race-forward nose and exhausts remain behind McFleurdel.
- McFleurdel appears no more than once as an AI opponent when the player selects another character.
- CI materializes and validates all three AA-07 GLBs; each begins with the binary glTF signature and declares `extras.forward: "-Z"`.
- CI inflates and validates every AA-07 PNG as complete RGBA image data.
- Product-owner acceptance is recorded only after the deployed game confirms McFleurdel is selectable and all approved assets load as intended on desktop and mobile.

## Toph / Grave Shift manual matrix

- AA-08 renders Toph's approved portrait, Turbo Bruiser descriptor, and 7 / 5 / 7 / 4 / 8 / 5 statistics.
- `Race as Toph` loads The Grave Shift rather than the fallback kart.
- The approved purple-dominant armored body, bronze perimeter, low splitter, integrated sidepods, flat skull shield, angular thorn crown, enclosed rear engine, connected wide tires, and twin violet exhausts load without clipping or floating geometry.
- Toph sits correctly in the open cockpit with the steering wheel forward of the driver.
- Rear, front, steer-left, steer-right, hit, and corrected victory states load from `toph-runtime-20260828-1`.
- Chase and rear views confirm the skull shield remains at the race-forward nose and the enclosed engine/exhausts remain behind Toph.
- Toph appears no more than once as an AI opponent when the player selects another character.
- CI materializes and validates all three AA-08 GLBs; each begins with the binary glTF signature and declares `extras.forward: "-Z"`.
- CI inflates and validates every AA-08 PNG as complete RGBA image data.
- Product-owner acceptance is recorded only after the deployed game confirms Toph is selectable and all approved assets load as intended on desktop and mobile.

## Mobile finish-state matrix

- Completing a race adds the `is-finished` state to the game shell before results become visible.
- Lap, time, speed, position, surface, performance, drift guidance, game help, and touch-driving controls leave the finished mobile view.
- The results card docks to the top of a portrait viewport and stays within 42% of the viewport height.
- Standings scroll inside their own compact region; they do not expand the card over the kart or victory driver frame.
- The lower chase-camera area remains unobstructed so the selected character's victory pose is visible.
- The results card stays above all retired touch targets, and Return to Hub remains reachable without scrolling the page.
- After the player finishes, the compact results panel leaves the live kart and victory pose clearly visible while all eight standings remain reachable.

## Manaconda / Wayfinder manual matrix

- AA-09 renders Manaconda's approved portrait and identifies the kart as The Wayfinder rather than a placeholder or fallback prototype.
- `Race as Manaconda` loads the wheel-free Wayfinder and the approved rear driver frame; no second modeled steering wheel appears.
- Manaconda sits within the recessed cockpit without floating or clipping, and the wheel contained in each driver frame reads in front of him.
- Visual left/right steering selects the matching approved frame; collision selects hit briefly; finishing selects victory.
- Chase and rear cameras confirm Wayfinder's grille/navigation core points forward and the rear satchel/twin exhausts remain behind Manaconda. No 180-degree visual correction is applied.
- The selected AA-09 profile remains 7 / 6 / 6 / 6 / 6 / 5 throughout the race.
- Desktop and mobile both load the controlled `manaconda-runtime-20260820-1` URLs rather than cached pre-integration assets.

## Accu / Pink Precision manual matrix

- AA-11 renders Accu's approved portrait and identifies the kart as Pink Precision rather than a placeholder or fallback prototype.
- `Race as Accu` loads Pink Precision and the approved rear driver frame. The compact armored hull, continuous treads, cannon, and heart-bullseye emblem remain visible.
- Accu sits inside the cockpit without floating or clipping. The 3D steering wheel stays in front of her and does not conflict with the driver art.
- Visual left/right steering selects the matching approved frame; collision selects hit briefly; finishing selects victory.
- Chase and rear cameras confirm the cannon and nose point forward while the antennae and exhausts remain behind Accu. No visual-root rotation is applied.
- The selected AA-11 profile remains 8 / 4 / 10 / 3 / 5 / 6 throughout the race.
- Desktop and mobile both load the controlled `accu-runtime-20260820-1` URLs rather than cached pre-integration assets.

## Slice 0 evidence boundary

Slice 0 validates only installation, typechecking, linting, unit testing, production build, the minimal app shell, repository organization, and CI. It does not validate rendering, physics, controls, AI, racing, items, audio playback, or performance requirements assigned to later slices.
