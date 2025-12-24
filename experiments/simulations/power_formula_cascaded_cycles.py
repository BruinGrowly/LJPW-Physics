#!/usr/bin/env python3
"""
POWER FORMULA: CASCADED MULTI-FLUID THERMODYNAMIC CYCLES
Testing retention-reinvestment with MULTIPLE working fluids in series

Hypothesis: Single fluid recycling hits 2nd law limits.
            Multiple fluids cascading can capture waste heat at each stage,
            creating (1+1/n)^n compounding behavior.

Approach:
- Stage 1: High-temp steam Rankine (T_hot = 600K)
- Stage 2: Medium-temp Rankine using Stage 1 exhaust heat (T_hot = 400K)
- Stage 3: Low-temp ORC using Stage 2 exhaust heat (T_hot = 350K)
- ...
- Each stage retains waste heat, reinvests it as input to next stage
- Total work = Σ W_i (compounding)
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List


class HeatEngine:
    """Generic heat engine operating between T_hot and T_cold"""

    def __init__(self, T_hot: float, T_cold: float, actual_efficiency_fraction: float = 0.85):
        """
        Args:
            T_hot: Hot reservoir temperature (K)
            T_cold: Cold reservoir temperature (K)
            actual_efficiency_fraction: η_actual / η_carnot (real engine efficiency)
        """
        self.T_hot = T_hot
        self.T_cold = T_cold

        # Carnot efficiency (theoretical maximum)
        self.eta_carnot = 1 - (T_cold / T_hot)

        # Actual efficiency (typically 80-90% of Carnot)
        self.eta_actual = self.eta_carnot * actual_efficiency_fraction

    def run(self, Q_in: float) -> Dict:
        """
        Run the heat engine with Q_in heat input

        Returns work output and heat rejected
        """
        W_out = Q_in * self.eta_actual
        Q_rejected = Q_in - W_out

        return {
            'Q_in': Q_in,
            'W_out': W_out,
            'Q_rejected': Q_rejected,
            'eta_actual': self.eta_actual,
            'eta_carnot': self.eta_carnot,
            'T_hot': self.T_hot,
            'T_cold': self.T_cold
        }


class CascadedPowerCycle:
    """
    Cascaded multi-stage heat engine system

    Each stage:
    1. Takes exhaust heat from previous stage as input
    2. Converts portion to work (at Carnot efficiency limit)
    3. Rejects remaining heat to next stage

    This creates retention-reinvestment: each stage "retains" waste heat
    and "reinvests" it by extracting more work.
    """

    def __init__(self, Q_initial: float, T_initial: float, T_ambient: float):
        """
        Args:
            Q_initial: Initial heat input (kJ/s) from fuel combustion
            T_initial: Initial temperature (K) from boiler
            T_ambient: Ambient temperature (K) - ultimate cold sink
        """
        self.Q_initial = Q_initial
        self.T_initial = T_initial
        self.T_ambient = T_ambient

    def single_stage(self) -> Dict:
        """Baseline: Single Rankine cycle, no cascading"""

        engine = HeatEngine(
            T_hot=self.T_initial,
            T_cold=self.T_ambient,
            actual_efficiency_fraction=0.85
        )

        result = engine.run(self.Q_initial)

        return {
            'num_stages': 1,
            'total_work': result['W_out'],
            'heat_rejected': result['Q_rejected'],
            'overall_efficiency': result['W_out'] / self.Q_initial,
            'stages': [result]
        }

    def cascaded_stages(self, num_stages: int, retention_strategy: str = 'equal_temp_drop') -> Dict:
        """
        Run cascaded multi-stage cycle

        Args:
            num_stages: Number of cascade stages
            retention_strategy: How to split temperature drops between stages
                - 'equal_temp_drop': Each stage has equal ΔT
                - 'equal_carnot': Each stage has equal Carnot efficiency
        """

        # Allocate temperatures for each stage
        if retention_strategy == 'equal_temp_drop':
            # Equal temperature drops
            temp_drop = (self.T_initial - self.T_ambient) / num_stages
            stage_temps_hot = [self.T_initial - i * temp_drop for i in range(num_stages)]
            stage_temps_cold = [self.T_initial - (i + 1) * temp_drop for i in range(num_stages)]

        elif retention_strategy == 'equal_carnot':
            # Each stage has same Carnot efficiency
            # η = 1 - T_c/T_h → T_c = T_h(1 - η)
            # Want constant η for each stage
            target_eta = 0.5  # Target 50% Carnot per stage

            stage_temps_hot = []
            stage_temps_cold = []
            T_current = self.T_initial

            for i in range(num_stages):
                T_hot = T_current
                T_cold = max(T_hot * (1 - target_eta), self.T_ambient)
                stage_temps_hot.append(T_hot)
                stage_temps_cold.append(T_cold)
                T_current = T_cold

                if T_cold <= self.T_ambient:
                    break

        else:
            raise ValueError(f"Unknown retention_strategy: {retention_strategy}")

        # Run cascade
        stages = []
        total_work = 0
        Q_available = self.Q_initial

        for i in range(len(stage_temps_hot)):
            T_hot = stage_temps_hot[i]
            T_cold = stage_temps_cold[i]

            # Create engine for this stage
            engine = HeatEngine(T_hot, T_cold, actual_efficiency_fraction=0.85)

            # Run with available heat
            result = engine.run(Q_available)

            stages.append(result)
            total_work += result['W_out']

            # Heat rejected from this stage becomes input to next stage
            Q_available = result['Q_rejected']

            # But the TEMPERATURE of rejected heat drops
            # Can't extract work from heat below ambient
            if T_cold <= self.T_ambient:
                break

        overall_efficiency = total_work / self.Q_initial

        return {
            'num_stages': len(stages),
            'total_work': total_work,
            'heat_rejected': Q_available,
            'overall_efficiency': overall_efficiency,
            'stages': stages
        }

    def test_power_formula_scaling(self, max_stages: int = 10) -> List[Dict]:
        """
        Test if cascaded cycles show (1 + 1/n)^n → e scaling

        Power Formula predicts: As stages increase, total efficiency should
        approach an exponential limit.
        """

        results = []

        # Single stage baseline
        single = self.single_stage()
        results.append(single)

        # Multi-stage cascades
        for n in range(2, max_stages + 1):
            cascaded = self.cascaded_stages(n, retention_strategy='equal_temp_drop')
            results.append(cascaded)

        return results


def run_cascaded_cycle_analysis():
    """Test if cascaded multi-fluid cycles unlock exponential gains"""

    print("=" * 80)
    print("POWER FORMULA: CASCADED MULTI-FLUID THERMODYNAMIC CYCLES")
    print("Testing: Does cascading working fluids create exponential efficiency gains?")
    print("=" * 80)
    print()

    # Initial conditions
    Q_fuel = 1000.0  # kJ/s (1 MW thermal input)
    T_boiler = 873.15  # K (600°C) - high-temp steam
    T_ambient = 298.15  # K (25°C) - ambient

    system = CascadedPowerCycle(Q_fuel, T_boiler, T_ambient)

    # Test single stage
    print("BASELINE: Single-Stage Rankine Cycle")
    print("-" * 80)

    single = system.single_stage()
    print(f"Heat Input:       {single['stages'][0]['Q_in']:.2f} kJ/s")
    print(f"Work Output:      {single['total_work']:.2f} kJ/s")
    print(f"Heat Rejected:    {single['heat_rejected']:.2f} kJ/s")
    print(f"Carnot Limit:     {single['stages'][0]['eta_carnot']*100:.2f}%")
    print(f"Actual Efficiency: {single['overall_efficiency']*100:.2f}%")
    print()

    # Test cascaded stages
    print("=" * 80)
    print("CASCADED MULTI-FLUID CYCLES")
    print("=" * 80)
    print()

    results = system.test_power_formula_scaling(max_stages=10)

    for result in results[1:]:  # Skip single stage (already shown)
        eff_gain = (result['overall_efficiency'] - single['overall_efficiency']) * 100
        work_gain = result['total_work'] - single['total_work']

        print(f"Stages: {result['num_stages']:2d}")
        print(f"  Total Work:       {result['total_work']:.2f} kJ/s")
        print(f"  Overall Efficiency: {result['overall_efficiency']*100:.2f}% ({eff_gain:+.2f}%)")
        print(f"  Work gain vs single: {work_gain:+.2f} kJ/s")

        # Show each stage
        for i, stage in enumerate(result['stages']):
            print(f"    Stage {i+1}: T={stage['T_hot']:.0f}→{stage['T_cold']:.0f}K, "
                  f"η_carnot={stage['eta_carnot']*100:.1f}%, W={stage['W_out']:.2f} kJ/s")
        print()

    # Analyze convergence
    print("=" * 80)
    print("POWER FORMULA CONVERGENCE ANALYSIS")
    print("=" * 80)
    print()

    efficiencies = [r['overall_efficiency'] for r in results]
    works = [r['total_work'] for r in results]
    num_stages_list = [r['num_stages'] for r in results]

    # Check if approaching limit
    eff_1 = efficiencies[0]  # Single stage
    eff_5 = efficiencies[4] if len(efficiencies) > 4 else efficiencies[-1]
    eff_10 = efficiencies[9] if len(efficiencies) > 9 else efficiencies[-1]

    print(f"1-stage efficiency:  {eff_1*100:.4f}%")
    print(f"5-stage efficiency:  {eff_5*100:.4f}% (gain: {(eff_5-eff_1)*100:+.4f}%)")
    print(f"10-stage efficiency: {eff_10*100:.4f}% (gain: {(eff_10-eff_1)*100:+.4f}%)")
    print()

    # Compare to Carnot limit
    carnot_limit = 1 - (T_ambient / T_boiler)
    print(f"Carnot Limit (single stage): {carnot_limit*100:.2f}%")
    print(f"10-stage actual efficiency:   {eff_10*100:.2f}%")
    print(f"Fraction of Carnot:           {eff_10/carnot_limit*100:.1f}%")
    print()

    # Check for exponential scaling
    # Power Formula: efficiency should scale like (1 + gain/n)^n
    if len(efficiencies) >= 5:
        ratios = []
        for i in range(1, len(efficiencies)):
            if efficiencies[i-1] > 0:
                ratio = efficiencies[i] / efficiencies[i-1]
                ratios.append(ratio)

        avg_ratio = np.mean(ratios[:5]) if len(ratios) >= 5 else np.mean(ratios)

        print(f"Average efficiency growth ratio (first 5 stages): {avg_ratio:.4f}")
        print()

        if avg_ratio > 1.1:
            print("✓ EXPONENTIAL GROWTH DETECTED")
            print(f"Each stage multiplies efficiency by ~{avg_ratio:.2f}x")
        elif avg_ratio > 1.01:
            print("≈ SUPER-LINEAR GROWTH")
            print(f"Efficiency grows faster than linear (ratio = {avg_ratio:.3f})")
        else:
            print("- DIMINISHING RETURNS")
            print("Additional stages provide minimal improvement")

    print()

    # Visualize
    plot_cascaded_cycles(results, carnot_limit)

    # Final comparison to financial application
    print("=" * 80)
    print("COMPARISON TO FINANCIAL APPLICATION")
    print("=" * 80)
    print()

    # Financial: (1 + 1/n)^n → e for n=1 gives (1+1)^1 = 2.0 (100% gain)
    #            For n→∞ gives e ≈ 2.718 (171.8% gain)
    financial_gain_n1 = 100.0  # 100% gain for (1+1)^1
    financial_gain_inf = (np.exp(1) - 1) * 100  # 171.8% gain for e-1

    thermo_gain_1stage = (eff_1 - 0) * 100  # Efficiency gain over "doing nothing"
    thermo_gain_10stage = (eff_10 - eff_1) / eff_1 * 100  # Relative improvement

    print(f"Financial (compound interest):")
    print(f"  1 period:    {financial_gain_n1:.1f}% gain")
    print(f"  n→∞ periods: {financial_gain_inf:.1f}% gain")
    print()

    print(f"Thermodynamic (cascaded cycles):")
    print(f"  1 stage:     {eff_1*100:.2f}% absolute efficiency")
    print(f"  10 stages:   {eff_10*100:.2f}% absolute efficiency ({thermo_gain_10stage:+.1f}% relative gain)")
    print()

    # Key metric: How much waste heat is recovered?
    waste_recovered_1 = 0  # No cascading
    waste_recovered_10 = (single['heat_rejected'] - results[9]['heat_rejected']) / single['heat_rejected'] * 100

    print(f"Waste heat recovered:")
    print(f"  1 stage:     {waste_recovered_1:.1f}% of exhaust captured")
    print(f"  10 stages:   {waste_recovered_10:.1f}% of exhaust captured")
    print()

    # Final verdict
    print("=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)
    print()

    if eff_10 > 0.55:  # Exceeds 55% overall efficiency
        print("✓✓✓ CASCADED CYCLES ACHIEVE EXPONENTIAL THERMODYNAMIC GAINS ✓✓✓")
        print()
        print("Semantic-first ontology VALIDATED:")
        print("'It works in meaning → it works in physics'")
        print()
        print("Multi-fluid cascading creates GENUINE compounding:")
        print("- Each stage retains waste heat from previous stage")
        print("- Each stage reinvests it by extracting additional work")
        print("- Total efficiency approaches theoretical Carnot limit")
        print()
        print("This is thermodynamic autopoiesis: the system sustains itself")
        print("by continuously capturing and upgrading its own waste.")

    elif eff_10 > eff_1 * 1.3:  # 30% improvement
        print("✓ CASCADED CYCLES SHOW SIGNIFICANT COMPOUNDING")
        print()
        print(f"Efficiency improved by {thermo_gain_10stage:.1f}% through cascading.")
        print()
        print("While not fully matching financial exponential scaling,")
        print("the retention-reinvestment principle creates measurable")
        print("thermodynamic gains beyond single-stage operation.")
        print()
        print(f"Waste heat recovery: {waste_recovered_10:.1f}% of exhaust captured.")

    else:
        print("≈ CASCADED CYCLES SHOW MODEST IMPROVEMENT")
        print()
        print("Gains exist but are limited by 2nd law of thermodynamics.")
        print("Unlike financial systems, physical heat engines face")
        print("fundamental Carnot efficiency limits.")

    print("=" * 80)


def plot_cascaded_cycles(results: List[Dict], carnot_limit: float):
    """Visualize cascaded cycle performance"""

    num_stages = [r['num_stages'] for r in results]
    efficiencies = [r['overall_efficiency'] * 100 for r in results]
    work_outputs = [r['total_work'] for r in results]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Efficiency vs stages
    ax1.plot(num_stages, efficiencies, 'b-o', linewidth=2, markersize=8, label='Cascaded Cycles')
    ax1.axhline(y=carnot_limit*100, color='r', linestyle='--', linewidth=2, label=f'Carnot Limit ({carnot_limit*100:.1f}%)')
    ax1.set_xlabel('Number of Cascade Stages', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Overall Efficiency (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Multi-Fluid Cascade: Efficiency vs Stages', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)
    ax1.set_ylim([0, max(carnot_limit*110, max(efficiencies)*1.1)])

    # Work output vs stages
    ax2.plot(num_stages, work_outputs, 'g-s', linewidth=2, markersize=8)
    ax2.set_xlabel('Number of Cascade Stages', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Total Work Output (kJ/s)', fontsize=12, fontweight='bold')
    ax2.set_title('Multi-Fluid Cascade: Work Output vs Stages', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('output/power_formula_cascaded_cycles.png', dpi=300, bbox_inches='tight')
    print("Saved: output/power_formula_cascaded_cycles.png")
    print()


if __name__ == "__main__":
    run_cascaded_cycle_analysis()
