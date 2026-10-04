# Troggle Trouble Math — Decompilation Report

Source: `Troggle Trouble Math (1994)(MECC)[Mac-PC].iso` (30,570,496 bytes, 14927×2048).
Hybrid Mac/PC disc. Volume ID `TROGGLE_TRO`. PC side is ISO9660; Mac side is HFS
(partition map at LBA 1). This report covers the PC side (Windows 3.11 game).

## 1. ISO layout (PC side, from PVD root at extent 20)

```
ACROREAD.EXE  1.4 MB   Acrobat reader (bundled docs)
AOL/SETUP.EXE 1.9 MB   America On-Line installer (unrelated shovelware)
AUTORUN.INF, DISK.ID, TEXT.CFG, PRODUCTS.LST, PRODUCT.PF
SETUP.EXE     232,231  Instalit 5.01w stub (NE 16-bit, PKWARE DCL 1.03)
INSTLL.EXE    141,312  MFC 1.0 “CD-ROM Installation” launcher (NE 16-bit, shows SSCREEN.BMP)
SSCREEN.BMP   308,278  8-bit 640×480 splash  | TLOGO.BMP 38,638 | SOFTKEY.ICO
TROGGLE.001   1,175,552  Instalit volume 1 (data + directory + disk table)
TROGGLE.002   1,457,152  Instalit volume 2 (data only)
TROGGLE.003   1,457,152  Instalit volume 3 (data only)
TROGGLE.004     148,371  Instalit volume 4 (data only, tail)
TROGGLE.INF       9,351  Instalit script (SoftKey dialect: DefineVariables, CopyFiles, QueAllFiles, ProgramManagerDDE, WritePrivateProfileString → TROGGLE.INI MusicFlag/SoundFlag)
WHAT.EXE        3,170  DOS menu helper used by FUN.BAT/INN.BAT
INN/          ~8 MB    ImagiNation Network DOS bundle (PART.1 7.7 MB + drivers/docs, unrelated)
MANUALS/MANUAL.PDF 1.16 MB scanned manual (image-heavy; text streams are mostly raster)
```

`SETUP.EXE` strings: `Version 5.01w`, `Stub to copy Instalit/Shadow and execute it`,
`Pgmloadr/Shadow/EXEFILE/BWCC.DLL`, `PKWARE Data Compression Library(tm) ... Version 1.03`,
`934730434875` (installer ID, also stored in volume 1 tail).
`INSTLL.EXE` strings: `products.lst`, `text.cfg`, `sscreen.bmp`, MFC `CInstaDoc/CInstaView`.

## 2. Instalit volumes (TROGGLE.001–.004)

Concatenated physical size 4,238,227. Each volume is a slice of one logical
implode stream; only volume 1 carries the directory.

- Data length of volume 1: `0x11E837` = **1,173,559** bytes (`d1[0:1173559]`).
  Tail key: `05 "[PVM]"` at 1173559, then file directory, then HMW disk table,
  then `0C "934730434875"`, `C6 EA 11 00`, `37 E8 11 00`.
- Disk table (`HMW44110D?`): `TROGGLE.001→DISK 2 … TROGGLE.004→DISK 5`,
  `TROGGLE.005–008 → FFFFFFFF` (floppy-only, absent on CD).
  Split points stored after each name match exactly:
  `1173559`, `1173559+1457152=2630711`, `+1457152=4087863`.
- Logical stream = `d1[0:1173559] + d2 + d3 + d4` = **4,236,234** bytes
  (physical minus 1993 bytes of directory/HMW).

File directory: 11 entries, each `1C <u32 comp_off> F0 <filename>\0 + ~42–52 bytes meta`.
`comp_off` is the blast-stream start in the logical stream:

