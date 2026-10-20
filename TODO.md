# Next session

The top of this file is the next session's work; the history of sessions
is at the bottom. Read the top, not the history.

## Where the port stands

| | |
|---|---|
| the disc on the kit | 122 files, almost all of the game in `DmanData/dmfc.bin` (405 entries, the game's own formats); battery clean (`docs/01`) |
| the OS | Escape from Monster Manor's and The Need for Speed's images, byte for byte: Portfolio 21.10, GRAPHIX 20.45.419, AUDIOFOLIO 21.10 |
| recompiled | `launchme` 665 functions, `lmadm` 94, `format` 35; no seeds; self-test 0 failures |
| `pfboot build/disc --boot --nvram build/nvram` | the logos, the title, the intro film, the attract loop through every kind of level: 100,000 fields with no stop |
| `... $(cat replays/to-the-gun-level.txt)` | the title's menu, the intro, the first light gun level with its HUD |
| the window | **the user's first play: "perfect", the mouse aligned** -- two shooting levels (`replays/first-play.txt`) |
| the Gamegun | on the port behind the pad (`--lightgun`): shots land, rounds count down, the crosshair goes where the gun points (`--lightgun-timing 12710,1024,205`), the game's calibration holds with Opera's timing (`docs/03`) |
| the kit | **d04785d** (`docs/10`): regressed on every other port, the same byte for byte |

```sh
# the port's build from the kit's working tree (session 1's scratchpad build.sh does this)
cd D:/Homebrew6 && PYTHONIOENCODING=utf-8 python -m 3dokit.recomp --out pc-demolitionman/build/recomp --optest \
  "launchme=pc-demolitionman/build/disc/launchme" \
  "lmadm=pc-demolitionman/build/disc/System/Programs/LMADM" "format=pc-demolitionman/build/disc/System/Programs/FORMAT"
export PATH=/c/msys64/mingw64/bin:$PATH                 # for cmake/ninja/clang only
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ && ninja -C build/recomp-build
build/recomp-build/pfboot build/disc --boot --trace 0 --nvram build/nvram --max-calls 30000000 \
  $(cat replays/first-shots.txt) --frames build/frames --frames-at 8990-9200/2
```

Session 1's scratchpad (`34f6d168-.../scratchpad`): `build.sh [--selftest]`,
`discall.sh KITPARENT OUT` (discovery over the 20 programs of the seven
discs), `regress.sh VARIANT KITPARENT` (the other ports' builds and
reference traces, `reg/out-old` 2ae02a2's, `reg/out-new` d04785d's),
`sheet.py`, `odis.py`, `g419.dis`, `af2110.dis`, `k2110.dis`, `eb2110.dis`
(the OS images whole), `cport4d.dis` (the gun's driverlet), `CPORT4D.aif`.

## The work, in order

### 1. Play it in the window

Played by the user at the end of session 1: the first two shooting levels
with the mouse as the gun, "perfect", the crosshair under the pointer
(`replays/first-play.txt`). Next, the user at the pad and the gun: the menus, the first levels of each kind
-- the shooting galleries, the fights with Phoenix, the maze, the car
chase -- with `--record`, the presses kept in `replays/`. Every stop on
the way read as before. Worth watching: whether the gun feels right with
the game's timing (`--lightgun-timing 12710,1024,205`) and how the game's
own calibration screen, if it has one, looks; the sound (the game plays
`dcsqxdhalfmono`, `directout`, `halfmono8`, `varmono8`, `mixer8x2`); the
frame rate of the fights and the maze against the console's.

### 2. The levels the attract loop does not show

Nine shooting levels, four fights, two mazes, one chase: each reached and
played; the passwords (the game saves progress by password) a quick way
to each.

### 3. Phoenix

The user's captures of the same moments (the title, a shooting level, a
fight) against the runtime's frames, as for the other ports.

### 4. On from there

* The cel engine's time (pc-escapefrommonstermanor's TODO #1).
* The gun's counter on a console, if anyone can measure one.
* The game's menu waits on the pad in a tight loop under a semaphore:
  millions of OS calls on a still menu; a long headless run needs a large
  `--max-calls`.

## Answered

* (Session 1) The kit's commit and this repository: the user's word in
  the session's brief ("a fine sessione pubblicheremo il repo nuovo
  pc-demolitionman e l'aggiornamento al repo 3dokit, con la riga del gioco
  in tabella e cosa ha regalato al kit").
* (Session 1) The other ports' submodules: moved to d04785d and pushed, the
  user's word (pc-crashnburn e5d8b19, PC-Immercenary 59fb785,
  pc-doctorhauzer 68092d6, pc-escapefrommonstermanor e4abf3c,
  pc-theneedforspeed 6552b0a).

## Questions for the user

* None open.

## Keep in mind

* **Chat in Italian, every file in English.** No game data, no OS bytes in
  any repository; hashes, sizes and addresses are fine.
* `PYTHONIOENCODING=utf-8` for the Python tools; run `python -m 3dokit...`
  from `D:/Homebrew6` to use the kit's working tree (from the port's root
  it is the submodule). mingw64 on PATH only for cmake, ninja, clang.
* Always `--max-calls`; never `--trace 1` a long run into a file -- grep
  the stream.
* The disc came as a CHD: `chdman extractcd` (MAME's, in
  `D:/Homebrew4/Pippin/mame/`) makes `iso/dm.cue` and `iso/dm.bin`.

# History

## Session 1 (2026-10-20/21) -- the repository, the disc, the boot, the Gamegun

* **The repository**: git, the BYOA `.gitignore` of the sister ports, MIT,
  the README, 3dokit as a submodule, `tools/dmfc.py`.
* **The disc** (`docs/01`): the CHD extracted; 122 files; the OS Monster
  Manor's and The Need for Speed's; the container's table read.
* **The recompiler**: `launchme`, LMADM, FORMAT, no seeds; self-test 0
  failures. Discovery learnt tail branches to code a table names, and
  tails two handlers share (the game's script interpreter).
* **The boot** (`docs/02`): six stops answered in the kit -- the
  interpreter's handlers twice, `SetReadAddress`, `WhereAttachment`, an
  uncoded 8-bit cel, `GetPixelAddress` and the pixel calls -- then the
  attract loop for 100,000 fields, and the first shooting level.
* **The Gamegun** (`docs/03`): the port's bytes (Opera), the disc's
  driverlet read whole, the game's handler and calibration; the kit's
  light gun, checked on the game's crosshair.
* **The kit**: regressed on the six other ports, committed (d04785d) and
  pushed; this repository published; every other port's submodule moved
  to d04785d.
* **The window**: the user played the first two shooting levels with the
  mouse as the gun -- "perfect", the mouse aligned; the record replays it.
