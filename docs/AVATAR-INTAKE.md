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

## Runtime integration handoff

Before an approved package is marked ready, the implementer must record and verify:

- A base-aware, controlled revision for every public runtime asset URL. Change that revision (or the filename) whenever bytes at a stable URL change.
- Production LFS materialization: `lfs: true` checkout, `git lfs fsck`, and a build-time binary-signature check for every required GLB.
- A driver-frame selector that preloads rear, front, steer-left, steer-right, hit, victory, front-steer-left, front-steer-right, front-hit, and front-victory frames. Steering must select the matching kart-turn direction; collision and finish states must take precedence. A missing chase-oriented action frame retains rear, while a missing camera-facing action frame retains front; neither failure may blank the driver or expose the wrong facing.
- Chase- and rear-camera verification of kart nose, steering wheel, driver, cockpit, wheel, and mount orientation. Correct an authored-axis mismatch only at the visual root and record the exact transform; gameplay physics and coordinates remain canonical.
- Fresh desktop and mobile manual confirmation that the selected production kart—not the fallback—renders and remains controlled through the race.

## Efficient 3D candidate workflow

The Hearthwarden reached geometry approval in two candidates, the shortest kart review cycle recorded through 2026-09-03. Use this sequence for later karts:

1. Lock the construction language, signature silhouette, asymmetrical features, and explicit exclusions before modeling.
2. Inspect approved builders for scale, node names, material count, authored forward axis, and triangle budgets. Reuse the exporter and primitive helpers without copying another kart's identity.
3. Generate LOD0, LOD1, and LOD2 from one deterministic source. Reject the build immediately if any LOD exceeds its budget or changes the required thirteen-node hierarchy.
4. Review front three-quarter, rear three-quarter, top, and profile views before sending the GLB. Check the kart's signature details against the written lock and against the closest existing roster silhouette.
5. Treat every prop, emblem, plant, bracket, exhaust, wheel, and steering column as structural geometry. Verify numerical overlap with its support so a favorable review angle cannot hide a floating part.
6. Give every revised candidate new filenames and links. Do not overwrite a review URL because browser and viewer caches can show stale geometry.
7. Send the direct LOD0 GLB with the review sheet. Keep LOD1 and LOD2 available for contract review, then rerun deterministic hash checks after the final correction.

This process does not remove the product-owner geometry gate or the later in-game placement and live-playtest gates.

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
- 512×512 front-steer-left frame:
- 512×512 front-steer-right frame:
- 512×512 front-hit frame:
- 512×512 front-victory frame:
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
