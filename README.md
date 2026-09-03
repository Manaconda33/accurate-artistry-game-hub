# Manaconda's Minigame Mayhem

Manaconda's Minigame Mayhem is a modular HTML5 minigame collection whose first playable experience is a 3D kart racer with illustrated 2D drivers inside stylized 3D karts. The approved requirements baseline is Product Requirements Document v1.1.

The canonical repository `Manaconda33/manacondas-minigame-mayhem` is intentionally public. Publication and deployment changes remain approval-gated under the PRD workflow.

## Current state

**Current slice:** Slice 3 - Character Selection & Avatar Ingestion.

The current implementation includes the competitive Grand Prix systems defined for Slice 4, which were completed early because of a documented sequencing error. Slice 3 has resumed in the PRD-defined order and begins with deliberate, one-at-a-time avatar intake and approval. No production identity, likeness, kart, or balance-slot mapping will be inferred. Items remain Slice 5.

## Live test build

[Open the latest GitHub Pages checkpoint](https://manaconda33.github.io/manacondas-minigame-mayhem/)

Every Slice 1+ checkpoint is deployed through the repository’s `github-pages` environment for product-owner manual confirmation.

## Local setup

Prerequisites:

- Node.js 22 or newer compatible release
- npm
- Git LFS before adding production binary assets

```bash
git lfs install
npm ci
npm run dev
```

Vite prints the local development URL when the server starts.

## Commands

| Command                | Purpose                                              |
| ---------------------- | ---------------------------------------------------- |
| `npm run dev`          | Start the Vite development server.                   |
| `npm run build`        | Typecheck and create a production build in `dist/`.  |
| `npm run typecheck`    | Run strict TypeScript validation.                    |
| `npm run lint`         | Run ESLint with zero warnings permitted.             |
| `npm run test`         | Run Vitest in watch mode.                            |
| `npm run test:ci`      | Run Vitest once with coverage for CI.                |
| `npm run format`       | Apply Prettier formatting.                           |
| `npm run format:check` | Verify formatting without changing files.            |
| `npm run validate`     | Run typecheck, lint, CI tests, and production build. |

## Architecture summary

- **Application:** TypeScript single-page application built by Vite.
- **Rendering baseline:** Three.js.
- **Physics baseline:** Rapier 3D through `@dimforge/rapier3d-compat`.
- **Audio baseline:** Howler.js backed by Web Audio.
- **Testing:** Vitest with jsdom and V8 coverage.
- **Quality gates:** strict TypeScript, ESLint, Prettier, unit tests, production build, and GitHub Actions.
- **Asset governance:** Fixed-size runtime avatar PNGs live in normal Git. Git LFS remains required for production 3D models, audio, and high-resolution source art.
- **Continuity:** repository documents are authoritative; Cowork/chat history is supplemental.

The `src/game/` directories reserve PRD-defined system boundaries. Their presence is architectural scaffolding, not evidence that those systems are implemented.

## Repository map

- `docs/` - approved PRD, working Markdown PRD, decisions, testing rules, and implementation status.
- `public/assets/` - governed asset roots for characters, karts, track, items, and audio.
- `src/app/` - game-hub application shell.
- `src/audio/` - future audio integration boundary.
- `src/config/` and `src/schemas/` - future configuration and validation boundaries.
- `src/game/` - future gameplay system boundaries organized by domain.
- `src/ui/` - future interface and HUD boundary.
- `tests/` - automated test suite.
- `.github/workflows/` - repository CI.

## Project source of truth

- [Approved implementation PRD](docs/PRD.md)
- [Word PRD v1.1](docs/Accurate_Artistry_Game_Hub_PRD_v1.1.docx)
- [Architecture decisions](docs/DECISIONS.md)
- [Current implementation status](docs/IMPLEMENTATION-STATUS.md)
- [Testing and evidence requirements](docs/TESTING.md)
- [Restricted Work Git LFS publication](docs/LFS-PUBLISHING.md)
- [Avatar intake and approval contract](docs/AVATAR-INTAKE.md)
- [Roster profile allocation](docs/ROSTER-MAPPING.md)

Future Cowork sessions must read these files before implementation, update them as decisions and evidence change, and execute only the currently approved slice.

## Binary asset policy

`.gitattributes` keeps the PRD's 256 x 256 avatar portraits and 512 x 512 driver frames in normal Git at their runtime paths. Production GLB/GLTF support binaries, common production audio formats, and high-resolution PNG/WebP source art remain in Git LFS. Do not place high-resolution masters in the runtime portrait or driver-frame paths. Policy changes require an approved record in `docs/DECISIONS.md`.

When a hosted Work shell cannot reach GitHub, `docs/LFS-PUBLISHING.md` defines the approved GitHub Actions fallback for assets that committed source can reproduce byte-for-byte. Other LFS assets require an authenticated external handoff.
