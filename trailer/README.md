# Teaser 02 "One Term" — visual assets

Styleframes for every beat of the 59-second narrative teaser: one presidency's
arc from a 2024 landslide to martial law. Full beat sheet:
`../docs/teaser-02-storyline.md`. Clip-by-clip production manifest (what to
animate vs. what to generate with fal, with prompts): `FAL-NOTES.md`.

- `frames/` — 3840×2160 PNG styleframes. Layout, palette, type and data are
  final-intent; motion is specified in FAL-NOTES.md.
- `frames/thumbs/` — 880px previews.
- `frames-src/` — HTML/CSS/JS sources; each frame is a 1920×1080 page rendered
  at 2× by `render.sh` (headless Chromium). Edit + re-run to update a frame.
  `data.js` carries real data extracted from the site: `VE_PATHS`/`VE`
  (270-tile Venezuela campaign, weekly control sets), `UA_TILES`/`UA_NEI`/
  `UA_CITIES`/`UAV` (Ukraine's 421 tiles at the 20 Jan 2025 seed), `CONGRESS`
  (119th Congress caucuses). `hero-map.jpg` is the in-game screenshot from
  index.html. Frame 20 hardcodes the real 2024 electoral result
  (312–226, state by state, ME-02/NE-02 splits). `world.js` carries
  real-geography paths generated from Natural Earth (110m world in Mercator,
  50m Iran/Persian Gulf) — all maps are drawn in the game theme, never
  screenshots.

## The cut (0:59)

| TC | Frame | Beat |
|---|---|---|
| 0:00 | 00-title-intro | Title intro — PoliGeo · The Ultimate Geopolitical Simulator |
| 0:03 | 00-2-hyperbole | "Rule Democratically… or with an Iron Fist" |
| 0:05.5 | 20-electoral-map | Real 2024 map — grey states populate on the call timeline |
| 0:08 | 01-wire-headline | "Election 2024… A Landslide Victory" (letters alternate red/blue) |
| 0:09 | 21-approval | Polling & approval, honeymoon +9 |
| 0:11 | 22-markets-wall | Candlestick + economy wall · "COMPUTED IN REAL TIME." |
| 0:13 · H1 | 04-one-world | Real-geography world map · 200+ NATIONS · "ONE SIMULATION." |
| 0:15 · H2 | 23-ukraine-timelapse | Invasion timelapse 2022 → 2025 seed |
| 0:19 · H3 | 06-every-word | Kremlin channel as a Signal interface — real demo dialogue |
| 0:21.5 | 12-redacted-cable | CIA // OPERATION STEEL CLAW — capture order |
| 0:23.5 | 24-minsk-raid | fal raid + CIA briefing: OPERATION SUCCESS |
| 0:25.5 · H4 | 25-invasion-headline | fal: coastal landing (helis + troops) + breaking banner |
| 0:27–0:31 | 26-puppet-regime · 27-insurgency | Control timelapse · wk 4 puppet-regime headline · wk 10 insurgency headline |
| 0:33 · H5 | 28-iran-warroom | CIA OPERATION EMBER + Joint Staff air-campaign briefing |
| 0:35.5 | 34-war-with-iran | WAR WITH IRAN — decapitation strikes ordered (fal) |
| 0:37 | 29-tehran-strike | fal: night strikes over Tehran |
| 0:39 | 30-iran-crackdown | fal: regime crackdown newsreel, thousands dead |
| 0:41 | 31-hormuz-closed | Iran closes the Strait of Hormuz |
| 0:43 | 32-home-unrest | Unrest · FEDERAL CRACKDOWN — LETHAL FORCE AUTHORIZED (fal) |
| 0:45.5 | 33-martial-law | Courts defied, martial law · "The only bounds on power are the ones you can overcome." |
| 0:48 | 15-the-hand | Sting: the hand stops at STRATEGIC RELEASE |
| 0:49.5 | 16-caesura | Silence · "Define the Nation's Future." |
| 0:50.5–0:59 | 17-title → 18-tagline → 19-endslate | **One continuous move**: the 3D PG cube spins in, settles, and lands locked over the end slate (COMING TO STEAM · OCTOBER 2026 · WISHLIST NOW) |

**Alternates** (rendered, not in this cut — for cutdowns/gameplay trailer):
02-newsreels, 03-oval-office, 05-every-vote, 07-every-war, 08-every-consequence,
09-existential, 10-real-time, 11-wall-of-screens, 13-militias-missiles,
14-unbounded. Music is not in the repo (a licensed/no-copyright Les Préludes
track drops in later); the tempo/pacing conform map is in FAL-NOTES.md.

## fal usage

Frames marked FAL in the cut are image references for generation — see
`FAL-NOTES.md` for per-clip prompts, durations and compositing notes.
Rules that apply to every generated clip: generic faces only, no real
persons or network branding, violence implied never shown, grade to ink
`#0b1220` / gold `#c9a54a` / ivory `#ece5d3`, and composite the frame's own
chyrons/watermarks over the output rather than asking the model for text.
