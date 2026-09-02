# Architecture and Product Decisions

This file is the current decision register. The complete original ADR-001 through ADR-021 record is preserved verbatim at `docs/history/DECISIONS-through-ADR-021.md` and remains authoritative except where a later ADR explicitly supersedes an earlier decision.

Future sessions must read this current register and follow the historical link when implementing behavior governed by ADR-001 through ADR-021.

## Existing governing decisions

ADR-001 through ADR-021 remain in force according to their recorded status in `docs/history/DECISIONS-through-ADR-021.md`, including repository governance, Vite/TypeScript/Three.js/Rapier/Howler baselines, Git LFS policy, slice/deployment gates, roster mapping, runtime character asset delivery, orientation rules, unique AI identity sampling, and the approved production locks for existing characters.

ADR-020's historical Cleo-to-AA-06 production mapping is superseded only with respect to **current active roster assignment** by ADR-022 below. Cleo's approved likeness, kart design, source rights, asset approvals, and historical acceptance evidence remain valid archive records.

## ADR-022: Archive Cleo and release AA-06 from active production

- **Date:** 2026-08-26
- **Status:** Approved
- **Context:** Manny directed that Cleo be removed from production while preserving her complete character package and all related work so she can be restored later if desired. Cleo was an active production identity in `characterManifest`, selectable by the player, eligible for the randomized AI grid, and mapped to AA-06 Grip Specialist.
- **Options considered:** Delete Cleo and her assets; retain Cleo as an inactive but profile-reserving production definition; preserve the full package as an archive while returning AA-06 to a governed active-roster placeholder.
- **Decision:** Remove Cleo from the active manifest and AI/player roster. Preserve her complete approved production definition as `archivedCleo`, keep every runtime PNG, GLB/LFS object, deterministic builder, character record, asset brief, hashes, mount, and prior acceptance evidence, and index them in `docs/CHARACTER-ARCHIVE.md`. Restore the active AA-06 slot to a generic placeholder and return AA-06 to `Available` in the roster ledger. Remove AA-06 GLBs from the active runtime-asset signature requirement without deleting the files.
- **Rationale:** This makes the retirement real at runtime while keeping restoration low-risk and lossless. A semantic archive avoids unnecessary LFS moves or binary churn, preserves historical evidence, maintains the PRD's twelve-slot scaffold, and prevents an inactive character from consuming a balance profile indefinitely.
- **Product impact:** Cleo no longer appears in Character Select and cannot appear as an AI racer. AA-06 remains visible only as an unfinished placeholder until a future approved character occupies it. No approved Cleo artwork or 3D work is destroyed.
- **Implementation impact:** `characterManifest` excludes Cleo; `archivedCleo` retains her former complete definition; AA-06 is a placeholder; the roster ledger marks AA-06 available; Cleo's three GLBs are no longer active build dependencies; archive/restoration documentation becomes part of the character-governance workflow.
- **Restoration gate:** Reintroducing Cleo requires explicit Manny approval, a current balance-profile decision, active-manifest reactivation, fresh runtime/LFS validation, full repository validation, deployment, and live product-owner confirmation. Historical 2026-08-21 acceptance does not substitute for current deployment evidence.
- **Approval:** Manny's explicit instruction on 2026-08-26 to remove Cleo from production while retaining her assets and related character work in an archive for possible later return.

## ADR-023: Lock Keeg production identity, kart, and AA-04 balance profile

