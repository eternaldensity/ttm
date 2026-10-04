# Troggle Trouble Math (1994, MECC) — Decompiled + Modern Recreation

The bundled ISO only runs on Windows 3.11. This repo preserves it and ships a
playable modern tribute that runs in any current browser.

- **Play it:** open `modern/troggle.html` (or `python3 -m http.server -d modern 8000`).
  Live build deploys from `modern/` via GitHub Actions → Pages.
- **How the original works:** [`docs/DECOMPILATION.md`](docs/DECOMPILATION.md) —
  ISO layout, Instalit multi-volume archive, PKWARE DCL streams, NE 16-bit
  executable, MECC resource libraries (255 story templates, 84 Magenta scripts).
- **Re-extract the original files:** [`tools/extract_instalit.py`](tools/extract_instalit.py)
  rebuilds the logical stream (`d1[:1173559]+d2+d3+d4`) and explodes all 11
  payloads. Needs a DCL-implode decoder (e.g. `pip install dclimplode`).

## Layout

```
modern/troggle.html   single-file HTML5 tribute (no build, no network)
docs/DECOMPILATION.md full decompilation report
tools/extract_instalit.py  byte-exact ISO → payload extractor
```

## Notes

- The 30 MB source ISO stays local (gitignored) and no 1994 binaries, art, or
  audio are embedded in the recreation — mechanics, level order, and wording
  are clean-room work in the same spirit.
- Original payloads (EXE, MIDs, MCLs) belong to MECC/SoftKey; the extractor is
  for preservation on media you own.
