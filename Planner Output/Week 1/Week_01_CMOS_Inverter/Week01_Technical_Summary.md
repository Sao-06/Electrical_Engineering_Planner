# Week 1 Technical Summary — CMOS Inverter Analysis

---

## Operating Regions

A MOSFET does not operate in just one region — it transitions through **cutoff, saturation, and linear** depending on the relationship between terminal voltages. For an NMOS with source at GND:

- **Cutoff**: Vgs < Vtn — no channel, no current
- **Saturation**: Vgs > Vtn, Vds > (Vgs − Vtn) — channel is pinched off, current depends on Vgs² (gate-controlled)
- **Linear**: Vds < (Vgs − Vtn) — channel is fully formed, current depends on both Vgs and Vds

The key insight is that when NMOS first turns on (Vin rising from 0), Vout ≈ Vdd, so Vds is large — this places NMOS in **saturation first**, not linear. It only enters linear as Vout is pulled down.

---

## Terminal Assignments

| Device | Source | Vgs (turn-on voltage) | Vds (drop across channel) |
|--------|--------|-----------------------|---------------------------|
| NMOS | GND | Vgs = Vin | Vds = Vout |
| PMOS | Vdd | Vsg = Vdd − Vin | Vsd = Vdd − Vout |

This asymmetry is critical: NMOS and PMOS respond to Vin in **opposite** directions. As Vin rises, NMOS turns on harder (Vgs increases) while PMOS turns off (Vsg decreases). This complementary push-pull behavior drives Vout from Vdd to GND and is the foundation of the CMOS inverter's rail-to-rail swing.

---

## IV Characteristics and the Shockley Model

The long-channel Shockley model (with channel-length modulation λ) captures the dependence of drain current on gate voltage in saturation:

$$I_{DS} = \frac{k_n}{2}(V_{GS} - V_{tn})^2 (1 + \lambda V_{DS})$$

From the IV curves, the saturation region shows near-flat current lines separated by gate voltage — confirming that **gate voltage controls current in saturation**, not Vds. The linear region shows strong Vds dependence, and the transition boundary (Vds = Vgs − Vth) is visible as the knee between the two regions.

---

## VTC and the Five Operating Regions

The Voltage Transfer Characteristic (VTC) maps Vin → Vout and reveals five distinct regions based on which device is in saturation/linear:

1. NMOS off, PMOS linear → Vout = Vdd
2. NMOS saturation, PMOS linear
3. Both in saturation (transition region — steepest gain)
4. NMOS linear, PMOS saturation
5. PMOS off, NMOS linear → Vout = 0

The VTC is continuous and smooth — it is an **analog function**. Digital logic treats it as a step, but the underlying physics is always analog. The switching threshold Vm (where Vin = Vout) depends on the kp/kn ratio: a larger PMOS (higher kp) shifts Vm toward Vdd.

---

## Noise Margins

Noise margins quantify how much signal degradation a receiver can tolerate before misreading a logic level:

$$NM_H = V_{OH} - V_{IH} \quad , \quad NM_L = V_{IL} - V_{OL}$$

VIL and VIH are defined where |dVout/dVin| = 1 (unity-gain points). Signals between VIL and VIH fall in the **undefined region** — the circuit may produce unpredictable output. This reveals that even a well-designed CMOS gate has a finite window of reliability, not a perfect binary response.

---

## Mobility and Transconductance

PMOS has lower transconductance (kp < kn) because it relies on **hole mobility**, which is roughly half that of electron mobility in silicon. This is why PMOS is typically sized larger (wider W) than NMOS to achieve symmetric switching. In this project, kp = 100 µA/V² vs kn = 200 µA/V² — a 2× ratio. This directly affects the VTC symmetry: an unmatched inverter shifts Vm away from Vdd/2.

---

## Simplifying Assumptions Used

- Vs = 0 for NMOS (source tied to GND) → Vgs = Vin, Vds = Vout
- Vs = Vdd for PMOS (source tied to Vdd) → Vsg = Vdd − Vin, Vsd = Vdd − Vout
- Long-channel model (no short-channel effects)
- No subthreshold current (hard cutoff at Vth)

These assumptions keep the model tractable and analytically solvable. They are reasonable for 180nm at low-to-moderate Vds but break down for sub-22nm nodes where short-channel effects dominate.

---

## Python Simulation vs Industry Tools

Simulating CMOS circuits in Python — deriving currents from the Shockley equations and solving for Vout numerically — is valuable precisely because it forces engagement with the underlying math. Every plot is the direct output of a formula, making the connection between theory and result explicit.

Industry simulation tools like LTspice take a different approach: you draw the schematic, assign SPICE model parameters, and the solver handles the numerics automatically. This is far faster for design iteration and handles effects (parasitics, temperature variation, non-ideal models) that a hand-written script would require enormous effort to replicate. In a real workspace, writing Python to simulate a full circuit from scratch would be impractical.

The right takeaway is that both approaches are complementary: Python for building intuition and verifying understanding of fundamental equations; SPICE tools for realistic circuit simulation and design work. Learning LTspice or ngspice is a natural next step to bridge from conceptual understanding to professional-grade simulation.

---

## Reflection on AI-Assisted Learning

Estimated time: ~3 hours. Actual time: 6+ hours.

AI tools can accelerate code generation and concept explanation, but they cannot compress the time needed to **build intuition**. Working through why NMOS enters saturation before linear, or why Vds = Vout (not Vin), requires tracing through the logic yourself — the AI can provide the answer, but not the understanding. The gap between receiving an answer and owning it is where the learning actually happens.
