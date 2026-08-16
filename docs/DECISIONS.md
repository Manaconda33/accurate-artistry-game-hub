# Architecture and Product Decisions

This log records approved or implementation-shaping decisions. Future sessions must update it when a decision changes architecture, scope, authority, asset handling, acceptance criteria, or delivery sequencing.

## Decision format

### Decision ADR-NNN: Title

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Approved | Rejected | Superseded
- **Context:** Why a decision was needed.
- **Options considered:** Meaningful alternatives.
- **Decision:** The selected direction.
- **Rationale:** Why it best satisfies the PRD.
- **Product impact:** User-facing or product consequences.
- **Implementation impact:** Technical consequences.
- **Approval:** Source of approval.

## ADR-001: GitHub is the durable source of truth

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** The project requires reliable continuity across Cowork sessions.
- **Options considered:** Conversation-only context; local-only files; a private GitHub repository.
- **Decision:** `Manaconda33/accurate-artistry-game-hub` is the canonical project repository. Repo documentation and committed code supersede chat history when they conflict.
- **Rationale:** Versioned files provide durable requirements, decisions, status, and evidence.
- **Product impact:** None at runtime.
- **Implementation impact:** Every checkpoint must update repository documentation before closing.
- **Approval:** Final PRD v1.1 and Slice 0 authorization.

## ADR-002: TypeScript and Vite SPA baseline

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** The PRD specifies a modular HTML5 single-page application.
- **Options considered:** Unbundled JavaScript; alternative SPA frameworks; TypeScript with Vite.
- **Decision:** Use a framework-light TypeScript SPA built by Vite with strict compiler checks.
- **Rationale:** Fast iteration, modern browser output, low framework overhead, and testable modules.
- **Product impact:** Supports the modular game-hub shell and future games.
- **Implementation impact:** Vite owns development and production builds; TypeScript project references enforce strict checks.
- **Approval:** Final PRD v1.1.

## ADR-003: Runtime technology baselines

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** Rendering, physics, and audio foundations must be selected before gameplay work.
- **Options considered:** PRD-supported alternatives.
- **Decision:** Three.js is the rendering baseline; Rapier 3D (`@dimforge/rapier3d-compat`) is the physics dependency; Howler.js with Web Audio is the audio baseline.
- **Rationale:** Matches the approved PRD and supports web delivery.
- **Product impact:** Establishes the future kart racer’s technical foundation without implementing it in Slice 0.
- **Implementation impact:** Dependencies are installed now; integrations are deferred to their approved slices.
- **Approval:** Final PRD v1.1 and Slice 0 instructions.

## ADR-004: npm and committed lockfile

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** Local and CI installs must be reproducible.
- **Options considered:** npm, pnpm, yarn.
- **Decision:** Use npm and commit `package-lock.json`. CI must install with `npm ci`.
- **Rationale:** npm ships with Node.js and requires no additional package-manager bootstrap.
- **Product impact:** None.
- **Implementation impact:** Dependency changes must update the lockfile.
- **Approval:** Slice 0 implementation decision within approved scope.

## ADR-005: Git LFS binary asset policy

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** Large binary game assets must not pollute normal Git history.
- **Options considered:** Normal Git blobs; external asset host; Git LFS.
- **Decision:** Use Git LFS patterns in `.gitattributes` for GLB/GLTF support binaries, production audio, and high-resolution PNG/WebP assets in character, kart, and track asset trees.
- **Rationale:** Keeps repository history manageable while retaining versioned asset references.
- **Product impact:** No current runtime impact; production assets are not included in Slice 0.
- **Implementation impact:** Contributors must install Git LFS and run `git lfs install` before adding matching assets. Generated/runtime derivatives should not be committed unless the PRD later requires them.
- **Approval:** Final PRD v1.1 and Slice 0 instructions.

## ADR-006: Slice 0 contains no gameplay implementation

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** The checkpoint must prove the toolchain without leaking into Slice 1.
- **Options considered:** Early renderer/physics experiments; static app-shell proof.
- **Decision:** Ship only a tested static app shell. Do not initialize Three.js, Rapier, Howler, gameplay, track, AI, camera, item, or race systems.
- **Rationale:** Preserves the explicit authorization boundary.
- **Product impact:** The app confirms bootstrap status but is not a playable build.
- **Implementation impact:** Architecture directories and dependencies exist; implementation remains deferred.
- **Approval:** Manny’s Slice 0 execution instruction.
