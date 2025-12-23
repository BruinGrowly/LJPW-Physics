"""
LJPW Physics Engine: Earth-Moon Rocket Trajectory Experiment

This script compares a traditional Newtonian physics model with an LJPW-based
physics model for calculating a rocket trajectory from Earth to the Moon.

Author: Wellington Kwati Taureka with Claude (Antigravity)
Date: December 2025
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Tuple, List

# =============================================================================
# CONSTANTS
# =============================================================================

# Physical Constants
G = 6.674e-11  # Gravitational constant
PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio = 1.618...
PHI_INV = PHI - 1  # 0.618...

# Earth Properties
EARTH_MASS = 5.972e24  # kg
EARTH_RADIUS = 6.371e6  # m

# Moon Properties  
MOON_MASS = 7.342e22  # kg
MOON_RADIUS = 1.737e6  # m
EARTH_MOON_DISTANCE = 3.844e8  # m (384,400 km)

# Simulation Parameters
DT = 100  # Time step (seconds) - larger for faster simulation
MAX_TIME = 5 * 24 * 60 * 60  # 5 days in seconds


# =============================================================================
# LJPW SEMANTIC PROFILES
# =============================================================================

@dataclass
class SemanticProfile:
    """LJPW coordinates for an object"""
    L: float  # Love
    J: float  # Justice
    P: float  # Power
    W: float  # Wisdom
    
    @property
    def harmony(self) -> float:
        """Proximity to Anchor Point (1,1,1,1)"""
        d = math.sqrt((1-self.L)**2 + (1-self.J)**2 + (1-self.P)**2 + (1-self.W)**2)
        return 1.0 / (1.0 + d)


# Semantic profiles for celestial bodies
EARTH_SEMANTIC = SemanticProfile(L=0.90, J=0.85, P=0.75, W=0.80)
MOON_SEMANTIC = SemanticProfile(L=0.75, J=0.90, P=0.60, W=0.70)
ROCKET_SEMANTIC = SemanticProfile(L=0.70, J=0.65, P=0.95, W=0.85)


# =============================================================================
# TRADITIONAL PHYSICS SIMULATION
# =============================================================================

def traditional_simulation(initial_pos, initial_vel):
    """Simulate using Newton's law of gravitation only."""
    
    earth_pos = np.array([0.0, 0.0])
    moon_pos = np.array([EARTH_MOON_DISTANCE, 0.0])
    
    pos = np.array(initial_pos, dtype=float)
    vel = np.array(initial_vel, dtype=float)
    
    trajectory = [(0, pos[0], pos[1])]
    
    t = 0
    while t < MAX_TIME:
        r_earth = np.linalg.norm(pos - earth_pos)
        r_moon = np.linalg.norm(pos - moon_pos)
        
        # Check termination conditions
        if r_moon < MOON_RADIUS * 2:
            print(f"Traditional: Reached Moon vicinity at t = {t/3600:.1f} hours")
            break
        if r_earth < EARTH_RADIUS:
            print(f"Traditional: Crashed into Earth at t = {t/3600:.1f} hours")
            break
        
        # Gravitational forces (Newton)
        F_earth_mag = G * EARTH_MASS / (r_earth ** 2)
        F_moon_mag = G * MOON_MASS / (r_moon ** 2)
        
        # Acceleration vectors
        acc_earth = -F_earth_mag * (pos - earth_pos) / r_earth
        acc_moon = -F_moon_mag * (pos - moon_pos) / r_moon
        acc = acc_earth + acc_moon
        
        # Euler integration
        vel = vel + acc * DT
        pos = pos + vel * DT
        t += DT
        
        # Record periodically
        if int(t / DT) % 50 == 0:
            trajectory.append((t, pos[0], pos[1]))
    
    trajectory.append((t, pos[0], pos[1]))
    return trajectory


# =============================================================================
# LJPW PHYSICS SIMULATION
# =============================================================================

