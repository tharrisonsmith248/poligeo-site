# Teaser 02 "One Term" — visual assets

Styleframes for every beat of the 56-second narrative teaser: one presidency's
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
  (119th Congress caucuses). `hero-map.jpg` is the engine screenshot from
  index.html. Frame 20 hardcodes the real 2024 electoral result
  (312–226, state by state, ME-02/NE-02 splits).

## The cut (0:56)

| TC | Frame | Beat |
|---|---|---|
| 0:00 | 01-wire-headline | Cold open — the engine calls the election |
| 0:02 | 20-electoral-map | Real 2024 map, 312–226 · "A LANDSLIDE." |
| 0:05 | 21-approval | Polling & approval, honeymoon +9 |
| 0:07.5 | 22-markets-wall | Candlestick + economy wall · "COMPUTED IN REAL TIME." |
| 0:10 · H1 | 04-one-engine | Brass slam — engine globe · "ONE ENGINE." |
| 0:12 · H2 | 23-ukraine-timelapse | Invasion timelapse 2022 → 2025 seed |
| 0:16 · H3 | 06-every-word | Kremlin channel — most hostile reply sent |
| 0:18.5 | 12-redacted-cable | Covert order: capture the President of Belarus |
| 0:20.5 | 24-minsk-raid | fal: the Minsk raid |
| 0:22.5 · H4 | 25-invasion-headline | "US launches full-scale invasion of Venezuela" |
| 0:24–0:28 | 26-puppet-regime · 27-insurgency | Control timelapse · wk 4 puppet-regime headline · wk 10 insurgency headline |
| 0:30 · H5 | 28-iran-warroom | Iran war interface: covert unrest + air campaign |
| 0:32.5 | 08-every-consequence | Decapitation strikes lever flips ON |
| 0:34 | 29-tehran-strike | fal: night strikes over Tehran |
| 0:36 | 30-iran-crackdown | fal: regime crackdown newsreel, thousands dead |
| 0:38 | 31-hormuz-closed | Iran closes the Strait of Hormuz |
| 0:40 | 32-home-unrest | Leftist unrest · ORDER: FEDERAL CRACKDOWN (fal clips) |
| 0:42.5 | 33-martial-law | Courts defied, martial law · "The only bounds on power are the ones you can overcome." |
| 0:45 | 15-the-hand | Sting: the hand stops at STRATEGIC RELEASE |
| 0:46.5 | 16-caesura | Silence · "The Ultimate Geopolitical Simulator." |
| 0:47.5 | 17-title | PG cube + wordmark (85% of runtime) |
| 0:49.5 | 18-tagline | "History is in session." |
| 0:51.5 | 19-endslate | COMING TO STEAM · OCTOBER 2026 · WISHLIST NOW |

**Alternates** (rendered, not in this cut — for cutdowns/gameplay trailer):
02-newsreels, 03-oval-office, 05-every-vote, 07-every-war, 09-existential,
10-real-time, 11-wall-of-screens, 13-militias-missiles, 14-unbounded.

## fal usage

Frames marked FAL in the cut are image references for generation — see
`FAL-NOTES.md` for per-clip prompts, durations and compositing notes.
Rules that apply to every generated clip: generic faces only, no real
persons or network branding, violence implied never shown, grade to ink
`#0b1220` / gold `#c9a54a` / ivory `#ece5d3`, and composite the frame's own
chyrons/watermarks over the output rather than asking the model for text.
