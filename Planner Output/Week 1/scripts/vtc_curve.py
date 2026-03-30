"""
CMOS Inverter - Voltage Transfer Characteristic (VTC)
Week 1: DC Analysis and Simulation in Python

Computes and plots Vout vs Vin for a CMOS inverter using the
Shockley long-channel MOSFET model with bisection root-finding.
"""

import os
import numpy as np
import matplotlib.pyplot as plt

# ── MOSFET Parameters ──────────────────────────────────────────
VDD = 5.0        # Supply voltage (V)
VTN = 0.7        # NMOS threshold voltage (V)
VTP = -0.7       # PMOS threshold voltage (V)
KN = 1e-4        # NMOS process transconductance kn = un*Cox*(W/L) (A/V^2)
KP = 1e-4        # PMOS process transconductance kp = up*Cox*(W/L) (A/V^2)

# ── MOSFET Current Models ─────────────────────────────────────

def ids_nmos(Vin, Vout):
    """NMOS drain current (Shockley model). Vgs = Vin, Vds = Vout."""
    Vgs = Vin
    Vds = Vout
    if Vgs - VTN <= 0:
        return 0.0
    elif Vds <= Vgs - VTN:
        return KN * ((Vgs - VTN) * Vds - Vds**2 / 2)
    else:
        return KN / 2 * (Vgs - VTN)**2


def ids_pmos(Vin, Vout):
    """PMOS drain current (Shockley model). Vsg = VDD - Vin, Vsd = VDD - Vout."""
    Vsg = VDD - Vin
    Vsd = VDD - Vout
    if Vsg + VTP <= 0:
        return 0.0
    elif Vsd <= Vsg + VTP:
        return KP * ((Vsg + VTP) * Vsd - Vsd**2 / 2)
    else:
        return KP / 2 * (Vsg + VTP)**2


# ── Bisection Solver ──────────────────────────────────────────

def solve_vout(Vin, tol=1e-9):
    """Find Vout where Ids_nmos = Ids_pmos using bisection."""
    lo, hi = 0.0, VDD
    for _ in range(100):
        mid = (lo + hi) / 2
        diff = ids_nmos(Vin, mid) - ids_pmos(Vin, mid)
        if diff > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


# ── Compute VTC ───────────────────────────────────────────────

Vin = np.linspace(0, VDD, 1000)
Vout = np.array([solve_vout(v) for v in Vin])

# ── Plot ──────────────────────────────────────────────────────

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(Vin, Vout, 'b-', linewidth=2, label='VTC')
ax.plot([0, VDD], [0, VDD], 'k--', alpha=0.3, label='Vout = Vin')

ax.set_xlabel('Input Voltage  Vin (V)', fontsize=12)
ax.set_ylabel('Output Voltage  Vout (V)', fontsize=12)
ax.set_title('CMOS Inverter — Voltage Transfer Characteristic', fontsize=14)
ax.set_xlim(0, VDD)
ax.set_ylim(-0.1, VDD + 0.1)
ax.grid(True, alpha=0.3)
ax.legend(fontsize=11)

ax.annotate(f'VDD = {VDD} V\nVTn = {VTN} V\nVTp = {VTP} V\nkn = kp = {KN:.0e} A/V²',
            xy=(0.97, 0.97), xycoords='axes fraction',
            ha='right', va='top', fontsize=9,
            bbox=dict(boxstyle='round,pad=0.4', fc='lightyellow', alpha=0.8))

plt.tight_layout()

# Save figure
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FIGURES_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), 'figures')
os.makedirs(FIGURES_DIR, exist_ok=True)
fig.savefig(os.path.join(FIGURES_DIR, 'vtc_curve.png'), dpi=150)
print(f"Saved: {os.path.join(FIGURES_DIR, 'vtc_curve.png')}")

plt.show()