- **Date:** 2026-08-26
- **Status:** Approved
- **Context:** Slice 3 resumed one-character-at-a-time avatar intake after Krios production closure. Manny supplied a definitive Keeg racing reference and a written character description, confirmed source/control rights, and approved the character and kart design locks.
- **Decision:** Keeg is the active production identity for AA-04 Balanced Racer. His kart is The Mycelial Majesty. The supplied Keeg racing image is the definitive visual authority for likeness and kart design. His selection descriptor uses the AA archetype name, `Balanced Racer`, consistent with the existing roster presentation contract.
- **Character lock:** Flamboyant male witch; well-trimmed beard; tall silver-trimmed pointed witch hat; layered purple, lavender, silver, and pastel enchanted robes; ornate rings, jeweled accessories, elaborate belt; theatrical magic; clever, charismatic, expressive, sophisticated presentation; mushrooms as a canonical secondary motif.
- **Kart lock:** Arcane grand-tourer / enchanted luxury racer with a low wide chassis, rounded shield-like nose, open cockpit, sculpted side pods, royal purple/violet surfaces, blackened-metal secondary surfaces, silver filigree, lavender magical glow, physically connected wheels, and structurally integrated mushroom ornamentation.
- **Balance mapping:** AA-04 Balanced Racer — Speed 7 / Acceleration 7 / Weight 5 / Handling 7 / Mini-Turbo 5 / Traction 5.
- **Rationale:** The profile provides a versatile, responsive, technically capable driving identity without displacing Kraken's drift-specialist role or overlapping heavyweight identities. The substantial enchanted kart retains medium-class presence while remaining broadly controllable.
- **Provenance:** Manny confirmed that he created or controls the definitive supplied reference and authorizes its transformation into production game assets.
- **Implementation gate:** This approval does not approve derived portrait/driver art, GLB geometry, runtime integration, or live activation. Those remain separately approval-gated under the Slice 3 avatar pipeline.
- **Approval:** Manny approved the character and definitive visual authority, confirmed rights, approved The Mycelial Majesty kart design/name, and approved AA-04 Balanced Racer on 2026-08-26.

## ADR-024: Lock McFleurdel production identity, kart, and AA-07 balance profile

- **Date:** 2026-08-27
- **Status:** Approved
- **Context:** Manny supplied a definitive McFleurdel racing reference, confirmed the character lock and transformation rights, and approved the proposed kart and driving identity during Slice 3 intake.
- **Decision:** McFleurdel is the active production identity for AA-07 High-Speed Cruiser. Her kart is The Fleur de Nuit. The supplied racing image is definitive visual authority for both character and kart.
- **Character lock:** Pale human woman; sharply divided black-and-white hair; violet eyes; dark lips; precise eyeliner; tailored black gothic formalwear with pinstripes, silver fleur-de-lis embroidery, dark-academia structure, subtle punk and occult accents; controlled, observant, quietly intimidating demeanor.
- **Kart lock:** Low gothic grand-tourer with black lacquer bodywork, architectural silver filigree, plum throne cockpit, fleur-de-lis nose shield, four exposed connected wheels, integrated candle-like violet flame fixtures, and purple exhaust energy.
- **Balance mapping:** AA-07 High-Speed Cruiser — Speed 8 / Acceleration 6 / Weight 7 / Handling 5 / Mini-Turbo 4 / Traction 6.
- **Provenance:** Manny confirmed he controls the definitive reference and authorizes transformation into game assets.
- **2D approval:** Manny approved the portrait, front, rear, steer-left, steer-right, corrected hit, and corrected victory designs on 2026-08-27. The normalized runtime files pass the PRD size and alpha contract.
- **Implementation closure:** Manny approved The Fleur de Nuit Candidate 9. Deterministic LOD0/LOD1/LOD2 matched the approved hashes and passed the temporary LFS publication bridge. PR #37 passed branch CI, merged at `aa24b655d30ba65438f512e0544e313da3fc343e`, and post-merge CI/Pages deployment passed in run `33037485975`. Manny manually confirmed the live game on 2026-08-27. McFleurdel's production checkpoint is complete.
- **Approval:** Manny approved the character lock, definitive reference, rights, The Fleur de Nuit name/design, AA-07 mapping, and complete 2D design package on 2026-08-27.

## ADR-025: Lock Toph production identity, kart, and AA-08 balance profile

- **Date:** 2026-08-28
- **Status:** Approved
- **Context:** Manny supplied a definitive Toph racing reference, confirmed transformation rights, approved the written character lock, and approved the proposed kart and driving identity during Slice 3 intake.
- **Decision:** Toph is the active production identity for AA-08 Turbo Bruiser. His kart is The Grave Shift. The supplied racing image is definitive visual authority for both character and kart.
- **Character lock:** Stylish young man; shaggy blond hair; pale teal eyes; rectangular black glasses; black ear gauges; fitted black beanie with small purple, silver, and bronze pins; oversized black hoodie with an original purple thorn-like graphic; relaxed, confident, alternative, slightly mischievous presentation.
- **Kart lock:** Low aggressive street-racer construction; dark bronze frame; black and deep-purple bodywork; exposed mechanical structure; wide tires; purple exhaust energy; thorned-skull nose shield.
- **Balance mapping:** AA-08 Turbo Bruiser — Speed 7 / Acceleration 5 / Weight 7 / Handling 4 / Mini-Turbo 8 / Traction 5.
- **Provenance:** Manny confirmed he controls the definitive reference and authorizes transformation into production game assets.
- **2D approval:** Manny approved the portrait, front, rear, steer-left, steer-right, hit, and corrected victory designs on 2026-08-28. Runtime normalization and validation are part of the pre-kart checkpoint.
- **Implementation gate:** This approval does not approve GLB geometry, runtime integration, manifest activation, or live deployment. Those remain separately gated under the Slice 3 avatar pipeline.
- **Approval:** Manny approved the character lock, definitive reference, rights, The Grave Shift name/design, AA-08 mapping, and complete 2D design package on 2026-08-28.

