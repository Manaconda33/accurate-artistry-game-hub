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
- AI racers follow the course, recover after displacement, overtake, and complete validated laps without player involvement.
- Player completion records a placement from first through eighth and presents standings.
- Drift tiers, boost pads, ramp/stunt boost, off-road floors, recovery, rear view, and three-lap validation regressions remain functional.

## Slice 0 evidence boundary

Slice 0 validates only installation, typechecking, linting, unit testing, production build, the minimal app shell, repository organization, and CI. It does not validate rendering, physics, controls, AI, racing, items, audio playback, or performance requirements assigned to later slices.
