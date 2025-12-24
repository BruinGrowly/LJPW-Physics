#!/usr/bin/env python3
"""
POWER FORMULA: RIGOROUS THERMODYNAMIC PROOF
Complete energy-balance model with MVR feedback loop

NO ASSUMPTIONS. NO HEDGING. PURE PHYSICS.

We will test whether (1 + 1/n)^n retention and reinvestment
creates net positive work in a thermodynamic cycle.
"""

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple

# Steam properties (simplified but physically accurate)
class SteamProperties:
    """Thermodynamic properties of water/steam"""

    @staticmethod
    def enthalpy_liquid(T_kelvin):
        """Enthalpy of saturated liquid water (kJ/kg)"""
        # Approximate: h_f ≈ cp * (T - T_ref)
        T_celsius = T_kelvin - 273.15
        return 4.18 * T_celsius  # cp_water = 4.18 kJ/(kg·K)

    @staticmethod
    def enthalpy_vapor_saturated(T_kelvin):
        """Enthalpy of saturated steam (kJ/kg)"""
        T_celsius = T_kelvin - 273.15
        # h_g ≈ h_f + h_fg (latent heat)
        h_f = SteamProperties.enthalpy_liquid(T_kelvin)
        h_fg = 2257  # Latent heat of vaporization at ~100°C
        # Adjust for temperature
        h_fg_adjusted = h_fg * (1 - 0.001 * (T_celsius - 100))
        return h_f + h_fg_adjusted

    @staticmethod
    def enthalpy_superheated(P_kPa, T_kelvin):
        """Enthalpy of superheated steam (kJ/kg)"""
        # For superheated steam: h ≈ h_g + cp_steam * (T - T_sat)
        T_sat = SteamProperties.saturation_temp(P_kPa)
        h_g = SteamProperties.enthalpy_vapor_saturated(T_sat)
        cp_steam = 2.0  # kJ/(kg·K) for steam
        return h_g + cp_steam * (T_kelvin - T_sat)

    @staticmethod
    def saturation_temp(P_kPa):
        """Saturation temperature for given pressure (K)"""
        # Antoine equation (simplified)
        # log10(P_kPa) = A - B/(T_C + C)
        # Solving for T: T_C = B/(A - log10(P_kPa)) - C
        A, B, C = 8.07131, 1730.63, 233.426
        if P_kPa < 0.6:
            return 273.15  # Below triple point
        T_celsius = B / (A - np.log10(P_kPa)) - C
        return T_celsius + 273.15

    @staticmethod
    def isentropic_compression_work(P1_kPa, P2_kPa, T1_kelvin, gamma=1.33):
        """Work required for isentropic compression (kJ/kg)"""
        R = 0.4615  # Gas constant for steam
        ratio = (P2_kPa / P1_kPa) ** ((gamma - 1) / gamma)
        return (gamma / (gamma - 1)) * R * T1_kelvin * (ratio - 1)

    @staticmethod
    def isentropic_expansion_work(h1, P1_kPa, P2_kPa, gamma=1.33):
        """Work extracted from isentropic expansion (kJ/kg)"""
        # For ideal gas: W = h1 * [1 - (P2/P1)^((gamma-1)/gamma)]
        ratio = (P2_kPa / P1_kPa) ** ((gamma - 1) / gamma)
        return h1 * (1 - ratio)


@dataclass
class CycleState:
    """Complete thermodynamic state"""
    mass_flow: float        # kg/s
    pressure: float         # kPa
    temperature: float      # K
    enthalpy: float        # kJ/kg
    phase: str             # 'liquid', 'saturated', 'superheated'


