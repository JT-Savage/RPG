#!/usr/bin/env python3
"""Pure-stdlib chiptune audio generator for the Godot JRPG.

Generates all music tracks and SFX as 16-bit mono WAV @ 22050 Hz.
Uses ONLY the Python standard library: wave, struct, math, random, os, array.

Run:  python3 generate_audio.py
"""

import array
import math
import os
import random
import wave

SR = 22050
TWO_PI = 2.0 * math.pi

BASE = os.path.dirname(os.path.abspath(__file__))
MUSIC_DIR = os.path.join(BASE, "audio", "music")
SFX_DIR = os.path.join(BASE, "audio", "sfx")

# ---------------------------------------------------------------------------
# Core helpers
# ---------------------------------------------------------------------------

NOTE_OFFSETS = {"C": 0, "D": 2, "E": 4, "F": 5, "G": 7, "A": 9, "B": 11}


def note_freq(name):
    """'C4' / 'F#3' / 'Bb2' -> frequency in Hz (A4 = 440)."""
    letter = name[0].upper()
    rest = name[1:]
    semis = NOTE_OFFSETS[letter]
    if rest and rest[0] in "#b":
        semis += 1 if rest[0] == "#" else -1
        rest = rest[1:]
    octave = int(rest)
    midi = (octave + 1) * 12 + semis
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def midi_freq(midi):
    return 440.0 * (2.0 ** ((midi - 69) / 12.0))


def write_wav(path, buf, peak_target=0.35):
    """Write a float buffer (list of floats) to a 16-bit mono WAV."""
    peak = max(1e-9, max(abs(v) for v in buf))
    scale = (peak_target / peak) if peak > peak_target else 1.0
    data = array.array("h")
    for v in buf:
        s = int(v * scale * 32767.0)
        if s > 32767:
            s = 32767
        elif s < -32768:
            s = -32768
        data.append(s)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def add_tone(buf, start, dur, freq, wave_type, vol, rnd=None,
             attack=0.005, decay=0.05, sustain=0.7, release=0.04,
             duty=0.5, vibrato_hz=0.0, vibrato_depth=0.0,
             freq_end=None, gate=0.92):
    """Render one note additively into buf starting at sample index `start`.

    Simple ADSR; gate fraction keeps release inside the slot so loops stay
    seamless.  freq_end != None gives a linear pitch sweep.
    """
    n = int(dur * SR)
    if n <= 0:
        return
    end = min(start + n, len(buf))
    n = end - start
    if n <= 0:
        return
    a_n = max(1, int(attack * SR))
    d_n = max(1, int(decay * SR))
    r_n = max(1, int(release * SR))
    gate_n = int(n * gate)
    rel_start = max(1, gate_n - r_n)

    ph = 0.0
    f0 = freq
    df = ((freq_end - freq) / n) if freq_end is not None else 0.0
    inv_sr = 1.0 / SR
    sin = math.sin
    uni = rnd.uniform if rnd is not None else None

    for i in range(n):
        # envelope
        if i >= gate_n:
            break
        if i < a_n:
            env = i / a_n
        elif i < a_n + d_n:
            env = 1.0 - (1.0 - sustain) * (i - a_n) / d_n
        elif i < rel_start:
            env = sustain
        else:
            env = sustain * (1.0 - (i - rel_start) / r_n)
            if env < 0.0:
                env = 0.0
        f = f0 + df * i
        if vibrato_hz:
            f += vibrato_depth * f * sin(TWO_PI * vibrato_hz * i * inv_sr)
        ph += f * inv_sr
        if ph >= 1.0:
            ph -= int(ph)
        if wave_type == "square":
            v = 1.0 if ph < duty else -1.0
        elif wave_type == "triangle":
            v = 4.0 * abs(ph - 0.5) - 1.0
        elif wave_type == "sine":
            v = sin(TWO_PI * ph)
        elif wave_type == "saw":
            v = 2.0 * ph - 1.0
        else:  # noise
            v = uni(-1.0, 1.0)
        buf[start + i] += v * env * vol


def add_noise_burst(buf, start, dur, vol, rnd, decay_pow=2.0, lowpass=0.0):
    """Decaying white-ish noise; lowpass in [0,1) smooths it toward a rumble."""
    n = int(dur * SR)
    end = min(start + n, len(buf))
    n = end - start
    if n <= 0:
        return
    prev = 0.0
    uni = rnd.uniform
    for i in range(n):
        env = (1.0 - i / n) ** decay_pow
        v = uni(-1.0, 1.0)
        if lowpass > 0.0:
            v = lowpass * prev + (1.0 - lowpass) * v
            prev = v
        buf[start + i] += v * env * vol


