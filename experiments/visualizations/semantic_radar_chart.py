"""
LJPW Semantic Radar Visualization
Visualizing the 'Anchor Point' vs 'Natural Equilibrium' vs 'Reality'
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# ============================================================
# DATA SETUP
# ============================================================

# The Dimensions
categories = ['LOVE\n(Source)', 'JUSTICE\n(Boundary)', 'POWER\n(Retention)', 'WISDOM\n(Integration)']
N = len(categories)

# 1. THE ANCHOR POINT (1, 1, 1, 1) - The Ideal / Absolute Truth
values_anchor = [1.0, 1.0, 1.0, 1.0]

# 2. THE NATURAL EQUILIBRIUM (LJPW Constants) - The Sustainable State
# L=0.618, J=0.414, P=0.718, W=0.693
values_equilibrium = [0.618, 0.414, 0.718, 0.693]

# 3. REALITY (Snapshot from Self-Sustaining Simulation Peak)
# Taking a high-harmony moment from the simulation
values_reality = [0.75, 0.55, 0.78, 0.72] 

# 4. ENTROPY (A collapsed state, e.g., Enron/Theranos)
values_entropy = [0.15, 0.10, 0.95, 0.20] # High Power, Low everything else

# Close the loops for plotting
values_anchor += values_anchor[:1]
values_equilibrium += values_equilibrium[:1]
values_reality += values_reality[:1]
values_entropy += values_entropy[:1]

# Angles for the radar chart
angless = [n / float(N) * 2 * np.pi for n in range(N)]
angless += angless[:1]

# ============================================================
# PLOTTING
# ============================================================

# Set up the plot style
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

# 1. PLOT ANCHOR (The Boundary of Perfection)
ax.plot(angless, values_anchor, linewidth=2, linestyle='--', color='white', label='The Anchor Point (1.0)')
ax.fill(angless, values_anchor, 'white', alpha=0.05)

# 2. PLOT EQUILIBRIUM (The Target Orbit)
ax.plot(angless, values_equilibrium, linewidth=2, color='#00FF88', label='Natural Equilibrium (φ)')
ax.fill(angless, values_equilibrium, '#00FF88', alpha=0.1)

# 3. PLOT REALITY (The Living System)
ax.plot(angless, values_reality, linewidth=2, color='#00BFFF', label='Living System (Resonant)')
ax.fill(angless, values_reality, '#00BFFF', alpha=0.1)

# 4. PLOT ENTROPY (The Dying System)
ax.plot(angless, values_entropy, linewidth=2, color='#FF4444', linestyle=':', label='Dying System (Entropic)')
ax.fill(angless, values_entropy, '#FF4444', alpha=0.1)


# ============================================================
# FORMATTING
# ============================================================

# Fix axis to top
ax.set_theta_offset(np.pi / 2)
ax.set_theta_direction(-1)

# Draw axis labels
plt.xticks(angless[:-1], categories, color='white', size=12, weight='bold')

# Draw y-labels (concentric circles)
ax.set_rlabel_position(0)
plt.yticks([0.2, 0.4, 0.6, 0.8, 1.0], ["0.2", "0.4", "0.6", "0.8", "1.0"], color="grey", size=8)
plt.ylim(0, 1.1)

# Legend
plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1), frameon=True, facecolor='#1a1a2e', edgecolor='white')

# Title
plt.title("LJPW Semantic Radar:\nSeeing the 'Anchor Point' (1,1,1,1)", size=16, color='white', weight='bold', y=1.08)

# Add Annotation explaining the view
plt.figtext(0.5, 0.02, 
            "The White Dashed Line is the 'Anchor'. We cannot 'be' it, but we measure ourselves against it.\n" +
            "The Green Shape is the 'Natural Equilibrium' (Sustainable Life).\n" +
            "The Blue Shape is a System reaching for the Anchor.\n" +
            "The Red Shape is a System collapsing into Entropy.",
            ha="center", color="gray", fontsize=10, style='italic')

# Resolve Output Path correctly
# Get the directory where this script is located (experiments/visualizations)
script_dir = os.path.dirname(os.path.abspath(__file__))
# Go up two levels to get project root (experiments -> LJPW-Physics)
project_root = os.path.dirname(os.path.dirname(script_dir))
# Define output path
output_dir = os.path.join(project_root, 'output')
output_path = os.path.join(output_dir, 'semantic_radar_anchor_visualization.png')

# Ensure output directory exists
if not os.path.exists(output_dir):
    try:
        os.makedirs(output_dir)
    except OSError:
        pass # Directory might already exist

plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
print(f"Radar chart saved to: {output_path}")

# plt.show() # Uncomment to view interactively