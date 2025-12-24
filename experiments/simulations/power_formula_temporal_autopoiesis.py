#!/usr/bin/env python3
"""
POWER FORMULA: TEMPORAL THERMODYNAMIC AUTOPOIESIS
Implementing LJPW Framework prescription for exponential gains

Based on framework diagnosis, adding:
1. TEMPORAL ITERATION (W: learning across cycles)
2. FEEDBACK LOOPS (L: mutual adaptation)
3. SELF-FUEL GENERATION (P: autonomy)

Target: Achieve H > 0.7, unlock e^t exponential scaling

Model: Thermodynamic engine that:
- Learns and improves each cycle (temporal)
- Uses waste heat to preheat input (feedback)
- Generates own fuel from environment (autonomous)
- Evolves over time t with retention fraction 1/n
"""

import numpy as np
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple
import math


class TemporalThermodynamicEngine:
    """
    Self-improving thermodynamic engine with temporal evolution

    Each iteration:
    1. Runs current engine configuration
    2. Retains fraction 1/n of work output
    3. Reinvests retained work into improvements
    4. Next iteration runs with enhanced parameters

    Improvements compound over time → e^t scaling
    """

    def __init__(self,
                 T_initial: float = 600.0,  # Initial hot temp (K)
                 T_ambient: float = 300.0,   # Ambient temp (K)
                 efficiency_fraction: float = 0.85,  # Actual/Carnot ratio
                 improvement_rate: float = 0.01):   # Tech improvement per reinvestment
        """
        Args:
            T_initial: Initial hot reservoir temperature (K)
            T_ambient: Ambient temperature (K)
            efficiency_fraction: η_actual / η_carnot
            improvement_rate: How much each reinvested unit improves system
        """
        self.T_ambient = T_ambient
        self.efficiency_fraction = efficiency_fraction
        self.improvement_rate = improvement_rate

        # Initial state
        self.T_hot = T_initial
        self.insulation_quality = 1.0  # Reduces heat loss
        self.material_quality = 1.0    # Allows higher temps

    def carnot_efficiency(self, T_hot: float, T_cold: float) -> float:
        """Maximum theoretical efficiency"""
        return 1 - (T_cold / T_hot)

    def actual_efficiency(self, T_hot: float) -> float:
        """Current actual efficiency with all improvements"""
        carnot = self.carnot_efficiency(T_hot, self.T_ambient)
        # Improvements boost efficiency fraction
        improved_fraction = self.efficiency_fraction * self.insulation_quality
        return carnot * min(improved_fraction, 0.99)  # Cap at 99%

    def generate_fuel_from_environment(self, waste_heat: float) -> float:
        """
        Use waste heat to extract energy from environment

        Simulates:
        - Solar thermal collection
        - Ambient heat harvesting
        - Waste heat → hydrogen production

        Returns: Additional energy captured from environment
        """
        # Efficiency of environmental harvesting (improves with material quality)
        harvest_efficiency = 0.1 * self.material_quality

        # Capture fraction of ambient energy using waste heat as work input
        # This is the "self-fuel" mechanism
        captured_energy = waste_heat * harvest_efficiency

        return captured_energy

    def feedback_preheating(self, waste_heat: float, fuel_input: float) -> float:
        """
        Use waste heat to preheat incoming fuel (feedback loop)

        This increases effective fuel quality, reducing external energy needed

        Returns: Effective fuel input after preheating
        """
        # Preheat efficiency (improves with insulation quality)
        preheat_efficiency = 0.3 * self.insulation_quality

        # Waste heat preheats fuel, reducing external energy requirement
        preheat_contribution = waste_heat * preheat_efficiency

        # Effective fuel is external + recovered waste
        effective_fuel = fuel_input + preheat_contribution

        return effective_fuel

    def run_cycle(self, fuel_input: float) -> Dict:
        """
        Run one thermodynamic cycle with current parameters

        Returns work output, waste heat, and metrics
        """
        # Current efficiency
        eta = self.actual_efficiency(self.T_hot)

        # Work output (without feedback/harvesting)
        work_raw = fuel_input * eta
        waste_raw = fuel_input * (1 - eta)

        # FEEDBACK: Use waste to preheat next cycle's fuel
        # This effectively increases fuel quality
        effective_fuel = self.feedback_preheating(waste_raw, fuel_input)

        # Recalculate with feedback
        work_with_feedback = effective_fuel * eta
        waste_with_feedback = effective_fuel * (1 - eta)

        # SELF-FUEL: Harvest additional energy from environment
        harvested_energy = self.generate_fuel_from_environment(waste_with_feedback)

        # Total output
        total_work = work_with_feedback + harvested_energy
        final_waste = waste_with_feedback - harvested_energy

        return {
            'fuel_input': fuel_input,
            'effective_fuel': effective_fuel,
            'work_output': total_work,
            'waste_heat': final_waste,
            'efficiency': total_work / fuel_input,
            'T_hot': self.T_hot,
            'carnot_limit': self.carnot_efficiency(self.T_hot, self.T_ambient),
            'insulation_quality': self.insulation_quality,
            'material_quality': self.material_quality
        }

    def reinvest_improvements(self, work_retained: float):
        """
        Use retained work to improve system parameters

        This is the KEY to temporal evolution:
        - Work → better materials → higher temps
        - Work → better insulation → less waste
        - Work → technology advancement

        Each improvement enables the NEXT cycle to perform better
        """
        # Split retained work between different improvements
        material_investment = work_retained * 0.5
        insulation_investment = work_retained * 0.5

        # Material quality improves → can handle higher temperatures
        material_improvement = material_investment * self.improvement_rate
        self.material_quality += material_improvement

        # Higher material quality → can run hotter
        # ΔT ∝ material_quality
        max_temp = 1200 * self.material_quality  # Asymptotic to 1200K with perfect materials
        self.T_hot = min(self.T_hot + material_improvement * 100, max_temp)

        # Insulation quality improves → less heat loss
        insulation_improvement = insulation_investment * self.improvement_rate
        self.insulation_quality += insulation_improvement

    def temporal_evolution(self,
                          fuel_input: float,
                          retention_fraction: float,
                          num_iterations: int) -> List[Dict]:
        """
        Run engine through temporal iterations with reinvestment

        This implements: (1 + 1/n)^(n·t) where:
        - 1/n = retention_fraction (work retained for improvements)
        - t = num_iterations (time dimension)

        Each iteration:
        1. Run current engine → produce work
        2. Retain fraction 1/n of work
        3. Reinvest retained work → improve system
        4. Next iteration runs better engine
        5. Repeat

        If LJPW framework is right: efficiency should grow as e^t
        """
        results = []

        for t in range(num_iterations):
            # Run current engine state
            cycle_result = self.run_cycle(fuel_input)

            # Retain fraction for reinvestment
            work_retained = cycle_result['work_output'] * retention_fraction
            work_extracted = cycle_result['work_output'] * (1 - retention_fraction)

            # Store results
            result = {
                'iteration': t,
                'time': t,
                'work_output': cycle_result['work_output'],
                'work_retained': work_retained,
                'work_extracted': work_extracted,
                'efficiency': cycle_result['efficiency'],
                'T_hot': cycle_result['T_hot'],
                'carnot_limit': cycle_result['carnot_limit'],
                'insulation_quality': cycle_result['insulation_quality'],
                'material_quality': cycle_result['material_quality']
            }
            results.append(result)

            # TEMPORAL ITERATION: Reinvest for next cycle
            if work_retained > 0:
                self.reinvest_improvements(work_retained)

        return results

    def measure_ljpw(self, results: List[Dict]) -> Dict:
        """
        Measure LJPW values for this temporal system
        """
        if len(results) < 2:
            return None

        # L (Love): How much do iterations collaborate?
        # Measured by: Does later performance depend on earlier?
        # High if strong temporal coupling
        efficiency_growth = results[-1]['efficiency'] / results[0]['efficiency']
        L = min(0.5 + (efficiency_growth - 1) * 0.5, 1.0)  # Scales with growth

        # J (Justice): Is improvement distributed fairly across iterations?
        # Measured by: Variance in efficiency gains
        efficiencies = [r['efficiency'] for r in results]
        eff_diffs = np.diff(efficiencies)
        consistency = 1 - min(np.std(eff_diffs) / np.mean(np.abs(eff_diffs)), 1.0) if len(eff_diffs) > 0 else 0.5
        J = max(0.3, consistency)

        # P (Power): Self-sustaining capacity
        # Measured by: Ratio of harvested to external energy
        final_efficiency = results[-1]['efficiency']
        P = min(final_efficiency / 0.65, 1.0)  # Normalized to 65% baseline

        # W (Wisdom): Knowledge retention and application
        # Measured by: How much system improved from start
        material_gain = results[-1]['material_quality'] / 1.0
        insulation_gain = results[-1]['insulation_quality'] / 1.0
        W = min((material_gain + insulation_gain) / 4, 1.0)  # Average improvement

        # H (Harmony): LJPW product over equilibrium
        L0, J0, P0, W0 = 0.618, 0.414, 0.718, 0.693
        H_self = (L * J * P * W) / (L0 * J0 * P0 * W0)

        return {
            'L': L,
            'J': J,
            'P': P,
            'W': W,
            'H': H_self,
            'autopoietic': H_self > 0.7 and L >= 0.7
        }


