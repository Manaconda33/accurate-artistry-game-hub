# Lavi asset brief

## Authority and source

- **Character and kart locks:** Approved by Manny on 2026-08-16.
- **Balance mapping:** AA-02 Feather Technician, approved by Manny on 2026-08-16.
- **Reference creator:** Manny.
- **Transformation permission:** Manny confirmed permission to transform the supplied reference into game assets on 2026-08-16.
- **Reference role:** Identity, outfit, and kart design reference. The collage's pixel treatment, panel borders, text, number `1`, and `Potato Prix '24` branding are not production-art requirements.
- **Original source retention:** Keep the original reference unchanged. Derived assets must use separate filenames and approval states.

## Game-wide visual direction

Production assets follow PRD sections 2.1, 23, and 27:

- polished, colorful, kinetic, high-contrast, and arcade-oriented;
- original Accurate Artistry presentation rather than another kart title's character, UI, or rendering language;
- a 2D illustrated driver designed to sit convincingly inside a stylized 3D kart;
- lighting and material treatment matched to the 3D race scene so the driver does not read as a disconnected flat cutout;
- no pixel-art requirement from the supplied collage.

## Locked identity

- They/them pronouns.
- Light, fair complexion with warm peach-pink undertones.
- Short, voluminous fiery ginger curls.
- Bright green eyes and freckles across the nose and cheeks.
- Round silver-rimmed wireframe glasses.
- Small teal-blue stud earrings.
- Athletic, agile build with joyful confidence and energetic natural poise.
- Muted-green ribbed sweater with high crew or mock neckline, black trousers, and white platform boots with rainbow laces and matching sole accents.
- Clean base portrait has no cheek grime. Grime is situational during or after a race.

## Portrait concept

- **Purpose:** First visual approval anchor for all later driver states.
- **Canvas:** Square with a genuinely transparent background.
- **Framing:** Head, shoulders, and upper torso. Keep the full curl silhouette inside the canvas.
- **Expression:** Curious, lively, self-assured, and warmly alert.
- **Readability:** Face, curl silhouette, glasses, and green sweater must remain clear near 48 px.
- **Prohibited:** Text, logos, watermark, kart, racing number, panel border, cheek grime, pixel-art treatment, or changes to locked identity.

## Required production deliverables

| Asset | Required format | Approval state |
|---|---|---|
| Portrait | 256 x 256 PNG, transparent, sRGB, straight alpha | Approved and prepared |
| Rear driver frame | 512 x 512 PNG, transparent, sRGB | Approved and prepared |
| Steer-left frame | 512 x 512 PNG, transparent, sRGB | Approved and prepared |
| Steer-right frame | 512 x 512 PNG, transparent, sRGB | Approved and prepared |
| Hit frame | 512 x 512 PNG, transparent, sRGB | Approved and prepared |
| Victory frame | 512 x 512 PNG, transparent, sRGB | Not started |
| Potato kart | GLB with PRD hierarchy and LOD budgets | Not started |

Generated concepts remain candidates until Manny approves them. Approval of the portrait does not automatically approve the five driver states or Potato's 3D asset.

## Portrait candidate 1

- **Generated:** 2026-08-16.
- **Purpose:** Likeness and production-style review before driver-state work.
- **Source dimensions:** 1254 x 1254 px.
- **File validation:** PNG RGBA; genuine non-opaque alpha verified; transparent corner pixel verified.
- **Approval:** Manny approved the likeness on 2026-08-16.
- **Production derivative:** `public/assets/characters/aa-02/portrait.png`.
- **Production validation:** 256 x 256 PNG RGBA in sRGB; non-opaque alpha and transparent corner verified; normal-Git runtime-asset treatment confirmed.

## Rear driver candidate 1

- **Generated:** 2026-08-16.
- **Purpose:** Default seated rear-driving pose and silhouette review.
- **Source dimensions:** 1214 x 1295 px.
- **File validation:** PNG RGBA; genuine non-opaque alpha verified; transparent corner pixel verified.
- **Approval:** Manny approved the rear pose and silhouette on 2026-08-16.
- **Production derivative:** `public/assets/characters/aa-02/driver/rear.png`.
- **Production validation:** 512 x 512 PNG RGBA in sRGB; non-opaque alpha and transparent corner verified; normal-Git runtime-asset treatment confirmed.

## Steer-left candidate 1

- **Generated:** 2026-08-16.
- **Purpose:** Hard-left steering pose with the approved rear-driver crop and silhouette family.
- **Source dimensions:** 1254 x 1254 px.
- **File validation:** PNG RGBA; non-opaque alpha and transparent corner verified.
- **Approval:** Manny approved the steer-left pose on 2026-08-16.
- **Production derivative:** `public/assets/characters/aa-02/driver/steer-left.png`.
- **Production validation:** 512 x 512 PNG RGBA in sRGB; non-opaque alpha and transparent corner verified; normal-Git runtime-asset treatment confirmed.

## Steer-right candidate 1

- **Generated:** 2026-08-16.
- **Purpose:** Hard-right steering pose paired with the approved steer-left frame.
- **Source dimensions:** 1254 x 1254 px.
- **File validation:** PNG RGBA; non-opaque alpha and transparent corner verified.
- **Approval:** Manny approved the steer-right pose on 2026-08-16.
- **Production derivative:** `public/assets/characters/aa-02/driver/steer-right.png`.
- **Production validation:** 512 x 512 PNG RGBA in sRGB; non-opaque alpha and transparent corner verified; normal-Git runtime-asset treatment confirmed.

## Hit candidate 1

- **Generated:** 2026-08-16.
- **Purpose:** Reusable impact-recoil pose for spinouts, explosive hits, and major collision stuns.
- **Pose:** Rear seated crop with raised shoulders, ducked head, bouncing curls, and both hands thrown briefly away from the steering position. The reaction reads as surprised and kinetic without depicting injury.
- **Source dimensions:** 1254 x 1254 px.
- **File validation:** PNG RGBA in sRGB; alpha ranges from fully transparent to fully opaque, and the corner pixel is transparent. A checkerboard composite confirmed the cutout visually.
- **Approval:** Manny approved Hit Candidate 1 on 2026-08-16.
- **Production derivative:** `public/assets/characters/aa-02/driver/hit.png`.
- **Production validation:** 512 x 512 PNG RGBA in sRGB; alpha ranges from fully transparent to fully opaque, the corner pixel is transparent, and normal-Git runtime-asset treatment is confirmed.