# ---------------------------------------------------------------------------
# Music engine
# ---------------------------------------------------------------------------

SCALES = {
    "major":      [0, 2, 4, 5, 7, 9, 11],
    "minor":      [0, 2, 3, 5, 7, 8, 10],
    "harm_minor": [0, 2, 3, 5, 7, 8, 11],
    "dorian":     [0, 2, 3, 5, 7, 9, 10],
    "phrygian":   [0, 1, 3, 5, 7, 8, 10],
    "lydian":     [0, 2, 4, 6, 7, 9, 11],
    "mixolydian": [0, 2, 4, 5, 7, 9, 10],
}

RHYTHMS = {
    # patterns of note lengths in beats; each list sums to 4 (one bar)
    "fast": [
        [0.5, 0.5, 1.0, 0.5, 0.5, 1.0],
        [0.5] * 8,
        [1.0, 0.5, 0.5, 0.5, 0.5, 1.0],
        [0.5, 0.5, 0.5, 0.5, 1.0, 1.0],
    ],
    "medium": [
        [1.0, 1.0, 1.0, 1.0],
        [1.0, 0.5, 0.5, 1.0, 1.0],
        [2.0, 1.0, 1.0],
        [1.5, 0.5, 1.0, 1.0],
    ],
    "slow": [
        [2.0, 2.0],
        [2.0, 1.0, 1.0],
        [3.0, 1.0],
        [4.0],
    ],
    "sparse": [
        [4.0],
        [2.0, 2.0],
        [3.0, 1.0],
    ],
}


def scale_midi(root_midi, scale, degree):
    """Scale degree (can exceed 7 / be negative) -> midi note."""
    intervals = SCALES[scale]
    octave, idx = divmod(degree, 7)
    return root_midi + 12 * octave + intervals[idx]


def compose_track(cfg):
    """Procedurally compose one looping chiptune track from a config dict."""
    rnd = random.Random(cfg["seed"])
    bpm = cfg["bpm"]
    bars = cfg["bars"]
    spb = 60.0 / bpm                  # seconds per beat
    total_beats = bars * 4
    total = int(round(total_beats * spb * SR))
    buf = [0.0] * total
    prog = cfg["progression"]
    root = cfg["root"]                # midi note of key root (melody register base)
    scale = cfg["scale"]
    mel_wave = cfg.get("melody_wave", "square")
    bass_wave = cfg.get("bass_wave", "triangle")
    mel_vol = cfg.get("melody_vol", 0.16)
    bass_vol = cfg.get("bass_vol", 0.14)
    rest_p = cfg.get("rest_p", 0.10)
    rhythm = RHYTHMS[cfg.get("rhythm", "medium")]
    vib = cfg.get("vibrato", 0.0)
    duty = cfg.get("duty", 0.5)
    descend = cfg.get("descend", False)

    def beat_sample(b):
        return int(round(b * spb * SR))

    # --- Melody: seeded random walk over the scale, chord tone on bar starts
    deg = 7  # start an octave above root
    for bar in range(bars):
        chord_deg = prog[bar % len(prog)]
        pat = rnd.choice(rhythm)
        beat = bar * 4.0
        first = True
        for length in pat:
            if rnd.random() < rest_p and not first:
                beat += length
                continue
            if first:
                # land on a chord tone (root/3rd/5th of current chord)
                deg = chord_deg + 7 + rnd.choice([0, 2, 4])
            else:
                step = rnd.choice([-2, -1, -1, 1, 1, 2] if not descend
                                  else [-3, -2, -2, -1, -1, 1])
                deg += step
                deg = max(4, min(13, deg))
            midi = scale_midi(root, scale, deg)
            add_tone(buf, beat_sample(beat), length * spb, midi_freq(midi),
                     mel_wave, mel_vol, rnd, duty=duty,
                     vibrato_hz=5.0 if vib else 0.0, vibrato_depth=vib,
                     sustain=0.75, release=0.06,
                     gate=0.9 if length <= 1.0 else 0.95)
            beat += length
            first = False

    # --- Bass
    bass_mode = cfg.get("bass", "beat")
    bass_oct = cfg.get("bass_oct", -2)  # octaves below root register
    for bar in range(bars):
        chord_deg = prog[bar % len(prog)]
        chord_root = scale_midi(root, scale, chord_deg) + 12 * bass_oct
        bar_beat = bar * 4.0
        if bass_mode == "drone":
            add_tone(buf, beat_sample(bar_beat), 4 * spb, midi_freq(chord_root),
                     bass_wave, bass_vol, rnd, attack=0.05, sustain=0.9,
                     release=0.2, gate=0.98)
        elif bass_mode == "beat":
            for q in range(4):
                off = 0 if q % 2 == 0 else 7  # root / fifth
                add_tone(buf, beat_sample(bar_beat + q), spb,
                         midi_freq(chord_root + off), bass_wave, bass_vol,
                         rnd, sustain=0.6, gate=0.85)
        elif bass_mode == "eighth":
            for e in range(8):
                add_tone(buf, beat_sample(bar_beat + e * 0.5), 0.5 * spb,
                         midi_freq(chord_root), bass_wave, bass_vol, rnd,
                         sustain=0.55, gate=0.8)
        elif bass_mode == "ostinato":
            riff = cfg.get("bass_riff", [0, 0, 3, 0, 0, 5, 3, 0])
            for e, semi in enumerate(riff):
                if semi is None:
                    continue
                add_tone(buf, beat_sample(bar_beat + e * 0.5), 0.5 * spb,
                         midi_freq(chord_root + semi), bass_wave, bass_vol,
                         rnd, sustain=0.6, gate=0.82)

    # --- Arpeggio (optional)
    if cfg.get("arp"):
        arp_vol = cfg.get("arp_vol", 0.06)
        for bar in range(bars):
            chord_deg = prog[bar % len(prog)]
            tones = [chord_deg, chord_deg + 2, chord_deg + 4, chord_deg + 7]
            for e in range(8):
                midi = scale_midi(root, scale, tones[e % 4])
                add_tone(buf, beat_sample(bar * 4.0 + e * 0.5), 0.5 * spb,
                         midi_freq(midi), "square", arp_vol, rnd, duty=0.25,
                         sustain=0.5, gate=0.7)

    # --- Percussion (optional)
    if cfg.get("perc"):
        pv = cfg.get("perc_vol", 0.10)
        for bar in range(bars):
            bb = bar * 4.0
            for q in (0.0, 2.0):  # kick
                s = beat_sample(bb + q)
                add_tone(buf, s, 0.10, 110.0, "sine", pv * 1.2, rnd,
                         freq_end=45.0, sustain=0.8, release=0.03, gate=1.0)
            for q in (1.0, 3.0):  # snare
                add_noise_burst(buf, beat_sample(bb + q), 0.09, pv, rnd,
                                decay_pow=2.5)
            for e in range(8):    # hats
                add_noise_burst(buf, beat_sample(bb + e * 0.5), 0.03,
                                pv * 0.35, rnd, decay_pow=3.0)

    return buf


