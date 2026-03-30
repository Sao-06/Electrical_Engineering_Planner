# EE Internship Skills - Weekly Project Plan

---

## Week 2: CMOS Inverter Transient Analysis and Power Dissipation

**Date:** Saturday, April 11, 2026 | 12:00 PM - 3:30 PM (3.5 hrs)
**Domain:** IC Design and VLSI (Foundation+)
**Student:** Sao Aphisith Sithisack
**Prerequisite:** Week 1 — CMOS Inverter DC Analysis (VTC, noise margins, I-V models)

---

### 1. Topic

**CMOS Inverter Transient Response, Propagation Delay, and Power Dissipation Analysis**

Week 1 answered: "What is the output for a given DC input?" This week answers: "How *fast* does the output switch, and how much *energy* does it cost?" These are the two questions that dominate every IC design decision — speed vs. power is the central tradeoff from smartphone chips to data center GPUs.

---

### 2. Objective

**Design goal:** Extend your Week 1 CMOS inverter model with a load capacitance and transient simulation to extract propagation delays and compute all three components of power dissipation (dynamic, short-circuit, and static leakage).

**Measurable technical targets:**
1. Extract propagation delays t_pHL and t_pLH and verify that t_pHL < t_pLH for the baseline (equal W/L) design, with both in the range of 10–200 ps
2. Compute dynamic power P_dyn = α · C_L · V_DD² · f and verify it dominates total power at f = 1 GHz
3. Demonstrate that doubling C_L approximately doubles propagation delay (linear relationship)

**Maps to roles at:** NVIDIA (Digital/Analog IC Design, Timing Analysis), Apple (SoC Power Architecture), TSMC (Process Characterization), ARM (Digital Design, Low-Power), Intel (Circuit Design), Qualcomm (Low-Power Mobile SoC)

---

### 3. Project Summary

You will extend your Week 1 Python inverter model by adding a load capacitance (C_L) at the output node and simulating the inverter's transient response to a step input. Using numerical integration (Euler's method), you will compute V_out(t) during both high-to-low and low-to-high transitions, extract propagation delays (t_pHL, t_pLH), rise/fall times, and then compute all three power components. A sweep of C_L values will demonstrate the delay-capacitance relationship that underpins all static timing analysis. Your deliverable is an extended Python notebook with transient waveforms, delay extraction, power breakdown pie chart, and a 1-page technical summary.

---

### 4. Step-by-Step Instructions

#### Step 1: Set Up — Import Week 1 Code (10 min)
- Create a new folder: `Week_02_CMOS_Transient/`
- Create a new notebook: `cmos_inverter_transient.ipynb`
- Copy your NMOS and PMOS I-V functions (`i_ds_nmos`, `i_ds_pmos`) from Week 1
- Verify they still work by spot-checking: `i_ds_nmos(1.8, 0.9)` should return a positive current
- Add new imports:
  ```python
  import numpy as np
  import matplotlib.pyplot as plt
  from matplotlib.gridspec import GridSpec
  ```

#### Step 2: Define Transient Simulation Parameters (10 min)
Add these parameters to your existing 180nm process parameters:
```
C_L = 50e-15        # Load capacitance: 50 fF (typical fanout-of-4 inverter)
V_DD = 1.8          # Supply voltage (same as Week 1)
dt = 0.1e-12        # Time step: 0.1 ps (must be << t_p for accuracy)
t_total = 500e-12   # Total simulation time: 500 ps
t_step = 100e-12    # Input step occurs at t = 100 ps (gives settling time)
```

> **Why 50 fF?** A typical minimum-sized inverter driving 4 similar inverters (fanout-of-4, or FO4) sees roughly 50 fF in a 180nm process. FO4 delay is a universal benchmark — Intel and ARM use it to compare process nodes.

#### Step 3: Implement the Transient Simulation Engine (35 min)
This is the core of the project. The idea: at each time step, compute the net current into the output capacitor, then update V_out.

**The physics:**
```
I_net = I_pmos(V_in, V_out) - I_nmos(V_in, V_out)
dV_out = I_net / C_L * dt
V_out_new = V_out + dV_out
```

