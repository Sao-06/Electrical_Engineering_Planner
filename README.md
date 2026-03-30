# Electrical Engineering Internship Skills Planner

A structured, semester-long weekly project plan for building hands-on electrical engineering skills relevant to IC design, photonics, and semiconductor internships at companies like NVIDIA, TSMC, Apple, IBM, ARM, ASML, and Lumentum.

## Overview

This planner generates progressive weekly mini-projects (2-3 hours each) that build demonstrable, portfolio-ready skills across core EE domains:

- **IC Design & VLSI** - CMOS circuits, layout, simulation
- **Semiconductor Physics & Nanoelectronics** - Device modeling, FinFETs
- **Photonics & Opto-electronics** - Ring resonators, waveguides
- **Digital Design & Verification** - RTL, testbenches, synthesis
- **Mixed-Signal & RF** - ADCs, PLLs, amplifiers

Each week includes step-by-step instructions, Python simulation scripts, expected results, and deliverables suitable for a technical portfolio.

## Repository Structure

```
├── EE_PLANER_CLAUDE.md          # AI agent prompt / planner specification
├── Documentation.md             # Progress log tracking weekly completion
├── Planner Output/
│   ├── Week 1/
│   │   ├── Week_01_CMOS_Inverter_Fundamentals.md   # Full project plan
│   │   ├── scripts/                                 # Python simulation scripts
│   │   │   ├── vtc_curve.py
│   │   │   ├── gain_plot.py
│   │   │   ├── noise_margins.py
│   │   │   └── power_dissipation.py
│   │   └── figures/                                 # Generated plots
│   │       ├── vtc_curve.png
│   │       ├── gain_plot.png
│   │       ├── noise_margins.png
│   │       └── power_dissipation.png
│   └── Week 2/
│       └── Week_02_CMOS_Inverter_Transient_and_Power.md
└── README.md
```

## Weekly Progress

| Week | Topic | Status |
|------|-------|--------|
| 1 | CMOS Inverter DC Analysis & VTC Modeling | Planned |
| 2 | CMOS Inverter Transient Response & Power Dissipation | Planned |
| 3-16 | Coming soon | - |

## Tools Used

- **Python** (NumPy, Matplotlib) - Circuit modeling and simulation
- **MATLAB** - Analysis and visualization
- **Vivado** - Digital design and FPGA synthesis
- **KiCad** - Schematic capture and PCB layout

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Electrical-Engineering-Planner.git
   ```
2. Install Python dependencies:
   ```bash
   pip install numpy matplotlib
   ```
3. Run any week's scripts from the `Planner Output/Week N/scripts/` directory:
   ```bash
   python vtc_curve.py
   ```

## License

This project is for educational purposes.