# pc-demolitionman

Toward a native PC port of **Demolition Man** (Virgin Interactive, 3DO,
1994): the tie-in made alongside the film, in its 3DO version a game of its
own -- nine light gun levels, four one-on-one fights between John Spartan
and Simon Phoenix, two first-person mazes and a car chase, the film's
soundtrack, and full-motion video shot for the game with Sylvester
Stallone and Wesley Snipes. This version was only ever released on the
3DO (the Jaguar CD and PlayStation versions were cancelled; the SNES,
Genesis and Sega CD games are different games), which is what makes it
worth keeping. The goal is the game running natively on PC by **static
recompilation**: the 3DO original's own ARM60 code turned into C++ and run
on a reimplementation of the 3DO's OS, booting the disc as the console
boots it, in a window in real time, with its sound -- and with its light
gun, the 3DO Gamegun, as the mouse.

It is the sixth port built on
[3dokit](https://github.com/vs-sr-dev/3dokit), the game-agnostic 3DO
toolkit -- after [pc-immercenary](https://github.com/vs-sr-dev/pc-immercenary),
[pc-crashnburn](https://github.com/vs-sr-dev/pc-crashnburn),
[pc-doctorhauzer](https://github.com/vs-sr-dev/pc-doctorhauzer),
[pc-escapefrommonstermanor](https://github.com/vs-sr-dev/pc-escapefrommonstermanor)
and [pc-theneedforspeed](https://github.com/vs-sr-dev/pc-theneedforspeed)
-- and the first with a light gun. 3dokit is taken here as a submodule:
clone with `--recursive`, or run `git submodule update --init`.

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets, no OS code. You need your own original disc. The
work is done on the US release, one data track, here as a MAME CHD turned
into a .cue and a raw .bin by MAME's `chdman extractcd` (`docs/01`).
Hashes, sizes and addresses are written down here; bytes of the product
are not.

## Layout

    docs/            what the kit reads on this disc, the boot and the light gun, what the kit got
    tools/           dmfc.py, the game's container read
    replays/         presses (pfboot --pad and --gun options), to replay
    3dokit/          game-agnostic 3DO toolkit (submodule)
    iso/, build/     your disc and everything derived from it (ignored by git)

## The route

The route the other ports have walked: **recompile** the programs
(`3dokit.recomp`, checked by its self-test against an ARM60 interpreter),
**boot** the disc on the Portfolio runtime (`pfboot`) one OS call at a
time, each call the runtime does not answer read in the disc's own OS code
and put in the kit, and **compare and play**, recording the presses to
guard later changes.

The game is one program, `launchme`, and one container of data,
`DmanData/dmfc.bin`, which it reads itself. It runs on the very OS images
of Escape from Monster Manor and The Need for Speed (Portfolio 21.10). The
disc's own `LMADM` and `FORMAT` are recompiled too, for the console's
NVRAM, where the game keeps its high scores.

## Tools

The Python tools need Python 3.8+, and capstone for the code; run them from
the repository root. Building the C++ needs CMake, Ninja, clang and SDL3
(MSYS2's mingw64).

```sh
chdman extractcd -i "Demolition Man (USA).chd" -o iso/dm.cue -ob iso/dm.bin
D=iso/dm.cue
export PYTHONIOENCODING=utf-8

# the disc: volume, ROM tags, every copy compared; extract it
python -m 3dokit.disc "$D"
python -m 3dokit.disc "$D" --verify
python -m 3dokit.disc "$D" --extract build/disc
python tools/dmfc.py build/disc/DmanData/dmfc.bin            # the container's table

# the code
python -m 3dokit.aif --scan build/disc
python -m 3dokit.portfolio build/disc/launchme --sites
python -m 3dokit.recomp.discover build/disc/launchme --report

# the recompiler and its self-test
python -m 3dokit.recomp --out build/recomp --optest "launchme=build/disc/launchme" \
  "lmadm=build/disc/System/Programs/LMADM" "format=build/disc/System/Programs/FORMAT"
python -m 3dokit.recomp.selftest --image launchme=build/disc/launchme --auto \
  --out build/recomp/selftest/launchme.txt          # and lmadm, format the same way
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++
ninja -C build/recomp-build
build/recomp-build/selftest build/recomp/selftest/*.txt

# the disc as the console starts it, the NVRAM kept in build/nvram; the attract loop, headless
build/recomp-build/pfboot build/disc --boot --trace 0 --nvram build/nvram --max-calls 15000000 \
  --frames build/frames --frames-at 0-100000/20

# in a window: the pad on the keyboard (arrows; Z X C for A B C; Enter Start; Q W for L R) and
# the Gamegun on the mouse -- the pointer aims, the left button is the trigger, the right the
# gun's option button
build/recomp-build/pfboot build/disc --boot --trace 0 --nvram build/nvram --window \
  --lightgun-timing 12710,1024,205 --record build/play.txt
```

`--lightgun-timing 12710,1024,205` makes the gun's counter the one the
game's own calibration expects (1,271 counts a line, 3.2 a pixel, 205
before the picture's first pixel), so the crosshair is where the pointer
is from the start. Without it the gun counts as the Opera emulator does,
which puts the crosshair some 33 pixels left of and 10 below the pointer
until the game is calibrated: aim at the middle of the play area (160, 90)
and press the option button, then the trigger (`docs/03`).

## Status

**Session 1**: the repository; the disc read by the kit (122 files, almost
all of the game in one 409 MB container of its own); the OS the same as
Monster Manor's and The Need for Speed's; `launchme`, `LMADM` and `FORMAT`
recompiled with no seeds, the self-test at 0 failures; and the boot, stop
by stop: the Warner Bros. and Virgin logos, the title, the intro film, and
the attract loop through **every kind of level** -- the light gun
rooftop, the fight with Phoenix, the car chase, the first-person maze, the
bonus tally -- for 100,000 fields (28 minutes) with no stop; and from the
title's menu into the game, the first light gun level with its HUD.
Then **the 3DO Gamegun**: the kit now carries a light gun on the Control
Port behind the pad, its five bytes made into events as the disc's own
driverlet (`CPORT4D.ROM`) makes them; the game's shots land, its ammunition
counts down, its crosshair goes where the gun points. On the way the kit
learnt the game's script interpreter (tail branches to handlers a table
names, and tails they share), GRAPHIX 20.45's read address and pixel
calls, the 21.10 kernel's `IsMemReadable`, the audio folio's
`WhereAttachment`, and the cel engine's uncoded 8-bit cels. See `TODO.md`.

## Documentation

| | |
|---|---|
| [TODO](TODO.md) | the next session's work, and the history of sessions |
| [01-the-disc-on-the-kit](docs/01-the-disc-on-the-kit.md) | what 3dokit reads on this disc, and what it learnt from it |
| [02-the-boot](docs/02-the-boot.md) | the run to the attract loop and the game; the stops and what they asked |
| [03-the-gamegun](docs/03-the-gamegun.md) | the light gun: the port's bytes, the driverlet, the events, the game's calibration |
| [10-3dokit](docs/10-3dokit.md) | what this port gave 3dokit |

## Licence

MIT -- see [LICENSE](LICENSE). Demolition Man is © 1993 Warner Bros. and
© 1994 Virgin Interactive Entertainment; this repository contains none of
it.