## ADR-026: Make Speed authoritative for sustained player road velocity

- **Date:** 2026-08-30
- **Status:** Approved
- **Context:** Live tests showed Speed 5–6 drivers exceeding Speed 8–10 drivers without boost. The controller clamped velocity to a Speed-derived maximum before Rapier applied passive damping and collider friction, so lower Acceleration could prevent a driver from reaching that maximum.
- **Decision:** The custom arcade controller exclusively owns player-kart longitudinal deceleration, lateral grip, and surface response. Player kart bodies use zero passive linear damping and zero collider friction with the minimum friction-combine rule. `createKartTuning(stats).maxSpeed` remains the sustained full-throttle asphalt ceiling; Acceleration controls time-to-speed but not the ceiling.
- **Rationale:** This restores the existing PHYS-002 contract that Speed affects maximum road velocity while preserving Acceleration as a distinct, legible stat. It also keeps surface, coasting, braking, drift, and boost behavior inside the controller that already defines those systems.
- **Product impact:** A higher Speed score now produces a higher reachable unboosted asphalt maximum under equivalent conditions. Drivers sharing a Speed score converge to the same maximum even when their Acceleration differs.
- **Scope:** No roster statistics, tuning formulas, boost values, or AI pacing are changed. Numerical balance follows after the corrected player model is deployed and evaluated live.
- **Approval:** Manny requested implementation on 2026-08-30 after supplying live Kraken, Accu, Krios, and Lula speed evidence.

## ADR-027: Restore the PRD acceleration, off-road transition, and AI lane contracts

- **Date:** 2026-08-30
- **Status:** Approved
- **Context:** Live testing accepted the corrected Speed ceilings but found three remaining gameplay gaps. Acceleration values felt too similar because launch force was far above the PRD curve; entering dirt or grass clamped speed to the surface cap in one frame; AI used an excessive sample-count lookahead, cut across inside grass, and had no nearby-racer input for overtaking.
- **Decision:** Use the PRD launch formula `4.0 + 0.55 × Acceleration` with its speed-ratio taper. Preserve Traction-defined dirt and grass caps while reducing excess entry speed progressively. Calculate AI lookahead in the PRD's 5–14 meter range, constrain candidate lanes to the road with a kart margin, and give each AI nearby-racer position, speed, and lateral-offset data for committed passing decisions.
- **Rationale:** Each change closes an existing PHYS-004 or Slice 4 acceptance gap. Acceleration becomes visible without changing Speed ceilings, off-road entry remains readable without erasing Traction, and AI can follow the road and pass instead of targeting long chords or queuing on one line.
- **Product impact:** Low-Acceleration racers take longer to build momentum. Dirt and grass slow racers over a short transition. AI racers use multiple legal lines and can move around slower traffic.
- **Scope:** Driver stats, Speed ceilings, boost values, items, AI item use, and final difficulty tuning are unchanged.
- **Approval:** The existing PRD formulas and Slice 4 acceptance criteria govern this correction. Manny directed the follow-up on 2026-08-30 after testing the deployed Speed fix.

## ADR-028: Make kart-impact speed retention Weight-driven but bounded

