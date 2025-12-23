import numpy as np
import matplotlib.pyplot as plt
import math

class SemanticParticle:
    def __init__(self, name, x, y, vx, vy, L, J, P, W):
        self.name = name
        self.pos = np.array([float(x), float(y)])
        self.vel = np.array([float(vx), float(vy)])
        
        # Semantic Properties (The "Soul" of the particle)
        self.L = L # Love: Attractiveness (Gravitational Mass)
        self.J = J # Justice: Hardness (Collision Radius/Repulsion)
        self.P = P # Power: Inertia (Inertial Mass/Persistence)
        self.W = W # Wisdom: Interaction Range (Sensitivity)
        
        self.history_x = [self.pos[0]]
        self.history_y = [self.pos[1]]

class SemanticPhysicsSimulator:
    def __init__(self):
        print("--- Semantic Physics Engine: LJPW Interactions ---")
        # Universal Scaling Constants (tuning Meaning to Pixels)
        self.K_LOVE = 0.5  # Strength of Attraction
        self.K_TIME = 0.1  # Time step
        
    def update(self, particles, steps=1000):
        for t in range(steps):
            for i, p1 in enumerate(particles):
                force = np.array([0.0, 0.0])
                
                for j, p2 in enumerate(particles):
                    if i == j: continue
                    
                    # 1. CALCULATE VECTOR
                    r_vec = p2.pos - p1.pos
                    distance = np.linalg.norm(r_vec)
                    if distance < 0.1: distance = 0.1 # Prevent singularity
                    direction = r_vec / distance
                    
                    # 2. SEMANTIC FORCE CALCULATION (Not Newton's Law)
                    # Standard Physics: F = G * m1 * m2 / r^2
                    # LJPW Physics: Interaction = (Source1 * Source2) / Space
                    
                    # Love (L) determines the "Call" (Attraction)
                    attraction_strength = (p1.L * p2.L) 
                    
                    # Wisdom (W) determines the "Range" (Inverse Square Law emergence)
                    # If Wisdom is perfect (1.0), signal decays naturally (1/r^2).
                    # W acts as the "medium clarity".
                    decay = distance ** 2
                    
                    # Total Pull Vector
                    pull = direction * (self.K_LOVE * attraction_strength / decay)
                    
                    # Justice (J) determines "Repulsion" (Collision)
                    # If they get too close, Justice kicks in (Pauli Exclusion).
                    if distance < (p1.J + p2.J):
                        # Repulsion force (Elasticity)
                        push = -direction * ((p1.J + p2.J) - distance) * 2.0
                        force += push
                    else:
                        force += pull
                
                # 3. APPLY TO MOTION (Power)
                # Power (P) is Inertia.
                # High Power means "Hard to change state" (Mass).
                # Acceleration = Force / Power
                acceleration = force / p1.P 
                
                p1.vel += acceleration * self.K_TIME
                p1.pos += p1.vel * self.K_TIME
                
                p1.history_x.append(p1.pos[0])
                p1.history_y.append(p1.pos[1])
                
    def visualize(self, particles):
        plt.figure(figsize=(8, 8))
        
        for p in particles:
            plt.plot(p.history_x, p.history_y, label=f"{p.name} (P={p.P}, L={p.L})")
            # Mark end position
            plt.scatter([p.pos[0]], [p.pos[1]])
            
        plt.title('Semantic Physics: Orbits from Meaning')
        plt.xlabel('Space X')
        plt.ylabel('Space Y')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.axis('equal')
        
        plt.savefig('semantic_orbit_output.png')
        print("Visualized output saved to 'semantic_orbit_output.png'")

if __name__ == "__main__":
    sim = SemanticPhysicsSimulator()
    
    # --- SETUP: A Solar System ---
    # The Sun: High Love (Attractor), High Power (Massive), Static
    sun = SemanticParticle(
        name="Sun (Source)", 
        x=0, y=0, vx=0, vy=0, 
        L=10.0, J=1.0, P=100.0, W=1.0
    )
    
    # The Planet: Moderate Power (Inertia), Moderate Love
    # We give it velocity (Action) perpendicular to the Sun.
    planet = SemanticParticle(
        name="Earth (Seeker)", 
        x=10, y=0, vx=0, vy=0.7, 
        L=1.0, J=0.2, P=1.0, W=1.0
    )
    
    # A Comet: Low Power (Light), High Velocity
    comet = SemanticParticle(
        name="Comet (Visitor)", 
        x=-12, y=5, vx=0.2, vy=-0.8, 
        L=0.1, J=0.1, P=0.1, W=1.0
    )
    
    sim.update([sun, planet, comet], steps=3000)
    sim.visualize([sun, planet, comet])
