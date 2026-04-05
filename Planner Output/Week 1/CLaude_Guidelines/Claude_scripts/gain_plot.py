"""
CMOS Inverter - DC Gain Analysis (Dual-Panel Plot)
Week 1: DC Analysis and Simulation in Python

Plots VTC (top panel) and gain dVout/dVin (bottom panel)
with shared x-axis for direct visual comparison.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ── MOSFET Parameters ──────────────────────────────────────────
VDD = 5.0
VTN = 0.7
VTP = -0.7
KN = 1e-4
KP = 1e-4


def ids_nmos(Vin, Vout):
    Vgs, Vds = Vin, Vout
    if Vgs - VTN <= 0:
        return 0.0
    elif Vds <= Vgs - VTN:
        return KN * ((Vgs - VTN) * Vds - Vds**2 / 2)
    else:
        return KN / 2 * (Vgs - VTN)**2


def ids_pmos(Vin, Vout):
    Vsg, Vsd = VDD - Vin, VDD - Vout
    if Vsg + VTP <= 0:
        return 0.0
    elif Vsd <= Vsg + VTP:
        return KP * ((Vsg + VTP) * Vsd - Vsd**2 / 2)
    else:
        return KP / 2 * (Vsg + VTP)**2


def solve_vout(Vin, tol=1e-9):
    lo, hi = 0.0, VDD
    for _ in range(100):
        mid = (lo + hi) / 2
        diff = ids_nmos(Vin, mid) - ids_pmos(Vin, mid)
        if diff > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ── Compute VTC and Gain ─────────────────────────────────────

Vin = np.linspace(0, VDD, 2000)
Vout = np.array([solve_vout(v) for v in Vin])
gain = np.gradient(Vout, Vin)

# Find VIL, VIH (gain = -1 crossings)
def find_crossings(x, y, threshold):
    crossings = []
    for i in range(len(y) - 1):
        if (y[i] - threshold) * (y[i + 1] - threshold) < 0:
            frac = (threshold - y[i]) / (y[i + 1] - y[i])
            crossings.append(x[i] + frac * (x[i + 1] - x[i]))
    return crossings

crossings = find_crossings(Vin, gain, -1.0)
VIL = crossings[0] if len(crossings) >= 1 else 0
VIH = crossings[1] if len(crossings) >= 2 else VDD

# Peak gain
peak_idx = np.argmin(gain)
peak_gain = gain[peak_idx]
VM = Vin[peak_idx]

# ── Dual-Panel Plot ──────────────────────────────────────────

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(9, 8), sharex=True,
                                gridspec_kw={'height_ratios': [1, 1]})

# ── Top: VTC ──
ax1.plot(Vin, Vout, 'b-', linewidth=2, label='VTC')
ax1.plot([0, VDD], [0, VDD], 'k--', alpha=0.3)
ax1.axvline(VIL, color='royalblue', linestyle=':', alpha=0.6, label=f'VIL = {VIL:.2f} V')
ax1.axvline(VIH, color='green', linestyle=':', alpha=0.6, label=f'VIH = {VIH:.2f} V')
ax1.axvline(VM, color='red', linestyle='--', alpha=0.4)
ax1.plot(VM, Vout[peak_idx], 'ro', markersize=7, label=f'VM = {VM:.2f} V')

ax1.set_ylabel('Vout (V)', fontsize=12)
ax1.set_title('CMOS Inverter — VTC and DC Gain', fontsize=14)
ax1.set_ylim(-0.1, VDD + 0.1)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='center right', fontsize=9)

# ── Bottom: Gain ──
ax2.plot(Vin, gain, 'r-', linewidth=2, label='Gain (dVout/dVin)')
ax2.axhline(-1, color='gray', linestyle='--', alpha=0.5, label='Gain = −1')
ax2.axvline(VIL, color='royalblue', linestyle=':', alpha=0.6)
ax2.axvline(VIH, color='green', linestyle=':', alpha=0.6)

ax2.annotate(f'Peak gain = {peak_gain:.1f}\nat VM = {VM:.2f} V',
             xy=(VM, peak_gain), xytext=(VM + 0.8, peak_gain * 0.5),
             fontsize=9, fontweight='bold', color='red',
             arrowprops=dict(arrowstyle='->', color='red'))

ax2.set_xlabel('Input Voltage  Vin (V)', fontsize=12)
ax2.set_ylabel('Gain  dVout/dVin', fontsize=12)
ax2.set_xlim(0, VDD)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='lower right', fontsize=9)

plt.tight_layout()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
fig.savefig(os.path.join(FIGURES_DIR, 'gain_plot.png'), dpi=150)
print(f"Saved: {os.path.join(FIGURES_DIR, 'gain_plot.png')}")
print(f"\nPeak gain: {peak_gain:.2f} at VM = {VM:.3f} V")

plt.show()
