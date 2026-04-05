# EE Internship Skills - Documentation Log

---

## Week 1: CMOS Inverter DC Analysis and VTC Modeling

- **Timestamp started:** 2026-03-29
- **User:** Sao Aphisith Sithisack
- **Week number:** 1
- **Topic:** CMOS Inverter DC Characterization and Voltage Transfer Curve Modeling
- **Summary:** The student will model NMOS and PMOS transistor I-V characteristics using the Shockley long-channel model in Python, then combine them to construct a CMOS inverter VTC via current balancing. Key parameters (switching threshold V_M, noise margins NM_H and NM_L) will be extracted and verified. A sensitivity analysis varying the PMOS/NMOS strength ratio demonstrates why PMOS transistors are sized wider in practice.
- **Timestamp completed:** 2026-04-05
- **Progress:** Completed. Built full CMOS inverter DC analysis in Python (Jupyter notebook). Modeled NMOS/PMOS IV characteristics using Shockley long-channel model with channel-length modulation. Constructed VTC via bisection method (current balancing). Extracted switching threshold Vm, noise margins NM_H and NM_L, and identified all five operating regions. Ran sensitivity analysis on kp/kn ratio and visualized its effect on Vm symmetry. All plots saved as PNG under `Week_01_CMOS_Inverter/figures/`. Technical summary written and saved as `Week01_Technical_Summary.md`.
- **Blockers:** None
- **Time spent:** ~6 hours (estimated 3 hours)
- **Key takeaways:** NMOS enters saturation before linear because Vds = Vout ≈ Vdd when it first turns on; PMOS and NMOS have complementary Vin responses creating push-pull Vout behavior; VTC is fundamentally an analog function despite digital abstraction; noise margins define the reliable switching window; hole mobility causes PMOS to have lower transconductance than NMOS.
- **Deliverables:** `cmos_inverter_vtc.ipynb`, 6 PNG figures, `Week01_Technical_Summary.md`
- **Summary updates:**
  - Added "Python Simulation vs Industry Tools" section to technical summary: Python simulation is valuable for building intuition from first-principles math; LTspice/SPICE tools are faster and more realistic for design work; goal is to learn SPICE tools in future weeks.
- **Next action:** Begin Week 2 — CMOS Inverter Transient Analysis and Power Dissipation on April 11

---

## Week 2: CMOS Inverter Transient Analysis and Power Dissipation

- **Timestamp started:** 2026-03-30
- **User:** Sao Aphisith Sithisack
- **Week number:** 2
- **Topic:** CMOS Inverter Transient Response, Propagation Delay, and Power Dissipation
- **Summary:** Building on Week 1's DC model, the student will add a load capacitance and simulate the inverter's transient switching behavior using Euler's method in Python. Propagation delays (t_pHL, t_pLH) and rise/fall times will be extracted from the waveforms. All three CMOS power components (dynamic, short-circuit, leakage) will be computed and visualized. Sweep analyses over C_L and V_DD demonstrate the fundamental delay-capacitance and power-voltage tradeoffs central to IC design.
- **Progress:** Plan generated; project scheduled for Saturday, April 11, 2026
- **Blockers:** Requires completion of Week 1 (MOSFET I-V functions)
- **Next action:** Complete Week 1 project on April 4, then Week 2 on April 11
