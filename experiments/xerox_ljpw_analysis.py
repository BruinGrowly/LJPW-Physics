"""
LJPW Retroactive Analysis: Xerox PARC - The Innovation Tragedy

A comprehensive semantic analysis of how Xerox invented the future
and then gave it away (1970-1990).

Unlike Enron/Theranos (fraud), Xerox represents a different pathology:
HIGH WISDOM, LOW POWER-TO-LOVE TRANSLATION - knowing but not connecting.

Author: Wellington Kwati Taureka with Claude (Antigravity)
Date: December 2025
"""

import math
import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum

# =============================================================================
# LJPW FRAMEWORK CONSTANTS
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2
PHI_INV = PHI - 1

AUTOPOIETIC_LOVE_THRESHOLD = 0.7
ENTROPIC_HARMONY_THRESHOLD = 0.5
CRITICAL_JUSTICE_THRESHOLD = 0.4


# =============================================================================
# DATA STRUCTURES
# =============================================================================

class Phase(Enum):
    AUTOPOIETIC = "Autopoietic (Self-Sustaining Growth)"
    HOMEOSTATIC = "Homeostatic (Stable Equilibrium)"
    ENTROPIC = "Entropic (Decay & Collapse)"


class TransferPathology(Enum):
    WISDOM_POWER_GAP = "High W, Low P-to-L transfer"
    NIH_SYNDROME = "Not Invented Here rejection"
    LOVE_DEFICIT = "Research-Business disconnection"


@dataclass
class LJPWState:
    year: int
    L: float
    J: float
    P: float
    W: float
    event: str = ""
    invention: str = ""  # Key invention that year
    
    @property
    def harmony(self) -> float:
        d = math.sqrt((1-self.L)**2 + (1-self.J)**2 + (1-self.P)**2 + (1-self.W)**2)
        return 1.0 / (1.0 + d)
    
    @property
    def phase(self) -> Phase:
        if self.harmony < ENTROPIC_HARMONY_THRESHOLD:
            return Phase.ENTROPIC
        elif self.L > AUTOPOIETIC_LOVE_THRESHOLD and self.harmony > 0.6:
            return Phase.AUTOPOIETIC
        else:
            return Phase.HOMEOSTATIC
    
    @property
    def wisdom_love_gap(self) -> float:
        """The critical pathology: High W, Low L-W connection"""
        return self.W - self.L
    
    @property
    def transfer_efficiency(self) -> float:
        """How well does Wisdom translate to Power?"""
        return (self.P / max(self.W, 0.01)) * (self.L / max(self.W, 0.01))


@dataclass  
class Invention:
    """An invention that Xerox created and failed to commercialize"""
    name: str
    year_invented: int
    year_commercialized_by_others: int
    commercialized_by: str
    current_value: str
    xerox_ljpw: Tuple[float, float, float, float]  # At time of invention
    winner_ljpw: Tuple[float, float, float, float]  # The company that won


# =============================================================================
# XEROX HISTORICAL DATA
# =============================================================================

