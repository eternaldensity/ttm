# Troggle Trouble Math — Modern Recreation

Single-file HTML5 tribute to MECC’s 1994 Windows 3.11 / Mac game.
No original binaries, art, or audio embedded. No build step. No network.

## Run

Open `troggle.html` in any modern browser (Chrome/Edge/Firefox/Safari),
or serve it:

```sh
python3 -m http.server -d modern 8000
# → http://localhost:8000/troggle.html
```

## What was recreated (from the decompilation)

- 8 levels with the original names/order: Bongo Falls → Gobble Desert →
  Muncher Cave → Troggle Swamp → Muncher Cave → Gobble Desert →
  Bongo Falls → Transition Zone.
- Per level: 3 chests, 1 clue item + 2 treat boxes (items match the
  recovered Magenta scripts: TROG oil, energy crystal, jet pack, … Muncher).
- Triad from the original: **story problems** (grade-tagged like `[#123]`),
  **troggulate-by-equation** (`N` troggles → equation equal to `N`, `+` required),
  **60-second drills** to recharge.
- Energy (troggulate −10, phone −5, chest +10, drill +4/correct) and
  3 treat boxes as lives (3 strikes → Sparky goes home).
- Grades 1–7 scaling numbers/ops; Magenta phone/log; Bone-A-Fide Heroes
  high scores; save/load via `localStorage`; Space = troggulate, Esc = close.

See `../docs/DECOMPILATION.md` for the ISO/Instalit/NE/MCL findings and
`../tools/extract_instalit.py` for the byte-exact extractor.