MUSIC_CONFIGS = {
    # --- dict-referenced files -------------------------------------------
    "title_theme": dict(seed=101, bpm=104, bars=16, root=60, scale="major",
                        progression=[0, 5, 3, 4], rhythm="medium", arp=True,
                        bass="beat", melody_wave="square", duty=0.5),
    "overworld": dict(seed=102, bpm=128, bars=16, root=55, scale="major",
                      progression=[0, 3, 4, 0, 5, 3, 4, 4], rhythm="fast",
                      bass="eighth", arp=True, rest_p=0.15),
    "battle": dict(seed=103, bpm=160, bars=16, root=57, scale="minor",
                   progression=[0, 0, 5, 4], rhythm="fast", bass="eighth",
                   perc=True, duty=0.25, rest_p=0.08),
    "battle_kobold_heavy": dict(seed=104, bpm=172, bars=16, root=57,
                                scale="minor", progression=[0, 0, 3, 4],
                                rhythm="fast", bass="ostinato",
                                bass_riff=[0, 0, 0, 3, 0, 0, 5, 3],
                                bass_wave="square", bass_vol=0.17, perc=True,
                                duty=0.25),
    "boss_battle": dict(seed=105, bpm=150, bars=16, root=50,
                        scale="harm_minor", progression=[0, 0, 1, 0],
                        rhythm="fast", bass="ostinato",
                        bass_riff=[0, 0, 1, 0, 0, 3, 1, 0],
                        bass_wave="square", bass_vol=0.17, perc=True,
                        duty=0.33, rest_p=0.05),
    "final_boss": dict(seed=106, bpm=156, bars=16, root=52, scale="phrygian",
                       progression=[0, 1, 0, 3, 0, 1, 6, 0], rhythm="fast",
                       bass="ostinato", bass_riff=[0, 0, 1, 0, 6, 0, 1, 0],
                       bass_wave="square", bass_vol=0.18, perc=True,
                       duty=0.2, rest_p=0.05, vibrato=0.004),
    "town": dict(seed=107, bpm=96, bars=12, root=53, scale="major",
                 progression=[0, 3, 1, 4], rhythm="medium",
                 melody_wave="triangle", bass="beat", arp=True,
                 arp_vol=0.05, rest_p=0.15),
    "desert": dict(seed=108, bpm=110, bars=14, root=50, scale="phrygian",
                   progression=[0, 1, 0, 4], rhythm="medium", bass="beat",
                   melody_wave="square", duty=0.4, vibrato=0.006,
                   rest_p=0.12),
    "dungeon": dict(seed=109, bpm=80, bars=10, root=48, scale="minor",
                    progression=[0, 0, 1, 5], rhythm="slow",
                    melody_wave="triangle", bass="drone", bass_oct=-2,
                    rest_p=0.25, vibrato=0.003),
    "catacomb": dict(seed=110, bpm=56, bars=8, root=48, scale="phrygian",
                     progression=[0, 1], rhythm="sparse",
                     melody_wave="sine", mel_vol=0.13, bass="drone",
                     bass_wave="sine", rest_p=0.35, vibrato=0.005),
    "sad_theme": dict(seed=111, bpm=72, bars=12, root=57, scale="minor",
                      progression=[0, 5, 3, 4], rhythm="slow",
                      melody_wave="sine", bass="drone", vibrato=0.006,
                      rest_p=0.15),
    "victory": dict(seed=112, bpm=132, bars=12, root=60, scale="major",
                    progression=[0, 3, 4, 0], rhythm="medium", arp=True,
                    bass="beat", duty=0.5, rest_p=0.05),
    "game_over": dict(seed=113, bpm=60, bars=8, root=48, scale="minor",
                      progression=[0, 6, 5, 4], rhythm="slow",
                      melody_wave="triangle", bass="drone", descend=True,
                      rest_p=0.1, vibrato=0.004),
    "ending_good": dict(seed=114, bpm=84, bars=12, root=60, scale="major",
                        progression=[0, 3, 5, 4, 0, 3, 4, 0],
                        rhythm="medium", melody_wave="triangle", arp=True,
                        arp_vol=0.05, bass="beat", rest_p=0.12),
    "ending_best": dict(seed=115, bpm=120, bars=14, root=62, scale="major",
                        progression=[0, 4, 5, 3, 0, 3, 4, 0], rhythm="fast",
                        arp=True, bass="beat", perc=True, perc_vol=0.07,
                        rest_p=0.1),
    "new_game_plus": dict(seed=116, bpm=110, bars=14, root=60, scale="lydian",
                          progression=[0, 5, 3, 4], rhythm="medium",
                          arp=True, bass="beat", duty=0.33),
    # --- missing keys discovered in code ---------------------------------
    "ending_normal": dict(seed=117, bpm=80, bars=12, root=57, scale="dorian",
                          progression=[0, 3, 6, 4], rhythm="medium",
                          melody_wave="triangle", bass="drone", rest_p=0.15,
                          vibrato=0.004),
    "ending_bad": dict(seed=118, bpm=50, bars=6, root=45, scale="phrygian",
                       progression=[0, 1], rhythm="sparse",
                       melody_wave="sine", mel_vol=0.12, bass="drone",
                       bass_wave="sine", bass_vol=0.16, rest_p=0.4,
                       vibrato=0.007),
    "town_chaos": dict(seed=119, bpm=148, bars=14, root=53, scale="minor",
                       progression=[0, 3, 1, 4], rhythm="fast",
                       bass="eighth", bass_wave="square", perc=True,
                       perc_vol=0.08, duty=0.3, rest_p=0.08),
    "battle_boss": dict(seed=120, bpm=152, bars=16, root=52,
                        scale="harm_minor", progression=[0, 0, 5, 1],
                        rhythm="fast", bass="ostinato",
                        bass_riff=[0, 0, 3, 0, 0, 1, 3, 0],
                        bass_wave="square", bass_vol=0.17, perc=True,
                        duty=0.33),
    "battle_secret_boss": dict(seed=121, bpm=168, bars=16, root=51,
                               scale="harm_minor", progression=[0, 1, 0, 6],
                               rhythm="fast", bass="ostinato",
                               bass_riff=[0, 0, 1, 0, 0, 6, 1, 0],
                               bass_wave="square", bass_vol=0.18, perc=True,
                               duty=0.2, vibrato=0.004),
    "battle_final": dict(seed=122, bpm=158, bars=16, root=52,
                         scale="phrygian", progression=[0, 1, 6, 0],
                         rhythm="fast", bass="ostinato",
                         bass_riff=[0, 0, 1, 0, 6, 0, 1, 0],
                         bass_wave="square", bass_vol=0.18, perc=True,
                         duty=0.25, vibrato=0.004),
    "overworld_map": dict(seed=123, bpm=120, bars=16, root=55,
                          scale="mixolydian", progression=[0, 6, 3, 4],
                          rhythm="fast", bass="eighth", arp=True,
                          rest_p=0.15),
    "village": dict(seed=124, bpm=100, bars=12, root=50, scale="major",
                    progression=[0, 4, 3, 0], rhythm="medium",
                    melody_wave="triangle", bass="beat", arp=True,
                    arp_vol=0.05, rest_p=0.18),
    "grim": dict(seed=125, bpm=66, bars=8, root=47, scale="minor",
                 progression=[0, 1, 0, 5], rhythm="sparse",
                 melody_wave="sine", mel_vol=0.13, bass="drone",
                 bass_wave="triangle", rest_p=0.3, vibrato=0.005),
    "ethereal": dict(seed=126, bpm=70, bars=10, root=53, scale="lydian",
                     progression=[0, 3, 1, 4], rhythm="slow",
                     melody_wave="sine", arp=True, arp_vol=0.045,
                     bass="drone", bass_wave="sine", rest_p=0.2,
                     vibrato=0.004),
    "mountain": dict(seed=127, bpm=112, bars=14, root=55, scale="major",
                     progression=[0, 4, 5, 4], rhythm="medium",
                     bass="beat", bass_vol=0.16, duty=0.5, rest_p=0.1),
    "swamp": dict(seed=128, bpm=84, bars=12, root=52, scale="dorian",
                  progression=[0, 3, 0, 4], rhythm="medium",
                  melody_wave="triangle", bass="eighth", bass_wave="sine",
                  rest_p=0.2, vibrato=0.008),
    "orisia_theme": dict(seed=129, bpm=90, bars=12, root=56, scale="lydian",
                         progression=[0, 1, 4, 0], rhythm="medium",
                         melody_wave="sine", arp=True, arp_vol=0.05,
                         bass="drone", vibrato=0.004, rest_p=0.15),
    "final_dungeon": dict(seed=130, bpm=100, bars=12, root=54,
                          scale="harm_minor", progression=[0, 1, 0, 4],
                          rhythm="medium", bass="ostinato",
                          bass_riff=[0, None, 1, 0, None, 3, 1, 0],
                          bass_wave="triangle", rest_p=0.15,
                          vibrato=0.004),
    "dungeon_dark": dict(seed=131, bpm=70, bars=8, root=46, scale="phrygian",
                         progression=[0, 1, 0, 5], rhythm="sparse",
                         melody_wave="triangle", mel_vol=0.13, bass="drone",
                         bass_wave="sine", rest_p=0.3, vibrato=0.005),
}