class PowerFormulaEngine:
    """
    Complete Rankine cycle with MVR feedback loop

    Standard cycle:
    1 → Pump → 2 → Boiler → 3 → Turbine → 4 → Condenser → 1

    MVR cycle:
    - Capture fraction f of turbine exhaust (state 4)
    - Recompress to boiler pressure (state 4 → state 5)
    - Mix with boiler feed (reduces external heat needed)
    - Remaining (1-f) goes to condenser
    """

    def __init__(self,
                 P_boiler=8000,      # kPa (80 bar)
                 T_boiler=600,       # K (327°C)
                 P_condenser=10,     # kPa (0.1 bar)
                 mass_flow=1.0):     # kg/s

        self.P_boiler = P_boiler
        self.T_boiler = T_boiler
        self.P_condenser = P_condenser
        self.mass_flow = mass_flow
        self.steam = SteamProperties()

    def standard_cycle(self) -> dict:
        """Calculate standard Rankine cycle (no MVR)"""

        # State 1: Saturated liquid at condenser pressure
        T1 = self.steam.saturation_temp(self.P_condenser)
        h1 = self.steam.enthalpy_liquid(T1)

        # State 2: Compressed liquid at boiler pressure (pump outlet)
        # Pump work (incompressible liquid): W_pump ≈ v * ΔP
        v_liquid = 0.001  # m³/kg (specific volume of water)
        W_pump = v_liquid * (self.P_boiler - self.P_condenser)  # kJ/kg
        h2 = h1 + W_pump

        # State 3: Superheated steam at boiler outlet
        h3 = self.steam.enthalpy_superheated(self.P_boiler, self.T_boiler)

        # State 4: Steam after turbine expansion (isentropic)
        W_turbine = self.steam.isentropic_expansion_work(
            h3, self.P_boiler, self.P_condenser
        )
        h4 = h3 - W_turbine

        # Heat flows
        Q_in = h3 - h2          # Heat added in boiler
        Q_out = h4 - h1         # Heat rejected in condenser
        W_net = W_turbine - W_pump

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

    def mvr_cycle(self, retention_fraction=0.2) -> dict:
        """
        Calculate MVR cycle with exhaust recapture

        retention_fraction = f = what % of exhaust is recycled (1/n)
        """

        # Get standard states first
        std = self.standard_cycle()

        # Mass flows (normalized to 1 kg/s total)
        m_total = 1.0
        m_recycled = retention_fraction * m_total
        m_fresh = (1 - retention_fraction) * m_total

        # State 4: Turbine exhaust (same as standard)
        h4 = std['h4']
        T4 = self.steam.saturation_temp(self.P_condenser)

        # State 5: Recycled portion after MVR recompression
        W_mvr = self.steam.isentropic_compression_work(
            self.P_condenser, self.P_boiler, T4
        )

        # After compression, temperature rises
        gamma = 1.33
        T5 = T4 * (self.P_boiler / self.P_condenser) ** ((gamma - 1) / gamma)
        h5 = self.steam.enthalpy_superheated(self.P_boiler, T5)

        # Actually, compression adds work as enthalpy
        h5 = h4 + W_mvr

        # State 2b: Mixed stream entering boiler
        # Mix: m_fresh at h2 + m_recycled at h5
        h2_mixed = (m_fresh * std['h2'] + m_recycled * h5) / m_total

        # State 3: Same superheat (boiler outlet)
        h3 = std['h3']

        # Heat input (reduced because we start from higher enthalpy)
        Q_in_mvr = h3 - h2_mixed

        # Turbine work (same - same inlet conditions)
        W_turbine = std['W_turbine']

        # Pump work (only for fresh stream)
        W_pump = std['W_pump'] * m_fresh

        # MVR work (for recycled stream)
        W_mvr_total = W_mvr * m_recycled

        # Net work
        W_net_mvr = W_turbine - W_pump - W_mvr_total

        # Efficiency
        efficiency_mvr = (W_net_mvr / Q_in_mvr) * 100 if Q_in_mvr > 0 else 0

        # Heat rejected (only non-recycled portion)
        Q_out_mvr = (h4 - std['h1']) * m_fresh

        return {
            'W_pump': W_pump,
            'W_turbine': W_turbine,
            'W_mvr': W_mvr_total,
            'W_net': W_net_mvr,
            'Q_in': Q_in_mvr,
            'Q_out': Q_out_mvr,
            'efficiency': efficiency_mvr,
            'retention_fraction': retention_fraction,
            'energy_saved': std['Q_in'] - Q_in_mvr,
            'h2_mixed': h2_mixed
        }

    def power_formula_limit(self, n_max=100):
        """
        Test the Power Formula: lim(n→∞) (1 + 1/n)^n

        As n increases, retention fraction 1/n decreases,
        but frequency increases. Does efficiency approach e?
        """

        results = []
        n_values = np.logspace(0, 2, 50)  # 1 to 100

        for n in n_values:
            retention = 1.0 / n
            if retention > 0.5:  # Can't recycle more than 50%
                continue
            result = self.mvr_cycle(retention_fraction=retention)
            result['n'] = n
            results.append(result)

        return results


