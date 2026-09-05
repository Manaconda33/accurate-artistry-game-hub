# Slice 3 — Character Selection & Avatar Ingestion exit checklist

This checklist is the final, observable exit gate for Slice 3. Slice 3 is not complete because assets merely exist in the repository. Every item below must be evidenced against the validated deployed checkpoint. No item may be marked complete from source inspection alone when the requirement concerns runtime behavior.

## Exit rule

Slice 3 may be marked **COMPLETE / LIVE ACCEPTED** only when every required item is checked, the deployed commit is recorded, desktop and mobile acceptance pass, and no known blocker is being hidden behind a temporary workaround or “hero mode.” If a required check is unavailable, the honest status is **NOT COMPLETE — evidence pending**.

## 1. Governance and scope

- [ ] The repository is the authoritative `Manaconda33/manacondas-minigame-mayhem` checkout.
- [ ] The checkpoint is based on the current approved `main` and has a traceable branch, commit, PR, merge commit, and deployment commit.
- [ ] The PRD remains at Slice 3; no Slice 5 item, new balance experiment, or unrelated gameplay scope was silently added.
- [ ] Every active racer has one unique AA-01 through AA-12 profile.
- [ ] Alex is recorded as AA-01 Feather Sprinter with approved stats 6 / 9 / 2 / 8 / 7 / 4.
- [ ] Cleo remains archived and inactive; no archived asset was overwritten or silently reused.
- [ ] Approved identity, reference, rights, kart, raster, and geometry decisions are recorded in current documentation.

## 2. Character roster and selection

- [ ] Character Select renders exactly 12 selectable racer slots.
- [ ] Each slot displays the correct approved name, portrait, descriptor, and accent treatment.
- [ ] No user-facing slot displays `Racer 01`, `Roster placeholder`, `Fallback prototype`, or another temporary identity.
- [ ] Alex displays as Alex / Feather Sprinter / The Neon Vector.
- [ ] Selecting each racer updates the active profile without stale portrait, kart, descriptor, or stat data.
- [ ] The selected racer is the racer used when the race starts.
- [ ] A failed portrait request produces only the governed monogram fallback and does not break selection.
- [ ] The selected identity is not duplicated in the AI grid.

## 3. Balance-profile integrity

- [ ] All twelve profile IDs are unique.
- [ ] All six stats for every profile remain integers from 1 through 10.
- [ ] Every profile totals 36.
- [ ] The displayed profile matches the runtime tuning profile used by the selected kart.
- [ ] Alex's high Acceleration and Handling, low Weight, and lower Traction are represented by the approved AA-01 values; no replacement “balanced” placeholder remains.
- [ ] No stat, profile, or AI pace change was introduced as an unapproved balance adjustment.

## 4. Runtime asset contract

- [ ] Every active production racer supplies portrait, rear, front, steer-left, steer-right, hit, victory, front-steer-left, front-steer-right, front-hit, and front-victory assets.
- [ ] Every portrait is 256 x 256 RGBA with valid transparent margins.
- [ ] Every driver frame is 512 x 512 RGBA with valid transparent corners and decodable PNG data.
- [ ] No approved driver raster contains baked checkerboard, opaque neutral matte, kart geometry, or an unintended second steering wheel.
- [ ] Every production kart has materialized LOD0, LOD1, and LOD2 GLBs rather than LFS pointer text.
- [ ] Every required GLB begins with the binary glTF signature and declares `extras.forward: "-Z"`.
- [ ] Every kart stays within its LOD triangle budgets and retains the required node hierarchy and steering-control contract.
- [ ] Controlled revision queries or changed filenames prevent stale browser/cache responses after approved asset changes.
- [x] `git lfs fsck` passes against the published checkpoint (LFS bridge run `33989497206`).

## 5. Shared driver-state behavior

- [ ] Neutral chase view selects the rear-facing driver state.
- [ ] Positive and negative steering select the matching chase steer-left and steer-right states.
- [ ] Contact selects hit for the governed reaction window.
- [ ] Finish selects victory while leaving the race result readable.
- [ ] Rear-view camera selects the matching front neutral/action state for every visible production racer.
- [ ] Front steer-left and front steer-right preserve the commanded kart direction rather than mirroring to viewer direction.
- [ ] Front hit and front victory load the matching front-facing states.
- [ ] Releasing rear view restores the simulation-driven chase state.
- [ ] Missing front-action assets use the approved neutral-front fallback rather than a rear-facing action or blank sprite.
- [ ] Player and AI racers use the same state-selection contract.

