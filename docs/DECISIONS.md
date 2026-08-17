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
- **Status:** Superseded by ADR-012
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

## ADR-007: Every slice checkpoint requires a GitHub-hosted test deployment

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** Automated evidence does not let the product owner manually confirm the playable result.
- **Options considered:** Local-only preview; ad hoc external hosting; repeatable GitHub deployment environment.
- **Decision:** Beginning with Slice 1, every slice checkpoint must deploy its production build through GitHub. GitHub Pages and the `github-pages` environment are the default. The checkpoint report must include the live URL.
- **Rationale:** Keeps manual confirmation tied to versioned source and a repeatable repository workflow.
- **Product impact:** Manny can test each playable checkpoint before authorizing the next slice.
- **Implementation impact:** CI validates, packages, and deploys `dist/` after healthy pushes to `main`. Vite uses the repository Pages base path.
- **Approval:** Manny’s Slice 1 authorization and deployment requirement.

## ADR-008: Shorten Circuit Alpha and preserve playable off-road floors

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** Slice 1 manual confirmation required over a minute per lap, making repeated checkpoint testing unnecessarily slow. Full-width dirt removed player choice, sustained off-road slowdown could become an unplayable crawl, and the unlit sky read as a black rendering defect.
- **Options considered:** Keep the original 1.45 km target; reduce required laps; shorten the course while retaining three-lap and checkpoint rules.
- **Decision:** Shorten Circuit Alpha to approximately 0.90 km and retain three laps and twelve ordered checkpoints. Dirt becomes a partial-width optional lane. Grass and dirt receive distinct playable speed floors under throttle. Add a rendered gradient sky/horizon. Forward A/Left and D/Right must match chase-camera visual direction.
- **Rationale:** Reduces manual-test time without weakening lap validation or representative handling coverage, while directly resolving product-owner feedback.
- **Product impact:** Faster repeat testing, clearer route choice, playable off-road recovery, correct controls, and a finished-looking horizon.
- **Implementation impact:** Track coordinates and distance documentation are scaled; surface projection tracks signed lateral offset; off-road controller logic enforces floors; track rendering adds an original procedural sky.
- **Approval:** Manny’s Slice 1 manual confirmation and Slice 2 authorization.

## ADR-009: Competitive race is Slice 3 and mobile controls are session-gated

- **Date:** 2026-08-16
- **Status:** Superseded by ADR-010
- **Context:** Repository continuity had already established the competitive eight-racer race as Slice 3, and Manny added mobile touch control to that authorized slice.
- **Options considered:** Revert to the original PRD numbering; always render touch controls; render them only for coarse, no-hover primary input.
- **Decision:** Preserve the repository’s active sequence: competitive race in Slice 3, roster in Slice 4, items in Slice 5, and final hardening in Slice 6. Render touch controls only when `(hover: none) and (pointer: coarse)` matches.
- **Rationale:** Avoids invalidating completed checkpoints and keeps desktop gameplay uncluttered while enabling mobile play.
- **Product impact:** Mobile players receive on-screen steering, throttle, brake/reverse, drift, rear-view, and recovery controls. Desktop users retain keyboard controls without a touch overlay.
- **Implementation impact:** Input state accepts keyboard and pointer controls through the same fixed-step simulation. AI item use remains deferred until the Slice 5 item dependency exists.
- **Approval:** Manny’s explicit Slice 3 authorization and mobile-control instruction.

## ADR-010: Restore PRD slice order and use one-avatar approval gates

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** ADR-009 relied on an incorrect implementation-status entry instead of the PRD delivery section. AI/grid work was consequently executed before the PRD-defined character slice. Manny identified the mismatch and directed the project to continue following the PRD, with deliberate handling of each avatar.
- **Options considered:** Renumber the PRD around completed work; discard the AI implementation; preserve it as early Slice 4 work and resume Slice 3 in the approved order.
- **Decision:** Preserve the accepted AI/grid implementation as Slice 4 completed early. Restore Slice 3 to Character Selection & Avatar Ingestion. Process avatars individually through intake, review, approval, asset preparation, and roster mapping. Do not invent identity, character, visual, kart, or likeness details.
- **Rationale:** Restores the approved governance baseline without wasting validated work and protects the character roster from rushed or inferred decisions.
- **Product impact:** The current Grand Prix remains playable. Character selection will progress only as approved character packages become ready.
- **Implementation impact:** `docs/AVATAR-INTAKE.md` governs character inputs. Generic schema, validation, fallback, and UI framework work may proceed only when it does not assign unapproved content. Final identity-to-balance-slot mapping remains an explicit approval gate.
- **Approval:** Manny’s correction and instruction to continue the PRD slowly and accurately.