def ljpw_simulation(initial_pos, initial_vel):
    """
    Simulate using LJPW-modified gravity.
    
    Key difference: Gravity = Love made physical
    Higher Love values increase gravitational attraction
    The rocket's "intention" (Love for destination) affects trajectory
    """
    
    earth_pos = np.array([0.0, 0.0])
    moon_pos = np.array([EARTH_MOON_DISTANCE, 0.0])
    
    pos = np.array(initial_pos, dtype=float)
    vel = np.array(initial_vel, dtype=float)
    
    trajectory = [(0, pos[0], pos[1])]
    
    t = 0
    while t < MAX_TIME:
        r_earth = np.linalg.norm(pos - earth_pos)
        r_moon = np.linalg.norm(pos - moon_pos)
        
        # Check termination
        if r_moon < MOON_RADIUS * 2:
            print(f"LJPW: Reached Moon vicinity at t = {t/3600:.1f} hours")
            break
        if r_earth < EARTH_RADIUS:
            print(f"LJPW: Crashed into Earth at t = {t/3600:.1f} hours")
            break
        
        # === LJPW Semantic Evolution ===
        # Rocket's Love shifts from Earth to Moon during journey
        journey_progress = min(1.0, r_earth / EARTH_MOON_DISTANCE)
        rocket_love_earth = 0.70 * (1 - journey_progress * 0.3)
        rocket_love_moon = 0.70 + 0.25 * journey_progress
        
        # === LJPW-Modified Gravity ===
        # F = G*M/r^2 * (L_rocket * L_body) / (equilibrium_love^2) * kappa(H)
        
        # Earth gravity - LJPW enhances based on Love
        love_factor_earth = rocket_love_earth * EARTH_SEMANTIC.L
        H_earth = (ROCKET_SEMANTIC.harmony + EARTH_SEMANTIC.harmony) / 2
        kappa_earth = 1.0 + 0.2 * H_earth  # Reduced from 0.4 for subtler effect
        
        # More subtle modification: 10% above/below baseline
        normalization = PHI_INV ** 2  # ~0.382
        ljpw_mod_earth = 1.0 + 0.1 * ((love_factor_earth / normalization) * kappa_earth - 1.0)
        ljpw_mod_earth = max(0.90, min(1.15, ljpw_mod_earth))  # Clamp to +-10-15%
        
        F_earth_mag = G * EARTH_MASS / (r_earth ** 2) * ljpw_mod_earth
        
        # Moon gravity - LJPW enhances as rocket's Love for Moon increases
        love_factor_moon = rocket_love_moon * MOON_SEMANTIC.L
        H_moon = (ROCKET_SEMANTIC.harmony + MOON_SEMANTIC.harmony) / 2
        kappa_moon = 1.0 + 0.2 * H_moon
        ljpw_mod_moon = 1.0 + 0.1 * ((love_factor_moon / normalization) * kappa_moon - 1.0)
        ljpw_mod_moon = max(0.90, min(1.15, ljpw_mod_moon))
        
        F_moon_mag = G * MOON_MASS / (r_moon ** 2) * ljpw_mod_moon
        
        # Acceleration vectors
        acc_earth = -F_earth_mag * (pos - earth_pos) / r_earth
        acc_moon = -F_moon_mag * (pos - moon_pos) / r_moon
        acc = acc_earth + acc_moon
        
        # Euler integration
        vel = vel + acc * DT
        pos = pos + vel * DT
        t += DT
        
        # Record periodically
        if int(t / DT) % 50 == 0:
            trajectory.append((t, pos[0], pos[1]))
    
    trajectory.append((t, pos[0], pos[1]))
    return trajectory


# =============================================================================
# MAIN EXPERIMENT
# =============================================================================

