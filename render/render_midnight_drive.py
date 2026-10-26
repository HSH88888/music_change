"""tracks/02_midnight_drive.js 를 파이썬으로 합성해 오디오 파일로 렌더링.

Strudel 은 브라우저에서만 소리가 나므로, 같은 패턴을 numpy 로 직접 합성한다.
사용법: python3 render/render_midnight_drive.py [출력.wav]
"""
import sys

import numpy as np
from scipy import signal

SR = 44100
BPM = 118
BAR = 60 / BPM * 4          # setcpm(118/4): 1 cycle = 1 bar
BARS = 16
rng = np.random.default_rng(7)

A_MINOR = [0, 2, 3, 5, 7, 8, 10]


def degree(root_midi, n):
    """n("...").scale("A?:minor") 와 같은 스케일 도수 -> MIDI"""
    octave, idx = divmod(n, 7)
    return root_midi + 12 * octave + A_MINOR[idx]


def hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def env(n, attack, decay, sustain, release, hold):
    """ADSR. hold = 노트가 눌려 있는 샘플 수"""
    a, d, r = int(attack * SR), int(decay * SR), int(release * SR)
    e = np.zeros(n)
    t = np.arange(n)
    e[: max(a, 1)] = np.linspace(0, 1, max(a, 1))[: n]
    if a < n:
        seg = np.arange(min(d, n - a))
        e[a:a + len(seg)] = 1 - (1 - sustain) * seg / max(d, 1)
        e[a + d:hold] = sustain
    end_level = e[min(hold, n) - 1] if hold > 0 else 0
    rel = t[hold:] - hold
    e[hold:] = end_level * np.clip(1 - rel / max(r, 1), 0, 1)
    return e


def saw(freq, n, phase=0.0):
    t = np.arange(n) / SR
    return signal.sawtooth(2 * np.pi * freq * t + phase)


def lowpass(x, cutoff, order=2):
    b, a = signal.butter(order, min(cutoff, SR / 2 - 100) / (SR / 2))
    return signal.lfilter(b, a, x)


def highpass(x, cutoff, order=2):
    b, a = signal.butter(order, cutoff / (SR / 2), btype="high")
    return signal.lfilter(b, a, x)


def reverb(x, seconds, mix):
    n = int(seconds * SR)
    ir = rng.standard_normal((2, n)) * np.exp(-np.linspace(0, 7, n))
    ir = lowpass(ir, 5000)
    wet = np.stack([signal.fftconvolve(x[c], ir[c])[: x.shape[1]] for c in range(2)])
    wet /= np.max(np.abs(wet)) + 1e-9
    return x + mix * wet * np.max(np.abs(x))


class Track:
    def __init__(self, length):
        self.buf = np.zeros((2, length))

    def add(self, start_sec, mono, gain=1.0, pan=0.5, late_r=0.0):
        """pan: 0=L, 1=R. late_r: 오른쪽만 지연 (juxBy(.., x => x.late(..)) 흉내)"""
        s = int(start_sec * SR)
        lr = [np.cos(pan * np.pi / 2), np.sin(pan * np.pi / 2)]
        for c in range(2):
            off = s + (int(late_r * SR) if c == 1 else 0)
            seg = mono[: max(0, self.buf.shape[1] - off)]
            self.buf[c, off:off + len(seg)] += seg * gain * lr[c] * np.sqrt(2)


# ---------- 악기 ----------

def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 45 + 110 * np.exp(-t * 35)                       # penv: 피치가 빠르게 떨어짐
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 7)
    click = rng.standard_normal(n) * np.exp(-t * 300) * 0.3
    return np.tanh((body + click) * 1.8)


def clap():
    n = int(0.3 * SR)
    t = np.arange(n) / SR
    noise = signal.lfilter(*signal.butter(2, [900 / (SR / 2), 3000 / (SR / 2)], "band"),
                           rng.standard_normal(n))
    e = np.zeros(n)
    for k, d in enumerate([0, 0.011, 0.022]):              # 짝-짝-짝 겹친 손뼉
        i = int(d * SR)
        e[i:] += np.exp(-(t[: n - i]) * (180 if k < 2 else 22))
    return noise * e * 2.5


def hat(open_=False):
    n = int((0.35 if open_ else 0.06) * SR)
    t = np.arange(n) / SR
    return highpass(rng.standard_normal(n), 7000) * np.exp(-t * (9 if open_ else 70))


def supersaw(freq, n, voices=7, spread=0.012):
    out = np.zeros(n)
    for v in range(voices):
        det = 1 + spread * (v - (voices - 1) / 2) / ((voices - 1) / 2)
        out += saw(freq * det, n, rng.uniform(0, 2 * np.pi))
    return out / voices


# ---------- 패턴 (02_midnight_drive.js 와 동일) ----------