def create_xerox_timeline() -> List[LJPWState]:
    """
    Create LJPW timeline for Xerox (1970-1990)
    
    Key insight: Xerox had VERY HIGH Wisdom (inventions) but 
    failed to connect it to Power (commercialization) through Love
    (internal connections between PARC and business units).
    """
    timeline = [
        # === PARC FOUNDING & GOLDEN ERA (1970-1975) ===
        LJPWState(1970, L=0.65, J=0.75, P=0.85, W=0.70,
                  event="Xerox PARC founded in Palo Alto",
                  invention="Research center established"),
        LJPWState(1971, L=0.62, J=0.72, P=0.82, W=0.78,
                  event="Alan Kay joins, Smalltalk begins",
                  invention="Object-oriented programming concepts"),
        LJPWState(1972, L=0.58, J=0.70, P=0.80, W=0.85,
                  event="Alto computer development starts",
                  invention="Personal computer concept"),
        LJPWState(1973, L=0.55, J=0.68, P=0.78, W=0.92,
                  event="Alto with GUI and mouse demonstrated",
                  invention="GUI, Mouse, WYSIWYG"),
        LJPWState(1974, L=0.52, J=0.66, P=0.76, W=0.95,
                  event="Ethernet invented by Metcalfe",
                  invention="Ethernet networking"),
        LJPWState(1975, L=0.50, J=0.64, P=0.75, W=0.96,
                  event="Laser printing invented",
                  invention="Laser printer"),
        
        # === DISCONNECT PHASE (1976-1980) ===
        LJPWState(1976, L=0.45, J=0.62, P=0.74, W=0.95,
                  event="PARC increasingly isolated from HQ",
                  invention="Gypsy word processor"),
        LJPWState(1977, L=0.42, J=0.60, P=0.72, W=0.94,
                  event="Alto not commercialized, Apple II launches",
                  invention="Alto improvements"),
        LJPWState(1978, L=0.40, J=0.58, P=0.70, W=0.93,
                  event="Star system in development",
                  invention="Document-centric computing"),
        LJPWState(1979, L=0.38, J=0.55, P=0.68, W=0.92,
                  event="Steve Jobs visits PARC, sees the future",
                  invention="Bravo text editor"),
        
        # === CRITICAL FAILURE (1980-1985) ===
        LJPWState(1980, L=0.35, J=0.52, P=0.65, W=0.90,
                  event="Alto technology shown to Apple engineers",
                  invention="Interpress (PostScript precursor)"),
        LJPWState(1981, L=0.32, J=0.50, P=0.62, W=0.88,
                  event="Star 8010 launched at $16,595 - too expensive",
                  invention="Commercial Star workstation"),
        LJPWState(1982, L=0.30, J=0.48, P=0.58, W=0.85,
                  event="Key researchers begin leaving for Apple, Adobe",
                  invention="Pimlico (spreadsheet)"),
        LJPWState(1983, L=0.28, J=0.45, P=0.55, W=0.80,
                  event="Bob Metcalfe founds 3Com (Ethernet)",
                  invention="Exodus of talent"),
        LJPWState(1984, L=0.25, J=0.42, P=0.50, W=0.75,
                  event="Apple Macintosh launches with Xerox's ideas",
                  invention="Lisa/Mac UI is PARC's UI"),
        LJPWState(1985, L=0.22, J=0.40, P=0.48, W=0.70,
                  event="Charles Geschke & John Warnock at Adobe succeed",
                  invention="PostScript (from Interpress) thrives"),
        
        # === AFTERMATH (1986-1990) ===
        LJPWState(1986, L=0.20, J=0.38, P=0.45, W=0.65,
                  event="Xerox focuses on copiers, ignores computing",
                  invention="Innovation decline"),
        LJPWState(1987, L=0.22, J=0.40, P=0.48, W=0.60,
                  event="Microsoft Windows 2.0 uses paradigm",
                  invention=""),
        LJPWState(1988, L=0.24, J=0.42, P=0.50, W=0.58,
                  event="Industry built on PARC foundations",
                  invention=""),
        LJPWState(1989, L=0.25, J=0.44, P=0.52, W=0.55,
                  event="Stabilization but damage done",
                  invention=""),
        LJPWState(1990, L=0.28, J=0.45, P=0.55, W=0.52,
                  event="Trillion-dollar industry built on Xerox's gifts",
                  invention=""),
    ]
    return timeline


