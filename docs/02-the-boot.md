# 02. The boot

The disc started as the console starts it (`pfboot build/disc --boot`),
one OS call at a time; each call the runtime did not answer read in the
disc's own OS code and put into the kit (`10-3dokit.md`), then the run
again. Addresses are `launchme`'s unless another image is named; the OS
images are Portfolio 21.10's (GRAPHIX 20.45 build 419, AUDIOFOLIO 21.10,
the 21.10 kernel), read whole in the session's scratchpad.

## The stops

| # | Where | What stopped | What it was |
|---|---|---|---|
| 1 | call 1,301 | a call to 0x8f98, no function's entry | the game's script interpreter: its handlers are in a table of the read-write data (0x2931c on), frameless, and the first of them that discovery had found took the second's code in by a tail branch (0xd514's `b 0x8f78`), so the chain of the table broke. Discovery learnt that code a table or a pool names, reached by another function only through a branch, is a function of its own (six handlers) |
| 2 | call 1,023 | Graphics -52 `SetReadAddress` | GRAPHIX 20.45's 0x2af8, and -56 `ResetReadAddress` (0x2a50): the cel engine's read side of a bitmap (REGCTL2 and REGCTL0's low byte). Its buffer check is the 21.10 kernel's `IsMemReadable` (0x12070, the 47th entry of the kernel's table at 0x1c8e0, found through GRAPHIX's stub 0x26c): true unless the range passes VRAM's top |
| 3 | call 1,846 | audio SWI 30 `WhereAttachment` | AUDIOFOLIO 21.10's 0x62a8 (the SWI table at 0xb918 counts down from SWI 0): for a sample, CLIO's current DMA address of the attachment's FIFO less the sample's start |
| 4 | field 8,060 | the cel engine: an uncoded 8-bit cel | `RRRGGGBB` widened to five bits a component, as the kit's Python reader (from Opera's MADAM) already decoded it |
| 5 | field 8,540 | Graphics -16 `GetPixelAddress` | GRAPHIX 20.45's user functions follow its SWI table at 0x6a54, the last slot -4: -16 is 0x1a28 (a screen's pixel address), -8 `ReadPixel` 0x2cf8, -12 `ReadCLUTColor` 0x29e8 (`return 0`), -20 `WritePixel` 0x2c08 -- all four put in |
| 6 | field 11,400 | a call to 0x74ac, no function's entry | a handler of the interpreter's other table (0x29284 on) whose tail, 0x742c, another handler (0x74c8) had taken in first: a tail two handlers share is a function of its own too (+4 functions: 0x742c, 0x74ac, 0x6510, 0x8180) |

Then nothing: **100,000 fields (28 minutes of the console's time) with no
stop**, five minutes headless.

## The run

Without a press, the boot is the disc's scripts (LMADM on the NVRAM, and
FORMAT before the boot on a blank one, as a console comes), then
`launchme`: "Under License By:" and the Warner Bros. Consumer Products
shield, the copyright page (Warner Bros. 1993, Virgin 1994, the QSound
logo), the title over the film's poster, and the intro film -- "Los
Angeles 1996", the burning city, the helicopter, Spartan on the rope --
into the attract loop: each kind of level played by the game itself, its
banner across the bottom -- the light gun rooftop with its crosshair, the
fight with Phoenix in the burning warehouse, the car chase, the
first-person maze, the bonus tally ("HITS", "NORM MODE", "% ACCURACY",
"PERFECT AIM") -- then the Virgin logo and the intro again.

`replays/to-the-gun-level.txt` (Start three times from field 2600): the
title's menu ("START", field 2650), a curtain of fire, the Virgin logo, the
intro film, a film of Spartan on the roof, and **the first light gun level** --
the rooftop, the HUD across the bottom (Spartan's face, the badge, the
pistol and its 45 rounds, the score, the lives). With no gun the cryo-cons
shoot Spartan down, "CONTINUE?" counts down, and the game goes back to
its intro.

The menu loop waits on the pad in a tight loop under a semaphore (0x1f0c
on), so a still menu spends OS calls fast: `--max-calls` of tens of
millions for runs past it.

## Notes

* The game reads its pad through the event broker as an observer (its
  `OpenJoyPadSys`, 0x1638 on; a thread, `LookPad`, at 0x175c), and keeps
  the pads' bits per pod position (1 to 3, 0x28d94 on). Its trigger mask
  asks for the pad's Pressed, Released and Update and the light gun's
  Pressed, Released, Update and FireTracking (`03-the-gamegun.md`).
* The high scores go to `/NVRAM/DemolitionManHighScores2`; passwords keep
  the progress.
* The C library's `fwrite` would open the development station's `mac`
  device on its first write to a host file; nothing writes one.
