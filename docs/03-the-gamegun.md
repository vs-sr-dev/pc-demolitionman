# 03. The Gamegun

Demolition Man's nine shooting levels take the 3DO Gamegun (American Laser
Games' light gun) as well as the pad. On the console the gun is
daisy-chained behind the pad, which then carries it; the runtime puts it
there (`pfboot --lightgun`: the pad pod 1, the gun pod 2, position 2, the
first light gun). The game itself does not look at where the gun sits: its
handler takes the gun's events whatever their pod.

Three layers, each read in the disc's own code.

## 1. The port: five bytes

What a Gamegun puts on the Control Port is not in any document the session
had; the Opera emulator (`opera_pbus.c`) writes it as five bytes:

| byte | bits |
|---|---|
| 0 | the id, 0x4D |
| 1 | the trigger (bit 7), the option button (bit 3), the counter's bit 19 (bit 0) |
| 2 | the counter's bits 18-11 |
| 3 | the counter's bits 10-3 |
| 4 | the counter's bits 2-0 (bits 7-5), the lines the gun saw the beam on (bits 4-0) |

The counter is the time from the field's start to the beam passing where
the gun points. Opera counts it `((y * 12707 + x * 1030 * 10 / 320) / 10 +
12835) & 0xFFFFF` for the pixel (x, y) of the 320-wide picture -- 1,270.7
a line, 1,030 across the picture, 12,835 before it -- and, pointed off the
picture, sends the counter 0 and no lines.

## 2. The driverlet: `System/Drivers/CPORT4D.ROM`

`System/Drivers` holds a driverlet for each kind of pod, named by its id
(`CPORT1`, `CPORT41`, `CPORT49`, `CPORT4D`); the gun's is 1,392 bytes, an AIF image (1,360
bytes, entry 0x100, signed) behind a 32-byte header (`0xdead99a4`, the
length, `0xdeafb795`). Read whole:

* **0x230, the port's bytes**: the buttons as bits 31-27 of a word (byte 1's
  bits 7-3: the trigger 0x80000000, the option button 0x08000000), the
  counter's 20 bits, the line count; the buttons before kept. The events
  ready: Pressed, Update and DataArrived when a button went down
  (0xa80, with Released 0xe80 when another came up), Released, Update and
  DataArrived when one came up (0x680), DataArrived alone otherwise (0x80);
  and **FireTracking (0x100) while the trigger is down or was down the field
  before**.
* **0x2cc, the frames**: for each event a listener's masks ask for, in the
  order 21 Pressed, 22 Released, 23 Update, 24 FireTracking, 25
  DataArrived (Update also when the listener's queue overflowed), a frame
  of 12 bytes of data (0x150): the pod's number, position and generic
  number (0x134), then `LightGunEventData` -- the buttons (for Pressed those
  that went down, for Released those that came up, else all down), the
  counter, the line count.

The runtime's broker (3dokit `pf_event.cpp`) makes exactly these frames,
after the pad's, in the field's record.

## 3. The game

`launchme` configures its listener (0x17ac) with the trigger mask
`0xe0000f00` -- the pad's Pressed, Released, Update and the gun's events 21
to 24 -- and handles a record at 0x19f0. The gun's frames count only when
the gun is on (+0x84 of its input block at 0x28d50, set by 0x20ec when a
shooting level starts, 0x6f0c and 0xe464):

* **21 Pressed**: the trigger fires (+0x70, or the trigger's bit shifted
  into the pad's bits, 0x100000, when +0x7c says so); **the option button starts the calibration**
  (+0x98 set, the offsets cleared).
* **24 FireTracking**, the trigger held: fewer than two lines seen four
  fields running is a shot off the screen (+0x88); otherwise the counter,
  plus the X offset (+0x90), is divided by **1,271** -- the quotient plus the
  Y offset (+0x94) is y, the remainder times 10 / 32 is x. Calibrating, the
  offsets are set so that this shot is **(159, 90)**, the middle of the
  play area above the HUD.
* The offsets start at **-204 and 0** (the read-write data): the game's own
  idea of the counter at the picture's corner. Its x and y are the
  screen's pixels: the crosshair is drawn there.

With Opera's counter and those defaults the crosshair lands about 33
pixels left of and 10 below where the gun points; after the game's
calibration, within 2. With `--lightgun-timing 12710,1024,205` -- 1,271 a
line, 3.2 a pixel, 205 before the picture -- the counter is the one the
game's defaults expect, and the crosshair is where the gun points from the
first shot. No console has been measured; 1,271 counts a line is a 20 MHz
clock over an NTSC line, which Opera's 1,270.7 is near. The port's README
runs the window with the game's timing.

## Checked

`replays/first-shots.txt` (the game's timing): the shots at (160, 100) and
(40, 60) put the crosshair's centre on exactly those pixels (in a first
run the same shots, with Opera's timing, took the HUD's rounds from 45 down
one by one). `replays/calibration.txt` (Opera's timing): the
option button at field 9000, the trigger at (159, 90), then shots at (40,
60) and (250, 120) land at (42, 60) and (248, 120).

## In the window

The mouse is the gun: the pointer aims (off the picture when it leaves
it), the left button is the trigger, the right the option button.
`--record` writes the gun's presses as `--gun BUTTONS@FIELD+HELD:X,Y`, a
new line each time the aim moves while a button is down, so the replay
points the gun where the player did on each field the game reads it.

The user played it so (session 1, the game's timing): "it works perfectly
... the mouse is aligned perfectly", the mouse alone once in the game. The
record, `replays/first-play.txt` (153 presses over 10,600 fields), replays
it headless: the first level cleared at 1,700 points, its tally (15 hits,
88% accuracy, super aim x2), the second level's rooftop, its grenades shot
out of the air, 10,480 points and one round left.