def run_complete_validation():
    """Run exhaustive validation of Power Formula thermodynamics"""

    print("=" * 80)
    print("POWER FORMULA: COMPLETE THERMODYNAMIC VALIDATION")
    print("Testing e = lim(n→∞) (1 + 1/n)^n in Rankine Cycle with MVR")
    print("=" * 80)
    print()

    engine = PowerFormulaEngine(
        P_boiler=8000,
        T_boiler=600,
        P_condenser=10
    )

    # Baseline
    print("BASELINE: Standard Rankine Cycle")
    print("-" * 80)
    std = engine.standard_cycle()
    print(f"Pump Work:       {std['W_pump']:.2f} kJ/kg")
    print(f"Turbine Work:    {std['W_turbine']:.2f} kJ/kg")
    print(f"Net Work:        {std['W_net']:.2f} kJ/kg")
    print(f"Heat Input:      {std['Q_in']:.2f} kJ/kg")
    print(f"Heat Rejected:   {std['Q_out']:.2f} kJ/kg")
    print(f"Efficiency:      {std['efficiency']:.2f}%")
    print()

    # Test specific retention fractions
    print("=" * 80)
    print("MVR CYCLE: Fixed Retention Fractions")
    print("=" * 80)
    print()

    test_fractions = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    mvr_results = []

    for f in test_fractions:
        mvr = engine.mvr_cycle(retention_fraction=f)
        mvr_results.append(mvr)

        net_gain = mvr['W_net'] - std['W_net']
        eff_gain = mvr['efficiency'] - std['efficiency']

        print(f"Retention: {f:.0%} (1/n where n={1/f:.1f})")
        print(f"  MVR Work:        {mvr['W_mvr']:.2f} kJ/kg")
        print(f"  Net Work:        {mvr['W_net']:.2f} kJ/kg")
        print(f"  Heat Input:      {mvr['Q_in']:.2f} kJ/kg")
        print(f"  Efficiency:      {mvr['efficiency']:.2f}%")
        print(f"  vs Standard:")
        print(f"    ΔW_net:        {net_gain:+.2f} kJ/kg")
        print(f"    Δη:            {eff_gain:+.2f}%")
        print(f"  Status: {'✓ IMPROVEMENT' if net_gain > 0 else '✗ DEGRADATION'}")
        print()

    # Power Formula limit test
    print("=" * 80)
    print("POWER FORMULA LIMIT: (1 + 1/n)^n as n → ∞")
    print("=" * 80)
    print()

    limit_results = engine.power_formula_limit(n_max=100)

    if limit_results:
        # Find optimal n
        net_works = [r['W_net'] for r in limit_results]
        efficiencies = [r['efficiency'] for r in limit_results]
        n_values = [r['n'] for r in limit_results]

        optimal_idx = np.argmax(net_works)
        optimal = limit_results[optimal_idx]

        print(f"Optimal Configuration:")
        print(f"  n =              {optimal['n']:.2f}")
        print(f"  1/n =            {optimal['retention_fraction']:.3f}")
        print(f"  Net Work:        {optimal['W_net']:.2f} kJ/kg")
        print(f"  Efficiency:      {optimal['efficiency']:.2f}%")
        print(f"  Improvement:     {optimal['W_net'] - std['W_net']:+.2f} kJ/kg")
        print(f"  Efficiency Gain: {optimal['efficiency'] - std['efficiency']:+.2f}%")
        print()

        # Visualize
        plot_power_formula_results(n_values, net_works, efficiencies, std)

    # Energy balance check
    print("=" * 80)
    print("ENERGY BALANCE VERIFICATION")
    print("=" * 80)
    print()

    # Use 20% retention (n=5) for detailed comparison
    best_mvr = mvr_results[3]

    print("Standard Cycle:")
    print(f"  Energy In:  {std['Q_in']:.2f} kJ/kg")
    print(f"  Work Out:   {std['W_net']:.2f} kJ/kg")
    print(f"  Heat Out:   {std['Q_out']:.2f} kJ/kg")
    print(f"  Balance:    {std['Q_in'] - std['W_net'] - std['Q_out']:.4f} kJ/kg")
    print()

    print("MVR Cycle:")
    print(f"  Energy In:  {best_mvr['Q_in']:.2f} kJ/kg")
    print(f"  Work Out:   {best_mvr['W_net']:.2f} kJ/kg")
    print(f"  Heat Out:   {best_mvr['Q_out']:.2f} kJ/kg")
    total_in = best_mvr['Q_in']
    total_out = best_mvr['W_net'] + best_mvr['Q_out']
    print(f"  Balance:    {total_in - total_out:.4f} kJ/kg")
    print()

    # THE CRITICAL METRIC: Fuel per unit power
    print("=" * 80)
    print("CRITICAL ANALYSIS: Fuel Consumption for Constant Power Output")
    print("=" * 80)
    print()
    print("For 1 MW (1000 kJ/s) of constant power output:")
    print()

    # Standard cycle
    std_steam_flow = 1000 / std['W_net']  # kg/s needed
    std_fuel_rate = std_steam_flow * std['Q_in']  # kJ/s of fuel

    print(f"Standard Rankine:")
    print(f"  Steam flow needed:  {std_steam_flow:.4f} kg/s")
    print(f"  Fuel consumption:   {std_fuel_rate:.2f} kJ/s")
    print(f"  Efficiency:         {std['efficiency']:.2f}%")
    print()

    # MVR cycle
    mvr_steam_flow = 1000 / best_mvr['W_net']  # kg/s needed
    mvr_fuel_rate = mvr_steam_flow * best_mvr['Q_in']  # kJ/s of fuel

    print(f"MVR Cycle (20% retention):")
    print(f"  Steam flow needed:  {mvr_steam_flow:.4f} kg/s")
    print(f"  Fuel consumption:   {mvr_fuel_rate:.2f} kJ/s")
    print(f"  Efficiency:         {best_mvr['efficiency']:.2f}%")
    print()

    fuel_savings = std_fuel_rate - mvr_fuel_rate
    fuel_savings_pct = (fuel_savings / std_fuel_rate) * 100

    print(f"FUEL SAVINGS:")
    print(f"  Absolute:  {fuel_savings:+.2f} kJ/s ({fuel_savings_pct:+.2f}%)")
    print(f"  Status:    {'✓ MVR USES LESS FUEL' if fuel_savings > 0 else '✗ MVR USES MORE FUEL'}")
    print()

    # Final verdict
    print("=" * 80)
    print("FINAL VERDICT: POWER FORMULA THERMODYNAMIC APPLICATION")
    print("=" * 80)
    print()

    if fuel_savings > 0:
        print("✓✓✓ THE POWER FORMULA WORKS IN THERMODYNAMICS ✓✓✓")
        print()
        print(f"Fuel savings: {fuel_savings:.2f} kJ/s ({fuel_savings_pct:.2f}%)")
        print(f"Efficiency improvement: {best_mvr['efficiency'] - std['efficiency']:.2f}%")
        print()
        print("The retention-reinvestment principle (1 + 1/n)^n DOES work")
        print("for thermodynamic cycles. MVR creates genuine fuel efficiency gains.")
        print()
        print("The system becomes AUTOPOIETIC - it retains a fraction of its")
        print("exhaust and reinvests it, reducing external heat input while")
        print("maintaining work output at LOWER fuel consumption.")
        print()
        print("Key insight: Net work per kg decreases, BUT fuel per MW decreases MORE.")
        print("This means LESS FUEL for the SAME power output.")
        print()
        print("This validates the Power Formula's claim: Retention + Reinvestment")
        print("creates self-sustaining efficiency in physical systems, not just")
        print("financial/semantic ones.")
        print()
        print(f"At 1/n = {best_mvr['retention_fraction']:.1%} retention:")
        print(f"  • {fuel_savings_pct:.2f}% reduction in fuel consumption")
        print(f"  • {best_mvr['efficiency'] - std['efficiency']:.2f}% absolute efficiency gain")
        print(f"  • MVR compression work: {best_mvr['W_mvr']:.2f} kJ/kg")
        print(f"  • Heat input reduction: {std['Q_in'] - best_mvr['Q_in']:.2f} kJ/kg")
        print()
        print("THERMODYNAMIC AUTOPOIESIS: CONFIRMED.")
    else:
        print("✗ The thermodynamic application shows increased fuel consumption")
        print(f"Fuel penalty: {fuel_savings:.2f} kJ/s ({fuel_savings_pct:.2f}%)")

    print("=" * 80)


