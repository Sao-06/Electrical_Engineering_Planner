"""
CMOS Inverter - Noise Margin Visualization
Week 1: DC Analysis and Simulation in Python

Computes the VTC, identifies VIL/VIH (unity-gain points),
and visualizes the noise margins NMH and NML.
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
VIL = crossings[0] if len(crossings) >= 1 else 0
VIH = crossings[1] if len(crossings) >= 2 else VDD

# Corresponding output levels
VOH_idx = np.argmin(np.abs(Vin - VIL))
VOL_idx = np.argmin(np.abs(Vin - VIH))
VOH = Vout[VOH_idx]
VOL = Vout[VOL_idx]

NMH = VOH - VIH
NML = VIL - VOL

# Switching threshold VM (where Vin = Vout)
vm_idx = np.argmin(np.abs(Vin - Vout))
VM = Vin[vm_idx]

# ── Plot ─────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(9, 7))

# VTC curve
ax.plot(Vin, Vout, 'b-', linewidth=2, label='VTC', zorder=3)
ax.plot([0, VDD], [0, VDD], 'k--', alpha=0.3, label='Vout = Vin')

# Shade NMH region
ax.fill_between([VIH, VDD], VOH, VIH, alpha=0.15, color='green', label=f'NMH = {NMH:.2f} V')
ax.axhline(VOH, color='green', linestyle=':', alpha=0.5)
ax.axvline(VIH, color='green', linestyle=':', alpha=0.5)

# Shade NML region
ax.fill_between([0, VIL], VOL, VIL, alpha=0.15, color='royalblue', label=f'NML = {NML:.2f} V')
ax.axhline(VOL, color='royalblue', linestyle=':', alpha=0.5)
ax.axvline(VIL, color='royalblue', linestyle=':', alpha=0.5)

# Mark key points
ax.plot(VM, VM, 'ro', markersize=8, zorder=4, label=f'VM = {VM:.2f} V')
ax.plot(VIL, VOH, 's', color='green', markersize=7, zorder=4)
ax.plot(VIH, VOL, 's', color='royalblue', markersize=7, zorder=4)

# Annotations
offset = 0.15
ax.annotate(f'VIL = {VIL:.2f} V', xy=(VIL, 0), xytext=(VIL + offset, -0.4),
            fontsize=9, color='royalblue', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='royalblue'))
ax.annotate(f'VIH = {VIH:.2f} V', xy=(VIH, 0), xytext=(VIH + offset, -0.4),
            fontsize=9, color='green', fontweight='bold',
            arrowprops=dict(arrowstyle='->', color='green'))
ax.annotate(f'VOH = {VOH:.2f} V', xy=(0, VOH), xytext=(-0.6, VOH - 0.3),
            fontsize=9, color='green', fontweight='bold')
ax.annotate(f'VOL = {VOL:.2f} V', xy=(0, VOL), xytext=(-0.6, VOL + 0.2),
            fontsize=9, color='royalblue', fontweight='bold')

ax.set_xlabel('Input Voltage  Vin (V)', fontsize=12)
ax.set_ylabel('Output Voltage  Vout (V)', fontsize=12)
ax.set_title('CMOS Inverter — Noise Margins', fontsize=14)
ax.set_xlim(-0.2, VDD + 0.2)
ax.set_ylim(-0.6, VDD + 0.3)
ax.grid(True, alpha=0.3)
ax.legend(loc='center right', fontsize=10)

plt.tight_layout()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
fig.savefig(os.path.join(FIGURES_DIR, 'noise_margins.png'), dpi=150)
print(f"Saved: {os.path.join(FIGURES_DIR, 'noise_margins.png')}")
print(f"\nResults:")
print(f"  VIL = {VIL:.3f} V    VOH = {VOH:.3f} V    NMH = {NMH:.3f} V")
print(f"  VIH = {VIH:.3f} V    VOL = {VOL:.3f} V    NML = {NML:.3f} V")
print(f"  VM  = {VM:.3f} V")

plt.show()
