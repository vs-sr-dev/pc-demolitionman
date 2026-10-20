"""Demolition Man's container, DmanData/dmfc.bin.

Layout (read off the disc): a big-endian word count N, a word 0x800, then
N pairs (offset, size) in bytes, each entry starting on a 2048-byte block.

    python tools/dmfc.py build/disc/DmanData/dmfc.bin            # the table, each entry's kind
    python tools/dmfc.py build/disc/DmanData/dmfc.bin --extract build/dmfc
"""
import argparse
import os
import struct
import sys


def read_table(f):
    f.seek(0)
    n, hdr = struct.unpack('>II', f.read(8))
    ents = [struct.unpack('>II', f.read(8)) for _ in range(n)]
    return hdr, ents


def kind(head):
    tag = head[:4]
    if tag in (b'CCB ', b'PLUT', b'PDAT', b'IMAG', b'ANIM', b'XTRA', b'SCEL'):
        return 'cel:' + tag.decode()
    if tag == b'FORM' and head[8:12] in (b'AIFF', b'AIFC'):
        return head[8:12].decode().lower()
    if tag in (b'SHDR', b'FILM', b'SNDS', b'CTRL', b'FILL', b'SCEL'):
        return 'stream:' + tag.decode()
    if head[:4] == b'\x00\x00\x00\x00' and head[8:12] in (b'SHDR', b'FILM', b'CTRL', b'SNDS'):
        return 'stream?'
    if head[0x10:0x14] == b'\xe1\xa0\x00\x00' or head[:4] in (b'\xe1\xa0\x00\x00',):
        return 'aif'
    if all(32 <= c < 127 or c in (9, 10, 13) for c in head[:32]):
        return 'text'
    return 'data'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('file')
    ap.add_argument('--extract')
    a = ap.parse_args()
    with open(a.file, 'rb') as f:
        size = os.fstat(f.fileno()).st_size
        hdr, ents = read_table(f)
        print(f'{len(ents)} entries, header word 0x{hdr:x}, file {size} bytes')
        prev_end = 0
        for i, (off, ln) in enumerate(ents):
            f.seek(off)
            head = f.read(64)
            gap = off - prev_end
            prev_end = off + ln
            print(f'{i:4d} @0x{off:08x} {ln:10d}  {kind(head):14s} {head[:16].hex()}'
                  + (f'  gap {gap}' if gap >= 2048 else ''))
            if a.extract:
                os.makedirs(a.extract, exist_ok=True)
                f.seek(off)
                with open(os.path.join(a.extract, f'{i:03d}.bin'), 'wb') as o:
                    o.write(f.read(ln))
        if prev_end > size:
            print('past the end of the file!', file=sys.stderr)


if __name__ == '__main__':
    main()
