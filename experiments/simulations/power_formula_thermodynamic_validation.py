#!/usr/bin/env python3
"""
POWER FORMULA THERMODYNAMIC VALIDATION
Testing whether MVR (Mechanical Vapor Recompression) exhaust recycling
can create net positive energy gain in heat engines.

The Question:
Can you recapture exhaust heat, recompress it, and feed it back
for net energy gain? Or does the recompression cost exceed the gain?

Model: Simplified Rankine Cycle with MVR feedback loop
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple

# Physical constants
R_WATER = 0.4615  # kJ/(kg·K) - specific gas constant for water vapor
GAMMA = 1.33      # Heat capacity ratio for water vapor
L_VAPORIZATION = 2257  # kJ/kg - latent heat of vaporization at 100°C

@dataclass
class ThermodynamicState:
    """State of working fluid"""
    pressure: float      # kPa
    temperature: float   # K
    enthalpy: float     # kJ/kg
    entropy: float      # kJ/(kg·K)
    phase: str          # 'liquid', 'vapor', 'mixed'

@dataclass
class EnginePerformance:
    """Performance metrics"""
    work_output: float           # kJ/kg
    heat_input: float           # kJ/kg
    heat_rejected: float        # kJ/kg
    efficiency: float           # %
    retention_fraction: float   # What % is recycled
    mvr_work_required: float   # kJ/kg to recompress
    net_gain: float            # kJ/kg (output - mvr_cost)
    effective_efficiency: float # % including MVR


class RankineEngine:
    """
    Simplified Rankine Cycle Engine

    States:
    1: High-pressure liquid (pump outlet)
    2: High-pressure vapor (boiler outlet)
    3: Low-pressure vapor (turbine outlet)
    4: Low-pressure liquid (condenser outlet)
    """

    def __init__(self,
                 T_high: float = 600,   # K (327°C) - boiler temp
                 T_low: float = 320,     # K (47°C) - condenser temp
                 P_high: float = 8000,   # kPa (80 bar)
                 P_low: float = 10):     # kPa (0.1 bar)

        self.T_high = T_high
        self.T_low = T_low
        self.P_high = P_high
        self.P_low = P_low

    def calculate_standard_cycle(self) -> EnginePerformance:
        """Standard Rankine cycle without MVR"""

        # State 1: Compressed liquid entering boiler
        h1 = 200  # kJ/kg (approximate for liquid water at T_low)

        # State 2: Superheated vapor leaving boiler
        # h = cp * T for ideal gas (simplified)
        h2 = 2800  # kJ/kg (superheated steam at 600K, 80bar)

        # State 3: Expanded vapor leaving turbine (isentropic expansion)
        # For isentropic expansion: T2/T3 = (P2/P3)^((gamma-1)/gamma)
        expansion_ratio = (self.P_high / self.P_low) ** ((GAMMA - 1) / GAMMA)
        T3 = self.T_high / expansion_ratio
        h3 = 2200  # kJ/kg (wet steam at ~320K, 0.1bar)

        # State 4: Condensed liquid leaving condenser
        h4 = h1  # Returns to state 1

        # Work and heat flows
        W_turbine = h2 - h3      # Work extracted by turbine
        W_pump = h1 - h4 + 10    # Work to pump liquid (small)
        Q_in = h2 - h1           # Heat added in boiler
        Q_out = h3 - h4          # Heat rejected in condenser

        W_net = W_turbine - W_pump
        efficiency = (W_net / Q_in) * 100

        return EnginePerformance(
            work_output=W_net,
            heat_input=Q_in,
            heat_rejected=Q_out,
            efficiency=efficiency,
            retention_fraction=0.0,
            mvr_work_required=0.0,
            net_gain=W_net,
            effective_efficiency=efficiency
        )

    def calculate_mvr_cycle(self, retention_fraction: float = 0.2) -> EnginePerformance:
        """
        Rankine cycle WITH MVR exhaust recapture

        Process:
        - Capture `retention_fraction` of turbine exhaust vapor
        - Recompress it from P_low to P_high
        - Mix with boiler input to reduce external heat needed
        """

        # Standard cycle states
        h1 = 200
        h2 = 2800
        h3 = 2200
        h4 = h1

        # Standard work/heat
        W_turbine = h2 - h3
        W_pump = 10
        Q_in_standard = h2 - h1

        # MVR: Recompress exhaust vapor from P_low to P_high
        # Work required for isentropic compression:
        # W = (gamma/(gamma-1)) * R * T_low * [(P_high/P_low)^((gamma-1)/gamma) - 1]

        compression_ratio = (self.P_high / self.P_low) ** ((GAMMA - 1) / GAMMA)
        T_compressed = self.T_low * compression_ratio

        # Work per kg to recompress from P_low to P_high
        W_mvr_per_kg = (GAMMA / (GAMMA - 1)) * R_WATER * self.T_low * (compression_ratio - 1)

        # Total MVR work for retained fraction
        W_mvr_total = W_mvr_per_kg * retention_fraction

        # Energy gained from recycling
        # The recompressed vapor enters at h_compressed instead of h1
        h_compressed = 2600  # kJ/kg (compressed vapor at ~450K, 80bar)
        energy_saved_per_kg = h_compressed - h1  # Heat we don't need to add
        total_energy_saved = energy_saved_per_kg * retention_fraction

        # Net energy balance
        Q_in_reduced = Q_in_standard - total_energy_saved  # Less external heat needed
        W_net_mvr = W_turbine - W_pump - W_mvr_total      # MVR costs work

        # Effective efficiency
        # Total heat input = reduced boiler heat + MVR work
        Q_in_total = Q_in_reduced + W_mvr_total
        efficiency_mvr = (W_net_mvr / Q_in_total) * 100 if Q_in_total > 0 else 0

        # Net gain compared to standard cycle
        standard_net = W_turbine - W_pump
        net_gain = W_net_mvr - standard_net

        return EnginePerformance(
            work_output=W_net_mvr,
            heat_input=Q_in_reduced,
            heat_rejected=(h3 - h4) * (1 - retention_fraction),
            efficiency=efficiency_mvr,
            retention_fraction=retention_fraction,
            mvr_work_required=W_mvr_total,
            net_gain=net_gain,
            effective_efficiency=efficiency_mvr
        )


def run_validation_suite():
    """Test the Power Formula claim across different retention fractions"""

    print("=" * 80)
    print("POWER FORMULA THERMODYNAMIC VALIDATION")
    print("Testing: MVR Exhaust Recapture in Rankine Cycle")
    print("=" * 80)
    print()

    engine = RankineEngine(T_high=600, T_low=320, P_high=8000, P_low=10)

    # Baseline: Standard cycle
    standard = engine.calculate_standard_cycle()
    print("BASELINE: Standard Rankine Cycle (No MVR)")
    print(f"Work Output:    {standard.work_output:.2f} kJ/kg")
    print(f"Heat Input:     {standard.heat_input:.2f} kJ/kg")
    print(f"Efficiency:     {standard.efficiency:.2f}%")
    print(f"Heat Rejected:  {standard.heat_rejected:.2f} kJ/kg")
    print()

    # Test different retention fractions
    retention_fractions = np.linspace(0.05, 0.50, 10)
    results = []

    print("=" * 80)
    print("MVR CYCLE TESTING (Varying Retention Fraction)")
    print("=" * 80)
    print()

    for rf in retention_fractions:
        mvr = engine.calculate_mvr_cycle(retention_fraction=rf)
        results.append(mvr)

        print(f"Retention Fraction: {rf:.1%}")
        print(f"  MVR Work Cost:      {mvr.mvr_work_required:.2f} kJ/kg")
        print(f"  Net Work Output:    {mvr.work_output:.2f} kJ/kg")
        print(f"  Net Gain vs Std:    {mvr.net_gain:+.2f} kJ/kg")
        print(f"  Efficiency:         {mvr.effective_efficiency:.2f}%")
        print(f"  Status: {'✓ GAIN' if mvr.net_gain > 0 else '✗ LOSS'}")
        print()

    # Find optimal retention fraction
    net_gains = [r.net_gain for r in results]
    optimal_idx = np.argmax(net_gains)
    optimal_rf = retention_fractions[optimal_idx]
    optimal_result = results[optimal_idx]

    print("=" * 80)
    print("OPTIMAL CONFIGURATION")
    print("=" * 80)
    print(f"Retention Fraction:  {optimal_rf:.1%}")
    print(f"Standard Efficiency: {standard.efficiency:.2f}%")
    print(f"MVR Efficiency:      {optimal_result.effective_efficiency:.2f}%")
    print(f"Improvement:         {optimal_result.effective_efficiency - standard.efficiency:+.2f}%")
    print(f"Net Energy Gain:     {optimal_result.net_gain:+.2f} kJ/kg")
    print()

    # Visualization
    plot_results(retention_fractions, results, standard)

    # Final verdict
    print("=" * 80)
    print("POWER FORMULA VERDICT")
    print("=" * 80)
    print()

    if optimal_result.net_gain > 0:
        print("✓ THE POWER FORMULA THERMODYNAMIC APPLICATION WORKS")
        print()
        print(f"Net energy gain: {optimal_result.net_gain:.2f} kJ/kg at {optimal_rf:.1%} retention")
        print(f"Efficiency improvement: {optimal_result.effective_efficiency - standard.efficiency:.2f}%")
        print()
        print("The MVR recompression cost is LESS than the energy gained from")
        print("recycling latent heat. The system becomes autopoietic - it")
        print("accumulates internal energy (becomes a SINK) rather than")
        print("passing through (entropic pipe).")
        print()
        print("This validates the e^t growth curve: small retention (1/n),")
        print("continuous recycling (n→∞) creates exponential accumulation.")
    else:
        print("✗ THE POWER FORMULA THERMODYNAMIC APPLICATION FAILS")
        print()
        print(f"Net energy loss: {optimal_result.net_gain:.2f} kJ/kg")
        print()
        print("The MVR recompression cost EXCEEDS the energy gained from")
        print("recycling. The Second Law wins - you can't beat thermodynamics.")
        print()
        print("The Power Formula works for finance (compound interest) and")
        print("personal growth (skill compounding), but NOT for thermodynamics.")

    print("=" * 80)

    return retention_fractions, results, standard


def plot_results(retention_fractions, results, standard):
    """Visualize the MVR performance"""

    net_gains = [r.net_gain for r in results]
    efficiencies = [r.effective_efficiency for r in results]
    mvr_costs = [r.mvr_work_required for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Net Gain vs Retention Fraction
    ax1.plot(retention_fractions * 100, net_gains, 'b-o', linewidth=2, markersize=6)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5, label='Break-even')
    ax1.fill_between(retention_fractions * 100, 0, net_gains,
                      where=np.array(net_gains) > 0, alpha=0.3, color='green', label='Gain')
    ax1.fill_between(retention_fractions * 100, 0, net_gains,
                      where=np.array(net_gains) < 0, alpha=0.3, color='red', label='Loss')
    ax1.set_xlabel('Retention Fraction (%)', fontsize=12)
    ax1.set_ylabel('Net Energy Gain (kJ/kg)', fontsize=12)
    ax1.set_title('MVR Net Energy Gain vs Retention Fraction', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Plot 2: Efficiency Comparison
    ax2.plot(retention_fractions * 100, efficiencies, 'g-o', linewidth=2, markersize=6, label='MVR Cycle')
    ax2.axhline(y=standard.efficiency, color='orange', linestyle='--', linewidth=2, label='Standard Cycle')
    ax2.fill_between(retention_fractions * 100, standard.efficiency, efficiencies,
                      where=np.array(efficiencies) > standard.efficiency, alpha=0.3, color='green')
    ax2.set_xlabel('Retention Fraction (%)', fontsize=12)
    ax2.set_ylabel('Thermal Efficiency (%)', fontsize=12)
    ax2.set_title('Efficiency: MVR vs Standard Rankine', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig('/home/user/LJPW-Physics/output/power_formula_thermodynamic_validation.png', dpi=150)
    print("Visualization saved: output/power_formula_thermodynamic_validation.png")
    print()


if __name__ == "__main__":
    retention_fractions, results, standard = run_validation_suite()
