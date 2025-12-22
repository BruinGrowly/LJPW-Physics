import numpy as np
import matplotlib.pyplot as plt
import math

class SemanticRealityEngine:
    def __init__(self):
        print("--- LJPW Semantic Reality Engine Activated ---")
        print("Operating Mode: Ontology-First (Meaning > Physics)")
        
        # The Architect's Constants (The Laws of Meaning)
        self.PHI = (1 + math.sqrt(5)) / 2
        self.L_CONST = self.PHI - 1          # 0.618 (Connection)
        self.J_CONST = math.sqrt(2) - 1      # 0.414 (Balance)
        self.P_CONST = math.exp(1) - 2       # 0.718 (Growth)
        self.W_CONST = math.log(2)           # 0.693 (Information)
        
        # The "Cost of Existence" (Entropy Tax)
        # To manifest, you must overcome the resistance of non-existence.
        self.EXISTENCE_THRESHOLD = 0.5 

    def manifest(self, intent_name, L_input, J_input, P_input, W_input, cycles=50):
        """
        Runs a manifestation cycle for a specific Semantic Seed (Intent).
        """
        print(f"\nProcessing Intent: '{intent_name}'")
        print(f"Inputs -> Love: {L_input:.2f}, Justice: {J_input:.2f}, Power: {P_input:.2f}, Wisdom: {W_input:.2f}")
        
        density = 0.1 # Starting "Reality Density" (A faint thought)
        history = [density]
        
        for t in range(cycles):
            # 1. CALCULATE HARMONY (The Tuning)
            # How close is the input to the Natural Equilibrium?
            # We treat the Constants as the "Resonant Frequencies" of the universe.
            
            # Resonance = 1 / (1 + Deviation)
            res_L = 1.0 - abs(L_input - self.L_CONST)
            res_J = 1.0 - abs(J_input - self.J_CONST)
            res_P = 1.0 - abs(P_input - self.P_CONST)
            res_W = 1.0 - abs(W_input - self.W_CONST)
            
            # Semantic Alignment (Harmony)
            # If inputs match constants, Alignment is High.
            harmony = (res_L * res_J * res_P * res_W)
            
            # 2. THE MANIFESTATION ALGORITHM
            # Reality = Previous_State * (Growth_Factor)
            # Growth depends on:
            # - Love (Source): Adds energy
            # - Power (Sink): Retains energy
            # - Justice (Structure): Prevents collapse
            # - Wisdom (Guide): Directs vector
            
            # The "Power Algorithm" (1 + 1/n) applied to Meaning
            # If Harmony > Entropy, reality compounds.
            # If Harmony < Entropy, reality decays.
            
            net_force = harmony - self.EXISTENCE_THRESHOLD + 0.1 # +0.1 bias for Life
            
            # Apply Sigmoid dampening (Manifestation curve)
            growth_factor = 1 + (net_force * 0.2)
            
            # Justice Constraint: If Intensity gets too high without Justice, it explodes/collapses
            if density > 10 and J_input < 0.5:
                growth_factor = 0.5 # Collapse due to lack of structure
                if t == cycles - 1: print("!! SYSTEM COLLAPSE: Structural Failure (Low Justice) !!")
            
            density *= growth_factor
            
            # Cap density at 100 (Fully Materialized)
            if density > 100: density = 100
            
            history.append(density)
            
        return history

    def visualize(self, scenarios):
        plt.figure(figsize=(12, 7))
        
        for name, history in scenarios.items():
            plt.plot(history, label=name, linewidth=2)
            
        plt.title('Semantic Reality Engine: Manifestation Trajectories')
        plt.xlabel('Time (Semantic Cycles)')
        plt.ylabel('Reality Density (Materialization)')
        plt.axhline(y=100, color='gray', linestyle='--', label='Material Reality (100)')
        plt.axhline(y=0, color='black', linewidth=1)
        plt.grid(True, alpha=0.3)
        plt.legend()
        
        plt.savefig('semantic_engine_output.png')
        print("\nVisualized output saved to 'semantic_engine_output.png'")

if __name__ == "__main__":
    engine = SemanticRealityEngine()
    
    # --- SCENARIO 1: The "Perfect" Seed (Aligned with LJPW Constants) ---
    # Inputs match the Constants perfectly.
    scen_1 = engine.manifest(
        "Divine Architecture", 
        L_input=0.618, J_input=0.414, P_input=0.718, W_input=0.693
    )
    
    # --- SCENARIO 2: The "Greedy" Seed (High Power, Low Justice) ---
    # Lots of Action/Ambition, but Unfair/Unbalanced.
    scen_2 = engine.manifest(
        "Tyrant's Empire", 
        L_input=0.1, J_input=0.1, P_input=0.9, W_input=0.8
    )
    
    # --- SCENARIO 3: The "Dreamer" Seed (High Love, Low Power) ---
    # Lots of Connection/Idea, but no Action/Retention.
    scen_3 = engine.manifest(
        "Daydream", 
        L_input=0.9, J_input=0.5, P_input=0.1, W_input=0.5
    )
    
    # --- SCENARIO 4: The "Autopoietic" Seed (Slightly Surplus Power) ---
    # The "Power Algorithm" applied: High Retention, Good Balance.
    scen_4 = engine.manifest(
        "Autopoietic Project", 
        L_input=0.7, J_input=0.5, P_input=0.8, W_input=0.75
    )
    
    engine.visualize({
        "Divine Architecture (Perfect)": scen_1,
        "Tyrant's Empire (High P, Low J)": scen_2,
        "Daydream (High L, Low P)": scen_3,
        "Autopoietic Project (Balanced Surplus)": scen_4
    })