- **Date:** 2026-08-30
- **Status:** Approved
- **Context:** Kart-to-kart contact used relative mass for lateral displacement but did not explicitly reduce forward speed. Manny requested a measurable Weight advantage while requiring Accu at Weight 10 to retain meaningful collision risk.
- **Decision:** Meaningful closing impacts reduce positive forward velocity with the governed PRD retention curve. Impact severity scales with closing speed; the racer's Weight sets the base loss; the opponent's Weight applies a small bounded pressure modifier. Retention is clamped to 65–96%, and contacts below 0.75 m/s do not reduce speed. Lateral velocity and knockback remain intact.
- **Rationale:** The 15-point full-impact loss range makes Weight legible without erasing the value of positioning or collision avoidance. At severe impact, Accu retains approximately 86% against a Weight 2 racer, while that Weight 2 racer retains approximately 67% against Accu. Accu therefore gains a clear advantage but still loses roughly 14% of forward speed.
- **Scope:** The change applies equally to player and AI kart contacts. It does not alter driver stats, mass-based lateral impulse, walls, items, Speed ceilings, Acceleration, or surface response.
- **Approval:** Manny explicitly requested Weight-driven collision speed reduction on 2026-08-30 and specified that Weight 10 must not become virtually immune.

## ADR-029: Make character Speed authoritative for AI straight-line pace

- **Date:** 2026-08-31
- **Status:** Approved
- **Context:** Live testing found that player-controlled racers frequently reached their Speed-defined maximum while AI-controlled versions did not. AI desired speed used an absolute 20.5–26.0 m/s range derived from grid profile pace rather than the selected character's kart tuning. The first circuit profile peaked at 24.1 m/s against a 29.7 m/s character maximum.
- **Decision:** Each AI driver receives its selected character's `maxSpeed` and uses that value as its neutral clear-straight target. Profile pace now adjusts the curvature penalty, preserving difficulty differences through corner-speed judgment rather than an unrelated straight-line ceiling. Leading AI receives no hidden top-speed reduction. Trailing top-speed allowance is clamped to the PRD's 4% maximum and passed explicitly to the kart controller.
- **Rationale:** Speed must describe the same physical capability whether a character is controlled by the player or AI. Corner judgment, braking, overtaking, collisions, and surface response provide sufficient honest sources of race-performance variation.
- **Product impact:** AI versions of high-Speed racers can now use their straight-line advantage, while low-Speed racers retain their lower cap. Clear straights become more competitive without giving every AI identical performance or altering player handling.
- **Scope:** Roster stats, player caps, Acceleration, Weight collision response, lane selection, items, and global difficulty settings are unchanged.
- **Approval:** Manny approved the character-cap AI balance model on 2026-08-31 after confirming that AI racers consistently appeared unable to reach the maximum speeds available to players.

## ADR-030: Render the race minimap from shared Circuit Alpha topology

- **Date:** 2026-08-31
- **Status:** Approved
- **Context:** TRACK-004 and UI-001 require a race minimap, but the live HUD exposed only textual rank and lap information. Manny requested a minimap that tracks all racers and explicitly required mobile placement to be considered.
- **Decision:** Normalize Circuit Alpha's ordered 384 world samples into one aspect-preserving SVG view box and reuse that same immutable point set for the rendered course and progress-interpolated racer markers. Render each racer as a nearest-neighbor head crop from their approved transparent 2D portrait; render the player last at a larger size with a gold outline. Place the map below Lap on desktop and as a reduced upper-left element on mobile. Hide it with the rest of the live HUD during the finish presentation.
- **Rationale:** Deriving the map from the race-progress topology prevents visual drift between the course, lap logic, and marker positions. SVG stays sharp across desktop and mobile without a new image asset, while a single static path plus eight lightweight markers stays within the HUD performance budget.
- **Product impact:** Players can read pack spacing and approaching traffic without relying only on rank. The map remains visible during normal and rear-camera driving but does not compete with mobile controls or the victory pose.
- **Scope:** This closes the minimap portion of Slice 6. It does not add item HUD, player portrait HUD, final-lap treatment, pause, audio, or other remaining Slice 6 work.
- **Approval:** Manny requested the racer-tracking minimap and mobile-aware placement on 2026-08-31, then selected pixel-rendered driver heads as the marker treatment before publication.

## ADR-031: Use one driver-sprite state contract for player and AI racers

