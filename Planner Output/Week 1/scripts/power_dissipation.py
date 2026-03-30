"""
CMOS Inverter - Static Power Dissipation
Week 1: DC Analysis and Simulation in Python

Plots the static (short-circuit) power drawn from VDD
at each DC operating point of the CMOS inverter.
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


# ── Compute VTC and Power ────────────────────────────────────

Vin = np.linspace(0, VDD, 2000)
Vout = np.array([solve_vout(v) for v in Vin])

# Current through both transistors at each operating point
Ids = np.array([ids_nmos(vin, vout) for vin, vout in zip(Vin, Vout)])
Power = VDD * Ids  # Static power from supply

# Convert to microwatts for readability
Power_uW = Power * 1e6

# Peak power
peak_idx = np.argmax(Power_uW)
VM = Vin[peak_idx]
P_peak = Power_uW[peak_idx]

# ── Plot ─────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(9, 6))

ax.plot(Vin, Power_uW, 'purple', linewidth=2, label='Static Power')
ax.fill_between(Vin, 0, Power_uW, alpha=0.1, color='purple')

ax.plot(VM, P_peak, 'ro', markersize=8, zorder=4)
ax.annotate(f'Peak = {P_peak:.1f} \u00b5W\nat VM = {VM:.2f} V',
            xy=(VM, P_peak), xytext=(VM + 0.7, P_peak * 0.85),
            fontsize=10, fontweight='bold', color='red',
            arrowprops=dict(arrowstyle='->', color='red'))

ax.set_xlabel('Input Voltage  Vin (V)', fontsize=12)
ax.set_ylabel('Static Power (\u00b5W)', fontsize=12)
ax.set_title('CMOS Inverter \u2014 Static Power Dissipation', fontsize=14)
ax.set_xlim(0, VDD)
ax.set_ylim(0, P_peak * 1.15)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

ax.annotate(f'VDD = {VDD} V\nkn = kp = {KN:.0e} A/V\u00b2',
            xy=(0.97, 0.97), xycoords='axes fraction',
            ha='right', va='top', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', fc='lightyellow', alpha=0.8))

plt.tight_layout()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
fig.savefig(os.path.join(FIGURES_DIR, 'power_dissipation.png'), dpi=150)
print(f"Saved: {os.path.join(FIGURES_DIR, 'power_dissipation.png')}")
print(f"\nPeak static power: {P_peak:.2f} \u00b5W at VM = {VM:.3f} V")

plt.show()