# ---------------------------------------------------------------------------
# SFX builders
# ---------------------------------------------------------------------------

def buf_seconds(sec):
    return [0.0] * int(sec * SR)


def sfx_blip(freq=880.0, dur=0.08, wave_type="square"):
    b = buf_seconds(dur + 0.02)
    add_tone(b, 0, dur, freq, wave_type, 0.3, random.Random(1),
             sustain=0.6, release=0.02, gate=0.9)
    return b


def sfx_two_tone(f1, f2, step=0.09, wave_type="square"):
    b = buf_seconds(step * 2 + 0.05)
    r = random.Random(2)
    add_tone(b, 0, step, f1, wave_type, 0.28, r, sustain=0.7, gate=0.9)
    add_tone(b, int(step * SR), step * 1.4, f2, wave_type, 0.28, r,
             sustain=0.7, gate=0.9)
    return b


def sfx_jingle(notes, step=0.11, wave_type="square", vol=0.26, last_hold=2.2):
    b = buf_seconds(step * (len(notes) - 1) + step * last_hold + 0.1)
    r = random.Random(3)
    for i, n in enumerate(notes):
        dur = step * (last_hold if i == len(notes) - 1 else 1.15)
        add_tone(b, int(i * step * SR), dur, note_freq(n), wave_type, vol, r,
                 sustain=0.7, release=0.05, gate=0.95)
    return b