- **Date:** 2026-08-31
- **Status:** Approved
- **Context:** Production AI drivers remained on their rear frame while turning, colliding, finishing, and appearing in the player's rear-view camera. Three active drivers also lacked the required front frame, and Accu exposed baked checkerboard pixels and incorrect cockpit depth.
- **Decision:** Player and AI sprites use the same ordered state selector: victory, hit, front during rear view, steering, then rear. Every involved racer receives a hit window after kart contact. Character-specific neutral/front placement overrides remain manifest data. New or repaired bitmap derivatives stay outside runtime paths until they pass alpha validation and Manny's visual approval.
- **Rationale:** A single selector prevents player and AI behavior from drifting while preserving character-specific art and cockpit placement. Keeping visual candidates approval-gated protects existing likeness and asset locks.
- **Product impact:** AI drivers visibly react to the race rather than appearing static, and rear view can show every driver's face once all missing front assets are approved.
- **Scope:** This does not change AI driving decisions, physics, roster stats, kart geometry, cameras, race ranking, or character identity.
- **Implementation closure:** Manny approved the Lavi, corrected Manaconda, and Accu front candidates plus deterministic alpha cleanup on 2026-08-31. All active production packages now contain six validated states; Accu's three affected wheel apertures are transparent; controlled revisions prevent stale cached art.
- **Approval:** Manny requested complete driver-state behavior and the Accu corrections on 2026-08-31.

## ADR-032: Record the canonical repository as public

- **Date:** 2026-08-31
- **Status:** Approved
- **Context:** Project-session instructions still described `Manaconda33/accurate-artistry-game-hub` as private, while GitHub reports the canonical repository as public. That mismatch created an avoidable publication-authority stop during the Accu correction.
- **Decision:** Treat and describe the canonical GitHub repository as public in durable project guidance. Public visibility does not grant blanket authority to publish, merge, deploy, delete, or change protected state; the existing PRD and approval gates continue to govern each action.
- **Product impact:** Future sessions can assess disclosure risk and repository state accurately before proposing or executing work.
- **Implementation impact:** `AGENTS.md` and `README.md` explicitly identify the repository as public. Stale external project instructions should be updated to match when their settings surface is available.
- **Approval:** Manny confirmed the repository is public and approved correcting the project instructions on 2026-08-31.

## ADR-033: Accept Accu's deployed camera and steering-control correction

- **Date:** 2026-08-31
- **Status:** Approved
- **Context:** PR #54's vertical-only placement left Accu's chase hair cut by a firm horizontal cockpit seam and did not expose a readable steering wheel in rear-camera view. PR #56 instead corrected sprite depth and moved Pink Precision's modeled steering control only for the neutral front frame.
- **Decision:** Preserve PR #56's chase-oriented driver position `[0, 0.82, -0.72]`, neutral front position `[0, 0.9, 0.22]`, and front-frame-only modeled steering-control position `[0, 1.46, -0.46]`. Preserve the accepted chase-state wheel suppression and stopped-on-grass relaunch behavior.
- **Evidence:** PR #56 CI run `33447987037` and main validation/deployment run `33448083520` passed. Manny then approved the deployed chase-camera hair edge, rear-camera seated composition and visible wheel, chase-state wheel suppression, and grass relaunch behavior.
- **Product impact:** Accu and Pink Precision now pass their runtime camera-presentation checkpoint without changing approved PNG or GLB bytes, physics, camera selection, or other drivers.
- **Approval:** Manny approved the deployed correction on 2026-08-31.

## ADR-034: Preserve driver actions in front-facing camera views

- **Date:** 2026-09-01
- **Status:** Approved
- **Context:** Amendment 1.9 completed one neutral front frame per active production driver, but rear-camera steering fell back to neutral front while hit and victory could expose rear-oriented action art. This breaks pose continuity when the camera faces the front of a kart.
- **Decision:** Add front-steer-left, front-steer-right, front-hit, and front-victory to the production driver contract. Select action first and facing second for player and AI racers. During the one-character-at-a-time rollout, missing front actions use neutral front as the only allowed front-facing fallback.
- **Rationale:** The camera should change the view of the simulated state, not erase or reverse the state. A neutral-front fallback preserves facing without publishing unapproved art.
- **Scope:** No approved chase or neutral-front raster is replaced. Identity, kart geometry, stats, physics, camera placement, and steering-control ownership remain unchanged. Each character's new raster package and public integration remain separately approval-gated.
- **Rollout:** Kraken is first because his approved front-victory frame already satisfies one quarter of the new contract.
- **Kraken pilot approval:** Manny approved Kraken's front-steer-left, front-steer-right, and front-hit candidates on 2026-09-01. Integrate them with the unchanged approved front-victory frame and require live verification before beginning another driver.
- **Approval:** Manny directed the project to address the missing front-facing steering, hit, and victory states on 2026-09-01.

## ADR-035: Accept Kraken's front-action pilot

