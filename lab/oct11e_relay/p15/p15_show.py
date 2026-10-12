import numpy as np, json, wave
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
S = np.vstack([np.load('spec_0_5500.npy'), np.load('spec_5500_11001.npy')])
t, a, b, sa, sb = S.T
P = json.load(open('p15_points.json'))
gam = [z[0] for z in P['zeros']]; az = [z[1] for z in P['zeros']]
np.savetxt('p15_spectrum.csv', S, delimiter=',', header='t,a,b,se_a,se_b', comments='', fmt='%.6f')
# off-zero noise check: a(t) more than 0.6 away from every zero
far = np.min(np.abs(t[:, None] - np.array(gam)[None, :]), axis=1) > 0.6
print('off-zero a(t): mean %.3f sd %.3f max %.3f  (se ~ %.3f)' % (a[far].mean(), a[far].std(), a[far].max(), sa[far].mean()))
order = np.argsort(-a); peaks = []
for i in order:                                    # top local maxima, 1.0 apart
    if all(abs(t[i] - p) > 1.0 for p in peaks): peaks.append(t[i])
    if len(peaks) == 16: break
print('16 highest peaks of a(t):', ' '.join(f'{p:.2f}' for p in sorted(peaks)))
# ---- figure (light surface, single series -> no legend; zeros as muted ticks)
ink, ink2, mute, blue, surf = '#0b0b0b', '#52514e', '#9a9890', '#2a78d6', '#fcfcfb'
fig, (ax, ax2) = plt.subplots(2, 1, figsize=(11, 8.2), dpi=160, facecolor=surf, gridspec_kw={'height_ratios': [1.25, 1]})
ax.set_facecolor(surf); ax2.set_facecolor(surf)
ax.fill_between(t, -sa, sa, color='#e4e3df', lw=0)
ax.text(5.4, -0.68, 'grey: ±1 s.e. if the residuals were coin-flip noise — the real background is quieter, because it is the other zeros', fontsize=8, color=ink2)
ax.axhline(0, color=mute, lw=0.8); ax.axhline(1, color=ink2, lw=1, ls=(0, (4, 3)))
ax.text(60.4, 1, 'a = 1\nexplicit formula', va='center', ha='left', fontsize=8.5, color=ink2)
ax.plot(t, a, color=blue, lw=1.6)
for k, (g, y) in enumerate(zip(gam, az), 1):
    ax.plot([g, g], [1.32, 1.42], color=ink2, lw=1)
    ax.text(g, 1.46, f'γ{k}', ha='center', va='bottom', fontsize=8, color=ink2)
    ax.plot(g, y, 'o', ms=4.5, mfc=blue, mec=surf, mew=1.2, zorder=5)
ax.set_xlim(5, 60); ax.set_ylim(-0.75, 1.62)
ax.set_xlabel('frequency t   (a wave cos(t·ln x) across the layers)', color=ink2, fontsize=9.5)
ax.set_ylabel('amplitude a(t) in the layer-count residuals', color=ink2, fontsize=9.5)
for s in ('top', 'right'): ax.spines[s].set_visible(False)
for s in ('left', 'bottom'): ax.spines[s].set_color(mute)
ax.tick_params(colors=ink2, labelsize=8.5)
fig.suptitle('The wheel rings at the zeta zeros', x=0.065, ha='left', fontsize=14, color=ink, y=0.985)
ax.set_title('Prime counts on 1.8 million layers (numbers up to 1.6 trillion), minus the smooth expectation. '
             'Ticks: the first 13 zeta zeros.', loc='left', fontsize=9, color=ink2, pad=26)
J = json.load(open('joint_400_m1000.json')); gj, aj = np.array(J['gamma']), np.array(J['a'])
ax2.axhline(1, color=ink2, lw=1, ls=(0, (4, 3)))
ax2.plot(gj, aj, 'o', ms=4.2, mfc=blue, mec=surf, mew=0.8)
ax2.set_xlim(0, 405); ax2.set_ylim(0.82, 1.18)
ax2.set_xlabel('zeta zero height γ  (all 202 zeros below 400, fitted together)', color=ink2, fontsize=9.5)
ax2.set_ylabel('amplitude in the layer counts', color=ink2, fontsize=9.5)
ax2.set_title('Fit every zero at once (layers 1,000–1.8M): each comes back at loudness 1. Mean 1.002; scatter 0.7% for the first 13, 3% near 300.',
              loc='left', fontsize=9, color=ink2, pad=8)
for s_ in ('top', 'right'): ax2.spines[s_].set_visible(False)
for s_ in ('left', 'bottom'): ax2.spines[s_].set_color(mute)
ax2.tick_params(colors=ink2, labelsize=8.5)
fig.tight_layout(); fig.savefig('wheel_zeta_spectrum.png', facecolor=surf); print('figure ok')
# ---- sonification: (1) 36 s sweep, loudness = a(t)^2 (clipped), soft tick at each true zero; (2) 9 s chord
sr = 22050; f = lambda x: 16.0 * x                       # t -> Hz  (14.13 -> 226 Hz, 60 -> 960 Hz)
T1 = 36.0; n1 = int(sr * T1); tau = np.arange(n1) / sr
tt = 5 + 55 * tau / T1
env = np.interp(tt, t, np.clip(a, 0, None)) ** 2
env = np.convolve(env, np.ones(441) / 441, mode='same')  # 20 ms smoothing
phase = 2 * np.pi * np.cumsum(f(tt)) / sr
sweep = 0.75 * env / env.max() * np.sin(phase) + 0.02 * np.sin(phase)
for g in gam:                                            # tick when the sweep crosses each true zero
    i = int((g - 5) / 55 * T1 * sr); k = np.arange(int(0.03 * sr))
    sweep[i:i + len(k)] += 0.12 * np.exp(-k / (0.006 * sr)) * np.sin(2 * np.pi * 2400 * k / sr)
T2 = 9.0; n2 = int(sr * T2); tau2 = np.arange(n2) / sr; chord = np.zeros(n2)
aJ = json.load(open('joint_400_m1000.json'))['a'][:13]
for k, (g, y) in enumerate(zip(gam, aJ)):
    on = 0.35 * k; e = np.clip((tau2 - on) / 0.05, 0, 1) * np.exp(-np.clip(tau2 - on, 0, None) / 6.0)
    chord += max(y, 0) * e * np.sin(2 * np.pi * f(g) * tau2)
chord *= 0.85 / np.abs(chord).max(); fade = np.ones(n2); fade[-sr:] = np.linspace(1, 0, sr); chord *= fade
gap = np.zeros(int(0.8 * sr)); x = np.concatenate([sweep, gap, chord])
x = np.int16(np.clip(x, -1, 1) * 32000)
with wave.open('wheel_zeta_zeros.wav', 'wb') as W:
    W.setnchannels(1); W.setsampwidth(2); W.setframerate(sr); W.writeframes(x.tobytes())
print('audio ok', round(len(x) / sr, 1), 's')
