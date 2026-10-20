# What this port gave 3dokit

3dokit (`3dokit/`, a submodule from
[vs-sr-dev/3dokit](https://github.com/vs-sr-dev/3dokit)) was started by
Immercenary's port and grew on Crash 'n Burn's, Doctor Hauzer's, Escape
from Monster Manor's and The Need for Speed's; Demolition Man is its sixth
game, the third on Portfolio 21.10 (the very OS images of the two before
it), and the first with a light gun. The submodule was taken at
**2ae02a2**; it is at **d04785d**.

## Session 1

One commit, **d04785d**. What it adds:

| file | What |
|---|---|
| `runtime/pf_event.cpp`, `pf.h` | **the light gun**: a Gamegun on the Control Port after the pad (pod 2, position 2, the first light gun), its five bytes made into events as the disc's driverlet `System/Drivers/CPORT4D.ROM` makes them (`03-the-gamegun.md`): Pressed, Released and Update when its buttons change, FireTracking while the trigger is or was down, DataArrived always, each frame's `LightGunEventData` (buttons, the 20-bit counter, the line count); the counter's timing Opera's unless told; presses scheduled or from the host, the host's recorded as `--gun` options |
| `runtime/pf_main.cpp` | `pfboot --lightgun`, `--lightgun-timing L,W,O`, `--gun BUTTONS@FIELD[+H][:X,Y]` |
| `runtime/pf_window.cpp` | with a gun on the port, the mouse is the gun: the pointer aims, the left button the trigger, the right the option button |
| `recomp/discover.py` | code of another function that reaches it only by a branch -- no word of that function running into it, its own descent inside that function's -- is a function of its own when a table or a pool names it, or when a pointed function's descent branches to it too (a tail two of them share); the branch becomes a tail call (`_splits`) |
| `runtime/pf_graphics.cpp` | GRAPHIX 20.45's `SetReadAddress` (0x2af8) and `ResetReadAddress` (0x2a50), `GetPixelAddress` (0x1a28), `ReadPixel` (0x2cf8), `WritePixel` (0x2c08), `ReadCLUTColor` (0x29e8, `return 0`); `GRAFERR_COORDRANGE`. The folio's user functions follow its SWI table at 0x6a54, which counts down from SWI 0 |
| `runtime/pf_mem.cpp` | the 21.10 kernel's `IsMemReadable` (0x12070, the 47th entry of its table at 0x1c8e0): true for no bytes, else unless the range passes VRAM's top |
| `runtime/pf_audio.cpp`, `pf_dsp.cpp` | `WhereAttachment` (AUDIOFOLIO 21.10's 0x62a8): CLIO's current DMA address of the attachment's FIFO less the sample's start (`pf_dsp_dma_address`) |
| `runtime/pf_cel.cpp` | uncoded 8-bit cels: `RRRGGGBB` widened to five bits a component, `cel.py`'s rule (Opera's MADAM) |
| `README.md` | this port among the ports; the light gun; the checks and the gaps |

### Discovery, checked

Over the 20 programs of the seven discs (`discall.sh` in the session's
scratchpad, the kit at 2ae02a2 and the working tree): **only this disc's
`launchme` (+10 functions) and The Need for Speed's `LaunchMe` (+1)
change**, problems 0 everywhere. The Need for Speed's new function is
0x319e4, `mov r2, #1; b 0x31918` -- a wrapper of its cel loader that a
table (0x3ed04) names and 0x1034c reached with a branch; before, a call
through that table would have stopped on no function's entry.

### Regression

The other six ports built from 2ae02a2 and from the working tree
(`regress.sh` in the session's scratchpad), their reference traces run on
both: **every one the same byte for byte** -- Crash 'n Burn's `launchme`
(529 lines) and boot (125,270), Immercenary's `p` (539,774) and boot
(810,154), OMF2097's `LaunchMe` (107), Doctor Hauzer's boot (893,209),
Escape from Monster Manor's boot (1,090,080), The Need for Speed's boot to
the race (800,961). None of them attaches a gun.