**Algorithm for a falling transition (V_in steps from 0 → V_DD):**
1. Initialize: `V_out = V_DD` (output starts high)
2. At `t = t_step`, V_in jumps from 0 to V_DD
3. For each time step after the jump:
   - Compute `I_nmos = i_ds_nmos(V_in, V_out)` — this pulls V_out down
   - Compute `I_pmos = i_ds_pmos(V_DD - V_in, V_DD - V_out)` — this tries to hold V_out up
   - `I_net = I_pmos - I_nmos` (negative means V_out is falling)
   - `V_out += I_net / C_L * dt`
   - Clamp V_out to [0, V_DD] to prevent numerical overshoot
4. Store V_out at each time step

**Algorithm for a rising transition (V_in steps from V_DD → 0):**
- Same structure, but initialize `V_out = 0` (output starts low)
- At `t = t_step`, V_in jumps from V_DD to 0
- Now I_pmos dominates and V_out rises

Write a function `simulate_transient(v_in_start, v_in_end, v_out_init, C_L, dt, t_total, t_step)` that returns arrays of `time` and `V_out`.

> **Tip:** Use a simple for-loop here. Euler's method at 0.1 ps steps over 500 ps is only 5000 iterations — Python handles this instantly.

#### Step 4: Plot Transient Waveforms (15 min)
Create a 2x1 subplot figure:

**Top panel:** V_in(t) — the step input (show both falling and rising input on the same axes)
**Bottom panel:** V_out(t) — the transient response

For both transitions on the same figure:
- Plot the high-to-low output transition (V_out falls) in blue
- Plot the low-to-high output transition (V_out rises) in red
- Add horizontal dashed lines at V_DD/2 (the 50% point for delay measurement)
- Add vertical dashed lines at the delay measurement points

Label axes with proper units (time in ps, voltage in V). Save as `transient_waveforms.png`.

**Expected shape:** V_out should follow an exponential-like curve (not perfectly exponential because MOSFET current is voltage-dependent, unlike a resistor). The falling transition should be faster than the rising transition (since NMOS is stronger at equal sizing).

#### Step 5: Extract Propagation Delays (20 min)
From your simulation data, extract:

| Parameter | Definition | How to Extract |
|-----------|-----------|---------------|
| t_pHL | Propagation delay, high-to-low | Time from V_in reaching V_DD/2 to V_out falling to V_DD/2 |
| t_pLH | Propagation delay, low-to-high | Time from V_in reaching V_DD/2 to V_out rising to V_DD/2 |
| t_p | Average propagation delay | (t_pHL + t_pLH) / 2 |
| t_fall | Fall time (90% to 10% of V_DD) | Time for V_out to go from 1.62V to 0.18V |
| t_rise | Rise time (10% to 90% of V_DD) | Time for V_out to go from 0.18V to 1.62V |

**Implementation:** Use `numpy.interp` or find the nearest index where V_out crosses the threshold:
```python
# Example: find t_pHL
idx_cross = np.argmin(np.abs(v_out_fall - V_DD/2))
t_pHL = time[idx_cross] - t_step  # subtract input step time
```

Print all five parameters in a formatted table. Verify:
- t_pHL < t_pLH (NMOS is stronger → faster pull-down)
- Both delays are in the range 10–200 ps for 50 fF load
- t_fall < t_rise (same reason)

#### Step 6: Capacitance Sweep — Delay vs. C_L (20 min)
Sweep C_L from 10 fF to 200 fF in 10 steps and extract t_pHL, t_pLH, and t_p for each:

```python
C_L_values = np.linspace(10e-15, 200e-15, 10)
t_pHL_values = []
t_pLH_values = []
for C_L in C_L_values:
    # Run falling transition simulation
    # Extract t_pHL
    # Run rising transition simulation
    # Extract t_pLH
```

Plot:
- x-axis: C_L (in fF)
- y-axis: delay (in ps)
- Three lines: t_pHL, t_pLH, t_p
- Add a linear fit line to show the linear relationship

Save as `delay_vs_capacitance.png`.

**Expected result:** Nearly linear relationship. The slope gives you the effective resistance of the transistors: R_eff = t_p / (0.69 · C_L). This RC model is the foundation of all delay estimation in digital IC design.

#### Step 7: Compute Power Dissipation Components (25 min)
CMOS power has three components. Compute each for f = 1 GHz, α = 0.1 (activity factor):

**1. Dynamic (switching) power:**
```
P_dynamic = α · C_L · V_DD² · f
```
This is the dominant component in modern digital ICs. α = 0.1 means 10% of nodes switch each clock cycle (typical for a processor).