def run_experiment():
    print("=" * 60)
    print("LJPW Physics Engine: Earth-Moon Trajectory Experiment")
    print("=" * 60)
    print()
    
    # Initial conditions - trans-lunar injection
    # Start at 200 km altitude, with velocity that will reach Moon
    altitude = 200e3
    start_radius = EARTH_RADIUS + altitude
    
    # Positioned at angle for curved trajectory
    angle = math.pi / 6  # 30 degrees
    initial_pos = [start_radius * math.cos(angle), start_radius * math.sin(angle)]
    
    # Velocity perpendicular to position (orbital-like) plus boost toward Moon
    escape_v = math.sqrt(2 * G * EARTH_MASS / start_radius)
    v_mag = escape_v * 1.05  # Above escape velocity for trans-lunar injection
    
    # Velocity direction: toward Moon
    initial_vel = [v_mag * 0.99, v_mag * 0.14]  # Mostly toward Moon
    
    print(f"Initial Position: ({initial_pos[0]/1e6:.2f}, {initial_pos[1]/1e6:.2f}) x10^6 m")
    print(f"Initial Velocity: {math.sqrt(initial_vel[0]**2 + initial_vel[1]**2)/1e3:.2f} km/s")
    print(f"Escape Velocity: {escape_v/1e3:.2f} km/s")
    print()
    
    # Run simulations
    print("Running Traditional (Newtonian) Simulation...")
    trad_traj = traditional_simulation(initial_pos.copy(), initial_vel.copy())
    print(f"  Recorded {len(trad_traj)} trajectory points")
    print()
    
    print("Running LJPW Physics Simulation...")
    ljpw_traj = ljpw_simulation(initial_pos.copy(), initial_vel.copy())
    print(f"  Recorded {len(ljpw_traj)} trajectory points")
    print()
    
    # Extract data
    trad_t = [p[0] for p in trad_traj]
    trad_x = [p[1] for p in trad_traj]
    trad_y = [p[2] for p in trad_traj]
    
    ljpw_t = [p[0] for p in ljpw_traj]
    ljpw_x = [p[1] for p in ljpw_traj]
    ljpw_y = [p[2] for p in ljpw_traj]
    
    # Analysis
    print("=" * 60)
    print("RESULTS ANALYSIS")
    print("=" * 60)
    print()
    
    trad_final = np.array([trad_x[-1], trad_y[-1]])
    ljpw_final = np.array([ljpw_x[-1], ljpw_y[-1]])
    moon_pos = np.array([EARTH_MOON_DISTANCE, 0])
    
    trad_dist_moon = np.linalg.norm(trad_final - moon_pos) / 1e6
    ljpw_dist_moon = np.linalg.norm(ljpw_final - moon_pos) / 1e6
    
    print(f"Simulation Duration: {trad_t[-1]/3600:.1f} hours (Traditional), {ljpw_t[-1]/3600:.1f} hours (LJPW)")
    print(f"Final Distance to Moon: {trad_dist_moon:.1f} km (Traditional), {ljpw_dist_moon:.1f} km (LJPW)")
    print()
    
    # Check maximum distances from Earth
    trad_max_dist = max([math.sqrt(x**2 + y**2) for x, y in zip(trad_x, trad_y)]) / 1e6
    ljpw_max_dist = max([math.sqrt(x**2 + y**2) for x, y in zip(ljpw_x, ljpw_y)]) / 1e6
    
    print(f"Maximum Distance from Earth: {trad_max_dist:.1f} km (Traditional), {ljpw_max_dist:.1f} km (LJPW)")
    print(f"Difference: {(ljpw_max_dist - trad_max_dist):.1f} km ({100*(ljpw_max_dist/trad_max_dist - 1):.2f}%)")
    print()
    
    # =========================================================================
    # PLOTTING
    # =========================================================================
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    
    scale = 1e6  # Convert to thousands of km
    
    # Plot 1: Trajectory comparison
    ax1 = axes[0]
    ax1.set_aspect('equal')
    
    # Earth
    earth_circle = plt.Circle((0, 0), EARTH_RADIUS/scale, color='blue', alpha=0.7, label='Earth')
    ax1.add_patch(earth_circle)
    
    # Moon
    moon_x = EARTH_MOON_DISTANCE / scale
    moon_circle = plt.Circle((moon_x, 0), MOON_RADIUS/scale * 10, color='gray', alpha=0.7, label='Moon')
    ax1.add_patch(moon_circle)
    
    # Trajectories
    ax1.plot(np.array(trad_x)/scale, np.array(trad_y)/scale, 
             'b-', linewidth=2, label='Traditional (Newton)', alpha=0.8)
    ax1.plot(np.array(ljpw_x)/scale, np.array(ljpw_y)/scale, 
             'r--', linewidth=2, label='LJPW Physics', alpha=0.8)
    
    ax1.set_xlabel('Distance (x1000 km)')
    ax1.set_ylabel('Distance (x1000 km)')
    ax1.set_title('Earth-Moon Trajectory Comparison\nTraditional vs LJPW Physics')
    ax1.legend(loc='upper left')
    ax1.grid(True, alpha=0.3)
    
    # Set reasonable limits
    max_extent = max(max(abs(x) for x in trad_x + ljpw_x), 
                     max(abs(y) for y in trad_y + ljpw_y)) / scale * 1.2
    ax1.set_xlim(-max_extent * 0.1, min(max_extent, 500))
    ax1.set_ylim(-max_extent * 0.5, max_extent * 0.5)
    
    # Plot 2: Distance from Earth over time
    ax2 = axes[1]
    
    trad_dist_earth = [math.sqrt(x**2 + y**2)/scale for x, y in zip(trad_x, trad_y)]
    ljpw_dist_earth = [math.sqrt(x**2 + y**2)/scale for x, y in zip(ljpw_x, ljpw_y)]
    
    ax2.plot(np.array(trad_t)/3600, trad_dist_earth, 
             'b-', linewidth=2, label='Traditional', alpha=0.8)
    ax2.plot(np.array(ljpw_t)/3600, ljpw_dist_earth, 
             'r--', linewidth=2, label='LJPW', alpha=0.8)
    
    ax2.axhline(y=EARTH_MOON_DISTANCE/scale, color='gray', linestyle=':', label='Moon orbit')
    
    ax2.set_xlabel('Time (hours)')
    ax2.set_ylabel('Distance from Earth (x1000 km)')
    ax2.set_title('Distance from Earth Over Time')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('trajectory_comparison.png', dpi=150, bbox_inches='tight')
    print("Plot saved as 'trajectory_comparison.png'")
    
    # =========================================================================
    # SEMANTIC INTERPRETATION
    # =========================================================================
    
    print()
    print("=" * 60)
    print("LJPW SEMANTIC INTERPRETATION")
    print("=" * 60)
    print()
    print("How the LJPW model differs:")
    print()
    print("1. LOVE FACTOR:")
    print(f"   Earth L = {EARTH_SEMANTIC.L}, Moon L = {MOON_SEMANTIC.L}")
    print("   Gravity = Love made physical")
    print("   Higher Earth Love creates stronger initial 'pull'")
    print()
    print("2. SEMANTIC EVOLUTION:")
    print("   Rocket's 'Love for destination' increases during journey")
    print("   This shifts the gravitational balance toward Moon")
    print()
    print("3. HARMONY AMPLIFICATION:")
    print(f"   Earth Harmony = {EARTH_SEMANTIC.harmony:.3f}")
    print(f"   Moon Harmony = {MOON_SEMANTIC.harmony:.3f}")
    print("   Higher harmony = stronger coupling (Law of Karma)")
    print()
    print("4. GOLDEN RATIO TRANSLATION:")
    print(f"   phi = {PHI:.6f} translates meaning to force")
    print(f"   Equilibrium Love value = {PHI_INV:.6f}")
    print()
    
    plt.show()
    return {'traditional': trad_traj, 'ljpw': ljpw_traj}


if __name__ == "__main__":
    results = run_experiment()