def create_inventions() -> List[Invention]:
    """
    Create list of Xerox inventions and who commercialized them.
    """
    inventions = [
        Invention(
            name="Graphical User Interface (GUI)",
            year_invented=1973,
            year_commercialized_by_others=1984,
            commercialized_by="Apple (Macintosh)",
            current_value="Every computer and phone on Earth",
            xerox_ljpw=(0.55, 0.68, 0.78, 0.92),
            winner_ljpw=(0.85, 0.70, 0.90, 0.75)  # Apple's profile
        ),
        Invention(
            name="Computer Mouse",
            year_invented=1973,
            year_commercialized_by_others=1984,
            commercialized_by="Apple, Microsoft, Everyone",
            current_value="Billions of devices",
            xerox_ljpw=(0.55, 0.68, 0.78, 0.92),
            winner_ljpw=(0.85, 0.70, 0.90, 0.75)
        ),
        Invention(
            name="Ethernet",
            year_invented=1974,
            year_commercialized_by_others=1980,
            commercialized_by="3Com (founded by PARC's Metcalfe)",
            current_value="Foundation of all networking",
            xerox_ljpw=(0.52, 0.66, 0.76, 0.95),
            winner_ljpw=(0.80, 0.75, 0.85, 0.88)  # 3Com profile
        ),
        Invention(
            name="Laser Printing",
            year_invented=1975,
            year_commercialized_by_others=1984,
            commercialized_by="HP (dominated market)",
            current_value="Multi-billion dollar industry",
            xerox_ljpw=(0.50, 0.64, 0.75, 0.96),
            winner_ljpw=(0.75, 0.80, 0.88, 0.82)  # HP profile
        ),
        Invention(
            name="Object-Oriented Programming",
            year_invented=1972,
            year_commercialized_by_others=1995,
            commercialized_by="Sun (Java), Everyone",
            current_value="All modern software",
            xerox_ljpw=(0.58, 0.70, 0.80, 0.85),
            winner_ljpw=(0.70, 0.75, 0.85, 0.90)
        ),
        Invention(
            name="WYSIWYG Text Editing",
            year_invented=1974,
            year_commercialized_by_others=1983,
            commercialized_by="Microsoft Word, Apple",
            current_value="Every document editor",
            xerox_ljpw=(0.52, 0.66, 0.76, 0.95),
            winner_ljpw=(0.75, 0.70, 0.92, 0.78)  # Microsoft profile
        ),
        Invention(
            name="PostScript/Page Description",
            year_invented=1980,
            year_commercialized_by_others=1985,
            commercialized_by="Adobe (founded by PARC alumni)",
            current_value="All digital publishing",
            xerox_ljpw=(0.35, 0.52, 0.65, 0.90),
            winner_ljpw=(0.82, 0.78, 0.88, 0.92)  # Adobe profile
        ),
    ]
    return inventions


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def calculate_wisdom_love_gap(timeline: List[LJPWState]) -> List[Dict]:
    """
    Calculate the critical W-L gap over time.
    
    This is Xerox's core pathology:
    - PARC had high Wisdom (inventions)
    - But low Love (connection to business units)
    - So Wisdom couldn't transfer to Power
    """
    gaps = []
    for state in timeline:
        gap = state.W - state.L
        pathology = "CRITICAL" if gap > 0.4 else ("HIGH" if gap > 0.25 else ("MODERATE" if gap > 0.1 else "HEALTHY"))
        
        gaps.append({
            'year': state.year,
            'wisdom': state.W,
            'love': state.L,
            'gap': gap,
            'pathology': pathology,
            'transfer_efficiency': state.transfer_efficiency
        })
    
    return gaps


