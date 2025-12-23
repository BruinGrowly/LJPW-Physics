"""
LJPW Semantic Gravity Simulation
The Physics of Relationships: Interaction between Two Bodies
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Set style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'

# ============================================================ 
# PHYSICS CONSTANTS
# ============================================================ 

G_LOVE = 1.0     # The Universal Constant of Connection (Attraction)
K_JUSTICE = 0.5  # The Universal Constant of Boundaries (Repulsion)
DAMPING = 0.1    # Friction of the medium

# ============================================================ 
# CLASSES
# ============================================================ 

class SemanticBody:
    def __init__(self, name, x, y, vx, vy, L, J, P, W, color):
        self.name = name
        self.pos = np.array([x, y], dtype=float)
        self.vel = np.array([vx, vy], dtype=float)
        self.color = color
        
        # Internal LJPW State (Fixed for this simplified gravity test)
        self.L = L  # Determines Attraction Strength
        self.J = J  # Determines Boundary Strength
        self.P = P  # Determines Mass/Inertia
        self.W = W  # Determines Efficiency
        
        # Mass is proportional to Power
        self.mass = P

def calculate_derivatives(state, t, bodies):
    """
    Calculates accelerations for N bodies interacting via Semantic Gravity.
    State vector: [x1, y1, vx1, vy1, x2, y2, vx2, vy2, ...]
    """
    n_bodies = len(bodies)
    derivs = np.zeros_like(state)
    
    # Unpack state
    positions = state[0::4]  # x for all bodies
    velocities = state[2::4] # vx for all bodies
    
    # Reshape for easier indexing (N x 2)
    pos_matrix = np.zeros((n_bodies, 2))
    vel_matrix = np.zeros((n_bodies, 2))
    
    for i in range(n_bodies):
        pos_matrix[i] = [state[4*i], state[4*i+1]]
        vel_matrix[i] = [state[4*i+2], state[4*i+3]]
    
    # Calculate forces
    forces = np.zeros((n_bodies, 2))
    
    for i in range(n_bodies):
        for j in range(i + 1, n_bodies):
            # Distance vector
            r_vec = pos_matrix[j] - pos_matrix[i]
            r_mag = np.linalg.norm(r_vec)
            r_dir = r_vec / r_mag
            
            body_i = bodies[i]
            body_j = bodies[j]
            
            # --- THE SEMANTIC FORCE LAWS ---
            
            # 1. LOVE (Attraction): Inverse Square Law
            # Stronger Love = Stronger Pull
            f_love_mag = G_LOVE * (body_i.L * body_j.L) * (body_i.P * body_j.P) / (r_mag**2)
            
            # 2. JUSTICE (Boundaries): Short-range Repulsion
            # Repulsion kicks in if they get too close.
            # High Justice = Stronger Boundaries (harder to crash/merge)
            # Low Justice = Weak Boundaries (codependency/crash)
            # We model this as a Lennard-Jones style repulsion term (1/r^4 for sharp boundary)
            f_justice_mag = K_JUSTICE * (body_i.J * body_j.J) / (r_mag**4)
            
            # Net Force Magnitude (Attraction - Repulsion)
            f_net_mag = f_love_mag - f_justice_mag
            
            # Apply forces (Newton's 3rd Law)
            force_on_i = f_net_mag * r_dir
            forces[i] += force_on_i
            forces[j] -= force_on_i
            
    # Calculate derivatives
    for i in range(n_bodies):
        # F = ma -> a = F/m
        acc = forces[i] / bodies[i].mass
        
        # Apply Medium Damping (Friction)
        acc -= DAMPING * vel_matrix[i]
        
        # Update derivatives array
        derivs[4*i]   = vel_matrix[i][0] # dx/dt = vx
        derivs[4*i+1] = vel_matrix[i][1] # dy/dt = vy
        derivs[4*i+2] = acc[0]           # dvx/dt = ax
        derivs[4*i+3] = acc[1]           # dvy/dt = ay
        
    return derivs

def run_scenario(name, body1, body2, duration=20):
    print(f"Running Scenario: {name}...")
    t = np.linspace(0, duration, 1000)
    
    # Initial state vector
    state0 = np.concatenate([
        [body1.pos[0], body1.pos[1], body1.vel[0], body1.vel[1]],
        [body2.pos[0], body2.pos[1], body2.vel[0], body2.vel[1]]
    ])
    
    bodies = [body1, body2]
    
    # Integrate
    solution = odeint(calculate_derivatives, state0, t, args=(bodies,))
    
    return t, solution, bodies

# ============================================================ 
# SCENARIOS
# ============================================================ 

# Scenario 1: The "Power Couple" (High Love, High Justice)
# They should form a stable orbit with healthy distance.
couple_A = SemanticBody("Partner A", -2, 0, 0, 0.5, L=0.9, J=0.9, P=1.0, W=0.9, color='#00FF88')
couple_B = SemanticBody("Partner B", 2, 0, 0, -0.5, L=0.9, J=0.9, P=1.0, W=0.9, color='#00BFFF')

# Scenario 2: The "Parasitic Drain" (High Love, Low Justice)
# High Attraction but weak boundaries. They should spiral in and crash (Codependency).
parasite_A = SemanticBody("Victim", -2, 0, 0, 0.3, L=0.9, J=0.2, P=1.0, W=0.5, color='#00FF88')
parasite_B = SemanticBody("Leech", 2, 0, 0, -0.3, L=0.9, J=0.1, P=0.5, W=0.2, color='#FF4444')

# Scenario 3: The "Broken System" (Low Love, High Justice)
# Weak attraction, strong walls. They should drift apart (Isolation).
broken_A = SemanticBody("Loner A", -2, 0, 0, 0.1, L=0.1, J=0.9, P=1.0, W=0.5, color='#AAAAAA')
broken_B = SemanticBody("Loner B", 2, 0, 0, -0.1, L=0.1, J=0.9, P=1.0, W=0.5, color='#888888')

# Run Simulations
t1, sol1, bodies1 = run_scenario("The Power Couple", couple_A, couple_B)
t2, sol2, bodies2 = run_scenario("The Parasitic Crash", parasite_A, parasite_B)
t3, sol3, bodies3 = run_scenario("The Drift", broken_A, broken_B)

# ============================================================ 
# VISUALIZATION
# ============================================================ 

fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('Semantic Gravity: The Physics of Relationship', fontsize=16, fontweight='bold', color='white')

scenarios = [
    (sol1, bodies1, "1. The Power Couple (High L, High J)\nStable Orbit / Healthy Boundaries"),
    (sol2, bodies2, "2. The Parasitic Crash (High L, Low J)\nCodependency / Merger"),
    (sol3, bodies3, "3. The Drift (Low L, High J)\nIsolation / No Connection")
]

for ax, (sol, bodies, title) in zip(axes, scenarios):
    # Extract positions
    x1, y1 = sol[:, 0], sol[:, 1]
    x2, y2 = sol[:, 4], sol[:, 5]
    
    # Plot trajectories
    ax.plot(x1, y1, color=bodies[0].color, label=bodies[0].name, linewidth=1.5, alpha=0.8)
    ax.plot(x2, y2, color=bodies[1].color, label=bodies[1].name, linewidth=1.5, alpha=0.8)
    
    # Plot start/end points
    ax.scatter([x1[0], x2[0]], [y1[0], y2[0]], color='white', s=50, marker='o', label='Start')
    ax.scatter([x1[-1], x2[-1]], [y1[-1], y2[-1]], color='white', s=100, marker='*', label='End')
    
    # Styling
    ax.set_title(title, fontweight='bold', pad=10)
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.grid(True, alpha=0.2)
    ax.legend()
    ax.set_aspect('equal')

plt.tight_layout()
output_path = 'output/semantic_gravity_simulation.png'
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none')
print(f"Simulation saved to: {output_path}")

# Check for Crashes (Distance < 0.2)
dist2 = np.sqrt((sol2[:, 0] - sol2[:, 4])**2 + (sol2[:, 1] - sol2[:, 5])**2)
min_dist2 = np.min(dist2)
if min_dist2 < 0.5:
    print(f"\nANALYSIS: Scenario 2 resulted in a CRASH (Min Distance: {min_dist2:.2f})")
    print("Reason: High Love created attraction, but Low Justice failed to provide a boundary.")
else:
    print(f"\nANALYSIS: Scenario 2 maintained distance (Min: {min_dist2:.2f})")