BASS = [[0, 0, 7, 0] * 2, [-2, -2, 5, -2] * 2, [-5, -5, 2, -5] * 2, [-1, -1, 6, -1] * 2]
SUB = [0, -2, -5, -1]
SYNTH = [  # (도수, 길이[8분음표 칸]) / None = 쉼표
    [(7, 1), None, (9, 1), None, (11, 1), None, (9, 1), (7, 1)],
    [(6, 1), None, None, (4, 1), None, None, (2, 1), None],
    [(4, 1), None, (6, 1), None, (7, 1), None, (9, 1), None],
    [(8, 3), None, None, None, (7, 4), None, None, None],
]
PAD = [[57, 60, 64], [53, 57, 60], [55, 60, 64], [55, 59, 62]]   # Am F C G


def render(path):
    total = int((BARS * BAR + 3) * SR)
    drums, bass, sub, lead, pad = (Track(total) for _ in range(5))
    K, C, H, OH = kick(), clap(), hat(), hat(True)
    eighth = BAR / 8

    for bar in range(BARS):
        t0 = bar * BAR
        i = bar % 4
        intro = bar < 4
        fill = bar in (7, 15)

        # $DRUM
        for b in range(4):
            if not (intro and bar < 2):
                drums.add(t0 + b * BAR / 4, K, 0.85)
        for b in (1, 3):
            drums.add(t0 + b * BAR / 4, C, 0.5, pan=0.4, late_r=0.01)
        for s in range(8):
            pan = 0.5 + 0.15 * np.sin(2 * np.pi * (t0 + s * eighth) / BAR)
            drums.add(t0 + s * eighth, H, 0.28 if s % 2 == 0 else 0.16, pan=pan)
        if bar % 2 == 1:
            drums.add(t0 + 7 * eighth, OH, 0.22, pan=0.6)
        if fill:                                           # 마디 끝 스네어 필인
            for s in range(4):
                drums.add(t0 + BAR * 0.75 + s * BAR / 16, C, 0.25 + 0.08 * s)

        # $BASS (5마디부터)
        if bar >= 4:
            cutoff = 800 + 500 * np.sin(2 * np.pi * bar / 8)    # lpf(sine.range(..).slow(8))
            for s, d in enumerate(BASS[i]):
                n = int(eighth * SR * 1.3)
                x = 0.6 * saw(hz(degree(45 - 12, d)), n) + 0.4 * saw(hz(degree(45 - 12, d)) * 1.005, n)
                x = lowpass(x, cutoff) * env(n, 0.003, 0.15, 0.2, 0.05, int(eighth * SR * 0.9))
                bass.add(t0 + s * eighth, x, 0.55)

        # $SUB
        n = int(BAR * SR)
        x = np.sin(2 * np.pi * hz(degree(45 - 12, SUB[i])) * np.arange(n) / SR)
        sub.add(t0, x * env(n, 0.05, 0.1, 1, 0.3, int(n * 0.85)), 0.45 if not intro else 0.3)

        # $SYNTH (9마디부터)
        if bar >= 8:
            for s, ev in enumerate(SYNTH[i]):
                if ev is None:
                    continue
                d, length = ev
                hold = int(length * eighth * SR)
                n = hold + int(0.3 * SR)
                x = lowpass(supersaw(hz(degree(69, d)), n), 2200)
                x *= env(n, 0.02, 0.2, 0.5, 0.3, hold)
                lead.add(t0 + s * eighth, x, 0.32, pan=0.5, late_r=0.012)

        # $PAD
        hold = int(BAR * SR)
        n = hold + int(1.2 * SR)
        x = sum(supersaw(hz(m), n, voices=3, spread=0.006) for m in PAD[i])
        x = lowpass(x, 900) * env(n, 0.4, 0.2, 0.9, 1.2, hold)
        pad.add(t0, x, 0.12, pan=0.45, late_r=0.05)

    mix = (drums.buf
           + bass.buf
           + sub.buf
           + reverb(lead.buf, 1.8, 0.35)                    # .room(0.5)
           + reverb(pad.buf, 3.0, 0.6))                     # .room(0.8)

    # 킥에 맞춰 베이스/패드가 살짝 눌리는 사이드체인 펌핑
    t = np.arange(mix.shape[1]) / SR
    duck = 1 - 0.35 * np.exp(-((t % (BAR / 4)) * 14))
    mix = drums.buf + (mix - drums.buf) * duck

    mix = np.tanh(mix / np.max(np.abs(mix)) * 1.4) * 0.89  # 간단한 리미터
    fade = int(2.5 * SR)
    mix[:, -fade:] *= np.linspace(1, 0, fade)

    pcm = (mix.T * 32767).astype(np.int16)
    from scipy.io import wavfile
    wavfile.write(path, SR, pcm)
    print(f"wrote {path} ({mix.shape[1] / SR:.1f}s)")


if __name__ == "__main__":
    render(sys.argv[1] if len(sys.argv) > 1 else "midnight_drive.wav")
