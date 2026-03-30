# EE Internship Skills - Weekly Project Plan

---

## Week 1: CMOS Inverter DC Analysis and Simulation in Python

**Date:** Saturday, April 4, 2026 | 12:00 PM - 3:30 PM (3.5 hrs)
**Domain:** IC Design and VLSI (Foundation)
**Student:** Sao Aphisith Sithisack

---

### 1. Topic

**CMOS Inverter DC Characterization and Voltage Transfer Curve (VTC) Modeling**

This is the single most fundamental building block in all of IC design. Every digital chip - from NVIDIA GPUs to Apple's M-series SoCs - is built from CMOS inverters. Understanding its DC behavior is the first step toward analog and digital IC design roles.

---

### 2. Objective

**Design goal:** Model NMOS and PMOS transistor I-V characteristics from first principles, then combine them to construct and analyze a CMOS inverter's Voltage Transfer Characteristic (VTC) using Python.

**Measurable technical targets:**
1. Extract the inverter switching threshold (V_M) and verify it falls within 5% of V_DD/2 for a balanced inverter
2. Calculate noise margins (NM_H and NM_L) and verify both exceed 0.4 * V_DD

**Maps to roles at:** NVIDIA (Analog/Digital IC Design), TSMC (Process/Device Engineering), IBM (Circuit Design), Apple (SoC Design), ARM (Digital Design)

---

### 3. Project Summary

You will write a Python script that models the drain current equations for both NMOS and PMOS transistors (Shockley long-channel model), sweeps the input voltage from 0 to V_DD, and plots the full CMOS inverter VTC. From the VTC, you will extract key parameters: switching threshold (V_M), noise margins (NM_H, NM_L), and the five operating regions of the inverter. This project teaches the physics behind every digital gate and gives you vocabulary and intuition that directly comes up in IC design interviews. Your deliverable is a Python notebook with annotated plots, extracted parameters, and a 1-page technical summary.

---

### 4. Step-by-Step Instructions

#### Step 1: Set Up Your Environment (10 min)
- Create a new folder: `Week_01_CMOS_Inverter/`
- Open your preferred Python environment (Jupyter Notebook recommended, or VS Code)
- Install/verify packages:
  ```
  pip install numpy matplotlib
  ```
- Create a new notebook: `cmos_inverter_vtc.ipynb`

#### Step 2: Define Technology Parameters (10 min)
Set up the following parameters for a generic 180nm CMOS process:
```
V_DD = 1.8 V
V_tn = 0.4 V          (NMOS threshold voltage)
V_tp = -0.4 V         (PMOS threshold voltage)
k_n = 200 uA/V^2      (NMOS process transconductance, k'_n * W/L)
k_p = 100 uA/V^2      (PMOS process transconductance, k'_p * W/L)
lambda_n = 0.04 V^-1   (NMOS channel-length modulation)
lambda_p = 0.04 V^-1   (PMOS channel-length modulation)
```
> **Why 180nm?** It is a mature, well-documented process node used in many university courses and still in production for analog/mixed-signal ICs. The physics is identical to smaller nodes; only the numbers change.

#### Step 3: Implement the NMOS I-V Model (20 min)
Write a Python function `i_ds_nmos(Vgs, Vds)` that returns the drain current using the Shockley model:
- **Cutoff:** V_GS < V_tn --> I_DS = 0
- **Linear (Triode):** V_GS >= V_tn AND V_DS < V_GS - V_tn -->
  I_DS = k_n * [(V_GS - V_tn)*V_DS - 0.5*V_DS^2] * (1 + lambda_n * V_DS)
- **Saturation:** V_GS >= V_tn AND V_DS >= V_GS - V_tn -->
  I_DS = 0.5 * k_n * (V_GS - V_tn)^2 * (1 + lambda_n * V_DS)

**Verification:** Plot I_DS vs V_DS for V_GS = 0.6V, 1.0V, 1.4V, 1.8V. You should see the classic family of curves that flatten in saturation.

#### Step 4: Implement the PMOS I-V Model (15 min)
Write a function `i_ds_pmos(Vsg, Vsd)` using the same structure but with PMOS parameters:
- **Cutoff:** V_SG < |V_tp| --> I_SD = 0
- **Linear:** V_SG >= |V_tp| AND V_SD < V_SG - |V_tp| -->
  I_SD = k_p * [(V_SG - |V_tp|)*V_SD - 0.5*V_SD^2] * (1 + lambda_p * V_SD)