**2. Short-circuit power:**
During switching, there is a brief period where both NMOS and PMOS are simultaneously ON, creating a direct path from V_DD to GND.

Compute this numerically from your transient simulation:
```python
# During the transition, compute instantaneous short-circuit current
I_sc = min(I_nmos, I_pmos)  # at each time step during transition
E_sc = sum(I_sc * V_DD * dt)  # energy per transition
P_short_circuit = E_sc * 2 * f * alpha  # factor of 2 for rise + fall
```

**3. Static (leakage) power:**
```
I_leak = 10e-9    # 10 nA typical for 180nm (very small at this node)
P_static = I_leak * V_DD
```

> **Industry context:** At 180nm, dynamic power dominates. Below 45nm, leakage power becomes a serious problem — this is why FinFETs were invented. Intel's switch to FinFETs at 22nm was driven by leakage.

Print a power breakdown table:

| Component | Formula | Value | % of Total |
|-----------|---------|-------|-----------|
| Dynamic | α·C_L·V_DD²·f | ___ µW | ___% |
| Short-circuit | from simulation | ___ µW | ___% |
| Static | I_leak·V_DD | ___ nW | ___% |
| **Total** | | ___ µW | 100% |

#### Step 8: Power Breakdown Visualization (10 min)
Create a pie chart showing the three power components:
```python
fig, ax = plt.subplots(figsize=(6, 6))
sizes = [P_dynamic, P_short_circuit, P_static]
labels = ['Dynamic\n(Switching)', 'Short-Circuit', 'Static\n(Leakage)']
colors = ['#2196F3', '#FF9800', '#4CAF50']
ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
ax.set_title('CMOS Inverter Power Breakdown\n180nm, f=1GHz, α=0.1, C_L=50fF')
```
Save as `power_breakdown.png`.

#### Step 9: V_DD Scaling — The Cubic Benefit (20 min)
This analysis shows why voltage scaling is the most powerful knob for power reduction.

Sweep V_DD from 0.6V to 1.8V in 7 steps. For each V_DD:
1. Recompute the VTC (from Week 1 code) to get new V_M
2. Run the transient simulation to get new t_p
3. Compute P_dynamic = α · C_L · V_DD² · f

Plot a 1x2 figure:
- **Left:** t_p vs V_DD — delay increases as V_DD decreases (slower)
- **Right:** P_dynamic vs V_DD — power decreases as V_DD decreases (cubic-ish: V_DD² directly, plus reduced α at lower swing)

Add a theoretical V_DD² curve overlay on the power plot. Save as `vdd_scaling.png`.

> **Why this matters:** This is the Energy-Delay Product tradeoff. Apple's efficiency cores run at low V_DD for battery life; performance cores run at high V_DD for speed. Your plot literally shows this tradeoff.

#### Step 10: Write Your Technical Summary (15 min)
Create a 1-page document covering:
- **Title:** "Week 2: CMOS Inverter Transient Analysis and Power Dissipation"
- **Objective:** 2 sentences on what you built and why
- **Key Results Table:** t_pHL, t_pLH, t_p, t_rise, t_fall, P_dynamic, P_total
- **Key Plots:** Transient waveform + power breakdown (side by side)
- **Analysis:** 2-3 sentences on the delay-capacitance relationship and V_DD scaling
- **Connection to Week 1:** How the DC model (VTC) connects to the transient model
- **One thing I learned:** Your biggest takeaway

---

### 5. Schematic / Architecture Aid

```
        V_DD (1.8V)
         |
     +---+---+
     |       |
     |  PMOS |  I_charge (pulls V_out UP)
     |  (M2) |
     |       |
     +---+---+
         |
 V_in ---+---+-------> V_out
         |   |
     +---+---+  === C_L (50 fF)
     |       |   |
     |  NMOS |  GND
     |  (M1) |
     |       |  I_discharge (pulls V_out DOWN)
     +---+---+
         |
        GND

  Transient behavior:
  - V_in goes HIGH → NMOS ON, PMOS OFF → V_out falls (discharges C_L)
  - V_in goes LOW  → NMOS OFF, PMOS ON  → V_out rises (charges C_L)

  Speed is set by:  t_p ≈ 0.69 · R_eff · C_L
  Power is set by:  P = α · C_L · V_DD² · f
```

