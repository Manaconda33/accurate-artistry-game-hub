# Repository agent instructions

The canonical repository `Manaconda33/accurate-artistry-game-hub` is public. Do not describe or treat it as private. Public visibility does not waive the existing approval gates for publishing code, assets, documentation, deployments, or protected project state.

Read `docs/PRD.md`, `docs/IMPLEMENTATION-STATUS.md`, `docs/DECISIONS.md`, `docs/TESTING.md`, `docs/AVATAR-INTAKE.md`, `docs/ROSTER-MAPPING.md`, and `docs/LFS-PUBLISHING.md` before implementation work. Treat those files as authoritative over chat history.

For character work:

- Process one character at a time through intake, approval, asset preparation, roster allocation, validation, and publication.
- Update the character record, asset brief, implementation status, and roster ledger whenever a decision or approval changes them.
- Keep each AA profile unique unless Manny approves a remap.
- Treat deployed character art as an integration contract: use base-aware, revisioned runtime URLs for public assets; preload and select rear, steer-left, steer-right, hit, and victory frames; and preserve a visible rear-frame fallback if an optional frame fails.
- Verify each approved kart in the actual chase and rear cameras. If a visual-root transform is needed to align the asset with runtime forward, keep physics and gameplay coordinates unchanged and record the transform in the character record and asset brief.
- All production kart GLBs must declare `extras.forward: "-Z"`. In this runtime that convention requires the shared `NEGATIVE_Z_KART_VISUAL_YAW` (`Math.PI`) visual-root correction. Do not assign a character-specific zero yaw or infer orientation from builder labels. The manifest validator and runtime-asset gate must reject violations before deployment.

For binary assets:

- Follow `.gitattributes` and ADR-012. Never place an LFS-governed asset into normal Git as a workaround.
- Use normal authenticated Git and Git LFS when the environment can reach GitHub.
- When a hosted Work environment cannot push directly, use the GitHub Actions bridge in `docs/LFS-PUBLISHING.md` only for assets that committed source can reproduce byte-for-byte.
- If an asset cannot be reproduced to its approved LFS object ID, stop and request an authenticated external Git/LFS handoff.
- Remove every temporary materialization workflow after the upload and fetch-back checks pass. Record the run and object IDs in `docs/IMPLEMENTATION-STATUS.md`.
- Pages/production builds that copy LFS-governed runtime assets must check out LFS, pass `git lfs fsck`, and fail on a pointer or invalid binary signature before deployment. Do not rely on a runtime fallback as evidence that the production art is delivered.

Run the checks in `docs/TESTING.md` before presenting a checkpoint. Do not begin the next PRD slice without Manny's approval.
