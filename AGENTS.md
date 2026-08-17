# Repository agent instructions

Read `docs/PRD.md`, `docs/IMPLEMENTATION-STATUS.md`, `docs/DECISIONS.md`, `docs/TESTING.md`, `docs/AVATAR-INTAKE.md`, and `docs/ROSTER-MAPPING.md` before implementation work. Treat those files as authoritative over chat history.

For character work:

- Process one character at a time through intake, approval, asset preparation, roster allocation, validation, and publication.
- Update the character record, asset brief, implementation status, and roster ledger whenever a decision or approval changes them.
- Keep each AA profile unique unless Manny approves a remap.

For binary assets:

- Follow `.gitattributes` and ADR-012. Never place an LFS-governed asset into normal Git as a workaround.
- Use normal authenticated Git and Git LFS when the environment can reach GitHub.
- When a hosted Work environment cannot push directly, use the GitHub Actions bridge in `docs/LFS-PUBLISHING.md` only for assets that committed source can reproduce byte-for-byte.
- If an asset cannot be reproduced to its approved LFS object ID, stop and request an authenticated external Git/LFS handoff.
- Remove every temporary materialization workflow after the upload and fetch-back checks pass. Record the run and object IDs in `docs/IMPLEMENTATION-STATUS.md`.

Run the checks in `docs/TESTING.md` before presenting a checkpoint. Do not begin the next PRD slice without Manny's approval.