The load capacitance C_L represents the gate capacitance of whatever the inverter is driving (e.g., the next stage of logic). In a real chip, C_L also includes wire capacitance and drain junction capacitance.

---

### 6. Expected Results and Verification Checklist

- [ ] Transient simulation produces smooth V_out(t) waveforms (no oscillation, no NaN)
- [ ] Falling transition (t_pHL) is faster than rising transition (t_pLH) for equal W/L
- [ ] Both t_pHL and t_pLH are in the range 10–200 ps for C_L = 50 fF
- [ ] Delay vs. C_L plot shows approximately linear relationship
- [ ] R_eff extracted from slope is in the range 1–50 kΩ (reasonable for 180nm)
- [ ] Dynamic power dominates total power at 180nm (>85% of total)
- [ ] Power scales approximately as V_DD² (verified by V_DD sweep)
- [ ] Short-circuit power is 5–15% of dynamic power (typical for well-designed inverter)
- [ ] All plots are saved and properly labeled
- [ ] Technical summary is complete with results table and plots

---

### 7. Common Pitfalls and Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| V_out oscillates or goes negative/above V_DD | Time step (dt) too large; Euler's method is unstable | Reduce dt by 10x. Add clamping: `V_out = np.clip(V_out, 0, V_DD)` |
| V_out never reaches 0V or V_DD fully | Simulation time too short or channel-length modulation causing residual current | Increase t_total to 1 ns; check that the "off" transistor has near-zero current |
| t_pHL ≈ t_pLH (they should differ) | k_n and k_p might be set equal | Verify k_n = 200 µA/V², k_p = 100 µA/V² (PMOS is weaker → slower rise) |
| Delay doesn't scale linearly with C_L | Non-linear MOSFET current at different V_out levels | This is expected to be *approximately* linear; slight curvature is physically correct |
| Short-circuit power is zero | Checking wrong condition for simultaneous conduction | Both transistors are ON when V_tn < V_in < V_DD - |V_tp|. Check this window |
| Power values seem unreasonably large | Unit errors | Verify: C_L in Farads, V_DD in Volts, f in Hz. P_dynamic for one inverter should be in µW range at 1 GHz |
| Simulation is very slow | Too many time steps or Python loop inefficiency | 5000 steps should take <1 second. If >10,000 steps needed, consider adaptive dt |

---

### 8. Resources

1. **Tutorial/Video:** "CMOS Inverter Propagation Delay" by Razavi — UCLA lecture on YouTube. Search: "Razavi CMOS Propagation Delay Lecture". Covers the RC model derivation and delay equations.

2. **Tutorial/Video:** "Power Dissipation in CMOS" by NPTEL — Indian Institute of Technology lectures on YouTube. Search: "NPTEL CMOS Power Dissipation". Excellent breakdown of all three power components.

3. **Textbook Reference:** Rabaey, Chandrakasan, Nikolic, *Digital Integrated Circuits*, 2nd Ed, Chapter 5.4–5.5 — "Propagation Delay" and "Power Consumption" — the definitive reference for this exact topic.

4. **Textbook Reference:** Weste & Harris, *CMOS VLSI Design: A Circuits and Systems Perspective*, 4th Ed, Chapter 4.4–4.5 — RC delay model, Elmore delay, and power analysis.

5. **Textbook Reference:** Sedra/Smith, *Microelectronic Circuits*, 8th Ed, Chapter 14.4 — "Propagation Delay of the CMOS Inverter" — covers the transient analysis derivation.

6. **Industry Context:** "FO4 Delay as a Metric" — ARM and Intel use fanout-of-4 inverter delay as a standard benchmark when comparing process nodes. Your 50 fF simulation approximates this metric.

7. **Documentation:** SciPy `solve_ivp` documentation — if you want to upgrade from Euler's method to a proper ODE solver for better accuracy (extension challenge).

8. **Community:** r/chipdesign on Reddit — discussions on power-performance tradeoffs in modern process nodes; EE Stack Exchange for CMOS transient analysis questions.

---

### 9. Deliverables for Portfolio

| Deliverable | Format | Filename |
|-------------|--------|----------|
| Transient waveform plots (rise + fall) | PNG | `transient_waveforms.png` |
| Delay vs. capacitance sweep | PNG | `delay_vs_capacitance.png` |
| Power breakdown pie chart | PNG | `power_breakdown.png` |
| V_DD scaling (delay and power) | PNG | `vdd_scaling.png` |
| Python notebook (all code) | .ipynb | `cmos_inverter_transient.ipynb` |
| 1-page technical summary | PDF/MD | `week02_summary.pdf` |

