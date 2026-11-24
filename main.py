#!/usr/bin/env python3
"""news-23 b78 front-page-dense: copy entry.png (1024x1024) to $MAKEFUN_OUTPUT_DIR/entry.png.

Stdlib only (no PIL). Never writes next to itself: it writes only to MAKEFUN_OUTPUT_DIR,
so it also works from a read-only copy (with MAKEFUN_OUTPUT_DIR pointed elsewhere).
"""
import binascii
import hashlib
import os
import struct
import sys

MAX_BYTES = 1024 * 1024


def fail(msg):
    print("main.py: " + msg, file=sys.stderr)
    return 1


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is empty")
    out_dir_abs = os.path.abspath(out_dir)
    here_abs = os.path.abspath(here)
    if out_dir_abs == here_abs or out_dir_abs.startswith(here_abs + os.sep):
        return fail("MAKEFUN_OUTPUT_DIR must not be inside the repo")
    if not os.path.isfile(src):
        return fail("entry.png not found next to main.py")

    with open(src, "rb") as fh:
        data = fh.read()
    if len(data) > MAX_BYTES:
        return fail("entry.png is %d bytes, over the 1 MiB limit" % len(data))
    if len(data) < 8 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return fail("entry.png is not a PNG file")
    if len(data) < 57:
        return fail("entry.png is implausibly small (%d bytes)" % len(data))
    # Parse the IHDR chunk manually (no PIL): length, type, width, height,
    # bit depth, colour type, then its CRC.
    ihdr_len = struct.unpack(">I", data[8:12])[0]
    if data[12:16] != b"IHDR" or ihdr_len != 13:
        return fail("PNG IHDR chunk missing or malformed")
    width, height, bit_depth, colour_type = struct.unpack(">IIBB", data[16:26])
    if (width, height) != (1024, 1024):
        return fail("entry.png is %dx%d, expected 1024x1024" % (width, height))
    if bit_depth != 8 or colour_type not in (2, 6):
        return fail("unexpected PNG bit depth %d / colour type %d" % (bit_depth, colour_type))
    ihdr_crc = struct.unpack(">I", data[29:33])[0]
    if binascii.crc32(data[12:29]) & 0xFFFFFFFF != ihdr_crc:
        return fail("PNG IHDR CRC mismatch")
    # Walk every chunk: the last one must be a well-formed IEND (length 0,
    # correct CRC), and at least one IDAT must appear.
    pos, seen_idat, last_type = 8, False, None
    while pos + 8 <= len(data):
        clen = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        if pos + 12 + clen > len(data):
            return fail("PNG chunk %r overruns the file" % ctype)
        crc = struct.unpack(">I", data[pos + 8 + clen:pos + 12 + clen])[0]
        if binascii.crc32(data[pos + 4:pos + 8 + clen]) & 0xFFFFFFFF != crc:
            return fail("PNG chunk %r CRC mismatch" % ctype)
        if ctype == b"IDAT":
            seen_idat = True
        last_type = ctype
        pos += 12 + clen
        if ctype == b"IEND":
            break
    if last_type != b"IEND" or pos != len(data):
        return fail("PNG does not end with a well-formed IEND chunk")
    if not seen_idat:
        return fail("PNG has no IDAT chunk")

    os.makedirs(out_dir_abs, exist_ok=True)
    dst = os.path.join(out_dir_abs, "entry.png")
    with open(dst, "wb") as fh:
        fh.write(data)
    with open(dst, "rb") as fh:
        written = fh.read()
    if written != data:
        return fail("re-read of output does not match entry.png")
    print("entry.png: %d bytes, sha256 %s" % (len(data), hashlib.sha256(data).hexdigest()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
