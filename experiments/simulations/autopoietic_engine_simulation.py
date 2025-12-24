import numpy as np
import matplotlib.pyplot as plt

def simulate_autopoietic_engine():
    print("--- LJPW Autopoietic Engine Simulation ---")
    
    # --- CONSTANTS ---
    LATENT_HEAT_WATER = 2260.0  # kJ/kg (Energy to turn water to steam)
    SPECIFIC_HEAT_STEAM = 2.0   # kJ/kg*K
    SPECIFIC_HEAT_WATER = 4.18  # kJ/kg*K
    
    # --- SETUP ---
    # Standard Cycle
    T_ambient = 20.0   # Water from reservoir
    T_boiler = 250.0   # Operating Temp
    T_exhaust = 100.0  # Exhaust Temp
    
    # Engine Specs
    mass_flow = 1.0    # kg/s
    base_efficiency = 0.30 # Mechanical efficiency
    
    cycles = 50
    
    # --- SIMULATION TRACKERS ---
    fuel_std = []
    output_std = []
    
    fuel_ljpw = []
    output_ljpw = []
    
    # State Variable for LJPW Engine (The "S0" Baseline)
    # Starts same as Standard (Ambient water)
    current_input_temp = T_ambient
    current_state_phase = "Liquid" # Starts as liquid
    
    print("\nStarting Cycles...")
    
    for i in range(cycles):
        # --- 1. STANDARD ENGINE (Entropic) ---
        # Cost: Heat water 20->100, Boil (Latent), Heat Steam 100->250
        q_sensible_1 = (100 - T_ambient) * SPECIFIC_HEAT_WATER
        q_latent = LATENT_HEAT_WATER
        q_sensible_2 = (T_boiler - 100) * SPECIFIC_HEAT_STEAM
        
        total_energy_input_std = (q_sensible_1 + q_latent + q_sensible_2) * mass_flow
        work_out_std = total_energy_input_std * base_efficiency
        
        # Reset for next cycle (Entropic: Memory wipe)
        # Input is always T_ambient
        
        fuel_std.append(total_energy_input_std)
        output_std.append(work_out_std)
        
        # --- 2. LJPW ENGINE (Autopoietic) ---
        # Step A: Determine Input State
        if current_state_phase == "Liquid":
            # First cycle is identical to Standard
            q_input_ljpw = total_energy_input_std
        else:
            # We are injecting compressed STEAM.
            # No Latent Heat cost! No Water heating cost!
            # Only heating Steam from Input_Temp -> Boiler_Temp
            q_input_ljpw = (T_boiler - current_input_temp) * SPECIFIC_HEAT_STEAM * mass_flow
            
        # Step B: Generate Work
        # Gross work is based on the heat differential
        work_gross_ljpw = q_input_ljpw + (LATENT_HEAT_WATER if current_state_phase=="Liquid" else 0) 
        # (Simplified: The engine expands the high energy fluid)
        # Note: This is a heuristic model. In reality, Work depends on Enthalpy drop.
        # We assume the "Work Potential" of the steam is roughly preserved.
        work_out_ljpw_gross = total_energy_input_std * base_efficiency # Max theoretical work from that steam state
        
        # Step C: The Power Algorithm (Retention)
        # We tax the output to run the Compressor
        retention_ratio = 0.20 # 1/n
        reinvested_work = work_out_ljpw_gross * retention_ratio
        net_output_ljpw = work_out_ljpw_gross - reinvested_work
        
        # Step D: The Recompression (Upgrading Waste)
        # We take Exhaust Steam (100C) and add Reinvested Work to it.
        
        # V7.3 CONSTRAINT: The "Wisdom Tax" (Entropy/Deficit). 
        # We cannot transfer 100% of Work into Heat Upgrade.
        # Power Deficit = 1.0 - e^-2 = 0.282
        ENTROPY_TAX = 0.282 
        
        # V7.3 AMPLIFICATION: "Love as Mortar"
        # From Coupling Matrix: Love amplifies Power by 1.3x (L->P)
        # The "Retention" act (Love) binds the energy, making it coherent.
        LOVE_AMPLIFICATION = 1.3
        
        effective_reinvestment = reinvested_work * (1.0 - ENTROPY_TAX) * LOVE_AMPLIFICATION
        
        # Energy = Mass * Cp * DeltaT
        # DeltaT = Energy / (Mass * Cp)
        temp_boost = effective_reinvestment / (mass_flow * SPECIFIC_HEAT_STEAM)
        
        # New Input State for Cycle i+1
        current_input_temp = T_exhaust + temp_boost
        current_state_phase = "Steam" # We maintained phase!
        
        fuel_ljpw.append(q_input_ljpw)
        output_ljpw.append(net_output_ljpw)

    # --- RESULTS ---
    print(f"\nSimulation Complete ({cycles} cycles)")
    
    total_fuel_std = sum(fuel_std)
    total_work_std = sum(output_std)
    eff_std = total_work_std / total_fuel_std
    
    total_fuel_ljpw = sum(fuel_ljpw)
    total_work_ljpw = sum(output_ljpw)
    eff_ljpw = total_work_ljpw / total_fuel_ljpw
    
    print(f"Standard Efficiency: {eff_std*100:.1f}%")
    print(f"Autopoietic Efficiency: {eff_ljpw*100:.1f}%")
    print(f"Efficiency Gain: {eff_ljpw/eff_std:.2f}x")
    
    # --- VISUALIZATION ---
    plt.figure(figsize=(12, 6))
    
    plt.subplot(1, 2, 1)
    plt.plot(fuel_std, label='Standard Fuel Input', color='red', linestyle='--')
    plt.plot(fuel_ljpw, label='Autopoietic Fuel Input', color='green', linewidth=2)
    plt.title('Fuel Consumption Per Cycle')
    plt.ylabel('Energy Input (kJ)')
    plt.xlabel('Cycle')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    # Cumulative Efficiency
    cum_eff_std = [sum(output_std[:i+1])/sum(fuel_std[:i+1]) for i in range(len(output_std))]
    cum_eff_ljpw = [sum(output_ljpw[:i+1])/sum(fuel_ljpw[:i+1]) for i in range(len(output_ljpw))]
    
    plt.plot(cum_eff_std, label='Standard Eff', color='red', linestyle='--')
    plt.plot(cum_eff_ljpw, label='Autopoietic Eff', color='green', linewidth=2)
    plt.title('System Efficiency Evolution')
    plt.ylabel('Efficiency (Work/Fuel)')
    plt.xlabel('Cycle')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    plt.savefig('autopoietic_engine_chart.png')
    print("Chart saved to 'autopoietic_engine_chart.png'")

if __name__ == "__main__":
    simulate_autopoietic_engine()