**Portfolio links (fill in after completion):**
- GitHub repo: _______________
- Google Drive folder: _______________

---

### 10. Extension Challenge (Optional)

**If you finish early: Ring Oscillator Frequency Estimation**

A ring oscillator is an odd number of inverters connected in a loop — it oscillates at a frequency determined by the inverter delay. It is the standard test structure fabricated on every new process node.

1. Using your extracted t_p, compute the oscillation frequency for a 5-stage ring oscillator:
   ```
   f_osc = 1 / (2 · N · t_p)    where N = number of stages
   ```
2. Plot f_osc vs. number of stages (N = 3, 5, 7, 9, 11)
3. Plot f_osc vs. C_L for a 5-stage ring oscillator
4. Compare your computed f_osc to published 180nm ring oscillator data (~1–5 GHz range)

**Bonus:** Simulate the ring oscillator directly:
- Chain 5 inverter transient simulations with the output of each feeding the input of the next
- Start with a small perturbation and watch the oscillation build
- Measure the steady-state period and compare to your analytical formula

**Success criteria:**
- f_osc is in the 1–5 GHz range for 180nm with C_L = 50 fF
- f_osc scales as 1/N (verified by your plot)
- Direct simulation frequency matches analytical prediction within 20%

---

### Interview Question of the Week

> **"Walk me through the three components of power dissipation in a CMOS circuit. Which dominates at 180nm? At 7nm? What changed?"**

**Key points to hit in your answer:**
- **Dynamic power** (α·C_L·V_DD²·f): Dominates at 180nm and above. Proportional to V_DD² — this is why voltage scaling is so effective. Activity factor α captures that not all gates switch every cycle.
- **Short-circuit power**: Occurs during transitions when both transistors are momentarily ON. Typically 5–15% of dynamic power for well-designed circuits. Minimized by matching rise/fall times.
- **Static (leakage) power** (I_leak·V_DD): Negligible at 180nm, but becomes dominant below 45nm due to exponentially increasing sub-threshold leakage as transistors shrink. This drove the industry to FinFETs (22nm at Intel, 16nm at TSMC) — FinFETs have better gate control, reducing leakage by ~10x.
- **The crossover:** Around 90–65nm, leakage power started matching dynamic power, creating a "power wall" that ended simple frequency scaling (why clock speeds stopped increasing around 2005).
- Your power breakdown pie chart from this project demonstrates the 180nm case directly!

---

### Definition of Done

- [ ] Transient simulation implemented and producing smooth waveforms
- [ ] t_pHL < t_pLH verified numerically
- [ ] Delay vs. C_L shows linear relationship with R_eff extracted
- [ ] All three power components computed with correct units
- [ ] Power pie chart shows dynamic power dominance
- [ ] V_DD scaling analysis complete with delay-power tradeoff visible
- [ ] Can explain all three power components and the FinFET transition (interview question)
- [ ] 1-page technical summary written
- [ ] All files organized in `Week_02_CMOS_Transient/` folder

---

## Calendar Event (Copy-Paste Ready)

**Title:** EE Project: CMOS Inverter Transient Analysis & Power
**Date:** Saturday, April 11, 2026
**Time:** 12:00 PM - 3:30 PM
**Duration:** 3.5 hours
**Reminders:** 1 day before (Friday 12:00 PM), 1 hour before (Saturday 11:00 AM)
**Description:**
Week 2 - CMOS Inverter Transient Analysis and Power Dissipation (IC Design & VLSI)
Builds on Week 1 — uses your NMOS/PMOS models to simulate switching behavior.
Objective: Simulate transient response, extract propagation delays, compute power breakdown.
Checklist:
- [ ] Import and verify Week 1 MOSFET I-V functions
- [ ] Implement Euler-method transient simulation engine
- [ ] Plot transient waveforms (rising and falling transitions)
- [ ] Extract t_pHL, t_pLH, t_rise, t_fall
- [ ] Sweep C_L and plot delay vs. capacitance
- [ ] Compute dynamic, short-circuit, and leakage power
- [ ] Create power breakdown pie chart
- [ ] V_DD scaling analysis (delay and power vs. V_DD)
- [ ] Write 1-page technical summary