- **Saturation:** V_SG >= |V_tp| AND V_SD >= V_SG - |V_tp| -->
  I_SD = 0.5 * k_p * (V_SG - |V_tp|)^2 * (1 + lambda_p * V_SD)

> **Key insight for PMOS:** V_SG = V_DD - V_in, and V_SD = V_DD - V_out. The PMOS "sees" voltages referenced from V_DD.

#### Step 5: Plot NMOS and PMOS I-V Families (15 min)
Create a 1x2 subplot figure:
- Left: NMOS I_DS vs V_DS for V_GS = {0.6, 1.0, 1.4, 1.8} V
- Right: PMOS I_SD vs V_SD for V_SG = {0.6, 1.0, 1.4, 1.8} V
- Label axes, add legend, use grid
- Save as `mosfet_iv_curves.png`

**What to check:** Curves should be smooth, start at origin, rise linearly, then saturate. Higher gate voltages = higher saturation current.

#### Step 6: Build the Inverter VTC via Current Balancing (30 min)
This is the core of the project. For a CMOS inverter:
- NMOS: V_GS = V_in, V_DS = V_out
- PMOS: V_SG = V_DD - V_in, V_SD = V_DD - V_out
- **At DC equilibrium:** I_DS,nmos = I_SD,pmos (all current from PMOS flows into NMOS)

**Algorithm:**
1. Sweep V_in from 0 to V_DD in 1000 steps
2. For each V_in, sweep V_out from 0 to V_DD in 1000 steps
3. Compute I_nmos(V_in, V_out) and I_pmos(V_in, V_out)
4. Find the V_out where |I_nmos - I_pmos| is minimized -- this is the operating point
5. Store the (V_in, V_out) pair

> **Tip:** Use `numpy` vectorization on the V_out sweep for speed. The nested loop over V_in is fine at 1000 points.

#### Step 7: Plot the VTC (15 min)
- Plot V_out vs V_in
- Add a dashed line for V_out = V_in (the unity gain line)
- Mark V_M (switching threshold) where the VTC crosses V_out = V_in
- Add horizontal dashed lines at V_OH and V_OL
- Title: "CMOS Inverter VTC - 180nm Process"
- Save as `cmos_inverter_vtc.png`

**Expected shape:** The VTC should look like a steep "S" flipped horizontally. V_out should be high (~V_DD) for low V_in, and low (~0) for high V_in, with a sharp transition around V_DD/2.

#### Step 8: Extract Key Parameters (20 min)
From the VTC, extract and print:

| Parameter | Definition | Expected Value (180nm, balanced) |
|-----------|-----------|--------------------------------|
| V_OH | Maximum output high | ~ 1.8 V |
| V_OL | Minimum output low | ~ 0 V |
| V_M | Switching threshold (V_out = V_in crossing) | ~ 0.9 V (V_DD/2) |
| V_IH | Input high (where slope = -1, upper) | ~ 1.0 V |
| V_IL | Input low (where slope = -1, lower) | ~ 0.8 V |
| NM_H | Noise Margin High = V_OH - V_IH | > 0.72 V |
| NM_L | Noise Margin Low = V_IL - V_OL | > 0.72 V |

**To find V_IL and V_IH:** Compute dV_out/dV_in numerically using `numpy.gradient()`. Find the two points where the gain equals -1.

#### Step 9: Sensitivity Analysis - Vary k_p/k_n Ratio (20 min)
Plot VTCs for three different PMOS/NMOS strength ratios:
- k_p/k_n = 0.25 (weak PMOS) --> V_M shifts low
- k_p/k_n = 0.5 (our baseline, balanced) --> V_M ~ V_DD/2
- k_p/k_n = 1.0 (strong PMOS) --> V_M shifts high

Overlay all three VTCs on one plot. This demonstrates why PMOS transistors in real designs are made ~2x wider than NMOS -- to compensate for lower hole mobility.

Save as `vtc_sensitivity.png`

