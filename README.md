# FretFlow

A static, interaction-focused guitar learning site hosted on GitHub Pages.

Live: https://karso1.github.io/fretflow-guitar-lab/

## What is included

- 40 songs with direct listening links, clearly identified recording versions and Bilibili search fallbacks.
- Original teaching commentary covering expression, harmony, accompaniment and singing, plus a 15-minute practice plan for each song.
- 40 archived PNG teaching sheets with chord diagrams and original accompaniment exercises. These are explicitly simplified practice material, not complete original-song scores.
- A playable six-string instrument, shared-title page transitions, animated filtering, keyboard search, chord synthesis and a persistent practice dock.
- Search, categories, difficulty filtering, favorites, practice checklists and notes.
- Private raster-score uploads stored in browser IndexedDB, with image backup export and restore. They are not uploaded to this repository or shared between devices.
- The original fretboard, capo, triad, harmony and practice tools, visually updated in `lab.html`. Existing local practice data is preserved.

## Preview

```sh
python3 -m http.server 8767
```

Open the served site. No build step, account, API key or backend is required. Audio starts only after user interaction. External videos and third-party charts need an internet connection and may have regional, embedding, login or payment restrictions.

## Content maintenance

Edit `tools/build_content.py`, then run it to generate `content/songs.json` and `songs.js`.
`tools/build_sheets.py` renders PNGs using Pillow and the configured CJK font (currently macOS STHeiti).
`tools/build_lab.py` derives the updated learning tools from `content/original.html`.

All original 14 score URLs are retained in the dataset, even where a newer primary entry is supplied. The site does not reproduce protected third-party full scores or lyrics.

## Interaction and accessibility

Motion respects `prefers-reduced-motion`. Core tasks work by keyboard; the command palette supports arrows, Enter and Escape. There is no scroll interception, background autoplay or required intro. The audio visualization is drawn from the Web Audio analyser rather than a fake waveform.

Libraries: Motion (MIT) and Lucide (ISC). See `vendor/` for the distributed licenses. UI motion was informed by Motion Primitives' public interaction patterns; its React components were not copied into this vanilla-JavaScript app.