def build_sfx():
    out = {}
    # menus / ui
    out["menu_select"] = sfx_blip(880.0, 0.07)
    out["menu_confirm"] = sfx_two_tone(660.0, 990.0)
    out["menu_cancel"] = sfx_two_tone(660.0, 440.0)
    out["cursor_move"] = sfx_blip(1180.0, 0.05)
    out["confirm"] = sfx_two_tone(587.0, 880.0, step=0.08)

    # error buzz (also used for puzzle_wrong)
    def buzz(reps=2, f=110.0, dur=0.12, gap=0.05):
        b = buf_seconds(reps * (dur + gap) + 0.05)
        r = random.Random(4)
        for i in range(reps):
            add_tone(b, int(i * (dur + gap) * SR), dur, f, "square", 0.26, r,
                     duty=0.5, sustain=0.85, gate=0.95)
        return b
    out["error"] = buzz()
    out["puzzle_wrong"] = buzz(reps=2, f=98.0, dur=0.16)

    r = random.Random(42)

    # battle hits
    b = buf_seconds(0.35)
    add_noise_burst(b, 0, 0.18, 0.30, r, decay_pow=2.5, lowpass=0.6)
    add_tone(b, 0, 0.2, 90.0, "sine", 0.3, r, freq_end=40.0, sustain=0.8,
             release=0.05, gate=0.95)
    out["battle_hit_physical"] = b

    b = buf_seconds(0.6)
    add_tone(b, 0, 0.5, 400.0, "sine", 0.22, r, freq_end=2200.0,
             vibrato_hz=18.0, vibrato_depth=0.02, sustain=0.8, gate=0.95)
    add_noise_burst(b, int(0.1 * SR), 0.35, 0.06, r, decay_pow=2.0)
    out["battle_hit_magical"] = b

    b = buf_seconds(0.4)
    add_noise_burst(b, 0, 0.3, 0.14, r, decay_pow=1.5, lowpass=0.3)
    add_tone(b, 0, 0.3, 900.0, "sine", 0.12, r, freq_end=180.0,
             sustain=0.7, gate=0.9)
    out["battle_miss"] = b

    # spells
    b = buf_seconds(0.7)
    rf = random.Random(7)
    for _ in range(26):  # crackles
        st = rf.uniform(0.0, 0.55)
        add_noise_burst(b, int(st * SR), rf.uniform(0.02, 0.07),
                        rf.uniform(0.1, 0.26), rf, decay_pow=2.0,
                        lowpass=rf.uniform(0.0, 0.5))
    add_noise_burst(b, 0, 0.7, 0.10, rf, decay_pow=1.2, lowpass=0.85)
    out["spell_fire"] = b

    b = buf_seconds(0.9)
    ri = random.Random(8)
    for i in range(10):  # crystalline pings
        st = i * 0.07 + ri.uniform(0.0, 0.03)
        f = ri.choice([2093.0, 2637.0, 3136.0, 3520.0, 4186.0])
        add_tone(b, int(st * SR), 0.18, f, "sine", 0.16, ri,
                 sustain=0.4, release=0.08, gate=0.95)
    out["spell_ice"] = b

    b = buf_seconds(1.3)
    rt = random.Random(9)
    add_noise_burst(b, 0, 0.06, 0.45, rt, decay_pow=1.2)           # crack
    add_noise_burst(b, int(0.05 * SR), 1.2, 0.22, rt, decay_pow=2.2,
                    lowpass=0.93)                                   # rumble
    add_tone(b, int(0.04 * SR), 0.8, 70.0, "sine", 0.18, rt,
             freq_end=35.0, sustain=0.8, gate=0.95)
    out["spell_thunder"] = b

    out["spell_heal"] = sfx_jingle(["C5", "E5", "G5", "C6"], step=0.12,
                                   wave_type="sine", vol=0.2, last_hold=2.6)

    b = buf_seconds(0.9)
    rp = random.Random(10)
    add_tone(b, 0, 0.85, 440.0, "sine", 0.16, rp, vibrato_hz=6.0,
             vibrato_depth=0.05, sustain=0.85, gate=0.95)
    add_tone(b, 0, 0.85, 446.0, "sine", 0.16, rp, vibrato_hz=4.5,
             vibrato_depth=0.06, sustain=0.85, gate=0.95)
    add_tone(b, 0, 0.85, 333.0, "sine", 0.1, rp, vibrato_hz=7.0,
             vibrato_depth=0.08, sustain=0.85, gate=0.95)
    out["spell_psychic"] = b

    b = buf_seconds(0.15)
    rb = random.Random(11)
    for _ in range(4):
        add_noise_burst(b, int(rb.uniform(0, 0.08) * SR),
                        rb.uniform(0.015, 0.04), rb.uniform(0.15, 0.25),
                        rb, decay_pow=2.0)
    out["status_burn_tick"] = b

    b = buf_seconds(0.12)
    add_tone(b, 0, 0.09, 620.0, "sine", 0.32, r, freq_end=140.0,
             attack=0.002, sustain=0.9, gate=0.95)
    out["bubble_pop"] = b

    out["level_up"] = sfx_jingle(["C5", "E5", "G5", "C6", "E6"], step=0.1,
                                 wave_type="square", vol=0.22, last_hold=3.0)
    out["key_item_get"] = sfx_jingle(["G5", "C6", "E6", "G6"], step=0.11,
                                     wave_type="square", vol=0.22)
    out["treasure_chest"] = sfx_jingle(["E5", "G5", "C6"], step=0.1,
                                       wave_type="square", vol=0.22)
    out["save_point"] = sfx_jingle(["A5", "E6"], step=0.16, wave_type="sine",
                                   vol=0.2, last_hold=3.5)
    out["character_join"] = sfx_jingle(["C5", "E5", "A5"], step=0.12,
                                       wave_type="triangle", vol=0.24)
    out["puzzle_solved"] = sfx_jingle(["C5", "G5", "C6"], step=0.12,
                                      wave_type="sine", vol=0.22,
                                      last_hold=3.0)
    out["victory_fanfare"] = sfx_jingle(["G4", "C5", "E5", "G5"], step=0.13,
                                        wave_type="square", vol=0.24,
                                        last_hold=3.5)

    b = buf_seconds(0.06)
    rc = random.Random(12)
    add_noise_burst(b, 0, 0.025, 0.25, rc, decay_pow=2.0)
    add_tone(b, 0, 0.04, 420.0, "square", 0.15, rc, sustain=0.5, gate=0.9)
    out["puzzle_click"] = b

    b = buf_seconds(0.6)
    rd = random.Random(13)
    add_tone(b, 0, 0.5, 80.0, "saw", 0.22, rd, freq_end=160.0,
             vibrato_hz=11.0, vibrato_depth=0.12, sustain=0.8, gate=0.95)
    add_noise_burst(b, 0, 0.5, 0.07, rd, decay_pow=1.0, lowpass=0.8)
    out["door_open"] = b

    b = buf_seconds(0.7)
    re_ = random.Random(14)
    add_tone(b, 0, 0.35, 90.0, "saw", 0.18, re_, freq_end=150.0,
             vibrato_hz=9.0, vibrato_depth=0.1, sustain=0.8, gate=0.95)
    add_tone(b, int(0.38 * SR), 0.25, 660.0, "sine", 0.2, re_,
             sustain=0.6, release=0.08, gate=0.95)
    out["chest_open"] = b

    b = buf_seconds(1.3)
    rg = random.Random(15)
    add_tone(b, 0, 1.1, 65.0, "sine", 0.35, rg, freq_end=28.0,
             attack=0.005, sustain=0.9, release=0.2, gate=0.97)
    add_noise_burst(b, 0, 0.9, 0.2, rg, decay_pow=2.0, lowpass=0.9)
    out["flood_death_impact"] = b

    # hannah_scream: high distorted descending wail with vibrato
    n = int(1.3 * SR)
    b = [0.0] * n
    rh = random.Random(16)
    for i in range(n):
        t = i / SR
        f = 1800.0 - 1150.0 * (t / 1.3)
        f *= 1.0 + 0.06 * math.sin(TWO_PI * 7.5 * t)
        env = min(1.0, t / 0.02) * (1.0 - t / 1.3) ** 0.7
        v = math.sin(TWO_PI * f * t) + 0.5 * math.sin(TWO_PI * 2.01 * f * t)
        v *= 2.4  # drive into clipping for distortion
        v = max(-1.0, min(1.0, v))
        b[i] = v * env * 0.3 + rh.uniform(-1, 1) * env * 0.03
    out["hannah_scream"] = b

    b = buf_seconds(1.1)
    rr = random.Random(17)
    n = int(1.0 * SR)
    prev = 0.0
    for i in range(n):
        t = i / SR
        gate_mod = 1.0 if math.sin(TWO_PI * (32.0 - 14.0 * t) * t) > -0.4 else 0.25
        env = min(1.0, t / 0.05) * (1.0 - t) ** 1.2
        v = rr.uniform(-1, 1)
        prev = 0.88 * prev + 0.12 * v
        b[i] += prev * gate_mod * env * 1.4
        b[i] += 0.12 * math.sin(TWO_PI * (75.0 - 25.0 * t) * t) * env
    out["iris_berserk_roar"] = b

    b = buf_seconds(1.1)
    rs = random.Random(18)
    for _ in range(22):  # rattling bone clicks
        st = rs.uniform(0.0, 0.95)
        add_noise_burst(b, int(st * SR), rs.uniform(0.01, 0.035),
                        rs.uniform(0.12, 0.3), rs, decay_pow=1.5,
                        lowpass=rs.uniform(0.0, 0.4))
    add_tone(b, int(0.3 * SR), 0.7, 110.0, "triangle", 0.08, rs,
             vibrato_hz=5.0, vibrato_depth=0.03, sustain=0.7, gate=0.9)
    out["skeleton_summon"] = b

    b = buf_seconds(0.85)
    rw = random.Random(19)
    n = int(0.55 * SR)
    prev = 0.0
    for i in range(n):  # whoosh: rising filtered noise swell
        t = i / 0.55 / SR
        v = rw.uniform(-1, 1)
        prev = (0.95 - 0.5 * t) * prev + (0.05 + 0.5 * t) * v
        env = math.sin(math.pi * t)
        b[i] += prev * env * 0.55
    add_tone(b, int(0.58 * SR), 0.12, 700.0, "sine", 0.3, rw,
             freq_end=160.0, attack=0.002, sustain=0.9, gate=0.95)  # pop
    out["panda_transform"] = b

    b = buf_seconds(1.5)
    ru = random.Random(20)
    for i, nname in enumerate(["C5", "E5", "G5", "B5", "D6", "F#6"]):
        add_tone(b, int(i * 0.13 * SR), 0.3, note_freq(nname), "sine",
                 0.1 + i * 0.02, ru, vibrato_hz=6.0, vibrato_depth=0.01,
                 sustain=0.7, gate=0.95)
    add_tone(b, 0, 0.9, 220.0, "sine", 0.1, ru, freq_end=880.0,
             sustain=0.85, gate=0.95)  # riser
    add_noise_burst(b, int(0.9 * SR), 0.55, 0.3, ru, decay_pow=2.0,
                    lowpass=0.5)       # blast
    add_tone(b, int(0.9 * SR), 0.5, 100.0, "sine", 0.25, ru, freq_end=40.0,
             sustain=0.85, gate=0.95)
    out["hannah_ultimate_spell"] = b

    b = buf_seconds(1.1)
    add_tone(b, 0, 1.0, 880.0, "square", 0.2, r, freq_end=110.0,
             duty=0.4, sustain=0.85, release=0.15, gate=0.95)
    out["player_death"] = b

    b = buf_seconds(0.5)
    rv = random.Random(21)
    for i in range(4):  # poison bubbles
        st = i * 0.11 + rv.uniform(0, 0.02)
        f = rv.uniform(180.0, 320.0)
        add_tone(b, int(st * SR), 0.09, f, "sine", 0.2, rv, freq_end=f * 0.4,
                 sustain=0.8, gate=0.9)
    out["status_poison"] = b

    b = buf_seconds(1.5)
    rj = random.Random(22)
    add_noise_burst(b, 0, 0.12, 0.45, rj, decay_pow=1.0)
    add_noise_burst(b, int(0.05 * SR), 1.35, 0.3, rj, decay_pow=2.0,
                    lowpass=0.9)
    add_tone(b, 0, 1.0, 85.0, "sine", 0.25, rj, freq_end=30.0,
             sustain=0.85, release=0.2, gate=0.97)
    out["jerod_explosion"] = b

    b = buf_seconds(1.5)
    rfl = random.Random(23)
    n = int(1.45 * SR)
    prev = 0.0
    for i in range(n):  # rushing water swell
        t = i / n
        v = rfl.uniform(-1, 1)
        prev = 0.82 * prev + 0.18 * v
        env = math.sin(math.pi * min(1.0, t * 1.1)) if t < 0.91 else (1.0 - t) * 11.0
        env = max(0.0, env)
        b[i] += prev * env * 0.5
    add_tone(b, int(0.5 * SR), 0.8, 70.0, "sine", 0.15, rfl, freq_end=35.0,
             sustain=0.85, gate=0.95)
    out["flood_death"] = b

    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    os.makedirs(MUSIC_DIR, exist_ok=True)
    os.makedirs(SFX_DIR, exist_ok=True)

    print("Generating %d music tracks..." % len(MUSIC_CONFIGS))
    for name in sorted(MUSIC_CONFIGS):
        cfg = MUSIC_CONFIGS[name]
        buf = compose_track(cfg)
        path = os.path.join(MUSIC_DIR, name + ".wav")
        write_wav(path, buf, peak_target=0.35)
        print("  music/%s.wav  %.1fs  %d bytes"
              % (name, len(buf) / SR, os.path.getsize(path)))

    sfx = build_sfx()
    print("Generating %d sfx..." % len(sfx))
    for name in sorted(sfx):
        path = os.path.join(SFX_DIR, name + ".wav")
        write_wav(path, sfx[name], peak_target=0.5)
        print("  sfx/%s.wav  %.2fs  %d bytes"
              % (name, len(sfx[name]) / SR, os.path.getsize(path)))

    print("Done.")


if __name__ == "__main__":
    main()
