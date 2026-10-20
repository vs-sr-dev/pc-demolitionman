# 01. The disc on the kit

What 3dokit reads on Demolition Man's disc, tool by tool. Every number
below was produced in session 1 with 3dokit at 2ae02a2 plus the changes of
`10-3dokit.md`, the commands as in the README, `PYTHONIOENCODING=utf-8`
throughout.

## The disc

The user's image is the US release as a MAME CHD (`Demolition Man
(USA).chd`, 336,061,105 bytes, CHD v5, SHA-1
22c8381b3d7ff8c4f537c461c685da5777956ab3, data SHA-1
3a4d1e9be95ccdba4cb4cc3a3ef4bdc4f50608c9): one track, `MODE1_RAW`, 225,068
frames. MAME's `chdman extractcd` turns it into a .cue and a raw .bin of
2352-byte sectors (`iso/dm.cue`, `iso/dm.bin`: 529,359,936 bytes, SHA-1
865eb9c9b224daa8fa13c5b1ccffb3680ffa4c5e), which the kit reads as it
reads Immercenary's.

```
dm.cue: raw 2352, 224768 blocks of 2048 (image 225068), label 'CD-ROM',
  root 1 block(s) x1 copies; 122 files, 15 directories, 391.8 MiB
  rom tag 0f.0d  v0.0   -> System/Kernel/boot_code (5050 bytes, tag says 5168)
  rom tag 0f.07  v0.16  -> System/Kernel/os_code (85896 bytes)
  rom tag 0f.0c  v0.0   offset 0xaac8441b size 0x0
  rom tag 0f.02  v0.0   -> launchme (179312 bytes, tag counts blocks from block 0)
```

* **`--verify`**: the root stored once; 2 entries stored more than once,
  2 extra copies -- 1 identical, 1 `rom_tags` copy with its own relative
  offsets. Nothing differs.
* **The OS is Escape from Monster Manor's and The Need for Speed's, byte
  for byte**: `boot_code`, `os_code`, `misc_code`, GRAPHIX, AUDIOFOLIO,
  OPERAMATH, GRAFMATH, the shell, the event broker, `STARTOPERA`, LMADM,
  FORMAT and the Control Port driverlets `CPORT1.ROM`, `CPORT41.ROM` and
  `CPORT4D.ROM` all have those discs' hashes -- Portfolio 21.10, GRAPHIX
  20.45 build 419. `CPORT49.ROM` (the mouse's) is The Need for Speed's
  first copy.
* **The tree** is almost all one file: **`DmanData/dmfc.bin`**, 409,868,288
  bytes, the game's own container (below), and **`launchme`**, the game.
  `AppStartup` is the stock empty one; the System tree is the full one
  (63 DSP instruments, the System's programs, the drivers).

## The executables

`aif --scan`: **39 AIF images, 5 compressed, 12 signed, 0 failing**.
`launchme`: 179,312 bytes, read-only 0x28a4c, read-write 0x24d8,
zero-init 0x1b490, 804 relocations, no 3DO binary header (node 0), as The
Need for Speed's.

* **`arm60 --check`**: 41,271 words agree with capstone, 0 disagree (316
  decoded by capstone are ARMv4 or later, or data).
* **`recomp.discover`**: 665 functions (2 the AIF header's, 162 found by
  calls, 394 by prologues, 106 reached only by pointers), 39 switches, no
  seeds, problems 0. At 2ae02a2 it found 655 and the boot stopped twice on
  a call to no function's entry: the game's script interpreter, whose
  handlers sit in two tables of the read-write data (0x29284 and 0x2931c
  on) and end in tail branches -- to another handler a table names
  (0xd514's `b 0x8f78`) or to a tail two handlers share (0x74ac and 0x74c8
  both `b 0x742c`). The kit learnt both (`10-3dokit.md`).
* **`portfolio --sites`**: 343 SWI sites (Kernel 286 calls, File 10, audio
  47), 113 folio vector sites, 112 attributed: Graphics 42 slots, Kernel
  25, audio 45. Items opened by name: `SPORT` twice, `timer`, the
  `Graphics` and `audio` folios -- and a device `mac`, the development
  station's host link, which the console does not have: the C library's
  `fwrite` (0x28540) opens it on its first write to a host file (0x283cc),
  and no run so far has written one.

## The container, `DmanData/dmfc.bin`

Read off the disc (`tools/dmfc.py`): a big-endian count (405), a word
0x800, then 405 pairs (offset, size) in bytes, each entry on a 2048-byte
block from 0x1000 on; the entries' sizes add up to 409,578,310 bytes. Its
contents are the game's own formats, which the recompiled code reads
itself, so the port needs none of them understood:

* 32 entries open with `DMAN` and a length -- the levels' data;
* 22 are 153,600 bytes, 320 x 240 pixels of 16 bits: whole screens;
* others open with words that read as cel control words with no chunk
  headers (`0xf0c60000`, `0xf1ee0000`, ...), the largest 12,889,281 bytes:
  the films and the sprites, in the game's own forms -- there is no
  DataStream on the disc (`stream --scan`: 0 streams).

`cel --check` finds no cel files and `audio --scan` only the System's
`sinewave.aiff`: the game's pictures and sound are all in the container.
`dsp --verify` passes on the 63 instruments of `System/Audio/dsp`.
