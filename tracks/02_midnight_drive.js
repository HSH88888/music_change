// MIDNIGHT DRIVE — synthwave sketch
// 영상과 같은 구성: DRUM / BASS / SYNTH / SUB / PAD
setcpm(118/4)
const KEY = "A2:minor"

$DRUM: stack(
  s("bd*4").gain(0.85),
  s("[- cp]*2").decay(0.2).gain(0.6)
    .juxBy(0.5, x => x.late(0.01)),
  s("hh*8").gain("[0.35 0.2]*4").pan(sine.range(0.35, 0.65)),
  s("<- [- - - oh]>").gain(0.3),
).bank("RolandTR909")

$BASS: n("<[0 0 7 0]*2 [-2 -2 5 -2]*2 [-5 -5 2 -5]*2 [-1 -1 6 -1]*2>")
  .scale(KEY)
  .s("sawtooth").lpf(sine.range(400, 1200).slow(8))
  .decay(0.15).sustain(0.2)
  .gain(0.7)

$SYNTH: n("<[7 ~ 9 ~ 11 ~ 9 7] [6 ~ ~ 4 ~ ~ 2 ~] [4 ~ 6 ~ 7 ~ 9 ~] [8@3 ~ 7@4]>")
  .scale("A4:minor")
  .s("supersaw").gain(0.5)
  .attack(0.02).decay(0.2).sustain(0.5).release(0.3).lpf(2200)
  .room(0.5).orbit(2)

$SUB: n("<0 -2 -5 -1>").scale(KEY).transpose(-12)
  .s("sine").gain(1.0)
  .attack(0.05).release(0.3)
  .orbit(3)

$PAD: chord("<Am F C G>").voicing()
  .s("sawtooth").lpf(900).gain(0.2)
  .attack(0.4).release(1.2)
  .room(0.8).orbit(4)
  .juxBy(0.8, x => x.late(0.05))
