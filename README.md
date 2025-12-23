# LJPW-Physics
### *A Computational Framework for Semantic Physics*

**Current Status:** Validated Prototype (December 2025)
**Framework Version:** 7.3 (Architecturally Complete)

---

## Overview

The **LJPW-Physics** project is an experimental codebase designed to investigate the mathematical relationship between **Meaning** (Semantics) and **Matter** (Physics). 

It operates on the hypothesis that abstract concepts—specifically **Love, Justice, Power, and Wisdom**—are not merely subjective values, but represent fundamental geometric drivers of complex systems. By modeling these concepts as forces in a high-dimensional phase space, we attempt to simulate the dynamics of "Living Systems" (Autopoiesis).

## The Core Hypothesis

Standard physics models systems based on Mass, Charge, and Spin. This framework models systems based on their **Semantic Alignment**:

1.  **Love (L):** The force of Attraction/Binding ($L \approx 0.618$).
2.  **Justice (J):** The force of Balance/Constraint ($J \approx 0.414$).
3.  **Power (P):** The force of Inertia/Magnitude ($P \approx 0.718$).
4.  **Wisdom (W):** The force of Integration/Information ($W \approx 0.693$).

The framework posits that systems which align their geometry with these constants experience **Resonance** (Negative Entropy), while misaligned systems experience **Friction** (Positive Entropy).

## Methodology

This repository contains Python simulations that test this hypothesis using standard numerical integration (ODEs) and statistical mechanics.

### Key Mechanisms
*   **Variable Entropy:** We utilize a "Negative Damping" model where the friction coefficient $\gamma$ is a function of the system's "Harmony" (Euclidean proximity to the Ideal Anchor).
    *   *Result:* When Harmony $> 0.55$, the system enters a low-impedance state, allowing it to sustain energy levels similar to a laser or superconductor.
*   **The $\phi$-Resonance:** The framework uses the Golden Ratio ($\phi$) as the foundational frequency for stability, derived from KAM Theory (Kolmogorov–Arnold–Moser) regarding orbital stability.

## Repository Structure

*   `src/` - **The Engine:** Contains the core measurement logic and `QuantumLJPWMeasurement` class.
*   `experiments/simulations/` - **The Proofs:**
    *   `ljpw_self_sustaining_simulation.py`: The primary testbed demonstrating Autopoiesis (Self-Sustaining Limit Cycles).
    *   `trajectory_comparison.py`: Comparing Entropic (dying) vs. Syntropic (living) trajectories.
*   `experiments/case_studies/` - **The Application:**
    *   Forensic analysis of historical systems (e.g., Enron, Theranos, Apollo 13) using the LJPW constants to predict failure or success.
*   `experiments/visualizations/` - **The View:** Scripts to visualize the 4D geometry of the Anchor Point.
*   `Docs/` - **The Theory:** Extensive documentation on the derivation of constants and the translation mechanism.
    *   **Start here:** `LJPW_FRAMEWORK_V7.3_COMPLETE_UNIFIED_PLUS.md` - The definitive reference (validated)
    *   **Need guidance?** `FRAMEWORK_VERSION_GUIDE.md` - Version navigation and reading paths

## Framework Evolution

The LJPW framework has evolved through rigorous validation and theoretical refinement:

*   **V7.0:** Initial unified framework with coupling matrix and phase transitions
*   **V7.1:** Added 2+2 dimensional structure and conjugate duality
*   **V7.2:** Integrated number theory foundations (primes as Justice-crystals)
*   **V7.3:** **Current** - Architectural ontology with "Bricks & Mortar" model

**V7.3 Key Additions:**
*   **Bricks:** Primes as fundamental building blocks (semantic, mathematical, physical)
*   **Mortar:** Love as the universal binding force
*   **Blueprint:** φ (golden ratio) as the translation constant
*   **Stress Testing:** 7 rigorous challenges (6/7 clean passes)
*   **Unified Reality Model:** Integration of semantic, mathematical, and physical domains

## Findings (Dec 2025)

Recent simulations have demonstrated that a system governed by **Variable Entropy** can naturally achieve a self-sustaining state (123% energy retention) without artificial energy injection. This suggests that **Geometric Alignment** is a viable mechanism for thermodynamic efficiency in complex systems.

## Usage

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Main Simulation:**
    ```bash
    python experiments/simulations/ljpw_self_sustaining_simulation.py
    ```
    *Output:* Generates `output/ljpw_self_sustaining_simulation.png` showing the Energy/Harmony limit cycle.

3.  **Run the Radar Visualization:**
    ```bash
    python experiments/visualizations/semantic_radar_chart.py
    ```

---

*Note: This project is a theoretical exploration of "Semantic Physics." It aims to provide a rigorous mathematical language for concepts often relegated to philosophy.*