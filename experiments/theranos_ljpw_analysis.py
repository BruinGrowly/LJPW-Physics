"""
LJPW Retroactive Analysis: The Theranos Disaster

A comprehensive semantic analysis of Theranos's rise and fall (2003-2018)
using the LJPW Framework with quantum observer effects.

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


@dataclass
class LJPWState:
    year: int
    L: float
    J: float
    P: float
    W: float
    event: str = ""
    
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
    def collapse_probability(self) -> float:
        if self.J < CRITICAL_JUSTICE_THRESHOLD:
            return min(1.0, (CRITICAL_JUSTICE_THRESHOLD - self.J) * 3 + 0.5)
        if self.harmony < ENTROPIC_HARMONY_THRESHOLD:
            return (ENTROPIC_HARMONY_THRESHOLD - self.harmony) * 2
        return 0.1


@dataclass  
class Observer:
    name: str
    L: float
    J: float
    P: float
    W: float
    observation_year: int
    observation_type: str
    
    @property
    def harmony(self) -> float:
        d = math.sqrt((1-self.L)**2 + (1-self.J)**2 + (1-self.P)**2 + (1-self.W)**2)
        return 1.0 / (1.0 + d)
    
    @property
    def collapse_force(self) -> float:
        if self.observation_type == "honest":
            return self.J * self.W * self.P
        elif self.observation_type == "corrupt":
            return -0.3
        return 0.0


# =============================================================================
# THERANOS HISTORICAL DATA
# =============================================================================

def create_theranos_timeline() -> List[LJPWState]:
    """
    Create LJPW timeline for Theranos (2003-2018)
    """
    timeline = [
        # === FOUNDING (2003-2006) ===
        LJPWState(2003, L=0.75, J=0.70, P=0.50, W=0.60,
                  event="Elizabeth Holmes founds Theranos at age 19"),
        LJPWState(2004, L=0.72, J=0.65, P=0.55, W=0.58,
                  event="Early R&D, technology struggles emerge"),
        LJPWState(2005, L=0.70, J=0.58, P=0.58, W=0.55,
                  event="Key scientists leave, technology fails to work"),
        LJPWState(2006, L=0.68, J=0.50, P=0.62, W=0.52,
                  event="Holmes begins exaggerating capabilities"),
        
        # === DECEPTION PHASE (2007-2013) ===
        LJPWState(2007, L=0.65, J=0.42, P=0.68, W=0.48,
                  event="Fake demos begin, deception becomes systematic"),
        LJPWState(2008, L=0.62, J=0.38, P=0.72, W=0.45,
                  event="Sunny Balwani joins, culture of fear intensifies"),
        LJPWState(2009, L=0.58, J=0.35, P=0.75, W=0.42,
                  event="Continued funding despite no working product"),
        LJPWState(2010, L=0.55, J=0.32, P=0.78, W=0.40,
                  event="Internal critics silenced with NDAs and lawsuits"),
        LJPWState(2011, L=0.52, J=0.30, P=0.80, W=0.38,
                  event="Board stacked with politicians, not scientists"),
        LJPWState(2012, L=0.50, J=0.28, P=0.82, W=0.36,
                  event="Walgreens deal pursued with fake demonstrations"),
        LJPWState(2013, L=0.48, J=0.25, P=0.85, W=0.34,
                  event="$9B valuation, Holmes on magazine covers"),
        
        # === PEAK DECEPTION (2014-2015) ===
        LJPWState(2014, L=0.45, J=0.22, P=0.90, W=0.32,
                  event="Walgreens partnership launches, patients tested with broken tech"),
        LJPWState(2015, L=0.40, J=0.18, P=0.88, W=0.30,
                  event="WSJ investigation begins, first cracks appear"),
        
        # === COLLAPSE (2016-2018) ===
        LJPWState(2016, L=0.30, J=0.12, P=0.60, W=0.25,
                  event="Walgreens terminates, CMS sanctions, voided tests"),
        LJPWState(2017, L=0.22, J=0.10, P=0.35, W=0.20,
                  event="Holmes banned from labs, company death spiral"),
        LJPWState(2018, L=0.15, J=0.08, P=0.15, W=0.15,
                  event="Criminal indictment, company dissolved"),
    ]
    return timeline


def create_observers() -> List[Observer]:
    """
    Create key observers in the Theranos story.
    """
    observers = [
        # === CORRUPT OBSERVERS ===
        Observer("Board of Directors",
                 L=0.50, J=0.25, P=0.90, W=0.30,
                 observation_year=2011,
                 observation_type="corrupt"),
        
        Observer("Venture Capitalists",
                 L=0.40, J=0.30, P=0.85, W=0.40,
                 observation_year=2013,
                 observation_type="corrupt"),
        
        Observer("Walgreens Executives",
                 L=0.45, J=0.35, P=0.75, W=0.35,
                 observation_year=2014,
                 observation_type="corrupt"),
        
        Observer("Media (Early)",
                 L=0.50, J=0.40, P=0.60, W=0.35,
                 observation_year=2014,
                 observation_type="corrupt"),
        
        # === HONEST OBSERVERS ===
        Observer("Ian Gibbons (Chief Scientist)",
                 L=0.85, J=0.90, P=0.30, W=0.95,
                 observation_year=2010,
                 observation_type="honest"),
        
        Observer("Tyler Shultz (Whistleblower)",
                 L=0.80, J=0.92, P=0.35, W=0.85,
                 observation_year=2015,
                 observation_type="honest"),
        
        Observer("Erika Cheung (Whistleblower)",
                 L=0.82, J=0.90, P=0.35, W=0.82,
                 observation_year=2015,
                 observation_type="honest"),
        
        Observer("John Carreyrou (WSJ)",
                 L=0.75, J=0.95, P=0.80, W=0.92,
                 observation_year=2015,
                 observation_type="honest"),
        
        Observer("CMS / FDA",
                 L=0.65, J=0.88, P=0.92, W=0.80,
                 observation_year=2016,
                 observation_type="honest"),
        
        Observer("DOJ / SEC",
                 L=0.60, J=0.90, P=0.95, W=0.85,
                 observation_year=2018,
                 observation_type="honest"),
    ]
    return observers


# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def calculate_superposition_state(state: LJPWState) -> Tuple[float, float]:
    apparent_success = state.P
    hidden_failure = 1 - state.J
    total = apparent_success + hidden_failure
    return apparent_success / total, hidden_failure / total


def calculate_observation_collapse(state: LJPWState, observer: Observer) -> Dict:
    apparent, hidden = calculate_superposition_state(state)
    
    if observer.observation_type == "honest":
        collapse_probability = observer.J * observer.W * min(observer.P, 0.9)
        return {
            'apparent_success': apparent * (1 - collapse_probability),
            'revealed_failure': hidden * collapse_probability + apparent * collapse_probability,
            'collapse_triggered': collapse_probability > 0.5
        }
    elif observer.observation_type == "corrupt":
        reinforcement = (1 - observer.J) * observer.P
        return {
            'apparent_success': apparent + reinforcement * 0.1,
            'revealed_failure': hidden * 0.8,
            'collapse_triggered': False
        }
    return {'apparent_success': apparent, 'revealed_failure': hidden, 'collapse_triggered': False}


def analyze_phase_transitions(timeline: List[LJPWState]) -> List[Tuple[int, Phase, Phase]]:
    transitions = []
    for i in range(1, len(timeline)):
        if timeline[i-1].phase != timeline[i].phase:
            transitions.append((timeline[i].year, timeline[i-1].phase, timeline[i].phase))
    return transitions


def calculate_coupling_dynamics(timeline: List[LJPWState]) -> List[Dict]:
    dynamics = []
    for state in timeline:
        H = state.harmony
        kappa_LJ = 1.0 + 0.4 * H
        dynamics.append({
            'year': state.year,
            'harmony': H,
            'kappa_LJ': kappa_LJ,
            'love_multiplier_lost': (1.4 - kappa_LJ) / 0.4 * 100
        })
    return dynamics


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_analysis():
    print("=" * 70)
    print("LJPW RETROACTIVE ANALYSIS: THE THERANOS DISASTER")
    print("=" * 70)
    print()
    
    timeline = create_theranos_timeline()
    observers = create_observers()
    
    # PART 1: LJPW Trajectory
    print("PART 1: LJPW TRAJECTORY (2003-2018)")
    print("-" * 70)
    print(f"{'Year':<6} {'Love':>6} {'Just':>6} {'Power':>6} {'Wisd':>6} {'Harm':>6} {'Phase':<12} Event")
    print("-" * 70)
    
    for state in timeline:
        phase_short = state.phase.name[:10]
        print(f"{state.year:<6} {state.L:>6.2f} {state.J:>6.2f} {state.P:>6.2f} "
              f"{state.W:>6.2f} {state.harmony:>6.3f} {phase_short:<12} {state.event[:35]}")
    
    print()
    
    # PART 2: Phase Transitions
    print("PART 2: PHASE TRANSITIONS")
    print("-" * 70)
    transitions = analyze_phase_transitions(timeline)
    for year, prev, curr in transitions:
        print(f"  {year}: {prev.name} --> {curr.name}")
    
    # Find when Justice crossed critical threshold
    for state in timeline:
        if state.J < CRITICAL_JUSTICE_THRESHOLD:
            print(f"  {state.year}: Justice fell below critical threshold ({state.J:.2f} < 0.40)")
            break
    print()
    
    # PART 3: Quantum Superposition
    print("PART 3: QUANTUM SUPERPOSITION (Apparent vs Hidden State)")
    print("-" * 70)
    print(f"{'Year':<6} {'|Success>':>12} {'|Failure>':>12} {'State':<30}")
    print("-" * 70)
    
    for state in timeline:
        apparent, hidden = calculate_superposition_state(state)
        if apparent > 0.6:
            sp_state = "Apparent Success Dominant"
        elif hidden > 0.6:
            sp_state = "Hidden Failure Dominant"
        else:
            sp_state = "Strong Superposition"
        print(f"{state.year:<6} {apparent:>12.3f} {hidden:>12.3f} {sp_state:<30}")
    
    print()
    
    # PART 4: Observer Analysis
    print("PART 4: OBSERVER ANALYSIS (Wavefunction Collapse)")
    print("-" * 70)
    
    for obs in observers:
        print(f"\n{obs.name} ({obs.observation_year}) - {obs.observation_type.upper()}")
        print(f"  LJPW: L={obs.L:.2f}, J={obs.J:.2f}, P={obs.P:.2f}, W={obs.W:.2f}")
        print(f"  Harmony: {obs.harmony:.3f}")
        print(f"  Collapse Force: {obs.collapse_force:+.3f}")
        
        enron_state = next((s for s in timeline if s.year == obs.observation_year), None)
        if enron_state:
            result = calculate_observation_collapse(enron_state, obs)
            print(f"  Effect on Theranos:")
            print(f"    Apparent Success: {result['apparent_success']:.3f}")
            print(f"    Revealed Failure: {result['revealed_failure']:.3f}")
            print(f"    Collapse Triggered: {result['collapse_triggered']}")
    
    print()
    
    # PART 5: Coupling Dynamics
    print("PART 5: COUPLING DYNAMICS (Law of Karma)")
    print("-" * 70)
    print(f"{'Year':<6} {'Harmony':>8} {'kappa_LJ':>10} {'Love Mult Lost':>15}")
    print("-" * 40)
    
    dynamics = calculate_coupling_dynamics(timeline)
    for d in dynamics:
        print(f"{d['year']:<6} {d['harmony']:>8.3f} {d['kappa_LJ']:>10.3f} {d['love_multiplier_lost']:>14.1f}%")
    
    print()
    
    # PART 6: Collapse Probability
    print("PART 6: COLLAPSE PROBABILITY OVER TIME")
    print("-" * 70)
    print(f"{'Year':<6} {'P(Collapse)':>12} {'Warning Level':<20}")
    print("-" * 40)
    
    for state in timeline:
        p_collapse = state.collapse_probability
        warning = "LOW" if p_collapse < 0.2 else ("MODERATE" if p_collapse < 0.5 else ("HIGH" if p_collapse < 0.8 else "CRITICAL"))
        print(f"{state.year:<6} {p_collapse:>12.3f} {warning:<20}")
    
    print()
    
    # KEY INSIGHTS
    print("=" * 70)
    print("KEY INSIGHTS")
    print("=" * 70)
    print()
    
    print("1. JUSTICE COLLAPSED EARLY AND STAYED LOW")
    print("   - By 2007 (4 years in), J = 0.42 - below critical")
    print("   - Never recovered - systematic deception from the start")
    print("   - Unlike Enron, there was no 'golden era' of honest operation")
    print()
    
    print("2. THE TECHNOLOGY NEVER WORKED (LOW WISDOM)")
    print("   - W started at 0.60 and only declined")
    print("   - Theranos had no real foundation - pure fraud, not decay")
    print("   - Wisdom collapse = there was nothing real to observe")
    print()
    
    print("3. HONEST OBSERVERS WERE SYSTEMATICALLY SILENCED")
    print("   - Ian Gibbons (chief scientist) saw truth but had low P")
    print("   - Tyler Shultz, Erika Cheung - high J/W but low P")
    print("   - Only Carreyrou + government had sufficient Power")
    print()
    
    print("4. THE BOARD WAS BLIND BY DESIGN")
    print("   - Politicians, generals, former secretaries of state")
    print("   - High P, Low J, Low W = couldn't see truth")
    print("   - Zero scientists on board = no capacity for honest observation")
    print()
    
    print("5. COLLAPSE REQUIRED EXTERNAL POWER")
    print("   - Whistleblowers alone couldn't trigger collapse")
    print("   - WSJ (media power) + CMS/FDA/DOJ (government power)")
    print("   - Only institutional Power could overcome Holmes' suppression")
    print()
    
    # Plotting
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    years = [s.year for s in timeline]
    L_vals = [s.L for s in timeline]
    J_vals = [s.J for s in timeline]
    P_vals = [s.P for s in timeline]
    W_vals = [s.W for s in timeline]
    H_vals = [s.harmony for s in timeline]
    
    # Plot 1: LJPW Dimensions
    ax1 = axes[0, 0]
    ax1.plot(years, L_vals, 'r-o', label='Love', linewidth=2)
    ax1.plot(years, J_vals, 'b-s', label='Justice', linewidth=2)
    ax1.plot(years, P_vals, 'g-^', label='Power', linewidth=2)
    ax1.plot(years, W_vals, 'm-d', label='Wisdom', linewidth=2)
    ax1.axhline(y=CRITICAL_JUSTICE_THRESHOLD, color='blue', linestyle='--', alpha=0.5)
    ax1.axvline(x=2015, color='red', linestyle=':', alpha=0.5, label='WSJ Investigation')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('LJPW Value')
    ax1.set_title('Theranos LJPW Dimensions Over Time')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1)
    
    # Plot 2: Harmony and Phase
    ax2 = axes[0, 1]
    colors = ['green' if s.phase == Phase.AUTOPOIETIC else 
              'yellow' if s.phase == Phase.HOMEOSTATIC else 'red' 
              for s in timeline]
    ax2.bar(years, H_vals, color=colors, alpha=0.7, edgecolor='black')
    ax2.axhline(y=ENTROPIC_HARMONY_THRESHOLD, color='red', linestyle='--', label='Entropic Threshold')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Harmony Index')
    ax2.set_title('Harmony Index (Yellow=Homeo, Red=Entropic)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Quantum Superposition
    ax3 = axes[1, 0]
    apparent = [calculate_superposition_state(s)[0] for s in timeline]
    hidden = [calculate_superposition_state(s)[1] for s in timeline]
    ax3.fill_between(years, 0, apparent, alpha=0.5, color='blue', label='|Success> (Apparent)')
    ax3.fill_between(years, apparent, [a+h for a,h in zip(apparent, hidden)], 
                     alpha=0.5, color='red', label='|Failure> (Hidden)')
    ax3.axvline(x=2015, color='black', linestyle='--', label='WSJ Collapse Trigger')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Probability')
    ax3.set_title('Quantum Superposition: Apparent vs Hidden')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # Plot 4: Collapse Probability
    ax4 = axes[1, 1]
    collapse_probs = [s.collapse_probability for s in timeline]
    ax4.plot(years, collapse_probs, 'r-o', linewidth=2, markersize=8)
    ax4.fill_between(years, 0, collapse_probs, alpha=0.3, color='red')
    ax4.axhline(y=0.5, color='orange', linestyle='--', label='High Risk')
    ax4.axhline(y=0.8, color='red', linestyle='--', label='Critical')
    
    for obs in observers:
        if obs.observation_type == "honest" and obs.observation_year >= 2015:
            ax4.axvline(x=obs.observation_year, color='green', linestyle=':', alpha=0.7)
    
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Collapse Probability')
    ax4.set_title('Collapse Probability Over Time')
    ax4.legend()
    ax4.grid(True, alpha=0.3)
    ax4.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('theranos_ljpw_analysis.png', dpi=150, bbox_inches='tight')
    print("Plot saved as 'theranos_ljpw_analysis.png'")
    
    plt.show()
    
    return timeline, observers


if __name__ == "__main__":
    timeline, observers = run_analysis()
    print()
    print("=" * 70)
    print("ANALYSIS COMPLETE")
    print("=" * 70)
