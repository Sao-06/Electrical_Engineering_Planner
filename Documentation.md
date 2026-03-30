# EE Internship Skills - Documentation Log

---

## Week 1: CMOS Inverter DC Analysis and VTC Modeling

- **Timestamp started:** 2026-03-29
- **User:** Sao Aphisith Sithisack
- **Week number:** 1
- **Topic:** CMOS Inverter DC Characterization and Voltage Transfer Curve Modeling
- **Summary:** The student will model NMOS and PMOS transistor I-V characteristics using the Shockley long-channel model in Python, then combine them to construct a CMOS inverter VTC via current balancing. Key parameters (switching threshold V_M, noise margins NM_H and NM_L) will be extracted and verified. A sensitivity analysis varying the PMOS/NMOS strength ratio demonstrates why PMOS transistors are sized wider in practice.
- **Progress:** Plan generated; project scheduled for Saturday, April 4, 2026
- **Blockers:** None
- **Next action:** Complete Week 1 project on April 4

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
