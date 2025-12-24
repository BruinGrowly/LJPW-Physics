#!/usr/bin/env python3
"""
POWER FORMULA SENSITIVITY ANALYSIS
Maybe the concept works but requires different parameters?

Testing:
1. Different pressure ratios (maybe 800x is too extreme?)
2. Different capture points (before full expansion?)
3. Different working fluids (maybe water isn't optimal?)
4. Multi-stage compression (reduces work requirement)
"""

import numpy as np
import matplotlib.pyplot as plt

GAMMA = 1.33
R = 0.4615  # kJ/(kg·K)

def compression_work(P_low, P_high, T_low, gamma=GAMMA, R_gas=R):
    """Calculate isentropic compression work"""
    ratio = (P_high / P_low) ** ((gamma - 1) / gamma)
    return (gamma / (gamma - 1)) * R_gas * T_low * (ratio - 1)

def energy_from_heat_recycling(T_final, T_initial, cp=2.0):
    """Energy saved by starting at higher temperature"""
    return cp * (T_final - T_initial)

def test_pressure_ratios():
    """Test if lower pressure ratios make MVR viable"""
    print("=" * 80)
    print("TEST 1: Varying Pressure Ratios")
    print("=" * 80)
    print()

    T_low = 320  # K
    pressure_ratios = [10, 20, 50, 100, 200, 500, 800]

    for ratio in pressure_ratios:
        P_low = 10  # kPa
        P_high = P_low * ratio

        W_compress = compression_work(P_low, P_high, T_low)
        T_compressed = T_low * (ratio ** ((GAMMA - 1) / GAMMA))
        energy_saved = energy_from_heat_recycling(T_compressed, T_low)

        net_gain = energy_saved - W_compress

        print(f"Pressure Ratio: {ratio}x")
        print(f"  Compression Work: {W_compress:.2f} kJ/kg")
        print(f"  Energy Saved:     {energy_saved:.2f} kJ/kg")
        print(f"  Net Gain:         {net_gain:+.2f} kJ/kg")
        print(f"  Status: {'✓ VIABLE' if net_gain > 0 else '✗ NOT VIABLE'}")
        print()

def test_multi_stage_compression():
    """Test if multi-stage compression with intercooling helps"""
    print("=" * 80)
    print("TEST 2: Multi-Stage Compression")
    print("=" * 80)
    print()

    P_low = 10  # kPa
    P_high = 8000  # kPa
    T_low = 320  # K

    # Single-stage
    W_single = compression_work(P_low, P_high, T_low)

    # Two-stage with intercooling (optimal intermediate pressure = sqrt(P_low * P_high))
    P_inter = np.sqrt(P_low * P_high)
    W_stage1 = compression_work(P_low, P_inter, T_low)
    # After intercooling, T returns to T_low
    W_stage2 = compression_work(P_inter, P_high, T_low)
    W_two_stage = W_stage1 + W_stage2

    # Three-stage
    P_inter1 = (P_low * P_high ** 2) ** (1/3)
    P_inter2 = (P_low ** 2 * P_high) ** (1/3)
    W_three_stage = (compression_work(P_low, P_inter1, T_low) +
                     compression_work(P_inter1, P_inter2, T_low) +
                     compression_work(P_inter2, P_high, T_low))

    print(f"Single-Stage:     {W_single:.2f} kJ/kg")
    print(f"Two-Stage:        {W_two_stage:.2f} kJ/kg (saves {W_single - W_two_stage:.2f})")
    print(f"Three-Stage:      {W_three_stage:.2f} kJ/kg (saves {W_single - W_three_stage:.2f})")
    print()

    # Does this make MVR viable?
    energy_saved = 2400  # Approximate from not heating liquid to vapor
    print(f"Energy Saved from Recycling: {energy_saved:.2f} kJ/kg")
    print(f"Best Compression Cost:       {W_three_stage:.2f} kJ/kg")
    print(f"Net Gain:                    {energy_saved - W_three_stage:+.2f} kJ/kg")
    print(f"Status: {'✓ VIABLE' if (energy_saved - W_three_stage) > 0 else '✗ STILL NOT VIABLE'}")
    print()

def test_partial_expansion():
    """Test capturing exhaust BEFORE full expansion"""
    print("=" * 80)
    print("TEST 3: Partial Expansion (Capture Before Full Exhaust)")
    print("=" * 80)
    print()

    P_high = 8000  # kPa
    T_high = 600   # K

    # Standard: expand all the way to 10 kPa
    P_exhaust_std = 10
    W_turbine_std = 600  # kJ/kg (from previous simulation)

    # Alternative: expand only to 100 kPa, capture there
    P_capture = 100  # kPa (10x higher than standard)

    # Work extracted is proportional to pressure ratio
    ratio_std = P_high / P_exhaust_std
    ratio_partial = P_high / P_capture

    W_turbine_partial = W_turbine_std * (np.log(ratio_partial) / np.log(ratio_std))

    # Now recompress from 100 kPa to 8000 kPa (80x instead of 800x)
    W_recompress = compression_work(P_capture, P_high, T_high * 0.6)

    print(f"Standard Expansion (to {P_exhaust_std} kPa):")
    print(f"  Turbine Work:   {W_turbine_std:.2f} kJ/kg")
    print(f"  Recompression:  {compression_work(P_exhaust_std, P_high, 320):.2f} kJ/kg")
    print()

    print(f"Partial Expansion (to {P_capture} kPa):")
    print(f"  Turbine Work:   {W_turbine_partial:.2f} kJ/kg")
    print(f"  Recompression:  {W_recompress:.2f} kJ/kg")
    print()

    # Trade-off: less turbine work, but cheaper recompression
    net_std = W_turbine_std  # No recycling
    net_partial = W_turbine_partial - W_recompress + (W_recompress * 0.5)  # Partial energy gain

    print(f"Net Work (Standard):        {net_std:.2f} kJ/kg")
    print(f"Net Work (Partial + MVR):   {net_partial:.2f} kJ/kg")
    print(f"Difference:                 {net_partial - net_std:+.2f} kJ/kg")
    print()

def the_fundamental_problem():
    """Explain why MVR likely can't work for primary power generation"""
    print("=" * 80)
    print("THE FUNDAMENTAL PROBLEM")
    print("=" * 80)
    print()
    print("Thermodynamic engines convert heat to work by exploiting")
    print("temperature DIFFERENCE (Carnot efficiency = 1 - T_cold/T_hot).")
    print()
    print("MVR tries to UNDO expansion (compress vapor back up),")
    print("but compression ALWAYS requires work ≈ what you got from expansion.")
    print()
    print("The energy saved (latent heat) < compression work required")
    print("because you're fighting entropy. The Second Law wins.")
    print()
    print("However, MVR DOES work in specific applications:")
    print("  - Desalination (reuse latent heat of evaporation)")
    print("  - Heat pumps (move heat, don't generate work)")
    print("  - Refrigeration cycles (different goal)")
    print()
    print("The Power Formula's (1 + 1/n)^n structure applies to:")
    print("  ✓ Finance (compound interest)")
    print("  ✓ Biology (cell division, growth)")
    print("  ✓ Learning (skill compounding)")
    print("  ✗ PRIMARY thermodynamic power generation")
    print()
    print("The 'retention and reinvestment' principle is SEMANTIC,")
    print("not a universal physical law. Thermodynamics has its own rules.")
    print("=" * 80)

if __name__ == "__main__":
    test_pressure_ratios()
    print("\n")
    test_multi_stage_compression()
    print("\n")
    test_partial_expansion()
    print("\n")
    the_fundamental_problem()