## ADR-011: Use one-to-one roster profile allocation

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** The twelve production characters need distinct driving identities, and Manny requested a durable record of every used archetype.
- **Options considered:** Track assignments only inside individual avatar records; allow profiles to repeat; maintain a roster-wide one-to-one allocation ledger.
- **Decision:** `docs/ROSTER-MAPPING.md` is the allocation source of truth. Each AA-01 through AA-12 profile may be assigned to one production character only. A locked profile becomes unavailable to later characters unless Manny explicitly approves a remap. The manifest validator must reject duplicate profile IDs and duplicate production-character assignments.
- **Rationale:** A roster-wide ledger prevents accidental reuse and keeps all twelve characters statistically and behaviorally distinct.
- **Product impact:** Every character receives a unique six-stat profile and recognizable driving feel.
- **Implementation impact:** Avatar mapping records and the future manifest validator must agree with the ledger. Any remap updates the ledger, affected avatar records, decision log, and verification evidence.
- **Approval:** Manny's instruction to track used archetypes and explicit approval assigning AA-02 Feather Technician to Lavi.

## ADR-012: Keep fixed-size runtime avatar PNGs in normal Git

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** ADR-005 described Git LFS for high-resolution raster art, but `.gitattributes` routed every character PNG through LFS, including the PRD's small runtime portrait and driver frames. The connected GitHub publication workflow cannot upload LFS objects.
- **Options considered:** Keep all character PNGs in LFS; move all character PNGs to normal Git; exempt only the PRD-sized runtime portrait and driver-frame paths.
- **Decision:** Store `portrait.png` at 256 x 256 and PNGs under each character's `driver/` directory at 512 x 512 in normal Git. Keep high-resolution source art, GLB/GLTF support binaries, production audio, and other high-resolution character, kart, and track PNG/WebP assets in Git LFS.
- **Rationale:** The small runtime files can be delivered and reviewed directly without weakening the large-binary controls that protect repository history.
- **Product impact:** Runtime URLs and the PRD folder layout remain unchanged.
- **Implementation impact:** `.gitattributes` contains narrow exceptions for runtime avatar portraits and driver frames. High-resolution masters must not use those runtime paths.
- **Approval:** Manny's explicit approval on 2026-08-16.

## ADR-013: Use a GitHub Actions bridge for reproducible LFS assets in restricted Work environments

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** The connected GitHub app can write normal Git objects but cannot upload Git LFS objects. Hosted Work shells may also block direct GitHub network access, so a temporary deploy key cannot complete the push.
- **Options considered:** Store the binaries in normal Git; require a manual external push for every LFS asset; use a repository-scoped GitHub Actions runner to regenerate and upload deterministic assets.
- **Decision:** Use the procedure in `docs/LFS-PUBLISHING.md` as the default fallback when direct Git/LFS push is unavailable and committed source can reproduce the approved binary byte-for-byte. Upload only pre-approved object IDs, fetch them back from GitHub, run `git lfs fsck`, record the evidence, and remove the temporary workflow before review or merge.
- **Rationale:** GitHub's runner can reach the LFS service without exposing personal credentials or weakening the repository's binary policy.
- **Product impact:** None. Runtime paths and asset contents remain unchanged.
- **Implementation impact:** Every bridge workflow is temporary, branch-scoped, permission-limited, hash-gated, and ineligible for assets without deterministic committed source. Non-reproducible assets still require an authenticated external Git/LFS handoff.
- **Approval:** Manny's explicit approval after the Lavi Potato bridge passed on 2026-08-16.

## ADR-014: Launch Character Select with one production driver and governed fallbacks

- **Date:** 2026-08-16
- **Status:** Approved
- **Context:** Manny requested an efficient playable proof of Lavi and Potato while pausing the remaining one-character-at-a-time asset intake. Slice 3 still requires the complete twelve-slot framework and missing-asset resilience.
- **Options considered:** Hard-code Lavi directly into the race; wait for all twelve final portraits and karts; build the complete selection framework with Lavi as the first production entry and explicit fallbacks elsewhere.
- **Decision:** Character Select renders all twelve stable profile slots. Lavi is the default production entry and loads their approved portrait, driver art, Potato GLB, and AA-02 statistics. Other slots remain visibly provisional, use monogram portraits and the fallback kart, and do not receive community identities until their individual approval gates are complete.
- **Rationale:** Proves the approved hybrid 2D/3D asset pipeline now, preserves the PRD scaffold, and avoids reworking the selection path as each later character arrives.
- **Product impact:** Players can select Lavi and enter the current eight-racer Grand Prix in Potato. The remaining slots are functional for physics/fallback testing without misrepresenting unfinished characters.
- **Implementation impact:** A typed manifest and validator become the character source of truth; the selected stats configure player physics; portrait and kart load failures degrade safely.
- **Approval:** Manny's instruction on 2026-08-16 to pause additional character asset work, implement Lavi in the current build, and create portrait placeholders/scaffolding for the rest.
