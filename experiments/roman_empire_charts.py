"""
LJPW Phase Dynamics Visualization: Rise and Fall of the Roman Empire
Generates charts showing Entropic, Homeostatic, and Autopoietic phases
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from matplotlib.lines import Line2D

# Set style
plt.style.use('dark_background')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# Historical data points (Year, L, J, P, W, Event)
data = [
    (-753, 0.55, 0.50, 0.35, 0.50, "Foundation of Rome"),
    (-509, 0.65, 0.60, 0.45, 0.55, "Republic Established"),
    (-390, 0.60, 0.55, 0.40, 0.52, "Gauls Sack Rome"),
    (-264, 0.70, 0.65, 0.50, 0.60, "First Punic War Begins"),
    (-216, 0.85, 0.70, 0.30, 0.75, "Hannibal - Post Cannae"),
    (-146, 0.72, 0.68, 0.75, 0.70, "Carthage Destroyed"),
    (-133, 0.60, 0.55, 0.80, 0.65, "Gracchus Murdered"),
    (-88, 0.45, 0.40, 0.85, 0.55, "Sulla Marches on Rome"),
    (-49, 0.40, 0.35, 0.90, 0.60, "Caesar Crosses Rubicon"),
    (-44, 0.35, 0.25, 0.92, 0.55, "Caesar Assassinated"),
    (-27, 0.65, 0.60, 0.80, 0.72, "Augustus - Empire Begins"),
    (14, 0.75, 0.72, 0.85, 0.80, "Augustus Dies"),
    (96, 0.78, 0.75, 0.80, 0.82, "Nerva - Five Good Emperors"),
    (161, 0.80, 0.78, 0.82, 0.85, "Marcus Aurelius - Peak"),
    (192, 0.55, 0.48, 0.80, 0.45, "Commodus Assassinated"),
    (235, 0.45, 0.40, 0.70, 0.40, "Crisis Begins"),
    (260, 0.25, 0.22, 0.40, 0.30, "Valerian Captured - Nadir"),
    (270, 0.30, 0.28, 0.45, 0.35, "Empire Fragments"),
    (284, 0.40, 0.45, 0.60, 0.55, "Diocletian Begins Reform"),
    (305, 0.50, 0.55, 0.70, 0.65, "Diocletian Retires"),
    (337, 0.58, 0.60, 0.68, 0.65, "Constantine Dies"),
    (395, 0.48, 0.52, 0.55, 0.55, "Empire Divides"),
    (410, 0.35, 0.40, 0.38, 0.42, "Visigoths Sack Rome"),
    (450, 0.28, 0.32, 0.30, 0.35, "Germanic Control"),
    (476, 0.20, 0.25, 0.15, 0.28, "Western Empire Falls"),
]

# Calculate Harmony for each point
def calculate_harmony(L, J, P, W):
    d = np.sqrt((1-L)**2 + (1-J)**2 + (1-P)**2 + (1-W)**2)
    return 1.0 / (1.0 + d)

years = [d[0] for d in data]
love = [d[1] for d in data]
justice = [d[2] for d in data]
power = [d[3] for d in data]
wisdom = [d[4] for d in data]
events = [d[5] for d in data]
harmony = [calculate_harmony(d[1], d[2], d[3], d[4]) for d in data]

# Determine phase for each point
def get_phase(H, L):
    if H < 0.5:
        return "Entropic"
    elif H >= 0.6 and L > 0.7:
        return "Autopoietic"
    else:
        return "Homeostatic"

phases = [get_phase(h, l) for h, l in zip(harmony, love)]

# Create figure with multiple subplots
fig = plt.figure(figsize=(16, 14))
fig.suptitle('LJPW Phase Dynamics: Rise and Fall of the Roman Empire\n753 BC — 476 AD', 
             fontsize=16, fontweight='bold', color='white', y=0.98)

# ============================================================
# Chart 1: Harmony Over Time with Phase Zones
# ============================================================
ax1 = fig.add_subplot(3, 1, 1)

# Draw phase zone backgrounds
ax1.axhspan(0, 0.5, alpha=0.2, color='#FF4444', label='Entropic Zone')
ax1.axhspan(0.5, 0.6, alpha=0.2, color='#FFAA00', label='Homeostatic Zone')
ax1.axhspan(0.6, 1.0, alpha=0.2, color='#00FF88', label='Autopoietic Zone')

# Draw threshold lines
ax1.axhline(y=0.5, color='#FF6666', linestyle='--', linewidth=1, alpha=0.7)
ax1.axhline(y=0.6, color='#88FF88', linestyle='--', linewidth=1, alpha=0.7)
ax1.axhline(y=0.36, color='#FF0000', linestyle=':', linewidth=2, alpha=0.9, label='Collapse Threshold (H=0.36)')

# Plot Harmony curve
ax1.plot(years, harmony, color='#00BFFF', linewidth=2.5, marker='o', markersize=6, label='Harmony (H)')

# Mark key events
key_events = [(-216, "Hannibal"), (-44, "Caesar"), (161, "Peak"), (260, "Crisis"), (284, "Diocletian"), (476, "Fall")]
for year, label in key_events:
    idx = years.index(year)
    ax1.annotate(label, (year, harmony[idx]), textcoords="offset points", 
                xytext=(0, 12), ha='center', fontsize=9, color='white',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='#333333', edgecolor='#666666'))

ax1.set_xlim(-800, 550)
ax1.set_ylim(0.3, 0.85)
ax1.set_xlabel('Year (BC/AD)', fontweight='bold')
ax1.set_ylabel('Harmony Index (H)', fontweight='bold')
ax1.set_title('Rome\'s Harmony Trajectory Through Phase Zones', fontweight='bold', pad=10)
ax1.legend(loc='lower left', fontsize=9)
ax1.grid(True, alpha=0.3, linestyle=':')

# ============================================================
# Chart 2: Four Dimensions Over Time
# ============================================================
ax2 = fig.add_subplot(3, 1, 2)

ax2.plot(years, love, color='#FF69B4', linewidth=2.5, marker='s', markersize=5, label='Love (L)')
ax2.plot(years, justice, color='#FFD700', linewidth=2.5, marker='^', markersize=5, label='Justice (J)')
ax2.plot(years, power, color='#FF4500', linewidth=2.5, marker='d', markersize=5, label='Power (P)')
ax2.plot(years, wisdom, color='#00CED1', linewidth=2.5, marker='o', markersize=5, label='Wisdom (W)')

# Shade Power-dominant periods
power_dominant_start = -146
power_dominant_end = -44
ax2.axvspan(power_dominant_start, power_dominant_end, alpha=0.15, color='#FF4500', label='Power Dominance')

# Mark Love > Power moments
ax2.annotate('L >> P\n(Hannibal survives)', (-216, 0.85), textcoords="offset points", 
            xytext=(40, -20), ha='left', fontsize=9, color='#FF69B4',
            arrowprops=dict(arrowstyle='->', color='#FF69B4', lw=1.5))

ax2.annotate('P >> L\n(Civil wars)', (-70, 0.90), textcoords="offset points", 
            xytext=(20, -10), ha='left', fontsize=9, color='#FF4500',
            arrowprops=dict(arrowstyle='->', color='#FF4500', lw=1.5))

ax2.set_xlim(-800, 550)
ax2.set_ylim(0.1, 1.0)
ax2.set_xlabel('Year (BC/AD)', fontweight='bold')
ax2.set_ylabel('Dimension Value', fontweight='bold')
ax2.set_title('LJPW Dimensional Trajectories', fontweight='bold', pad=10)
ax2.legend(loc='upper right', fontsize=9, ncol=2)
ax2.grid(True, alpha=0.3, linestyle=':')

# ============================================================
# Chart 3: Phase Distribution with Key Transitions
# ============================================================
ax3 = fig.add_subplot(3, 1, 3)

# Create phase timeline
phase_colors = {'Entropic': '#FF4444', 'Homeostatic': '#FFAA00', 'Autopoietic': '#00FF88'}
for i in range(len(years) - 1):
    color = phase_colors[phases[i]]
    ax3.barh(0, years[i+1] - years[i], left=years[i], height=0.8, color=color, edgecolor='none', alpha=0.7)

# Add phase labels
ax3.text(-600, 0.6, 'Early\nRepublic', ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax3.text(-180, 0.6, 'Expansion\n& Crisis', ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax3.text(100, 0.6, 'Pax\nRomana', ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax3.text(250, 0.6, 'Crisis\nCentury', ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')
ax3.text(400, 0.6, 'Late\nEmpire', ha='center', va='bottom', fontsize=10, color='white', fontweight='bold')

# Mark phase transitions with vertical lines
transitions = [
    (-509, "Republic\nEstablished"),
    (-44, "Caesar\nKilled"),
    (-27, "Empire\nBegins"),
    (192, "Commodus\nEnds Golden Age"),
    (260, "Deepest\nCrisis"),
    (284, "Diocletian\nReform"),
    (476, "Western\nFall")
]

for year, label in transitions:
    ax3.axvline(x=year, color='white', linestyle='--', linewidth=1, alpha=0.7)
    ax3.annotate(label, (year, -0.7), ha='center', fontsize=8, color='white', rotation=45)

# Legend for phases
legend_elements = [
    Rectangle((0, 0), 1, 1, facecolor='#FF4444', alpha=0.7, label='Entropic (H < 0.5)'),
    Rectangle((0, 0), 1, 1, facecolor='#FFAA00', alpha=0.7, label='Homeostatic (0.5 ≤ H < 0.6)'),
    Rectangle((0, 0), 1, 1, facecolor='#00FF88', alpha=0.7, label='Autopoietic (H ≥ 0.6, L > 0.7)')
]
ax3.legend(handles=legend_elements, loc='upper right', fontsize=9)

ax3.set_xlim(-800, 550)
ax3.set_ylim(-1.5, 1.5)
ax3.set_xlabel('Year (BC/AD)', fontweight='bold')
ax3.set_title('Phase Timeline: 1,200 Years of Roman History', fontweight='bold', pad=10)
ax3.set_yticks([])
ax3.grid(True, alpha=0.3, linestyle=':', axis='x')

# Adjust layout
plt.tight_layout(rect=[0, 0.02, 1, 0.96])

# Save the figure
output_path = r'c:\Users\Well\Crush\Projects\LJPW_Physics\LJPW-Physics\Docs\roman_empire_ljpw_charts.png'
plt.savefig(output_path, dpi=150, facecolor='#1a1a2e', edgecolor='none', bbox_inches='tight')
print(f"Chart saved to: {output_path}")

plt.show()