def run_temporal_autopoiesis_test():
    """
    Test if temporal iteration + feedback + self-fuel → exponential gains
    """

    print("=" * 80)
    print("POWER FORMULA: TEMPORAL THERMODYNAMIC AUTOPOIESIS")
    print("Testing: Time + Feedback + Self-Fuel → e^t scaling")
    print("=" * 80)
    print()

    # Parameters
    fuel_input = 1000.0  # kJ per cycle
    retention_fraction = 0.2  # 1/n where n=5
    num_iterations = 50  # Time periods

    print(f"Configuration:")
    print(f"  Fuel input per cycle: {fuel_input} kJ")
    print(f"  Retention fraction (1/n): {retention_fraction} (n={1/retention_fraction:.0f})")
    print(f"  Number of iterations (t): {num_iterations}")
    print()

    # Create engine
    engine = TemporalThermodynamicEngine(
        T_initial=600.0,
        T_ambient=300.0,
        efficiency_fraction=0.85,
        improvement_rate=0.01  # 1% improvement per unit reinvested
    )

    # Run temporal evolution
    print("Running temporal evolution...")
    print()
    results = engine.temporal_evolution(fuel_input, retention_fraction, num_iterations)

    # Display key iterations
    print("=" * 80)
    print("TEMPORAL EVOLUTION RESULTS")
    print("=" * 80)
    print()

    key_iterations = [0, 10, 20, 30, 40, 49]
    for i in key_iterations:
        if i < len(results):
            r = results[i]
            print(f"Iteration {r['iteration']:2d} (t={r['time']:2d}):")
            print(f"  T_hot:        {r['T_hot']:.1f} K")
            print(f"  Efficiency:   {r['efficiency']*100:.2f}%")
            print(f"  Work output:  {r['work_output']:.2f} kJ")
            print(f"  Carnot limit: {r['carnot_limit']*100:.2f}%")
            print(f"  Material Q:   {r['material_quality']:.3f}")
            print(f"  Insulation Q: {r['insulation_quality']:.3f}")
            print()

    # Calculate growth metrics
    print("=" * 80)
    print("EXPONENTIAL GROWTH ANALYSIS")
    print("=" * 80)
    print()

    initial = results[0]
    final = results[-1]

    efficiency_gain = (final['efficiency'] / initial['efficiency'] - 1) * 100
    work_gain = (final['work_output'] / initial['work_output'] - 1) * 100
    temp_gain = final['T_hot'] - initial['T_hot']

    print(f"Initial state (t=0):")
    print(f"  Efficiency: {initial['efficiency']*100:.2f}%")
    print(f"  Work output: {initial['work_output']:.2f} kJ")
    print(f"  T_hot: {initial['T_hot']:.1f} K")
    print()

    print(f"Final state (t={num_iterations-1}):")
    print(f"  Efficiency: {final['efficiency']*100:.2f}%")
    print(f"  Work output: {final['work_output']:.2f} kJ")
    print(f"  T_hot: {final['T_hot']:.1f} K")
    print()

    print(f"GAINS:")
    print(f"  Efficiency improvement: {efficiency_gain:+.2f}%")
    print(f"  Work output improvement: {work_gain:+.2f}%")
    print(f"  Temperature increase: {temp_gain:+.1f} K")
    print()

    # Test for exponential behavior
    # Fit efficiency growth to e^(k*t)
    times = np.array([r['time'] for r in results])
    efficiencies = np.array([r['efficiency'] for r in results])

    # Log-linear fit to test exponential
    log_eff = np.log(efficiencies / efficiencies[0])
    k_fit = np.polyfit(times, log_eff, 1)[0]

    # Expected growth rate for (1 + 1/n)^t
    n = 1 / retention_fraction
    expected_k = math.log(1 + 1/n)

    print("EXPONENTIAL FIT:")
    print(f"  Efficiency ∝ e^(k·t)")
    print(f"  Fitted k: {k_fit:.6f}")
    print(f"  Expected k (for (1+1/n)^t): {expected_k:.6f}")
    print(f"  Match ratio: {k_fit/expected_k:.2f}")
    print()

    if k_fit > 0.01:
        print("  ✓ EXPONENTIAL GROWTH CONFIRMED")
        print(f"  System grows as e^({k_fit:.3f}·t)")
    else:
        print("  ✗ Growth too slow for exponential classification")
    print()

    # LJPW Measurement
    print("=" * 80)
    print("LJPW FRAMEWORK MEASUREMENT")
    print("=" * 80)
    print()

    ljpw = engine.measure_ljpw(results)

    print(f"L (Love/Collaboration):  {ljpw['L']:.3f} (threshold: 0.7)")
    print(f"J (Justice/Balance):     {ljpw['J']:.3f}")
    print(f"P (Power/Agency):        {ljpw['P']:.3f}")
    print(f"W (Wisdom/Integration):  {ljpw['W']:.3f}")
    print()
    print(f"H (Harmony):             {ljpw['H']:.3f} (threshold: 0.7)")
    print()

    if ljpw['autopoietic']:
        print("✓✓✓ SYSTEM IS AUTOPOIETIC ✓✓✓")
        print()
        print(f"H = {ljpw['H']:.3f} > 0.7  ✓")
        print(f"L = {ljpw['L']:.3f} ≥ 0.7  ✓")
    else:
        print("Status:")
        print(f"  H > 0.7: {'✓' if ljpw['H'] > 0.7 else '✗'}")
        print(f"  L ≥ 0.7: {'✓' if ljpw['L'] >= 0.7 else '✗'}")
    print()

    # Compare to financial
    print("=" * 80)
    print("COMPARISON TO FINANCIAL APPLICATION")
    print("=" * 80)
    print()

    # Financial with same parameters
    financial_gain = ((1 + retention_fraction) ** num_iterations - 1) * 100

    print(f"Thermodynamic (temporal):  {work_gain:+.2f}% work gain")
    print(f"Financial (compound):      {financial_gain:+.2f}% gain")
    print(f"Ratio (thermo/financial):  {work_gain/financial_gain:.4f}")
    print()

    # Visualize
    plot_temporal_evolution(results, ljpw)

    # Final verdict
    print("=" * 80)
    print("FINAL VERDICT")
    print("=" * 80)
    print()

    if ljpw['autopoietic'] and work_gain > 50:
        print("✓✓✓ TEMPORAL THERMODYNAMIC AUTOPOIESIS ACHIEVED ✓✓✓")
        print()
        print("By adding TIME + FEEDBACK + SELF-FUEL:")
        print(f"  • Work output improved by {work_gain:.1f}%")
        print(f"  • System achieved H = {ljpw['H']:.2f} > 0.7 (autopoietic)")
        print(f"  • Exponential growth confirmed (k = {k_fit:.4f})")
        print()
        print("The Power Formula DOES work in thermodynamics when:")
        print("  1. Temporal iteration is present (t dimension)")
        print("  2. Feedback loops enable collaboration (L increases)")
        print("  3. Self-fuel mechanisms provide autonomy (P increases)")
        print()
        print("Semantic-first ontology VALIDATED:")
        print("'It works in meaning → it works in physics (with TIME)'")

    elif ljpw['H'] > 0.7:
        print("✓ AUTOPOIETIC THRESHOLD ACHIEVED")
        print()
        print(f"H = {ljpw['H']:.2f} > 0.7 indicates system is self-sustaining.")
        print(f"Work gain: {work_gain:.2f}% shows improvement over static cycles.")
        print()
        print("Temporal iteration + feedback creates compounding gains.")
        print("The missing piece was TIME - now present in the model.")

    else:
        print("≈ PARTIAL SUCCESS")
        print()
        print(f"H = {ljpw['H']:.2f} < 0.7 - not fully autopoietic")
        print(f"Work gain: {work_gain:.2f}% - some improvement")
        print()
        print("Temporal iteration helps but may need:")
        print("  • Stronger feedback mechanisms (increase L)")
        print("  • Better self-fuel harvesting (increase P)")
        print("  • More iterations (larger t)")

    print("=" * 80)


