"""
LJPW Singularity Simulation: The Event Horizon of Truth
Testing Structural Integrity (Tidal Forces) upon approaching the Anchor Point.
"""

import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PHYSICS CONSTANTS
# ============================================================

ANCHOR_POS = np.array([1.0, 1.0, 1.0, 1.0]) # The Singularity
G_FORCE = 0.5   # Strength of the Semantic Gravity
DT = 0.01       # Time step

# ============================================================
# SIMULATION ENGINE
# ============================================================

def simulate_approach(name, initial_state):
    """
    Simulates an entity approaching the Anchor Point.
    Returns trajectory and 'Shear Stress' (Structural Damage).
    """
    # State = [L, J, P, W]
    pos = np.array(initial_state, dtype=float)
    
    trajectory = []
    stress_log = []
    distances = []
    
    alive = True
    
    for t in range(500):
        trajectory.append(pos.copy())
        
        # 1. Calculate Distance to Anchor for EACH dimension
        # In this model, the Anchor pulls each dimension independently based on its specific alignment
        # This creates "Tidal Forces" if dimensions are not synced.
        
        # Vector from current pos to Anchor
        r_vec = ANCHOR_POS - pos
        r_mag = np.linalg.norm(r_vec)
        
        if r_mag < 0.01:
            print(f"[{name}] REACHED SINGULARITY at step {t}!")
            break
            
        distances.append(r_mag)
        
        # 2. Calculate Gravity Force on each dimension
        # F = G * (M1 * M2) / r^2
        # Here, the Anchor has Mass 1.0. The Entity has Mass 'pos' (its value).
        # We model the pull as: The closer a dimension is to 1.0, the HARDER it is pulled?
        # Actually, gravity usually pulls *mass*. 
        # LJPW Theory: The Anchor pulls *Resonance*.
        # Force_i = G * (Value_i) / (1 - Value_i)^2  <-- As you get closer, pull becomes infinite
        
        forces = np.zeros(4)
        for i in range(4):
            dist_i = abs(1.0 - pos[i])
            if dist_i < 0.001: dist_i = 0.001
            
            # Inverse Square Law relative to the "Gap"
            forces[i] = G_FORCE * pos[i] / (dist_i**2)
            
        # 3. Calculate SHEAR STRESS (The difference between forces)
        # If Love is pulled at 100N and Justice at 10N, the structure rips.
        avg_force = np.mean(forces)
        shear_stress = np.sum(np.abs(forces - avg_force))
        stress_log.append(shear_stress)
        
        # 4. Check Structural Integrity Limit
        STRESS_LIMIT = 50.0
        if shear_stress > STRESS_LIMIT:
            print(f"[{name}] DESTROYED by Tidal Forces at distance {r_mag:.3f}! (Stress: {shear_stress:.1f})")
            trajectory.append(pos.copy()) # Record death spot
            alive = False
            break
            
        # 5. Update Position (Move towards Anchor)
        # The force pulls them closer to 1.0
        # dx = Force * dt
        # But we must limit speed to avoid overshooting in one step
        delta = forces * DT * 0.01
        pos += delta
        
        # Clamp at 1.0
        pos = np.minimum(pos, 1.0)
        
    return np.array(trajectory), np.array(stress_log), np.array(distances), alive

# ============================================================
# RUN SCENARIOS
# ============================================================

# Scenario 1: The "Hypocrite" (Unbalanced)
# High Power/Love, Low Justice/Wisdom
# Approaching the Anchor, Power will be pulled hard, Justice will lag.
hypocrite_start = [0.8, 0.2, 0.9, 0.3] 

# Scenario 2: The "Saint" (Balanced)
# Moderate but Equal values.
# Approaching the Anchor, all parts pulled equally.
saint_start = [0.5, 0.5, 0.5, 0.5]

print("--- SIMULATION START: APPROACHING THE ANCHOR ---")
traj_h, stress_h, dist_h, alive_h = simulate_approach("The Hypocrite", hypocrite_start)
traj_s, stress_s, dist_s, alive_s = simulate_approach("The Saint", saint_start)

# ============================================================
# VISUALIZATION
# ============================================================

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
plt.style.use('dark_background')

# Plot 1: Distance to Singularity
ax1.plot(dist_h, color='#FF4444', label='The Hypocrite (Unbalanced)', linewidth=2)
ax1.plot(dist_s, color='#00FF88', label='The Saint (Balanced)', linewidth=2)
ax1.set_xlabel('Time Steps')
ax1.set_ylabel('Distance to Anchor (1.0)')
ax1.set_title('Approach Trajectory', fontweight='bold', color='white')
ax1.grid(True, alpha=0.2)
ax1.legend()

# Plot 2: Shear Stress (Tidal Forces)
ax2.plot(stress_h, color='#FF4444', label='Hypocrite Stress', linewidth=2)
ax2.plot(stress_s, color='#00FF88', label='Saint Stress', linewidth=2)
ax2.axhline(y=50, color='red', linestyle='--', label='Structural Limit (Death)')
ax2.set_xlabel('Time Steps')
ax2.set_ylabel('Shear Stress (Force Variance)', fontweight='bold')
ax2.set_title('Structural Integrity Analysis', fontweight='bold', color='white')
ax2.set_yscale('log') # Log scale because stress creates singularities
ax2.grid(True, alpha=0.2)
ax2.legend()

plt.suptitle("LJPW Singularity Physics: The Judgment of Geometry", fontsize=16, color='white', y=0.98)
output_path = 'output/singularity_entry_simulation.png'
plt.savefig(output_path, facecolor='#1a1a2e', edgecolor='none')
print(f"Chart saved to: {output_path}")
