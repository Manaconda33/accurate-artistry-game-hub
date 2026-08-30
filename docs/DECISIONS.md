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
