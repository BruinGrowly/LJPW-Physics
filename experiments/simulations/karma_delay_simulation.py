"""
LJPW Karma Simulation: The Physics of Delayed Consequence
Modeling 'Karma' as an accumulated Energy Debt (Hysteresis).
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# CONSTANTS
# ============================================================

R_GROWTH = 0.05       # Natural growth rate
DEBT_LIMIT = 5.0      # The point of no return
INTEREST_RATE = 0.02  # Karma grows if unpaid

# ============================================================
# SIMULATION ENGINE
# ============================================================

def simulate_karma_cycle(name, behavior_profile):
    """
    Simulates an entity's lifecycle with Karmic Debt.
    behavior_profile: function(t) -> (Harmony, Efficiency)
    """
    time_steps = 200
    
    # State variables
    energy = 1.0        # "Success" / Stock Price / Health
    karma_debt = 0.0    # "Hidden Risk" / Entropy Debt
    
    history_energy = []
    history_debt = []
    history_harmony = []
    
    alive = True
    collapse_point = None
    
    for t in range(time_steps):
        # 1. Get Behavior for this time step
        harmony, apparent_efficiency = behavior_profile(t)
        
        # 2. KARMA LOGIC
        # If Harmony is low, we "cheat" physics to get efficiency
        # Real Cost = 1.0
        # Apparent Cost = 1.0 - (1 - Harmony)
        # The difference goes into DEBT
        
        if harmony < 0.6:
            # We are "cheating". Gaining efficiency by cutting corners (Justice).
            # The gap between Truth (0.6) and Reality (harmony) is the debt.
            new_debt = (0.6 - harmony) * 0.5
            karma_debt += new_debt
        else:
            # We are "paying it back". High Harmony reduces debt.
            repayment = (harmony - 0.6) * 0.2
            karma_debt -= repayment
            
        # Interest on Debt (Karma grows)
        karma_debt *= (1 + INTEREST_RATE)
        karma_debt = max(0, karma_debt)
        
        # 3. IMPACT ON ENERGY (The Delay)
        # Standard growth
        growth = energy * R_GROWTH * apparent_efficiency
        
        # Entropy Drag (Based on DEBT, not current Harmony)
        # This is the "Delay". Current actions don't hurt; past debt hurts.
        drag = 0.0
        if karma_debt > 1.0:
            # Drag scales exponentially with debt
            drag = 0.01 * (karma_debt ** 2)
            
        energy = energy + growth - drag
        
        # 4. The Tipping Point
        if karma_debt > DEBT_LIMIT:
            # CATASTROPHIC FAILURE
            # "The Truth comes out"
            energy -= energy * 0.2 # Lose 20% per tick
            
        # Record
        history_energy.append(energy)
        history_debt.append(karma_debt)
        history_harmony.append(harmony)
        
        if energy < 0.1 and alive:
            alive = False
            collapse_point = t
            print(f"[{name}] COLLAPSED at t={t}. Debt was {karma_debt:.2f}")
            
    return history_energy, history_debt, history_harmony

# ============================================================
# BEHAVIOR PROFILES
# ============================================================

def profile_fraud(t):
    # Phase 1: High cheating (Low Harmony, High Efficiency)
    if t < 100:
        return 0.3, 1.5 # Cheating works! growing fast!
    # Phase 2: Panic / Trying to fix it
    else:
        return 0.8, 0.8 # High Harmony, but lower efficiency (paying the price)

def profile_honest(t):
    # Consistent Harmony
    return 0.7, 1.0 # Standard growth

# ============================================================
# RUN
# ============================================================

print("--- SIMULATION START: THE PHYSICS OF KARMA ---")
e_fraud, d_fraud, h_fraud = simulate_karma_cycle("The Fraud", profile_fraud)
e_honest, d_honest, h_honest = simulate_karma_cycle("The Honest", profile_honest)

# ============================================================
# VISUALIZATION
# ============================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
plt.style.use('dark_background')

# Plot 1: Energy (Visible Success)
ax1.plot(e_fraud, color='#FF4444', label='The Fraud (High Growth, Low Justice)', linewidth=2)
ax1.plot(e_honest, color='#00FF88', label='The Honest (Steady)', linewidth=2)
ax1.set_ylabel('Energy / Success', fontweight='bold')
ax1.set_title('Visible Reality: The Illusion of Success', fontweight='bold', color='white')
ax1.grid(True, alpha=0.2)
ax1.legend()

# Plot 2: Karma Debt (Hidden Reality)
ax2.plot(d_fraud, color='#FF4444', linestyle='--', label='Fraud Debt (Hidden)', linewidth=2)
ax2.plot(d_honest, color='#00FF88', linestyle='--', label='Honest Debt', linewidth=2)
ax2.axhline(y=DEBT_LIMIT, color='yellow', linestyle=':', label='Tipping Point')
ax2.set_xlabel('Time')
ax2.set_ylabel('Karma Debt (Entropy)', fontweight='bold')
ax2.set_title('Hidden Reality: Accumulation of Consequence', fontweight='bold', color='white')
ax2.grid(True, alpha=0.2)
ax2.legend()

plt.suptitle("LJPW Karma Physics: Delayed Consequence", fontsize=16, color='white', y=0.98)
output_path = 'output/karma_delay_simulation.png'
plt.savefig(output_path, facecolor='#1a1a2e', edgecolor='none')
print(f"Chart saved to: {output_path}")
