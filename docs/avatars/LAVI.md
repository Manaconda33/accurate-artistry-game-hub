# Avatar intake: Lavi

- **Intake date:** 2026-08-16
- **Current phase:** Complete 2D driver set, then Potato 3D preparation
- **Intake status:** Approved
- **Character lock:** Approved by Manny on 2026-08-16
- **Kart lock:** Approved by Manny on 2026-08-16
- **Balance mapping lock:** AA-02 Feather Technician, approved by Manny on 2026-08-16
- **Asset approval:** Portrait and all five driver frames approved and prepared
- **Implementation verification:** Not started

This record captures Manny's written description and the supplied reference image. Image observations remain reference-only unless they appear in an approved lock. Lavi is assigned stable roster ID `aa-02` and balance profile AA-02 Feather Technician.

## Identity

- **Proposed display name:** Lavi
- **Stable internal ID:** `aa-02`
- **Pronouns:** They/them
- **Short selection-screen descriptor:** Unresolved
- **Personality:** Curious, lively, and resourceful. They combine high-energy spontaneity with grounded logic.
- **Defining traits supplied by Manny:** Joyful confidence, energetic natural poise, curiosity, liveliness, and resourcefulness.
- **Traits or interpretations to avoid:** Do not remove or contradict their approved pronouns, personality, athletic build, hair and facial features, glasses, outfit, or other must-preserve details.

## Visual direction

### Supplied character description

- **Body type and presence:** Athletic, agile frame carried with joyful confidence and energetic, natural poise.
- **Hair:** Short, voluminous fiery ginger curls.
- **Eyes:** Bright green.
- **Face:** Freckles across their nose and cheeks.
- **Glasses:** Round, silver-rimmed wireframe glasses.

### Approved visual locks

- Lavi has a light, fair complexion with warm peach-pink undertones, matching the supplied reference image.
- Lavi's racing outfit is a muted-green ribbed sweater with a high crew or mock neckline, black trousers, and white platform boots with rainbow laces and matching rainbow sole accents.
- Small teal-blue stud earrings are part of Lavi's standard design.
- Race grime across Lavi's cheek is situational. It may appear during or after a race but is not a permanent facial marking.

### Reference presentation details

These details are observations, not approved locks:

- A lively, self-assured expression while driving.
- Pixel-art/comic-panel presentation with white photo borders and racing-game iconography.

### Approved character lock

- **Palette:** Fiery ginger hair, bright green eyes, silver glasses, teal-blue earrings, muted-green sweater, black trousers, white boots, and rainbow footwear accents.
- **Must preserve:** Short voluminous curl silhouette, round wireframe glasses, bright green eyes, facial freckles, athletic build, approved outfit, and teal-blue stud earrings.
- **Small-scale simplification:** Individual freckles, knit texture, earring reflections, and separate rainbow eyelets may simplify when the asset is too small to display them cleanly. The overall curl, glasses, green-eye, green-sweater, and rainbow-footwear read must remain.
- **Situational detail:** Cheek grime may appear during or after a race but should be absent from the clean base portrait.
- **Additional symbols or props:** None required.

## Kart direction

- **Final name:** Potato
- **Kart type:** Character-specific novelty kart
- **Approved concept:** Lavi rides a natural potato kart. The body must read immediately as a potato rather than a conventional chassis with potato decoration.
- **Approved construction language:** A hidden mechanical frame supports the natural potato body. Only essential hardware should remain visible.
- **Approved art direction:** Realistic yet whimsical. The potato should retain believable russet skin, organic asymmetry, and natural surface variation while remaining playful and readable as a racing vehicle.
- **Approved surface treatment:** Irregular russet skin, shallow potato eyes, light traces of dry soil, a few scuffs, and two or three short sprouts near the rear. Potato must have no rot, trailing roots, or anthropomorphic face.
- **Approved hardware:** Recessed matte-black cockpit, four exposed treaded black tires with weathered dark-metal hubs, a compact steering wheel, and two short silver exhaust pipes. Hardware must look practical and slightly handmade rather than glossy.

### Details visible in the reference image

These details are observations, not approved locks:

- A large russet-potato body with irregular eyes, dimples, and surface marks.
- A recessed black cockpit cut into the top of the potato.
- Four exposed black tires with simple dark hubs.
- Minimal mechanical hardware, including a steering wheel and short exhaust pipes.

### Still unresolved

- Construction details needed to support the GLB hierarchy, wheel movement, steering wheel, exhaust, driver mount, and item mounts.

### Approved kart lock

- **Palette:** Natural russet brown, dry-soil earth tones, muted sprout green, matte black, weathered dark metal, and restrained silver exhaust accents.
- **Signature detail:** Two or three short rear sprouts.
- **Emblem:** None recommended. Potato's organic silhouette is its identifying mark.
- **Permitted technical adjustment:** Wheel spacing, cockpit depth, and hidden frame geometry may change enough to satisfy collision, animation, and driver-mount requirements without weakening the natural-potato silhouette.
- **Prohibited treatment:** Rot, trailing roots, an anthropomorphic face, glossy racing bodywork, the reference number `1`, and `Potato Prix '24` branding.

### Excluded reference details

- The number `1` is not part of Lavi or Potato's canon.
- `Potato Prix '24` is not part of the game or character canon.

## Gameplay and roster mapping

- **Desired driving feel:** Nimble, responsive, and technical, with quick launch and precise control.
- **Preferred strengths:** Acceleration, Handling, and Mini-Turbo.
- **Accepted weaknesses:** Low collision resistance, weaker off-road performance, and modest top speed.
- **Weight class:** Featherweight.
- **Assigned AA balance profile:** AA-02 Feather Technician.
- **Stats:** Speed 5, Acceleration 8, Weight 2, Handling 9, Mini-Turbo 8, Traction 4. Total: 36.
- **Mapping rationale:** AA-02 rewards quick reactions, clean lines, and controlled drifting. Its low Weight and Traction give Lavi clear weaknesses and keep their feel distinct from balanced, off-road, cruiser, and heavyweight profiles.
- **Manny's mapping approval:** Approved on 2026-08-16.
- **Roster uniqueness:** AA-02 is assigned to Lavi and unavailable to all later characters. `docs/ROSTER-MAPPING.md` governs allocations.

## Required asset states

| Asset | Status | Notes |
|---|---|---|
| 256 x 256 transparent portrait | Approved and prepared | `public/assets/characters/aa-02/portrait.png`; RGBA and normal-Git runtime treatment verified. |
| 512 x 512 rear driver frame | Approved and prepared | `public/assets/characters/aa-02/driver/rear.png`; RGBA and normal-Git runtime treatment verified. |
| 512 x 512 steer-left frame | Approved and prepared | `public/assets/characters/aa-02/driver/steer-left.png`; RGBA and normal-Git runtime treatment verified. |
| 512 x 512 steer-right frame | Approved and prepared | `public/assets/characters/aa-02/driver/steer-right.png`; RGBA and normal-Git runtime treatment verified. |
| 512 x 512 hit frame | Approved and prepared | `public/assets/characters/aa-02/driver/hit.png`; RGBA transparency and normal-Git runtime treatment verified. |
| 512 x 512 victory frame | Approved and prepared | `public/assets/characters/aa-02/driver/victory.png`; RGBA transparency and normal-Git runtime treatment verified. |
| Kart GLB or approved fallback | Not started | Preferred GLB hierarchy is defined in PRD section 11.9. |
| Source and rights record | Approved | Manny created the supplied reference and approved its transformation into game assets on 2026-08-16. |

## Current reference

- **Supplied file:** `1000027702.png`
- **Creator and rights:** Manny; transformation into game assets approved on 2026-08-16.
- **Production style:** The game-wide PRD style, not the collage's pixel/comic treatment.
- **Repository treatment:** Not committed as a production asset. The image remains a landscape concept reference, not one of the required transparent portrait, driver-frame, or GLB deliverables.
- **Asset brief:** `docs/assets/LAVI-ASSET-BRIEF.md`.

## Next approval questions

Publish the completed 2D asset set and its evidence. After publication succeeds, begin Potato's 3D asset preparation.