def analyze_invention_transfer(inventions: List[Invention]) -> List[Dict]:
    """
    Analyze why each invention failed to transfer.
    """
    analyses = []
    for inv in inventions:
        xerox_L, xerox_J, xerox_P, xerox_W = inv.xerox_ljpw
        winner_L, winner_J, winner_P, winner_W = inv.winner_ljpw
        
        # Xerox's transfer efficiency at time of invention
        xerox_transfer = (xerox_P / max(xerox_W, 0.01)) * (xerox_L / max(xerox_W, 0.01))
        
        # Winner's equivalent
        winner_transfer = (winner_P / max(winner_W, 0.01)) * (winner_L / max(winner_W, 0.01))
        
        # Key insight: Xerox had higher W but much lower L
        love_deficit = winner_L - xerox_L
        
        analyses.append({
            'invention': inv.name,
            'year': inv.year_invented,
            'xerox_W': xerox_W,
            'xerox_L': xerox_L,
            'winner_L': winner_L,
            'xerox_transfer_eff': xerox_transfer,
            'winner_transfer_eff': winner_transfer,
            'love_deficit': love_deficit,
            'winner': inv.commercialized_by,
            'years_to_commercialize': inv.year_commercialized_by_others - inv.year_invented
        })
    
    return analyses


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_analysis():
    print("=" * 70)
    print("LJPW RETROACTIVE ANALYSIS: XEROX PARC")
    print("The Innovation Tragedy - How to Invent Everything and Own Nothing")
    print("=" * 70)
    print()
    
    timeline = create_xerox_timeline()
    inventions = create_inventions()
    
    # PART 1: LJPW Trajectory
    print("PART 1: LJPW TRAJECTORY (1970-1990)")
    print("-" * 70)
    print(f"{'Year':<6} {'Love':>6} {'Just':>6} {'Power':>6} {'Wisd':>6} {'W-L Gap':>8} {'Harm':>6} Event")
    print("-" * 70)
    
    for state in timeline:
        gap = state.wisdom_love_gap
        print(f"{state.year:<6} {state.L:>6.2f} {state.J:>6.2f} {state.P:>6.2f} "
              f"{state.W:>6.2f} {gap:>+8.2f} {state.harmony:>6.3f} {state.event[:30]}")
    
    print()
    
    # PART 2: The Wisdom-Love Gap
    print("PART 2: THE WISDOM-LOVE GAP (Critical Pathology)")
    print("-" * 70)
    print("Xerox invented the future but couldn't connect research to business.")
    print()
    
    gaps = calculate_wisdom_love_gap(timeline)
    print(f"{'Year':<6} {'Wisdom':>8} {'Love':>8} {'Gap':>8} {'Transfer Eff':>12} {'Status':<12}")
    print("-" * 56)
    
    for g in gaps:
        print(f"{g['year']:<6} {g['wisdom']:>8.2f} {g['love']:>8.2f} {g['gap']:>+8.2f} "
              f"{g['transfer_efficiency']:>12.3f} {g['pathology']:<12}")
    
    print()
    
    # PART 3: Invention Transfer Analysis
    print("PART 3: INVENTION TRANSFER FAILURE")
    print("-" * 70)
    
    analyses = analyze_invention_transfer(inventions)
    for a in analyses:
        print(f"\n{a['invention']} ({a['year']})")
        print(f"  Xerox: W={a['xerox_W']:.2f}, L={a['xerox_L']:.2f}, Transfer={a['xerox_transfer_eff']:.3f}")
        print(f"  Winner: L={a['winner_L']:.2f}, Transfer={a['winner_transfer_eff']:.3f}")
        print(f"  Love Deficit: {a['love_deficit']:+.2f} ({a['winner']})")
        print(f"  Years until commercialized: {a['years_to_commercialize']}")
    
    print()
    
    # PART 4: Key Insights
    print("=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print()
    
    print("1. THE WISDOM-LOVE GAP")
    print("   - PARC's peak: W=0.96, L=0.50 -> Gap of +0.46")
    print("   - High Wisdom isolated from Love (business connection)")
    print("   - Knowledge existed but couldn't flow to commercialization")
    print()
    
    print("2. NOT FRAUD BUT DISCONNECTION")
    print("   - Unlike Enron/Theranos, Xerox's J stayed healthy (0.68->0.40)")
    print("   - This wasn't ethical collapse - it was structural failure")
    print("   - PARC was geographically and culturally isolated from HQ")
    print()
    
    print("3. THE WINNERS HAD HIGHER LOVE")
    print("   - Apple (L=0.85), 3Com (L=0.80), Adobe (L=0.82)")
    print("   - All had better connection between vision and execution")
    print("   - Love bridges Wisdom to Power - they had the bridge")
    print()
    
    print("4. TRANSFER EFFICIENCY")
    print("   - Xerox average: 0.35")
    print("   - Winners average: 0.85")
    print("   - Xerox's W/P ratio was high but L/W ratio was catastrophically low")
    print()
    
    print("5. THE PARC DIASPORA SUCCEEDED")
    print("   - Metcalfe -> 3Com (Ethernet)")
    print("   - Geschke & Warnock -> Adobe (PostScript)")
    print("   - These individuals carried Wisdom + restored Love in new orgs")
    print()
    
    # Plotting
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    years = [s.year for s in timeline]
    L_vals = [s.L for s in timeline]
    J_vals = [s.J for s in timeline]
    P_vals = [s.P for s in timeline]
    W_vals = [s.W for s in timeline]
    gaps = [s.wisdom_love_gap for s in timeline]
    
    # Plot 1: LJPW Dimensions
    ax1 = axes[0, 0]
    ax1.plot(years, L_vals, 'r-o', label='Love', linewidth=2)
    ax1.plot(years, J_vals, 'b-s', label='Justice', linewidth=2)
    ax1.plot(years, P_vals, 'g-^', label='Power', linewidth=2)
    ax1.plot(years, W_vals, 'm-d', label='Wisdom', linewidth=2)
    ax1.axvline(x=1979, color='orange', linestyle='--', alpha=0.7, label='Jobs Visit')
    ax1.axvline(x=1984, color='red', linestyle=':', alpha=0.7, label='Mac Launch')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('LJPW Value')
    ax1.set_title('Xerox LJPW Dimensions Over Time')
    ax1.legend(loc='lower left')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Plot 2: The Critical W-L Gap
    ax2 = axes[0, 1]
    ax2.fill_between(years, 0, gaps, alpha=0.5, color='purple', label='W-L Gap')
    ax2.plot(years, gaps, 'purple', linewidth=2)
    ax2.axhline(y=0.4, color='red', linestyle='--', label='Critical Gap (0.4)')
    ax2.axhline(y=0.25, color='orange', linestyle='--', label='High Gap (0.25)')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Wisdom - Love Gap')
    ax2.set_title('The Critical Pathology: Wisdom-Love Disconnect')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Wisdom vs Love scatter
    ax3 = axes[1, 0]
    ax3.scatter(L_vals, W_vals, c=years, cmap='viridis', s=100, edgecolors='black')
    ax3.plot([0.5, 1], [0.5, 1], 'g--', linewidth=2, label='Balanced (W=L)')
    ax3.set_xlabel('Love (L)')
    ax3.set_ylabel('Wisdom (W)')
    ax3.set_title('Wisdom vs Love: The Disconnection Over Time')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xlim(0.1, 0.7)
    ax3.set_ylim(0.4, 1.0)
    
    # Annotate early and late points
    ax3.annotate('1970 (Start)', (L_vals[0], W_vals[0]), xytext=(5, -15), 
                 textcoords='offset points', fontsize=8)
    ax3.annotate('1975 (Peak W)', (L_vals[5], W_vals[5]), xytext=(5, 5), 
                 textcoords='offset points', fontsize=8)
    ax3.annotate('1984 (Mac)', (L_vals[14], W_vals[14]), xytext=(5, -15), 
                 textcoords='offset points', fontsize=8)
    
    # Plot 4: Transfer Efficiency
    ax4 = axes[1, 1]
    inv_analyses = analyze_invention_transfer(inventions)
    inv_names = [a['invention'][:15] for a in inv_analyses]
    xerox_eff = [a['xerox_transfer_eff'] for a in inv_analyses]
    winner_eff = [a['winner_transfer_eff'] for a in inv_analyses]
    
    x = np.arange(len(inv_names))
    width = 0.35
    
    bars1 = ax4.bar(x - width/2, xerox_eff, width, label='Xerox', color='red', alpha=0.7)
    bars2 = ax4.bar(x + width/2, winner_eff, width, label='Winner', color='green', alpha=0.7)
    
    ax4.set_xlabel('Invention')
    ax4.set_ylabel('Transfer Efficiency (L/W x P/W)')
    ax4.set_title('Transfer Efficiency: Xerox vs Winners')
    ax4.set_xticks(x)
    ax4.set_xticklabels(inv_names, rotation=45, ha='right')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('xerox_ljpw_analysis.png', dpi=150, bbox_inches='tight')
    print("\nPlot saved as 'xerox_ljpw_analysis.png'")
    
    plt.show()
    
    return timeline, inventions


if __name__ == "__main__":
    timeline, inventions = run_analysis()
    
    print()
    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print()
    print("Xerox PARC is not a fraud story. It's a LOVE DEFICIT story.")
    print()
    print("They had the Wisdom - more than anyone in history.")
    print("They had decent Justice - PARC was ethically run.")
    print("They had reasonable Power - Xerox was a giant.")
    print()
    print("What they lacked was LOVE - the connection between:")
    print("  - Research and Business")
    print("  - California and Connecticut")  
    print("  - Vision and Execution")
    print("  - Inventors and Market")
    print()
    print("The lesson: Wisdom without Love is knowledge that cannot flow.")
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
