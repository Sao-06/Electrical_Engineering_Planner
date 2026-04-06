# Week 1 Technical Summary — CMOS Inverter Analysis

---

## Operating regions

A MOSFET moves through three states depending on terminal voltages — cutoff, saturation, and linear. For NMOS with source at GND:

- **Cutoff**: Vgs < Vtn — no channel, no current
- **Saturation**: Vgs > Vtn, Vds > (Vgs − Vtn) — channel pinched off, current set by Vgs²
- **Linear**: Vds < (Vgs − Vtn) — full channel, current depends on both Vgs and Vds

When NMOS first turns on (Vin rising from 0), Vout is still near Vdd, so Vds is large. That puts NMOS in saturation first. It only reaches linear after Vout gets pulled down far enough.

---

## Terminal assignments

| Device | Source | Gate-source voltage | Drain-source voltage |
|--------|--------|---------------------|----------------------|
| NMOS | GND | Vgs = Vin | Vds = Vout |
| PMOS | Vdd | Vsg = Vdd − Vin | Vsd = Vdd − Vout |

As Vin rises, NMOS turns on harder while PMOS shuts off. Vout gets pulled to GND from one side and pushed toward Vdd from the other — whichever wins determines the output.

---

## IV characteristics and the Shockley model

$$I_{DS} = \frac{k_n}{2}(V_{GS} - V_{tn})^2 (1 + \lambda V_{DS})$$

In saturation, the IV curves are nearly flat lines spaced by gate voltage — gate controls current, not Vds. The knee where the curves bend is exactly Vds = Vgs − Vth, the boundary into linear.

---

## VTC and the five operating regions

The VTC maps Vin → Vout across five regions:

1. NMOS off, PMOS linear → Vout = Vdd
2. NMOS saturation, PMOS linear
3. Both in saturation (steepest gain, sharpest transition)
4. NMOS linear, PMOS saturation
5. PMOS off, NMOS linear → Vout = 0

The VTC looks like a step, but it's a smooth analog curve. The switching threshold Vm (where Vin = Vout) shifts with the kp/kn ratio — a stronger PMOS pushes Vm toward Vdd.

---

## Noise margins

$$NM_H = V_{OH} - V_{IH} \qquad NM_L = V_{IL} - V_{OL}$$

VIL and VIH are the points where |dVout/dVin| = 1. Any input between them lands in undefined territory — the output is unreliable. Even a clean inverter has a finite window where it just doesn't know what to do.

---

## Mobility and transconductance

Holes move slower than electrons, so PMOS has lower transconductance than NMOS. In this project, kp = 100 µA/V² vs kn = 200 µA/V² — a 2× gap. That imbalance shifts Vm off-center, which is why PMOS is sized wider in practice to compensate.

---

## Simplifying assumptions

- NMOS source at GND → Vgs = Vin, Vds = Vout
- PMOS source at Vdd → Vsg = Vdd − Vin, Vsd = Vdd − Vout
- Long-channel model, no short-channel effects
- Hard cutoff at Vth (no subthreshold current)

These hold reasonably well at 180nm. Below 22nm they start to break.

---

## Python vs SPICE

Writing the simulation in Python meant deriving every current from the Shockley equations by hand. Annoying at times, but it meant I couldn't skip over the parts I didn't understand. That's the actual benefit. The problem is it doesn't scale — parasitics, temperature, real device models all need extra work that adds up fast. LTspice handles that by default. You draw the schematic, assign models, run the sim. The two aren't competing; they're for different things. Python for understanding, SPICE for actual design work.

---

## AI-assisted learning

Estimated: 3 hours. Actual: 6+.

The AI was useful for code and explanations, but it couldn't speed up the parts that actually took time — like figuring out why Vds = Vout and not Vin, or why NMOS hits saturation before linear. Getting an answer and understanding it are different things.