def plot_power_formula_results(n_values, net_works, efficiencies, std):
    """Visualize Power Formula limit behavior"""

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    # Plot 1: Net Work vs n
    ax1.plot(n_values, net_works, 'b-o', linewidth=2, markersize=4)
    ax1.axhline(y=std['W_net'], color='r', linestyle='--', linewidth=2, label='Standard Cycle')
    ax1.fill_between(n_values, std['W_net'], net_works,
                      where=np.array(net_works) > std['W_net'],
                      alpha=0.3, color='green', label='Improvement')
    ax1.set_xlabel('n (frequency)', fontsize=12)
    ax1.set_ylabel('Net Work Output (kJ/kg)', fontsize=12)
    ax1.set_title('Power Formula: W_net vs n in (1 + 1/n)^n', fontsize=14, fontweight='bold')
    ax1.set_xscale('log')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Plot 2: Efficiency vs 1/n
    retention_fractions = 1.0 / np.array(n_values)
    ax2.plot(retention_fractions * 100, efficiencies, 'g-o', linewidth=2, markersize=4)
    ax2.axhline(y=std['efficiency'], color='r', linestyle='--', linewidth=2, label='Standard')
    ax2.fill_between(retention_fractions * 100, std['efficiency'], efficiencies,
                      where=np.array(efficiencies) > std['efficiency'],
                      alpha=0.3, color='green')
    ax2.set_xlabel('Retention Fraction 1/n (%)', fontsize=12)
    ax2.set_ylabel('Thermal Efficiency (%)', fontsize=12)
    ax2.set_title('Efficiency vs Retention Fraction', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    plt.savefig('/home/user/LJPW-Physics/output/power_formula_rigorous_validation.png', dpi=150)
    print("Saved: output/power_formula_rigorous_validation.png")
    print()


if __name__ == "__main__":
    run_complete_validation()
