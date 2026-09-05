# Slice 3 — Character Selection & Avatar Ingestion exit checklist

This checklist is the final, observable exit record for Slice 3. Every item below is evidenced against the validated deployed checkpoint and Manny's final desktop/mobile product-owner approval on 2026-09-05.

## Exit rule

Slice 3 may be marked **COMPLETE / LIVE ACCEPTED** only when every required item is checked, the deployed commit is recorded, desktop and mobile acceptance pass, and no known blocker is being hidden behind a temporary workaround or “hero mode.” If a required check is unavailable, the honest status is **NOT COMPLETE — evidence pending**.

## 1. Governance and scope

- [x] The repository is the authoritative `Manaconda33/manacondas-minigame-mayhem` checkout.
- [x] The checkpoint is based on the current approved `main` and has a traceable branch, commit, PR, merge commit, and deployment commit.
- [x] The PRD remains at Slice 3; no Slice 5 item, new balance experiment, or unrelated gameplay scope was silently added.
- [x] Every active racer has one unique AA-01 through AA-12 profile.
- [x] Alex is recorded as AA-01 Feather Sprinter with approved stats 6 / 9 / 2 / 8 / 7 / 4.
- [x] Cleo remains archived and inactive; no archived asset was overwritten or silently reused.
- [x] Approved identity, reference, rights, kart, raster, and geometry decisions are recorded in current documentation.

## 2. Character roster and selection

- [x] Character Select renders exactly 12 selectable racer slots.
- [x] Each slot displays the correct approved name, portrait, descriptor, and accent treatment.
- [x] No user-facing slot displays `Racer 01`, `Roster placeholder`, `Fallback prototype`, or another temporary identity.
- [x] Alex displays as Alex / Feather Sprinter / The Neon Vector.
- [x] Selecting each racer updates the active profile without stale portrait, kart, descriptor, or stat data.
- [x] The selected racer is the racer used when the race starts.
- [x] A failed portrait request produces only the governed monogram fallback and does not break selection.
- [x] The selected identity is not duplicated in the AI grid.

## 3. Balance-profile integrity

- [x] All twelve profile IDs are unique.
- [x] All six stats for every profile remain integers from 1 through 10.
- [x] Every profile totals 36.
- [x] The displayed profile matches the runtime tuning profile used by the selected kart.
- [x] Alex's high Acceleration and Handling, low Weight, and lower Traction are represented by the approved AA-01 values; no replacement “balanced” placeholder remains.
- [x] No stat, profile, or AI pace change was introduced as an unapproved balance adjustment.

## 4. Runtime asset contract

- [x] Every active production racer supplies portrait, rear, front, steer-left, steer-right, hit, victory, front-steer-left, front-steer-right, front-hit, and front-victory assets.
- [x] Every portrait is 256 x 256 RGBA with valid transparent margins.
- [x] Every driver frame is 512 x 512 RGBA with valid transparent corners and decodable PNG data.
- [x] No approved driver raster contains baked checkerboard, opaque neutral matte, kart geometry, or an unintended second steering wheel.
- [x] Every production kart has materialized LOD0, LOD1, and LOD2 GLBs rather than LFS pointer text.
- [x] Every required GLB begins with the binary glTF signature and declares `extras.forward: "-Z"`.
- [x] Every kart stays within its LOD triangle budgets and retains the required node hierarchy and steering-control contract.
- [x] Controlled revision queries or changed filenames prevent stale browser/cache responses after approved asset changes.
- [x] `git lfs fsck` passes against the published checkpoint (LFS bridge run `33989497206`).

## 5. Shared driver-state behavior

- [x] Neutral chase view selects the rear-facing driver state.
- [x] Positive and negative steering select the matching chase steer-left and steer-right states.
- [x] Contact selects hit for the governed reaction window.
- [x] Finish selects victory while leaving the race result readable.
- [x] Rear-view camera selects the matching front neutral/action state for every visible production racer.
- [x] Front steer-left and front steer-right preserve the commanded kart direction rather than mirroring to viewer direction.
- [x] Front hit and front victory load the matching front-facing states.
- [x] Releasing rear view restores the simulation-driven chase state.
- [x] Missing front-action assets use the approved neutral-front fallback rather than a rear-facing action or blank sprite.
- [x] Player and AI racers use the same state-selection contract.

## 6. Driver/kart attachment and camera review

- [x] Every racer is seated behind the cockpit geometry without floating, sinking, or obvious torso discontinuity.
- [x] Every kart points race-forward in chase and rear views without changing physics or track coordinates.
- [x] Exactly one steering control is visible per racer state: the approved sprite-owned wheel or the kart-modeled wheel, never both and never neither.
- [x] Camera-facing hands remain aligned with the intended steering control.
- [x] Alex chase placement `[0, 0.92, -0.12]` and camera-facing placement `[0, 0.84, -0.12]` pass review.
- [x] The Neon Vector's hood motif is attached, the steering area is clean, and no render-white artifact or floating geometry appears.
- [x] The Neon Vector's exposed cyan/magenta cockpit-to-thruster conduits remain attached and readable in rear three-quarter/profile views.
- [x] All ten Alex states pass the same attachment review, including both steering directions, hit, and victory.

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
- [x] Pull request #92 passes required CI in run `33989589113` before merge.
- [x] Merge commit `617312394decfcb95af4f8fee6431ee9d339201b` is recorded.
- [x] Post-merge `main` run `33989653688` passes independently.
- [x] The GitHub Pages deployment environment reports success.
- [x] The live URL and deployed commit are recorded.
- [x] Deployed asset responses match the approved dimensions, revisions, and hashes where applicable.

## 9. Product-owner live acceptance

### Desktop

- [x] Character Select and race start pass for Alex and representative existing racers.
- [x] Alex passes chase neutral, steer-left, steer-right, hit, and victory.
- [x] Alex passes rear-view neutral, steer-left, steer-right, hit, and victory.
- [x] Alex's wheel ownership, seated occlusion, orientation, and conduit visibility pass.
- [x] Existing accepted racer regressions remain closed.

### Mobile

- [x] Character Select remains usable at the target mobile viewport.
- [x] Alex passes the same chase and rear-view state matrix under touch controls.
- [x] Sprites, steering controls, HUD, minimap, and results do not obscure one another.
- [x] The deployed mobile asset responses are the controlled revisions, not stale cached files.
- [x] Existing accepted racer regressions remain closed.

## 10. Evidence and closeout

- [x] `docs/IMPLEMENTATION-STATUS.md` records commands, results, counts, coverage, deployment, URL, deployed commit, manual scenarios, known defects, and limitations.
- [x] `docs/DECISIONS.md` records the final Alex integration/publication decision without claiming live acceptance prematurely.
- [x] The roster ledger shows all twelve profiles assigned exactly once.
- [x] PR #92 links this checklist and identifies every intentionally deferred item.
- [x] Any failed or unavailable evidence is recorded plainly; no manual result is inferred from an automated pass.
- [x] Only after every required item passes: status changes to **Slice 3 COMPLETE / LIVE ACCEPTED**.

## Final status

**SLICE 3 COMPLETE / LIVE ACCEPTED.** Alex's approved assets, manifest integration, full dependency-backed validation, deterministic geometry checks, offline attachment review, feature-branch publication, PR #92 CI/merge, LFS object fetch-back verification, deployment, artifact-byte verification, and desktop/mobile product-owner acceptance all pass. Manny approved the deployed result against checkpoint `daf1e3127478981e40cca9533300f8617f61004d` on 2026-09-05. Slice 5 remains unauthorized.