| file | comp_off | comp_len | uncomp |
|---|---|---|---|
| TROGGLE.EXE | 0 | 174,633 | 456,208 (NE 16-bit) |
| 1000.MID | 174,633 | 3,607 | 16,837 |
| 2000.MID | 178,240 | 2,030 | 7,936 |
| 3000.MID | 180,270 | 4,556 | 17,321 |
| 4000.MID | 184,826 | 2,473 | 7,359 |
| 500.MID | 187,299 | 679 | 3,550 |
| 5000.MID | 187,978 | 7,604 | 35,024 |
| 600.MID | 195,582 | 2,685 | 11,511 |
| TROGHELP.HLP | 198,267 | 47,807 | 175,111 (WinHelp) |
| DATA.MCL | 246,074 | 1,306,204 | 3,254,443 (MECC resources) |
| SOUND.MCL | true 1,552,278 (= dir 378,719 + 1,173,559) | 2,683,956 | 3,996,108 (MECC resources) |

Meta after each filename: `[XE\0|HLP\0|…] C3 20|20 <u32 comp_len> <u16 date> <6B> <01 01 01|08 01 01 01|02 02 01> <u32 uncomp_len> …`.
`comp_len`/`uncomp_len` verified by actually exploding each stream.

Compression is PKWARE DCL **implode** (`00 06 …` headers). Verified with
`dclimplode` (`decompressobj_blast`): first stream explodes to `MZP…` (MZ header),
MIDIs to `MThd…`, MCLs to `X\0 … MECC…`. Minimal prefix for EOF was used to
recover exact `comp_len` (e.g. TROGGLE.EXE needs 174,633 bytes → 456,208 out;
extra trailing bytes are ignored, which is how sequential extraction works).

Anomaly: directory `SOUND.MCL comp_off` (378,719) is the **volume-2-local**
offset; true logical start is +1,173,559. Its meta `comp_len` (2,683,956)
equals `logical_len − 1,552,278`, confirming the fix. `00 60 35 …` at the
stale offset is interior bytes of DATA.MCL’s stream (blast error −2), not a
stream start.

## 3. TROGGLE.EXE (456,208 bytes, NE 16-bit, Borland C++ 1993)

`MZ` → `e_lfanew 0x80` → `NE 05 1E`. Classes: `TProblemGenerator, CTroggulatorPane,
TTroggulator, CModuleManager, CSpTrog/CTrogGrp/CSpTrogb, CSpMuncher, CSpFrank,
CSpIntroTrog, CPuzzlePane, CHiScore, GameTimer, GradeData/SubGrade`.
Windows: `TROG/BORDER/ANIM/STATUS BAR/TROGGULATOR/XOVER/HISCORE/INTRO/PUZZLE/INFOBAR`.
Key strings:

- Levels: `Level 1: Bongo Falls`, `Level 2: Gobble Desert`, `Level 3: Muncher Cave`,
  `Level 4: Troggle Swamp`, `Level 5: Muncher Cave`, `Level 6: Gobble Desert`,
  `Level 7: Bongo Falls`, `Level 8: Transition Zone`, `Level to Level`.
- Systems: `Ready to troggulate!`, `No troggles to troggulate!`,
  `Not enough energy to troggulate!/to call Magenta!`, `Energy cells are full!`,
  `You must enter an equation.`, `You must use the + key`, `You can't use zero./1.`,
  `energy crystals`, `Sparky treats`, `drills`, `%d troggle`,
  `Grade Level:`, `Set the math grade level:`, `Adding:/Subtracting:/Multiplying:/Dividing:`,
  `Overall Success*`, `Bone-A-Fide Heroes`, `Hiscore0-3`, `Puzzle Room`,
  `Game paused. Click to continue.`, `TROGGLE.INI (MusicFlag/SoundFlag)`,
  `DATA.MCL is not in the … directory`, `256-color … 16-color` warning, MIDI-unavailable warning.