- **Date:** 2026-09-01
- **Status:** Approved
- **Context:** PR #59 deployed Kraken's approved front-steer-left, front-steer-right, and front-hit frames with the unchanged approved front-victory frame. The one-character rollout blocked the next driver until live verification passed.
- **Decision:** Accept Kraken's `kraken-runtime-20260901-2` camera-facing action package. Preserve its four front-action files, shared selector behavior, neutral-front fallback contract, placement, and steering-control ownership.
- **Evidence:** PR #59 head CI run `33464307463` and main run `33464380102` passed. Deployed response hashes matched the approved local files. Manny reported the requested steering, hit, victory, chase restoration, transparency, cockpit, and wheel checks passed on 2026-09-01.
- **Product impact:** Kraken's pilot is complete. The one-character rollout may begin the next active driver's separately reviewed package.
- **Approval:** Manny reported "Passed" after testing the deployed checkpoint on 2026-09-01.

## ADR-036: Approve the Manaconda and Krios front-action batch

- **Date:** 2026-09-01
- **Status:** Approved
- **Context:** Kraken's live pilot passed, unlocking the next rollout package. Manny authorized two drivers per batch and selected the next active-roster pair: Manaconda and Krios.
- **Decision:** Add approved front-steer-left, front-steer-right, front-hit, and front-victory frames for both drivers. Preserve each character's existing front placement and kart contract. Manaconda's four sprites each contain exactly one steering wheel because The Wayfinder is wheel-free. Krios's sprites contain no steering wheel or kart geometry because The Hornbreaker supplies the modeled control.
- **Transparency correction:** Krios's first review sheet retained baked pale matte inside the closed horn loops. Manny rejected that defect. The approved revision clears the enclosed horn apertures to alpha in both steering frames and victory; the hit frame was already clean. The runtime gate must reject future loss of the two substantial enclosed transparent horn apertures.
- **Controlled revisions:** `manaconda-runtime-20260901-3` and `krios-runtime-20260901-2`.
- **Scope:** Existing chase art, neutral front art, kart GLBs, placement, physics, stats, camera geometry, and shared selector behavior remain unchanged.
- **Approval:** Manny approved the revised two-driver package on 2026-09-01.

## ADR-037: Accept the Manaconda and Krios front-action batch

- **Date:** 2026-09-01
- **Status:** Approved
- **Context:** PR #62 deployed the approved Manaconda and Krios camera-facing steering, hit, and victory packages. PR #63 recorded the deployed bundle and matching response hashes. The rollout blocked the next pair until Manny completed the live camera/action check.
- **Decision:** Accept `manaconda-runtime-20260901-3` and `krios-runtime-20260901-2`. Preserve all eight front-action files, the shared selector behavior, each driver's approved front placement, and the existing steering-control ownership rules. Manaconda's sprites retain exactly one wheel. Krios's sprites remain wheel-free, and the enclosed areas between his horns remain transparent.
- **Evidence:** PR #62 head run `33507676888` and main run `33507775105` passed. PR #63 merged at `2ca852b47f16b8221275ee2b5542650d609b9a0d`; main run `33508253050` passed. The deployed bundle references both controlled revisions, and all eight response hashes match the approved files. Manny confirmed the requested live checks on 2026-09-01.
- **Product impact:** The Manaconda and Krios batch is complete. The next approved two-driver batch may enter visual review.
- **Approval:** Manny reported "Confirmed" after testing the deployed checkpoint on 2026-09-01.

## ADR-038: Approve the Keeg and McFleurdel front-action batch

- **Date:** 2026-09-01
- **Status:** Approved
- **Context:** After the Manaconda and Krios batch passed live testing, Manny authorized Keeg and McFleurdel as the next two-driver front-action batch. Keeg's first steering pair did not separate the directions clearly. McFleurdel's first review retained green and white matte in hair and arm gaps.
- **Decision:** Add four approved front-facing action frames for both drivers. Keeg's steering frames use opposite camera-side leans and distinct arm positions. McFleurdel's frames preserve black hair on the viewer's left and white hair on the viewer's right, with transparent black-curl interiors and arm gaps.
- **Regression controls:** The runtime gate decodes all eight files, checks 512 x 512 non-interlaced RGBA data and transparent corners, and rejects a connected pale matte component of 30 pixels or more in McFleurdel's reviewed steering gaps.
- **Controlled revisions:** `keeg-runtime-20260901-3` and `mcfleurdel-runtime-20260901-2`.
- **Scope:** Existing chase art, neutral front art, kart GLBs, placement, physics, stats, camera geometry, and shared selector behavior remain unchanged.
- **Approval:** Manny approved Keeg first, then approved McFleurdel after the corrected steering transparency review on 2026-09-01.

