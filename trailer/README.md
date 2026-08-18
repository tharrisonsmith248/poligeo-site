# Teaser 01 — visual assets

Styleframes for every beat of the 38-second announcement teaser
(see `../docs/teaser-01-treatment.md` for the full treatment).

- `frames/` — 3840×2160 PNG styleframes, one per beat, in cut order.
  These are the frame of reference for animation: layout, palette, type,
  and data are final-intent; motion is described in the treatment.
- `frames/thumbs/` — 880px previews of the same frames.
- `frames-src/` — the HTML/CSS/JS sources. Each frame is a 1920×1080 page
  rendered at 2× by headless Chromium (`frames-src/render.sh`). Edit the
  HTML, re-run the script, and the PNG updates. `data.js` carries real data
  extracted from the site: `VE_PATHS`/`VE` (the 270-tile Venezuela campaign),
  `UA_TILES`/`UA_NEI`/`UA_CITIES`/`UAV` (Ukraine's 421 tiles at the
  20 Jan 2025 seed), and `CONGRESS` (119th Congress caucus data).
  `hero-map.jpg` is the engine screenshot embedded in index.html.

## Frame → beat map

| Frame | Beat | Music cue | Built from |
|---|---|---|---|
| 01-wire-headline | 0:00 cold open | silence, ticker keys | Wire ticker |
| 02-newsreels | 0:01.5 | timpani roll begins | **fal ref** — 3 news reels |
| 03-oval-office | 0:04 | swell peaks | **fal ref** — Oval still + parallax |
| 04-one-engine | 0:06 H1 | crash, theme bar 1 | engine screenshot (hero-map.jpg) |
| 05-every-vote | 0:08 H2 | antecedent bar 3 | real 119th Congress caucus data |
| 06-every-word | 0:10 H3 | consequent begins | site diplomacy demo copy |
| 07-every-war | 0:12 H4 | consequent cadence | real 270-tile engine run, week 6 |
| 08-every-consequence | 0:14 H5 | broadening phrase | site lever demo + ripple charts |
| 09-existential | 0:18 H6 | answering phrase | real 421-tile Ukraine seed |
| 10-real-time | 0:20 | statement closes | PAM (203 agents) + barometer |
| 11-wall-of-screens | 0:22 H7 | stretto begins | **fal ref** — broadcast mosaic |
| 12-redacted-cable | 0:23 | motif step 2 | motion-gfx layout |
| 13-militias-missiles | 0:24 | motif steps 3–4 | engine-style map plates |
| 14-unbounded | 0:26 H8 | peak tutti | posture-ladder UI |
| 15-the-hand | 0:28 | music cuts off | **fal ref** — pre-title sting |
| 16-caesura | 0:29.5 | dead silence | type card |
| 17-title | 0:30 chord 1 | cadence chord 1 | assets/logo-pg.png + wordmark.png |
| 18-tagline | 0:32 chord 2 | cadence chord 2 | wordmark + tagline |
| 19-endslate | 0:34–0:38 | chord 3 held | end slate (Oct 2026 + wishlist CTA) |

## fal generation notes

Frames marked **fal ref** are compositions to feed as image references;
generate the live-action/photoreal versions with fal, then grade to the
frame's palette (ink `#0b1220`, gold `#c9a54a`, ivory `#ece5d3`) so
everything sits in one world. Keep all persons generic — no real faces,
no real network branding.

- **02 news reels** (×3, ~1s each, 4:3): "1990s-to-modern broadcast news
  footage, dark studio anchor desk mid-sentence / night motorcade with
  security escort / aircraft-carrier deck at dawn, deep navy grade, gold
  practicals, slight scanline texture, generic anchor, no logos."
  Composite the frame's lower-thirds and SIMULATED COVERAGE watermark on top.
- **03 Oval Office** (still → 2.5D parallax): "empty presidential office at
  dawn, resolute-style desk, high-back chair turned away, three tall arched
  windows, warm low light through glass, dust motes, dark navy shadows,
  cinematic, no people." Push in 4% over 2s.
- **11 wall of screens**: generate 3–4 anchor/broadcast clips (different
  languages/sets) and tile them into the frame's 4×3 mosaic; the mosaic
  chrome, lower-thirds and EMERGENCY plates come from the frame.
- **15 the hand**: "out-of-focus silhouette of a hand entering frame,
  fingers open, reaching toward a glowing brass lever and stopping short,
  single warm key light, everything else near-black." The frame gives the
  blocking; fal gives the photoreal hand. It must NOT touch the lever.
- **10 insets (optional)**: half-second crowd clips (confetti / protest)
  boxed like the 02 reels.

Everything else (maps, congress, chat, charts, ladder, cable, title cards)
animates from the real UI/engine layers in these frames — no generation
needed.