#### Step 10: Annotate the Five Operating Regions (15 min)
On your VTC plot, label the five regions of CMOS inverter operation:

| Region | V_in Range | NMOS | PMOS |
|--------|-----------|------|------|
| A | 0 to V_tn | Cutoff | Linear |
| B | V_tn to V_M | Saturation | Linear |
| C | V_M (transition) | Saturation | Saturation |
| D | V_M to V_DD+V_tp | Linear | Saturation |
| E | V_DD+V_tp to V_DD | Linear | Cutoff |

Add vertical dashed lines and region labels to the VTC plot. Save as `vtc_regions.png`

#### Step 11: Write Your Technical Summary (20 min)
Create a 1-page document (Word, Google Doc, or Markdown) covering:
- **Title:** "Week 1: CMOS Inverter DC Characterization"
- **Objective:** 2 sentences on what you did and why
- **Key Results:** Table of extracted parameters
- **Key Plot:** Your best VTC plot
- **Analysis:** 2-3 sentences on what the sensitivity analysis taught you
- **One thing I learned:** A sentence on your biggest takeaway

---

### 5. Schematic / Architecture Aid

```
        V_DD (1.8V)
         |
     +---+---+
     |       |
     |  PMOS |  (V_SG = V_DD - V_in)
     |  (M2) |  (V_SD = V_DD - V_out)
     |       |
     +---+---+
         |
 V_in ---+-------> V_out
         |
     +---+---+
     |       |
     |  NMOS |  (V_GS = V_in)
     |  (M1) |  (V_DS = V_out)
     |       |
     +---+---+
         |
        GND

  At DC: I_PMOS = I_NMOS  -->  determines V_out for each V_in
```

The inverter has ONE input (V_in) and ONE output (V_out). The PMOS pulls V_out toward V_DD; the NMOS pulls V_out toward GND. Whichever transistor is "stronger" at a given V_in wins.

---

### 6. Expected Results and Verification Checklist

- [ ] NMOS I-V family shows 4 distinct curves that saturate at different levels
- [ ] PMOS I-V family shows similar shape with PMOS parameters
- [ ] VTC has a sharp transition (not gradual) around V_DD/2
- [ ] V_M is within 5% of 0.9V for the balanced design (target: 0.855V - 0.945V)
- [ ] NM_H > 0.72V (40% of V_DD)
- [ ] NM_L > 0.72V (40% of V_DD)
- [ ] Sensitivity plot shows V_M shifting with k_p/k_n ratio
- [ ] All five operating regions are correctly labeled
- [ ] Technical summary is complete with table and plot

---

### 7. Common Pitfalls and Troubleshooting

| Problem | Cause | Fix |
|---------|-------|-----|
| VTC looks like a straight diagonal line | PMOS voltages not referenced correctly from V_DD | For PMOS: use V_SG = V_DD - V_in and V_SD = V_DD - V_out |
| V_out never reaches V_DD or 0V | Channel-length modulation too high, or sweep resolution too low | Try lambda = 0 first to verify, then add back. Increase sweep to 2000 points |
| I_DS goes negative | Negative V_DS being passed to saturation equation | Add `max(0, ...)` guard or check region conditions carefully |
| VTC is noisy or jagged | `argmin` finding inconsistent V_out values | Smooth the current difference before finding minimum; ensure V_out sweep is fine enough |
| V_M is far from V_DD/2 | k_p/k_n ratio not set to 0.5 | The balanced condition requires k_p = k_n/2 when mu_p ~ mu_n/2. Check your parameters |
| Gain never reaches -1 | Too coarse V_in sweep | Increase to 2000+ points for gradient calculation |

---

### 8. Resources

1. **Tutorial/Video:** "CMOS Inverter VTC" by Razavi - UCLA EE courses on YouTube. Search: "Razavi CMOS Inverter Lecture". Covers the exact theory behind this project.

2. **Textbook Reference:** Sedra/Smith, *Microelectronic Circuits*, 8th Ed, Chapter 14 (CMOS Digital Logic Circuits), Sections 14.1-14.3 -- covers inverter VTC, noise margins, and switching threshold derivation.

3. **Textbook Reference:** Rabaey, Chandrakasan, Nikolic, *Digital Integrated Circuits*, 2nd Ed, Chapter 5 -- "The CMOS Inverter" -- the gold standard reference for this exact topic.