## 6. Driver/kart attachment and camera review

- [ ] Every racer is seated behind the cockpit geometry without floating, sinking, or obvious torso discontinuity.
- [ ] Every kart points race-forward in chase and rear views without changing physics or track coordinates.
- [ ] Exactly one steering control is visible per racer state: the approved sprite-owned wheel or the kart-modeled wheel, never both and never neither.
- [ ] Camera-facing hands remain aligned with the intended steering control.
- [ ] Alex chase placement `[0, 0.92, -0.12]` and camera-facing placement `[0, 0.84, -0.12]` pass review.
- [ ] The Neon Vector's hood motif is attached, the steering area is clean, and no render-white artifact or floating geometry appears.
- [ ] The Neon Vector's exposed cyan/magenta cockpit-to-thruster conduits remain attached and readable in rear three-quarter/profile views.
- [ ] All ten Alex states pass the same attachment review, including both steering directions, hit, and victory.

## 7. Automated validation

- [x] `npm ci` completes from the committed lockfile.
- [x] `npm run typecheck` passes.
- [x] `npm run lint` passes with zero warnings.
- [x] `npm run test:ci` passes with 18 files / 93 tests and 89.71% statement coverage.
- [x] `npm run build` passes branding, runtime-asset, LFS-materialization, and production Vite checks.
- [x] `npm run validate` is recorded as the aggregate local result.
- [x] The exact approved runtime asset hashes are recorded for new or changed binary assets.
- [x] The production build contains all controlled character revisions and expected asset paths.

## 8. Publication and deployment

- [x] Publication approval is explicitly recorded after local validation passes.
- [x] The validated file tree is published to `feature/alex-neon-vector-local`; the connected GitHub integration created the remote commit because the hosted shell could not authenticate an HTTPS Git push.
- [ ] The pull request passes required CI before merge.
- [ ] The merge commit is recorded.
- [ ] The post-merge `main` workflow passes independently.
- [ ] The deployment environment reports success.
- [ ] The live URL and deployed commit are recorded.
- [ ] Deployed asset responses match the approved dimensions, revisions, and hashes where applicable.

## 9. Product-owner live acceptance

### Desktop

- [ ] Character Select and race start pass for Alex and representative existing racers.
- [ ] Alex passes chase neutral, steer-left, steer-right, hit, and victory.
- [ ] Alex passes rear-view neutral, steer-left, steer-right, hit, and victory.
- [ ] Alex's wheel ownership, seated occlusion, orientation, and conduit visibility pass.
- [ ] Existing accepted racer regressions remain closed.

### Mobile

- [ ] Character Select remains usable at the target mobile viewport.
- [ ] Alex passes the same chase and rear-view state matrix under touch controls.
- [ ] Sprites, steering controls, HUD, minimap, and results do not obscure one another.
- [ ] The deployed mobile asset responses are the controlled revisions, not stale cached files.
- [ ] Existing accepted racer regressions remain closed.

## 10. Evidence and closeout

- [ ] `docs/IMPLEMENTATION-STATUS.md` records commands, results, counts, coverage, deployment, URL, deployed commit, manual scenarios, known defects, and limitations.
- [ ] `docs/DECISIONS.md` records the final Alex integration/publication decision without claiming live acceptance prematurely.
- [ ] The roster ledger shows all twelve profiles assigned exactly once.
- [ ] The final PR links this checklist and identifies every intentionally deferred item.
- [ ] Any failed or unavailable evidence is recorded plainly; no manual result is inferred from an automated pass.
- [ ] Only after every required item passes: status changes to **Slice 3 COMPLETE / LIVE ACCEPTED**.

## Current status at Alex local checkpoint

**NOT COMPLETE — PR CI, deployment, and live evidence pending.** Alex's approved assets, manifest integration, full dependency-backed validation, deterministic geometry checks, offline attachment review, feature-branch publication, PR #92 creation, and LFS object fetch-back verification are complete. Merge, post-merge deployment, and desktop/mobile product-owner acceptance remain open.
