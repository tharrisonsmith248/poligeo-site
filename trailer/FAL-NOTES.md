# fal production notes — Teaser 02 "One Term"

Clip-by-clip manifest for building the trailer. Every clip is either
**ANIMATE** (motion-graphics/screen-capture built from the styleframe layers —
no generation) or **FAL** (generate video with fal, using the styleframe as
the image reference / first-frame conditioning, then grade and composite the
frame's UI chrome on top).

Global rules for all FAL clips:

- **Image ref**: pass the listed 4K frame from `frames/` as the reference /
  start frame; it fixes composition, palette and lighting.
- **Grade**: ink `#0b1220` shadows, gold `#c9a54a` practicals, ivory
  `#ece5d3` highlights. Cool navy night everywhere; warm gold is the only
  warmth in the film.
- **People**: generic faces only, never real persons or likenesses; crowds
  and anchors are anonymous. Real leaders exist only inside game UI (the
  Kremlin chat).
- **Violence**: implied, never graphic. Tracers, smoke, shields, silhouettes;
  no blood, no bodies, no injuries on camera.
- **Branding**: no real network logos. Composite the frame's own
  lower-thirds, watermarks (SIMULATED COVERAGE) and chyrons OVER the fal
  output — don't ask fal to render text (it garbles type).
- **Output**: 1080p or higher, 24 fps, 2–4 s per clip, subtle handheld or
  fixed-cam per note. Generate 3–4 variants per clip and pick in the edit.

## Clip list, in cut order

| # | TC | Ref frame | Type | Spec |
|---|----|-----------|------|------|
| 0 | 0:00 | 00-title-intro | ANIMATE | Cube glows in over faint province dots, wordmark resolves, gold rule draws, THE ULTIMATE GEOPOLITICAL SIMULATOR fades up letter-spaced. Calm — a lone horn/strings note, no drums yet. |
| 1 | 0:03 | 01-wire-headline | ANIMATE | Type-on with per-key jitter and key-click foley; cursor blink 1.1 s cycle. |
| 2 | 0:04.5 | 20-electoral-map | ANIMATE | States pop in call-order (safe states in bursts, the 7 gold-rimmed swing states one by one, GA last), EV counters run up to 312/226, "270 REACHED" chip lands with a soft gavel tick. |
| 3 | 0:07 | 21-approval | ANIMATE | Approval polyline draws left→right, big 57% odometer-rolls, cohort bars settle staggered, dots drift ±4 px. |
| 4 | 0:09 | 22-markets-wall | ANIMATE | Candles print one per 2 frames, tickers count, heatmap tiles pulse. |
| 5 | 0:11 | 04-one-world | ANIMATE | 4% push-out on the in-game map plate + counter races. (Optional: re-capture live from the game, DC → globe pull.) |
| 6 | 0:13 | 23-ukraine-timelapse | ANIMATE | Tile fills tween: 2025 base → Feb-2022 surge (0.8 s) → Nov-2022 pullback (0.8 s) → 2025 seed (1.2 s hold); stage chips light in sequence; EXISTENTIAL stamp slams last with a thud. |
| 7 | 0:17 | 06-every-word | ANIMATE | Putin bubble slides in, three replies flick, hostile reply locks with a key-click and gold flare. |
| 8 | 0:19.5 | 12-redacted-cable | ANIMATE | Cable types at 40 cps; black bars strike through words 3 frames after they appear; red EXECUTE annotation stamps at the end. |
| 9 | 0:21.5 | 24-minsk-raid | **FAL** | "Night exterior, neoclassical government palace in falling snow, five special-forces silhouettes stacked at the main door, two gold flashlight beams crossing, one dark van at the curb, single distant streetlight, deep navy shadows, cinematic still camera, slight snow drift, no gunfire, no faces." 2 s, fixed cam. Composite the frame's HUD (DENIABLE OPERATION · MINSK) + thermal readout on top. |
| 10 | 0:23.5 | 25-invasion-headline | ANIMATE | Banner cuts in on the hit; landing arrows draw over the dark tile map; ticker starts scrolling. |
| 11 | 0:25 | 26-puppet-regime (logic) | ANIMATE | Re-run the frame's week loop 1→4 at 10× (the JS already computes each week's tile set); fresh tiles flash gold rims. |
| 12 | 0:27 | 26-puppet-regime | ANIMATE | Hold week 4; chyron slides up. Optional 0.5 s FAL insert: "palace balcony at dusk, new flag unfurling, small crowd below, seen from far away, navy/gold grade, no faces." |
| 13 | 0:29 | 27-insurgency | ANIMATE | Week 10 map; insurgent tiles flicker crimson↔gold at 6 Hz; chyron slides up. Optional 0.5 s FAL insert: "jungle road at night, headlights of a pickup convoy through trees, silhouettes only, grainy long-lens." |
| 14 | 0:31 | 28-iran-warroom | ANIMATE | Panels populate top-down; strike markers pulse as ✓ lands on each; unrest dots flare gold; chyron up. |
| 15 | 0:33.5 | 08-every-consequence | ANIMATE | Third lever flips ON with a heavy clack; all three charts kink at the flip point; wire accelerates. |
| 16 | 0:35 | 29-tehran-strike | **FAL** | "Distant night skyline of a large Middle-Eastern city against a mountain ridge, anti-aircraft tracer lines rising slowly, two far-off orange explosion blooms with drifting smoke, city lights amber, deep navy sky, fixed long-lens news camera with slight atmospheric shimmer, no aircraft visible, no people." 2–3 s. Composite LIVE · TEHRAN slate + BREAKING chyron. |
| 17 | 0:37 | 30-iran-crackdown | **FAL** | "Grainy state-television footage at night: a dense crowd silhouetted against smoke and harsh spotlights, a line of riot shields in the foreground, tear-gas haze, warm sodium light against dark navy, handheld tremble, no violence on camera, no faces in focus." 2 s. Box it 4:3 inside the frame's monitor chrome; composite the fictional state-TV bar + Wire chyron. |
| 18 | 0:39 | 31-hormuz-closed | ANIMATE | The lane's dashes stop flowing; red X scribes on with two strokes; mines pop in; Brent candles print vertical; chyron up. |
| 19 | 0:41 | 32-home-unrest | **FAL** ×2 | (a) "American city avenue at dusk, very large protest crowd with banners and a road flare, government dome far in background, cool navy dusk with one warm flare, aerial-ish long lens, peaceful but tense, no faces in focus." 1.5 s. (b) "Night: police line advancing behind riot shields through drifting smoke, silhouettes only, blue-and-red light wash kept faint, no contact shown, handheld." 0.5–1 s, cut on the ORDER · ISSUED flare. Composite console UI + chyron from the frame. |
| 20 | 0:43.5 | 33-martial-law | ANIMATE | Headlines punch in one per beat; injunction doc slides in; RETURNED · UNREAD stamps with a thud; the card types on. Optional 0.5 s FAL insert: "armored vehicles parked on a wide empty capital boulevard at dawn, soldiers at ease, long shadows, no crowds, still camera." |
| 21 | 0:46 | 15-the-hand | **FAL** | "Extreme shallow-focus close-up: a hand enters frame in silhouette, fingers open, reaching toward a glowing brass lever knob, single warm key light on the knob, everything else near-black, the hand slows and stops just short, holds. No pull." 1.5 s. The frame gives the exact blocking; the hand must never touch the lever. |
| 22 | 0:47.5 | 16-caesura | ANIMATE | Instant type-on, dead silence. |
| 23 | 0:48.5 | 17-title | ANIMATE | 8–10 map tiles fly in along the frame's trail lines and lock into the cube on chord 1; wordmark resolves. |
| 24 | 0:50.5 | 18-tagline | ANIMATE | Rule draws on; tagline fades up. |
| 25 | 0:52.5 | 19-endslate | ANIMATE | Slate assembles top-down; CTA box draws on; hold ≥4 s; cut to black on the chord release; cursor keeps blinking to the last frame. |

## Assembly order

1. Lock the music: source/mock the marziale, place H1 at 0:11, caesura at
   0:47.5, chords at 0:48.5/0:50.5/0:52.5. Everything conforms to this.
2. Build all ANIMATE clips from `frames-src/` layers (each frame is HTML —
   animate with CSS/JS and screen-record at 4K60, or rebuild in AE from the
   PNGs).
3. Generate FAL clips (#9, 16, 17, 19, 21 + optional inserts), 3–4 variants
   each; grade; composite frame chrome on top.
4. Conform, add the diegetic foley layer (keys, gavel, stamp, lever clack,
   sonar pings — silence in the caesura), and land the end slate.
5. Deliverables: master 4K60 · Steam 1080p60 H.264+AAC with captions ·
   0:30 / 0:15 · 9:16 · poster frame at 0:53.