- Credits: Chuck Bilow; Mike Palmquist; Mark Paquette; Lester Craven; Al Lathrop;
  John Ojanen; Kirk Sumner; John Wlazlo; DeeDee Daus; Sheila Kelly; Ed Madrid;
  Larry Phenow; Glen Anderson; Chad Iverson; Mark Larson; Marty Euerle;
  Michael Oltmans; Timothy Roseth; Troy Small; LaDonna Williams; Elizabeth Grobel;
  Sally Ramirez; Tim Russell.

Gameplay (EXE + reviews + recovered text): 8-level rescue (Magenta + dog Sparky
vs robot TROG → Dr. FrankenTroggle, kidnapped Muncher). Per world: 3 hidden
chests (1 clue item + 2 treat boxes), chests opened by **story problems**;
random **troggle attacks** beaten by typing an equation equal to the troggle
count into the **Troggulator** (treats = lives, 3 strikes → Sparky sent home);
**1-minute drills** recharge energy. Grade levels 1–7 scale numbers/ops.

## 4. DATA.MCL (3,254,443 bytes) — MECC resource library `MECC … Troggle … 1.0`

Header `58 00` (=88), `MECC`, `Troggle`, `1.0`, `0E 00` (=14 entry size),
`16 08` (=2070 entries). Type dir (14×8B at 0x58): `TYPE(4)+count(2)+start(2)`.
Resource entries (2070×14B at 0xC8): `TYPE(4)+ID(2)+SIZE(4)+OFFSET(4)`.

Counts: CBMP 1070, STRP 255, RLES 173, ASEQ 171, ACEL 170, STR5 84, GSUB 60,
STR4 30, STR3 25, STR1 12, STR2 12, GRAD 6, CSTR 1, SPOS 1.
Tags: CBMP = compressed bitmap, RLES = RLE sprite, ASEQ/ACEL = animation,
STR1/STR2 = troggulator right/wrong one-liners (`[#…]` voicing + `[^…]` retry
level), STR3/STR4 = chest right/wrong with hints, STR5 = Magenta/TROG/end scripts
(2101s intro, 2201s troggulator lesson, 2301–2316 level clues/items, 2401–2416
hints, 2501–2513 busy lines, 2601–2610 sign-offs, 2701 TROG freed, 2702–2703
villain lines, 2801–2803 out-of-treats), STRP = 255 story templates
(`[#grades][@title]…[A][B][G][H][J][K][M][N][p][q][S]/[U]…[$Words]…[!formula]`),
GSUB (60×314B) = per-problem numeric generation params, GRAD (6) = grade tables,
CSTR/SPOS = small control tables.

## 5. SOUND.MCL (3,996,108 bytes) — `MECC … 61 00 …`

Same container. `RSND` ×161 audio resources. No RIFF/WAV magic in the raw
logical remainder (expected: MECC-packaged wave data, needs a separate RSND
parser — not required for the recreation, which re-synthesizes audio).

## 6. Other payloads

- 7× `.MID` (`MThd`, 3.5–35 KB, “Windows Basic”): background music; preserved in
  `decoded/` but re-rendered as WebAudio in the modern build.
- `TROGHELP.HLP` 175 KB WinHelp; `PRODUCT.PF` site-license stub.
- Mac HFS side not analyzed (PC game logic is complete without it).

## 7. Reproduction

Pure-Python ISO9660 reader (PVD extent 20) → extract `TROGGLE.00{1..4}` →
`logical = d1[:1173559]+d2+d3+d4` → PKWARE-DCL-blast each `comp_off`
(SOUND at `378719+1173559`) → verify `MZ/MThd/MECC` magics and
`comp_len/uncomp_len` against directory meta. See `tools/extract_instalit.py`.

## 8. Modern recreation

`modern/troggle.html` is a clean-room, single-file HTML5 implementation of the
loop above (8 levels, 3 chests, story/story-drill/troggulate triad, energy +
3 treat boxes, grade 1–7 scaling, Magenta phone, drills, high scores,
save/load). No original binary assets are embedded; story wording, art, and
audio are newly created in the same spirit. Original MIDIs/HLP/MCLs remain
only in `decoded/` for preservation.
