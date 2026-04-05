"""
CMOS Inverter - Noise Margin Visualization
Week 1: DC Analysis and Simulation in Python

Computes the VTC, identifies V_IL/V_IH (unity-gain points),
and visualizes the noise margins NM_H and NM_L.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ── MOSFET Parameters (180nm process) ─────────────────────────
V_DD = 1.8
V_tn = 0.4
V_tp = -0.4
k_n = 200       # NMOS process transconductance, k'_n * W/L (µA/V²)
k_p = 100       # PMOS process transconductance, k'_p * W/L (µA/V²)


def ids_nmos(Vin, Vout):
    Vgs, Vds = Vin, Vout
    if Vgs - V_tn <= 0:
        return 0.0
    elif Vds <= Vgs - V_tn:
        return k_n * ((Vgs - V_tn) * Vds - Vds**2 / 2)
    else:
        return k_n / 2 * (Vgs - V_tn)**2


def ids_pmos(Vin, Vout):
    Vsg, Vsd = V_DD - Vin, V_DD - Vout
    if Vsg + V_tp <= 0:
        return 0.0
    elif Vsd <= Vsg + V_tp:
        return k_p * ((Vsg + V_tp) * Vsd - Vsd**2 / 2)
    else:
        return k_p / 2 * (Vsg + V_tp)**2


def solve_vout(Vin, tol=1e-9):
    lo, hi = 0.0, V_DD
    for _ in range(100):
        mid = (lo + hi) / 2
        diff = ids_nmos(Vin, mid) - ids_pmos(Vin, mid)
        if diff > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ── Compute VTC and Gain ─────────────────────────────────────

Vin = np.linspace(0, V_DD, 2000)
Vout = np.array([solve_vout(v) for v in Vin])
gain = np.gradient(Vout, Vin)

# ── Find VIL, VIH (where gain = -1) ─────────────────────────

def find_crossings(x, y, threshold):
    """Find x-values where y crosses a threshold (linear interpolation)."""
    crossings = []
    for i in range(len(y) - 1):
        if (y[i] - threshold) * (y[i + 1] - threshold) < 0:
            frac = (threshold - y[i]) / (y[i + 1] - y[i])
            crossings.append(x[i] + frac * (x[i + 1] - x[i]))
    return crossings

crossings = find_crossings(Vin, gain, -1.0)
V_IL = crossings[0] if len(crossings) >= 1 else 0
V_IH = crossings[1] if len(crossings) >= 2 else V_DD

# Corresponding output levels
VOH_idx = np.argmin(np.abs(Vin - V_IL))
VOL_idx = np.argmin(np.abs(Vin - V_IH))
V_OH = Vout[VOH_idx]
V_OL = Vout[VOL_idx]

NM_H = V_OH - V_IH
NM_L = V_IL - V_OL

# Switching threshold V_M (where Vin = Vout)
vm_idx = np.argmin(np.abs(Vin - Vout))
V_M = Vin[vm_idx]

# ── Plot ─────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(9, 7))

# VTC curve
ax.plot(Vin, Vout, 'b-', linewidth=2, label='VTC', zorder=3)
ax.plot([0, V_DD], [0, V_DD], 'k--', alpha=0.3, label='Vout = Vin')

# Shade NMH region
ax.fill_between([V_IH, V_DD], V_OH, V_IH, alpha=0.15, color='green', label=f'NM_H = {NM_H:.2f} V')
ax.axhline(V_OH, color='green', linestyle=':', alpha=0.5)
ax.axvline(V_IH, color='green', linestyle=':', alpha=0.5)

# Shade NML region
ax.fill_between([0, V_IL], V_OL, V_IL, alpha=0.15, color='royalblue', label=f'NM_L = {NM_L:.2f} V')
ax.axhline(V_OL, color='royalblue', linestyle=':', alpha=0.5)
ax.axvline(V_IL, color='royalblue', linestyle=':', alpha=0.5)

# Mark key points
ax.plot(V_M, V_M, 'ro', markersize=8, zorder=4, label=f'V_M = {V_M:.2f} V')
ax.plot(V_IL, V_OH, 's', color='green', markersize=7, zorder=4)
ax.plot(V_IH, V_OL, 's', color='royalblue', markersize=7, zorder=4)

# Annotations
offset = 0.15
ax.annotate(f'V_IL = {V_IL:.2f} V', xy=(V_IL, 0), xytext=(V_IL + offset, -0.2),
            fontsize=9, color='royalblue', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='royalblue'))
ax.annotate(f'V_IH = {V_IH:.2f} V', xy=(V_IH, 0), xytext=(V_IH + offset, -0.2),
            fontsize=9, color='green', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='green'))
ax.annotate(f'V_OH = {V_OH:.2f} V', xy=(0, V_OH), xytext=(-0.3, V_OH - 0.15),
            fontsize=9, color='green', fontweight='bold')
ax.annotate(f'V_OL = {V_OL:.2f} V', xy=(0, V_OL), xytext=(-0.3, V_OL + 0.1),
            fontsize=9, color='royalblue', fontweight='bold')

ax.set_xlabel('Input Voltage  Vin (V)', fontsize=12)
ax.set_ylabel('Output Voltage  Vout (V)', fontsize=12)
ax.set_title('CMOS Inverter — Noise Margins', fontsize=14)
ax.set_xlim(-0.2, V_DD + 0.2)
ax.set_ylim(-0.3, V_DD + 0.2)
ax.grid(True, alpha=0.3)
ax.legend(loc='center right', fontsize=10)

plt.tight_layout()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
fig.savefig(os.path.join(FIGURES_DIR, 'noise_margins.png'), dpi=150)
print(f"Saved: {os.path.join(FIGURES_DIR, 'noise_margins.png')}")
print(f"\nResults:")
print(f"  V_IL = {V_IL:.3f} V    V_OH = {V_OH:.3f} V    NM_H = {NM_H:.3f} V")
print(f"  V_IH = {V_IH:.3f} V    V_OL = {V_OL:.3f} V    NM_L = {NM_L:.3f} V")
print(f"  V_M  = {V_M:.3f} V")

plt.show()