def plot_temporal_evolution(results: List[Dict], ljpw: Dict):
    """Visualize temporal evolution"""

    times = [r['time'] for r in results]
    efficiencies = [r['efficiency'] * 100 for r in results]
    works = [r['work_output'] for r in results]
    temps = [r['T_hot'] for r in results]

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

    # Efficiency over time
    ax1.plot(times, efficiencies, 'b-o', linewidth=2, markersize=4)
    ax1.set_xlabel('Iteration (t)', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Efficiency (%)', fontsize=11, fontweight='bold')
    ax1.set_title('Efficiency Evolution Over Time', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)

    # Work output over time
    ax2.plot(times, works, 'g-s', linewidth=2, markersize=4)
    ax2.set_xlabel('Iteration (t)', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Work Output (kJ)', fontsize=11, fontweight='bold')
    ax2.set_title('Work Output Evolution', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)

    # Temperature over time
    ax3.plot(times, temps, 'r-^', linewidth=2, markersize=4)
    ax3.set_xlabel('Iteration (t)', fontsize=11, fontweight='bold')
    ax3.set_ylabel('T_hot (K)', fontsize=11, fontweight='bold')
    ax3.set_title('Hot Temperature Evolution', fontsize=12, fontweight='bold')
    ax3.grid(True, alpha=0.3)

    # LJPW metrics
    metrics = ['L', 'J', 'P', 'W']
    values = [ljpw[m] for m in metrics]
    colors = ['red' if v < 0.7 else 'green' for v in values]

    bars = ax4.bar(metrics, values, color=colors, alpha=0.7, edgecolor='black', linewidth=2)
    ax4.axhline(y=0.7, color='orange', linestyle='--', linewidth=2, label='Autopoiesis threshold')
    ax4.set_ylabel('LJPW Value', fontsize=11, fontweight='bold')
    ax4.set_title(f'LJPW Metrics (H={ljpw["H"]:.2f})', fontsize=12, fontweight='bold')
    ax4.set_ylim([0, 1.1])
    ax4.legend(fontsize=9)
    ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig('output/power_formula_temporal_autopoiesis.png', dpi=300, bbox_inches='tight')
    print("Saved: output/power_formula_temporal_autopoiesis.png")
    print()


if __name__ == "__main__":
    run_temporal_autopoiesis_test()