## ADR-039: Accept the Keeg and McFleurdel front-action batch

- **Date:** 2026-09-01
- **Status:** Approved
- **Context:** PR #65 deployed the approved Keeg and McFleurdel camera-facing steering, hit, and victory packages. PR #66 recorded the deployed bundle, regression coverage, and matching response hashes. The rollout blocked the next pair until Manny completed the live camera/action check.
- **Decision:** Accept `keeg-runtime-20260901-3` and `mcfleurdel-runtime-20260901-2`. Preserve all eight front-action files, the shared selector behavior, each driver's approved front placement, and their modeled steering-control ownership. McFleurdel's reviewed black-curl interiors and arm gaps remain transparent.
- **Evidence:** PR #65 head run `33563640441` and main run `33563732551` passed. PR #66 merged at `f8a2ed8be0d72fde62c9403dae4b15e94222f7da`; main run `33564231150` passed. The deployed bundle references both controlled revisions, and all eight response hashes match the approved files. Manny confirmed both steering directions, hit, victory, chase restoration, transparency, cockpit placement, and single-wheel presentation on 2026-09-01.
- **Product impact:** The Keeg and McFleurdel batch is complete. Lavi, Toph, Lula, and Accu remain on the governed neutral-front fallback until their separately approved packages are published.
- **Approval:** Manny's final "Approved" records product-owner live acceptance and authorizes publication of this documentation checkpoint.

## ADR-040: Approve the Lavi and Toph front-action batch

- **Date:** 2026-09-02
- **Status:** Approved
- **Context:** Keeg and McFleurdel passed live acceptance, leaving Lavi, Toph, Lula, and Accu on the neutral-front rollout fallback. Manny approved Lavi and Toph as the next two-driver batch, then reviewed their four camera-facing action candidates per driver.
- **Decision:** Integrate the approved front-steer-left, front-steer-right, front-hit, and front-victory frames for Lavi and Toph. Commanded left leans toward the viewer's right; commanded right leans toward the viewer's left. Both packages remain free of wheel and kart geometry because Potato and The Grave Shift supply modeled steering controls.
- **Transparency treatment:** Lavi's generated files preserve native alpha. Toph's generated previews contained an opaque checkerboard, so the reviewed derivatives remove the edge-connected background and a one-pixel alpha fringe without changing the approved character artwork. The runtime gate must decode all eight files as 512 x 512 non-interlaced RGBA PNGs and reject non-transparent corners.
- **Controlled revisions:** `lavi-runtime-20260902-5` and `toph-runtime-20260902-2`.
- **Scope:** Existing chase art, neutral front art, kart GLBs, placement, physics, stats, camera geometry, and modeled steering controls remain unchanged.
- **Publication gate:** This approval authorizes local runtime integration and validation. Publishing the branch, opening or merging a pull request, deploying, and recording live acceptance require a later explicit approval.
- **Approval:** Manny approved both candidate sheets on 2026-09-02.

## ADR-041: Correct Lavi's camera-facing placement and accept Toph

- **Date:** 2026-09-02
- **Status:** Approved for local correction; publication pending
- **Context:** The deployed Lavi and Toph batch passed asset delivery and state selection. Manny accepted Toph. Lavi's camera-facing layer rendered too low behind Potato's tall body, leaving the head near the modeled wheel and hiding the torso.
- **Decision:** Preserve Toph at `[0, 0.45, -0.12]`. Raise only Lavi's neutral front and four front-action states to `[0, 0.9, -0.12]`. Keep Lavi's chase-facing states at the existing default position.
- **Rationale:** Lavi's neutral front image places the hands about 0.46 world units below the face at the runtime sprite scale. Raising the layer by 0.45 moves the hands to Potato's wheel while exposing enough upper body for a seated composition. The value also matches the proven front-height correction used by Accu without copying Accu's depth or wheel override.
- **Scope:** No PNG or GLB bytes change. Toph, Potato, camera logic, physics, stats, action selection, chase-facing placement, and modeled steering controls remain unchanged.
- **Approval gate:** Publishing, merging, deploying, and recording Lavi's live acceptance require Manny's explicit approval.
- **Approval:** Manny rejected Lavi's low live placement and confirmed Toph passes on 2026-09-02.
