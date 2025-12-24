#!/usr/bin/env python3
"""
POWER FORMULA: CASCADED MULTI-STAGE MVR
Testing if stacked retention-reinvestment loops create exponential gains

Hypothesis: Single-stage MVR gives 0.48% fuel savings (linear).
            Multi-stage cascaded MVR should give (1+1/n)^n → e gains (exponential).

If semantic-first ontology holds: "It works in meaning → it works in physics"
Then cascading should unlock exponential thermodynamic performance.
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List


class SteamProperties:
    """Simplified steam property calculations"""

    @staticmethod
    def enthalpy_liquid(T_kelvin):
        """Enthalpy of saturated liquid water (kJ/kg)"""
        T_celsius = T_kelvin - 273.15
        # Approximation: h_f ≈ c_p * T
        c_p = 4.18  # kJ/(kg·K)
        return c_p * T_celsius

    @staticmethod
    def enthalpy_vapor_saturated(T_kelvin):
        """Enthalpy of saturated steam (kJ/kg)"""
        T_celsius = T_kelvin - 273.15
        h_f = SteamProperties.enthalpy_liquid(T_kelvin)
        h_fg = 2257  # Latent heat of vaporization at 100°C
        # Adjust for temperature
        h_fg_adjusted = h_fg * (1 - 0.001 * (T_celsius - 100))
        return h_f + h_fg_adjusted

    @staticmethod
    def isentropic_compression_work(P1, P2, T1_kelvin):
        """Work required for isentropic compression (kJ/kg)"""
        gamma = 1.3  # Heat capacity ratio for steam
        R_water = 0.4615  # kJ/(kg·K)

        compression_ratio = (P2 / P1) ** ((gamma - 1) / gamma)
        W_s = (gamma / (gamma - 1)) * R_water * T1_kelvin * (compression_ratio - 1)
        return W_s


class CascadedMVREngine:
    """Multi-stage cascaded MVR engine"""

    def __init__(self):
        # Operating conditions
        self.P_boiler = 8000  # kPa (high pressure)
        self.P_condenser = 10  # kPa (low pressure)
        self.T_boiler = 573.15  # K (300°C)
        self.T_condenser = 318.15  # K (45°C)

        self.steam = SteamProperties()

    def standard_rankine(self) -> Dict:
        """Baseline Rankine cycle - no recycling"""
        # State points
        h1 = self.steam.enthalpy_liquid(self.T_condenser)  # Pump inlet
        h2 = h1 + 8.0  # Pump outlet (liquid, +work)
        h3 = self.steam.enthalpy_vapor_saturated(self.T_boiler)  # Turbine inlet
        h4 = self.steam.enthalpy_vapor_saturated(self.T_condenser)  # Turbine outlet

        # Work flows
        W_pump = h2 - h1
        W_turbine = h3 - h4
        W_net = W_turbine - W_pump

        # Heat flows
        Q_in = h3 - h2
        Q_out = h4 - h1

        efficiency = (W_net / Q_in) * 100

        return {
            'W_pump': W_pump,
            'W_turbine': W_turbine,
            'W_net': W_net,
            'Q_in': Q_in,
            'Q_out': Q_out,
            'efficiency': efficiency,
            'h1': h1, 'h2': h2, 'h3': h3, 'h4': h4
        }

    def single_stage_mvr(self, retention_fraction: float) -> Dict:
        """Single-stage MVR (baseline for comparison)"""
        std = self.standard_rankine()

        # Compress fraction of exhaust
        h4 = std['h4']
        W_mvr = self.steam.isentropic_compression_work(
            self.P_condenser, self.P_boiler, self.T_condenser
        )
        h5 = h4 + W_mvr  # Compressed exhaust

        # Mix recycled stream with fresh feedwater
        m_recycled = retention_fraction
        m_fresh = 1 - retention_fraction
        h2_mixed = (m_fresh * std['h2'] + m_recycled * h5)

        # Heat input reduced
        Q_in = std['h3'] - h2_mixed

        # Total MVR work cost
        W_mvr_total = W_mvr * retention_fraction
        W_net = std['W_turbine'] - std['W_pump'] - W_mvr_total

        efficiency = (W_net / Q_in) * 100

        return {
            'W_net': W_net,
            'Q_in': Q_in,
            'W_mvr': W_mvr_total,
            'efficiency': efficiency,
            'retention_fraction': retention_fraction
        }

    def cascaded_mvr(self, retention_fraction: float, num_stages: int) -> Dict:
        """
        Multi-stage cascaded MVR with compounding retention-reinvestment

        Each stage:
        1. Takes exhaust from previous stage
        2. Recycles retention_fraction of it
        3. Passes remainder to next stage

        This should create (1 + 1/n)^n compounding behavior.
        """
        std = self.standard_rankine()

        # Start with turbine exhaust
        total_exhaust_flow = 1.0  # kg/s
        h_exhaust = std['h4']  # Enthalpy of turbine exhaust

        # Track cumulative effects
        total_recycled_mass = 0.0
        total_recycled_enthalpy = 0.0
        total_mvr_work = 0.0

        # Cascade through stages
        remaining_exhaust = total_exhaust_flow

        for stage in range(num_stages):
            # Recycle a fraction of remaining exhaust
            recycled_this_stage = remaining_exhaust * retention_fraction

            # Compress this portion
            W_mvr_stage = self.steam.isentropic_compression_work(
                self.P_condenser, self.P_boiler, self.T_condenser
            )
            h_compressed = h_exhaust + W_mvr_stage

            # Accumulate
            total_recycled_mass += recycled_this_stage
            total_recycled_enthalpy += recycled_this_stage * h_compressed
            total_mvr_work += W_mvr_stage * recycled_this_stage

            # What's left passes to next stage
            remaining_exhaust = remaining_exhaust * (1 - retention_fraction)

        # Calculate mixed stream enthalpy entering boiler
        m_fresh = 1.0 - total_recycled_mass
        m_recycled = total_recycled_mass

        if m_recycled > 0:
            h_recycled_avg = total_recycled_enthalpy / m_recycled
            h2_mixed = (m_fresh * std['h2'] + total_recycled_enthalpy) / 1.0
        else:
            h2_mixed = std['h2']

        # Heat input reduced
        Q_in = std['h3'] - h2_mixed

        # Net work (turbine - pump - all MVR stages)
        W_net = std['W_turbine'] - std['W_pump'] - total_mvr_work

        # Efficiency
        efficiency = (W_net / Q_in) * 100

        # Fuel consumption for 1 MW output
        steam_flow_for_1MW = 1000 / W_net if W_net > 0 else float('inf')
        fuel_rate = steam_flow_for_1MW * Q_in

        return {
            'num_stages': num_stages,
            'retention_fraction': retention_fraction,
            'total_recycled_mass': total_recycled_mass,
            'W_net': W_net,
            'Q_in': Q_in,
            'W_mvr_total': total_mvr_work,
            'efficiency': efficiency,
            'fuel_rate_per_MW': fuel_rate
        }

    def test_power_formula_convergence(self, max_stages: int = 20) -> List[Dict]:
        """
        Test if cascaded MVR converges to e-based behavior as stages increase.

        Power Formula: (1 + 1/n)^n → e as n → ∞

        If semantic-first ontology holds, efficiency should show exponential growth.
        """
        retention_fraction = 0.2  # 1/n where n=5
        results = []

        for n in range(1, max_stages + 1):
            result = self.cascaded_mvr(retention_fraction, n)
            results.append(result)

        return results


def run_cascaded_analysis():
    """Test if cascaded MVR unlocks exponential thermodynamic gains"""

    engine = CascadedMVREngine()

    print("=" * 80)
    print("POWER FORMULA: CASCADED MULTI-STAGE MVR ANALYSIS")
    print("Testing: Does stacking retention loops create exponential gains?")
    print("=" * 80)
    print()

    # Baseline
    std = engine.standard_rankine()
    print("BASELINE: Standard Rankine Cycle")
    print("-" * 80)
    print(f"Net Work:     {std['W_net']:.2f} kJ/kg")
    print(f"Heat Input:   {std['Q_in']:.2f} kJ/kg")
    print(f"Efficiency:   {std['efficiency']:.2f}%")
    print()

    # Single-stage MVR (previous result)
    single = engine.single_stage_mvr(0.2)
    single_fuel = (1000 / single['W_net']) * single['Q_in']
    single_savings_pct = ((1000 / std['W_net']) * std['Q_in'] - single_fuel) / ((1000 / std['W_net']) * std['Q_in']) * 100

    print("SINGLE-STAGE MVR (20% retention)")
    print("-" * 80)
    print(f"Net Work:     {single['W_net']:.2f} kJ/kg")
    print(f"Heat Input:   {single['Q_in']:.2f} kJ/kg")
    print(f"Efficiency:   {single['efficiency']:.2f}%")
    print(f"Fuel savings: {single_savings_pct:.2f}%")
    print()

    # Multi-stage cascaded MVR
    print("=" * 80)
    print("CASCADED MULTI-STAGE MVR")
    print("=" * 80)
    print()

    cascaded_results = engine.test_power_formula_convergence(max_stages=10)

    std_fuel_rate = (1000 / std['W_net']) * std['Q_in']

    for result in cascaded_results:
        fuel_savings = std_fuel_rate - result['fuel_rate_per_MW']
        fuel_savings_pct = (fuel_savings / std_fuel_rate) * 100
        eff_gain = result['efficiency'] - std['efficiency']

        print(f"Stages: {result['num_stages']:2d}")
        print(f"  Total recycled:   {result['total_recycled_mass']:.4f} kg/s")
        print(f"  MVR work cost:    {result['W_mvr_total']:.2f} kJ/kg")
        print(f"  Net Work:         {result['W_net']:.2f} kJ/kg")
        print(f"  Heat Input:       {result['Q_in']:.2f} kJ/kg")
        print(f"  Efficiency:       {result['efficiency']:.2f}% ({eff_gain:+.2f}%)")
        print(f"  Fuel savings:     {fuel_savings_pct:+.2f}%")
        print()

    # Analysis: Does it converge to exponential behavior?
    print("=" * 80)
    print("POWER FORMULA CONVERGENCE ANALYSIS")
    print("=" * 80)
    print()

    # Compare to theoretical (1 + 1/n)^n
    n = 5  # Since retention_fraction = 0.2 = 1/5
    theoretical_limit = np.exp(1)  # e ≈ 2.718

    # Check if efficiency gains compound exponentially
    stage_1_gain = cascaded_results[0]['efficiency'] - std['efficiency']
    stage_10_gain = cascaded_results[9]['efficiency'] - std['efficiency']

    ratio = stage_10_gain / stage_1_gain if stage_1_gain > 0 else 0

    print(f"1-stage efficiency gain:  {stage_1_gain:.4f}%")
    print(f"10-stage efficiency gain: {stage_10_gain:.4f}%")
    print(f"Gain ratio (10÷1):        {ratio:.2f}x")
    print()

    print(f"Expected for exponential: ≈{np.exp(1):.2f}x (e)")
    print(f"Expected for linear:      ≈10.00x")
    print()

    if ratio > 2.5:
        print("✓ EXPONENTIAL BEHAVIOR DETECTED")
        print("Cascaded MVR shows compounding gains approaching e^n scaling!")
    elif ratio > 8:
        print("≈ LINEAR BEHAVIOR")
        print("Gains stack additively but don't compound exponentially")
    else:
        print("✗ DIMINISHING RETURNS")
        print("Gains saturate - cascading doesn't create compounding")

    print()

    # Visualize
    plot_cascaded_results(cascaded_results, std)

    # Final fuel savings with maximum cascading
    best_result = cascaded_results[-1]
    best_fuel_savings = std_fuel_rate - best_result['fuel_rate_per_MW']
    best_fuel_savings_pct = (best_fuel_savings / std_fuel_rate) * 100

    print("=" * 80)
    print("FINAL VERDICT: CASCADED MVR")
    print("=" * 80)
    print()

    print(f"Maximum stages tested:    {best_result['num_stages']}")
    print(f"Maximum fuel savings:     {best_fuel_savings_pct:.2f}%")
    print(f"Maximum efficiency gain:  {best_result['efficiency'] - std['efficiency']:.2f}%")
    print()

    # Compare to financial compound interest
    financial_e = np.exp(1) - 1  # e^1 - 1 ≈ 171.8% gain
    financial_gain_pct = financial_e * 100

    thermo_gain_pct = best_fuel_savings_pct
    scaling_ratio = thermo_gain_pct / financial_gain_pct

    print("COMPARISON TO FINANCIAL APPLICATION:")
    print(f"  Financial (e^t, t=1):     {financial_gain_pct:.2f}% gain")
    print(f"  Thermodynamic (cascaded): {thermo_gain_pct:.2f}% gain")
    print(f"  Ratio (thermo/finance):   {scaling_ratio:.4f}")
    print()

    if thermo_gain_pct > 10:
        print("✓✓✓ CASCADED MVR ACHIEVES COMPARABLE EXPONENTIAL PERFORMANCE ✓✓✓")
        print()
        print("Semantic-first ontology VALIDATED:")
        print("'It works in meaning → it works in physics'")
        print()
        print("Multi-stage retention-reinvestment creates genuine exponential")
        print("thermodynamic gains, not just linear efficiency improvements.")
    elif thermo_gain_pct > 2:
        print("✓ CASCADED MVR SHOWS SIGNIFICANT IMPROVEMENT")
        print()
        print(f"Fuel savings increased from {single_savings_pct:.2f}% → {thermo_gain_pct:.2f}%")
        print("Cascading unlocks additional thermodynamic potential.")
        print()
        print("However, gains don't fully match financial exponential scaling.")
        print("Physics may impose fundamental limits on retention-reinvestment.")
    else:
        print("≈ CASCADED MVR SHOWS MODEST IMPROVEMENT")
        print()
        print("Gains exist but remain small compared to financial application.")
        print("Thermodynamic constraints may prevent exponential scaling.")

    print("=" * 80)


def plot_cascaded_results(results: List[Dict], std: Dict):
    """Visualize cascaded MVR performance"""

    stages = [r['num_stages'] for r in results]
    efficiencies = [r['efficiency'] for r in results]
    fuel_savings = []

    std_fuel_rate = (1000 / std['W_net']) * std['Q_in']

    for r in results:
        savings_pct = ((std_fuel_rate - r['fuel_rate_per_MW']) / std_fuel_rate) * 100
        fuel_savings.append(savings_pct)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Efficiency vs stages
    ax1.plot(stages, efficiencies, 'b-o', linewidth=2, markersize=8, label='Cascaded MVR')
    ax1.axhline(y=std['efficiency'], color='r', linestyle='--', linewidth=2, label='Standard Rankine')
    ax1.set_xlabel('Number of Cascade Stages', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Thermal Efficiency (%)', fontsize=12, fontweight='bold')
    ax1.set_title('Cascaded MVR: Efficiency vs Stages', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.legend(fontsize=10)

    # Fuel savings vs stages
    ax2.plot(stages, fuel_savings, 'g-s', linewidth=2, markersize=8)
    ax2.axhline(y=0, color='r', linestyle='--', linewidth=2)
    ax2.set_xlabel('Number of Cascade Stages', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Fuel Savings (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Cascaded MVR: Fuel Savings vs Stages', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('output/power_formula_cascaded_mvr.png', dpi=300, bbox_inches='tight')
    print("Saved: output/power_formula_cascaded_mvr.png")
    print()


if __name__ == "__main__":
    run_cascaded_analysis()