4. **Textbook Reference:** Razavi, *Design of Analog CMOS Integrated Circuits*, 2nd Ed, Chapter 2 -- MOSFET modeling and I-V characteristics from an analog design perspective.

5. **Documentation:** NumPy gradient documentation: `numpy.gradient` -- you'll use this for computing dV_out/dV_in numerically.

6. **Industry Context:** TSMC's process technology pages describe how threshold voltages and mobility are characterized at each node -- the same parameters you're modeling here.

7. **Community:** r/ECE and r/chipdesign on Reddit -- active communities for IC design questions. Also the "Analog IC Design" Discord server.

8. **Python Reference:** Matplotlib documentation for creating publication-quality multi-panel figures with annotations.

---

### 9. Deliverables for Portfolio

| Deliverable | Format | Filename |
|-------------|--------|----------|
| MOSFET I-V characteristic plots | PNG | `mosfet_iv_curves.png` |
| CMOS Inverter VTC plot | PNG | `cmos_inverter_vtc.png` |
| Sensitivity analysis plot | PNG | `vtc_sensitivity.png` |
| Annotated five-region VTC | PNG | `vtc_regions.png` |
| Python notebook (all code) | .ipynb | `cmos_inverter_vtc.ipynb` |
| 1-page technical summary | PDF/MD | `week01_summary.pdf` |

**Portfolio links (fill in after completion):**
- GitHub repo: _______________
- Google Drive folder: _______________

---

### 10. Extension Challenge (Optional)

**If you finish early: Add Transient (Dynamic) Analysis**

Model the inverter's switching behavior by adding a load capacitance (C_L = 50 fF) and computing the propagation delays t_pHL and t_pLH:

1. Apply a step input from 0 to V_DD
2. At each time step, compute I_discharge (NMOS) or I_charge (PMOS)
3. Numerically integrate: dV_out/dt = I / C_L using Euler's method
4. Measure t_pHL (output falls from V_DD to V_DD/2) and t_pLH (output rises from 0 to V_DD/2)
5. Plot V_out vs time for both rising and falling transitions

**Success criteria:**
- t_pHL and t_pLH are in the range of 10-100 ps for these parameters
- t_pHL < t_pLH (because NMOS is stronger than PMOS at equal W/L)

---

### Interview Question of the Week

> **"Why are PMOS transistors typically made wider than NMOS transistors in a CMOS inverter, and how does this affect the switching threshold?"**

**Key points to hit in your answer:**
- Hole mobility is ~2-3x lower than electron mobility
- To balance pull-up and pull-down strength, W_p/W_n ~ 2-3x
- This centers V_M at V_DD/2, maximizing noise margins
- Your sensitivity analysis plot directly demonstrates this!

---

### Definition of Done

- [ ] All four plots generated and saved
- [ ] V_M within 5% of V_DD/2 (numerically verified)
- [ ] Both noise margins > 0.4 * V_DD (numerically verified)
- [ ] Can explain why PMOS is made wider (interview question)
- [ ] 1-page technical summary written
- [ ] All files organized in `Week_01_CMOS_Inverter/` folder

---

## Calendar Event (Copy-Paste Ready)

**Title:** EE Project: CMOS Inverter DC Analysis and VTC Modeling
**Date:** Saturday, April 4, 2026
**Time:** 12:00 PM - 3:30 PM
**Duration:** 3.5 hours
**Reminders:** 1 day before (Friday 12:00 PM), 1 hour before (Saturday 11:00 AM)
**Description:**
Week 1 - CMOS Inverter DC Characterization (IC Design & VLSI)
Objective: Model NMOS/PMOS I-V curves and build a CMOS inverter VTC in Python.
Checklist:
- [ ] Set up Python environment and define 180nm parameters
- [ ] Implement and verify NMOS I-V model
- [ ] Implement and verify PMOS I-V model
- [ ] Plot I-V families for both transistors
- [ ] Build VTC via current balancing algorithm
- [ ] Plot VTC and extract V_M, NM_H, NM_L
- [ ] Sensitivity analysis (vary k_p/k_n)
- [ ] Label five operating regions
- [ ] Write 1-page technical summary
