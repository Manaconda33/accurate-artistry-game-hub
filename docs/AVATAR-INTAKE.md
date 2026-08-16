# Avatar Intake and Approval Contract

This document governs Slice 3 character work. Each of the twelve avatars is developed individually. Repository implementation must not infer or finalize missing identity, likeness, story, visual, kart, or balance information.

## Working sequence for each avatar

1. **Intake:** Manny supplies the available character information and source references.
2. **Clarification:** Missing details that materially affect the result are identified and resolved.
3. **Character lock:** Manny approves the written character and visual specification.
4. **Kart lock:** Manny approves the kart concept, construction language, palette, and emblem treatment.
5. **Balance mapping:** The approved character is mapped to one available AA-01 through AA-12 profile. Appearance or personality alone must not determine the mapping.
6. **Asset preparation:** Approved source art is converted or commissioned to the PRD formats. Source, rights, and transformation notes are recorded.
7. **Implementation:** The approved record enters the manifest, selection UI, kart preview, driver-sprite pipeline, and race handoff.
8. **Verification:** Schema, fallback, visual, physics, and manual selection checks pass before that avatar is marked ready.

No later step implies approval of an earlier unresolved step.

## Per-avatar intake template

### Identity

- Proposed display name:
- Stable internal ID: assigned only after approval
- Pronunciation, if useful:
- Pronouns, if relevant:
- Short selection-screen descriptor:
- Character background/personality:
- Defining traits that must be preserved:
- Traits or interpretations to avoid:

### Visual direction

- Canonical visual description:
- Body type, silhouette, and scale:
- Face, hair, skin/fur/material, and distinguishing features:
- Clothing, armor, accessories, or props:
- Primary, secondary, and accent colors:
- Required symbols or motifs:
- Expression and attitude:
- Source/reference images:
- Elements that may be simplified at small HUD size:
- Elements that may never be changed or omitted:

### Kart direction

- Kart name or working title:
- Kart type or design family:
- Shape and construction language:
- Primary and accent colors:
- Materials and surface finish:
- Wheels, exhaust, cockpit, and signature details:
- Emblem/monogram treatment:
- Desired relationship between driver and kart:
- Details to avoid:

### Gameplay and roster mapping

- Desired driving feel:
- Preferred strengths:
- Accepted weaknesses:
- Weight-class preference, if any:
- Candidate AA balance profile: proposed only after character and kart locks
- Mapping rationale:
- Manny’s mapping approval:

### Required asset states

- 256×256 transparent portrait:
- 512×512 rear driver frame:
- 512×512 steer-left frame:
- 512×512 steer-right frame:
- 512×512 hit frame:
- 512×512 victory frame:
- Kart GLB or approved fallback configuration:
- Source and rights/provenance notes:

### Approval record

- Intake status: Draft | Needs clarification | Ready for review | Approved
- Character lock:
- Kart lock:
- Balance mapping lock:
- Asset approval:
- Implementation verification:
- Open questions:

## Batch rules

- Work on one avatar at a time unless Manny explicitly authorizes a batch.
- Before recommending a balance profile, review the full current ledger in `docs/ROSTER-MAPPING.md` and exclude every assigned profile.
- Record every approved AA-profile allocation in `docs/ROSTER-MAPPING.md`.
- Assign each AA-01 through AA-12 profile to no more than one character so all twelve characters retain distinct statistics and driving feel.
- Treat an assigned profile as unavailable unless Manny explicitly approves a remap.
- Unapproved avatars remain stable placeholder slots and must not block the generic fallback framework.
- Approval of text does not imply approval of generated or transformed art.
- Approval of visual art does not imply approval of a balance profile.
- Original source files are retained; derived game assets must not silently replace them.
- Store approved 256 x 256 portrait PNGs and 512 x 512 driver-frame PNGs at the PRD runtime paths under `public/assets/characters/<id>/` in normal Git. High-resolution source art, audio, and GLB assets follow the repository Git LFS policy.
