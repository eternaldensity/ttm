#!/usr/bin/env python3
"""Extract Troggle Trouble Math Instalit volumes without mounting.

Reads the ISO9660 PC side, pulls TROGGLE.001-004, rebuilds the logical
PKWARE-DCL stream (d1[:1173559]+d2+d3+d4) and explodes each file.

Needs a DCL-implode decoder (e.g. pip package `dclimplode` providing
decompressobj_blast). SOUND.MCL uses logical offset 378719+1173559.
"""
import os, struct, sys

ISO = os.path.join(os.path.dirname(__file__), "..",
                   "Troggle Trouble Math (1994)(MECC)[Mac-PC].iso")
OUT = os.path.join(os.path.dirname(__file__), "..", "decoded")
DATA_LEN = 1173559  # d1 data length (0x11E837); dir starts with 05 "[PVM]"
FILES = [
    ("TROGGLE.EXE",  0x000000),
    ("1000.MID",     0x02AA29),
    ("2000.MID",     0x02B840),
    ("3000.MID",     0x02C02E),
    ("4000.MID",     0x02D1FA),
    ("500.MID",      0x02DBA3),
    ("5000.MID",     0x02DE4A),
    ("600.MID",      0x02FBFE),
    ("TROGHELP.HLP", 0x03067B),
    ("DATA.MCL",     0x03C13A),
    ("SOUND.MCL",    0x05C75F + DATA_LEN),  # dir stores volume-2-local off
]

def parse_dir(extent, length, f):
    f.seek(extent * 2048)
    data = f.read(length)
    off, out = 0, []
    while off < len(data):
        ln = data[off]
        if ln == 0:
            off = ((off // 2048) + 1) * 2048
            continue
        rec = data[off:off + ln]
        flags = rec[25]
        ext = struct.unpack("<I", rec[2:6])[0]
        size = struct.unpack("<I", rec[10:14])[0]
        nl = rec[32]
        out.append((rec[33:33 + nl].decode(), flags, ext, size))
        off += ln
    return out

def main():
    iso = sys.argv[1] if len(sys.argv) > 1 else ISO
    out = sys.argv[2] if len(sys.argv) > 2 else OUT
    os.makedirs(out, exist_ok=True)
    with open(iso, "rb") as f:
        f.seek(16 * 2048 + 156)
        root = f.read(34)
        rext = struct.unpack("<I", root[2:6])[0]
        rlen = struct.unpack("<I", root[10:14])[0]
        ents = {n.split(";")[0]: (e, s) for n, fl, e, s in parse_dir(rext, rlen, f)}
    vols = []
    with open(iso, "rb") as f:
        for i in (1, 2, 3, 4):
            e, s = ents[f"TROGGLE.00{i}"]
            f.seek(e * 2048)
            vols.append(f.read(s))
    d1, d2, d3, d4 = vols
    assert len(d1) == 1175552 and d1[1173559:1173565] == b"\x05[PVM]", "volume 1 layout changed"
    logical = d1[:DATA_LEN] + d2 + d3 + d4
    print(f"logical stream: {len(logical)} bytes")
    try:
        import dclimplode
    except ImportError:
        print("install `dclimplode` to decompress (pip install dclimplode)")
        return 1
    for name, off in FILES:
        obj = dclimplode.decompressobj_blast()
        blob = obj.decompress(logical[off:])
        assert obj.eof, name
        open(os.path.join(out, name), "wb").write(blob)
        print(f"{name:15s} off={off:7d} -> {len(blob):7d} bytes")
    print("magic check: EXE=MZ, MID=MThd, MCL=MECC")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
