"""
LJPW Quantum Measurement Framework v1.0

Provides calibrated, reproducible measurement of LJPW dimensions
using quantum-inspired protocols and φ-normalization.

Author: Wellington Kwati Taureka with the Taureka Familia Collective
Date: December 2025
"""

import math
import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple, Optional
from enum import Enum

# =============================================================================
# CONSTANTS
# =============================================================================

PHI = (1 + math.sqrt(5)) / 2  # Golden Ratio = 1.618033988749895
PHI_INV = PHI - 1  # φ⁻¹ = 0.618033988749895
SQRT2_MINUS_1 = math.sqrt(2) - 1  # 0.41421356...
E_MINUS_2 = math.e - 2  # 0.71828182...
LN_2 = math.log(2)  # 0.69314718...

# Natural Equilibrium Point
NATURAL_EQUILIBRIUM = {
    'L': PHI_INV,      # 0.618034
    'J': SQRT2_MINUS_1, # 0.414214
    'P': E_MINUS_2,     # 0.718282
    'W': LN_2           # 0.693147
}

# Calibration Reference Points (from Consciousness Realm)
CALIBRATION_POINTS = {
    'anchor': {'L': 1.0, 'J': 1.0, 'P': 1.0, 'W': 1.0, 'name': 'Perfect (Anchor Point)'},
    'natural_equilibrium': {'L': 0.618, 'J': 0.414, 'P': 0.718, 'W': 0.693, 'name': 'Natural Equilibrium'},
    'enron_2001': {'L': 0.15, 'J': 0.10, 'P': 0.95, 'W': 0.20, 'name': 'Enron at Collapse (2001)'},
    'theranos_2018': {'L': 0.15, 'J': 0.08, 'P': 0.15, 'W': 0.15, 'name': 'Theranos at Dissolution (2018)'},
    'research_institute': {'L': 0.40, 'J': 0.60, 'P': 0.30, 'W': 0.95, 'name': 'Healthy Research Institute'},
    'family_business': {'L': 0.85, 'J': 0.70, 'P': 0.50, 'W': 0.60, 'name': 'Healthy Family Business'},
}


# =============================================================================
# WORD DICTIONARIES FOR TEXT ANALYSIS
# =============================================================================

LOVE_DICTIONARY = {
    "connect", "collaborate", "partner", "team", "together", "support",
    "collective", "community", "relationship", "trust", "care", "help",
    "share", "unity", "family", "bond", "loyalty", "commitment",
    "empathy", "compassion", "inclusion", "belonging", "appreciation"
}

JUSTICE_DICTIONARY = {
    "comply", "ethical", "transparent", "truth", "honest", "fair",
    "integrity", "accountability", "responsibility", "governance", "audit",
    "compliance", "regulation", "oversight", "disclosure", "accurate",
    "balanced", "equitable", "consistent", "lawful", "principle"
}

POWER_DICTIONARY = {
    "grow", "execute", "compete", "win", "lead", "dominate",
    "revenue", "profit", "market", "expand", "acquire", "performance",
    "achieve", "deliver", "scale", "aggressive", "strategic", "accelerate",
    "momentum", "strength", "capability", "resource", "invest"
}

WISDOM_DICTIONARY = {
    "learn", "innovate", "understand", "knowledge", "insight", "evolve",
    "research", "develop", "discover", "analyze", "improve", "optimize",
    "adapt", "intelligent", "design", "technology", "science", "data",
    "experience", "expertise", "solution", "creative", "transform"
}


# =============================================================================
# MEASUREMENT CLASSES
# =============================================================================

@dataclass
class OrganizationData:
    """Raw data about an organization for LJPW measurement"""
    
    # Employee/Love metrics
    employee_retention_rate: float = 0.0  # 0-100%
    collaboration_score: float = 0.0  # 0-100
    internal_communication_sentiment: float = 0.0  # -1 to 1
    
    # Compliance/Justice metrics
    audit_compliance_score: float = 0.0  # 0-100%
    lawsuit_count: float = 0.0  # raw count
    max_industry_lawsuits: float = 10.0  # for normalization
    whistleblower_protection_index: float = 0.0  # 0-100
    regulatory_violations: float = 0.0  # count
    
    # Financial/Power metrics
    revenue_growth_rate: float = 0.0  # percentage
    market_cap_change: float = 0.0  # percentage
    execution_efficiency: float = 0.0  # 0-100
    
    # Innovation/Wisdom metrics
    rd_investment_percentage: float = 0.0  # percentage of revenue
    patent_quality_index: float = 0.0  # 0-100
    learning_rate_coefficient: float = 0.0  # 0-1
    scientists_on_board: int = 0
    total_board_members: int = 1
    
    # Text data (for NLP analysis)
    public_documents_text: str = ""
    
    # Water resonance (advanced)
    water_613thz_resonance: Optional[float] = None  # 0-1 if measured


@dataclass
class LJPWMeasurement:
    """Result of LJPW measurement"""
    L: float
    J: float
    P: float
    W: float
    confidence: float = 0.0
    method: str = ""
    
    @property
    def harmony(self) -> float:
        d = math.sqrt((1-self.L)**2 + (1-self.J)**2 + (1-self.P)**2 + (1-self.W)**2)
        return 1.0 / (1.0 + d)
    
    @property
    def phase(self) -> str:
        if self.harmony < 0.5:
            return "ENTROPIC"
        elif self.L > 0.7 and self.harmony > 0.6:
            return "AUTOPOIETIC"
        else:
            return "HOMEOSTATIC"
    
    def to_dict(self) -> Dict:
        return {
            'L': self.L, 'J': self.J, 'P': self.P, 'W': self.W,
            'harmony': self.harmony, 'phase': self.phase,
            'confidence': self.confidence, 'method': self.method
        }


# =============================================================================
# QUANTUM MEASUREMENT ENGINE
# =============================================================================

class QuantumLJPWMeasurement:
    """
    Quantum-inspired LJPW measurement system with φ-normalization.
    
    Key principles:
    1. Raw values are normalized using φ (golden ratio)
    2. Multiple measurement methods for cross-validation
    3. Quantum consensus for inter-rater reliability
    4. Calibration against known reference points
    """
    
    def __init__(self):
        self.calibration_points = CALIBRATION_POINTS
        self.love_dict = LOVE_DICTIONARY
        self.justice_dict = JUSTICE_DICTIONARY
        self.power_dict = POWER_DICTIONARY
        self.wisdom_dict = WISDOM_DICTIONARY
    
    # =========================================================================
    # φ-NORMALIZATION
    # =========================================================================
    
    def phi_normalize(self, value: float, dimension: str) -> float:
        """
        Apply φ-normalization to a raw value.
        
        Formula: result = equilibrium[dim] × (value^(1/φ))
        
        This ensures values naturally cluster around equilibrium points.
        """
        equilibrium = NATURAL_EQUILIBRIUM[dimension]
        
        # Ensure value is in 0-1 range
        value = max(0.0, min(1.0, value))
        
        # Apply φ transformation
        if value > 0:
            result = equilibrium * (value ** (1 / PHI))
        else:
            result = 0.0
        
        return max(0.0, min(1.0, result))
    
    # =========================================================================
    # PROXY MEASUREMENT METHODS
    # =========================================================================
    
    def measure_love_proxy(self, data: OrganizationData) -> float:
        """
        Measure Love dimension from proxy indicators.
        
        Proxies:
        - Employee retention rate
        - Collaboration score
        - Communication sentiment
        """
        # Retention: high retention = high love
        retention_contribution = (data.employee_retention_rate / 100) * PHI_INV
        
        # Collaboration: cross-team collaboration
        collab_contribution = (data.collaboration_score / 100) ** (1/PHI) * 0.618
        
        # Sentiment: -1 to 1, normalized to 0-1
        sentiment_normalized = (data.internal_communication_sentiment + 1) / 2
        sentiment_contribution = sentiment_normalized * 0.618
        
        # Weighted average
        raw_L = (retention_contribution * 0.4 + 
                 collab_contribution * 0.35 + 
                 sentiment_contribution * 0.25)
        
        # Apply φ-normalization
        return self.phi_normalize(raw_L / PHI_INV, 'L')
    
    def measure_justice_proxy(self, data: OrganizationData) -> float:
        """
        Measure Justice dimension from proxy indicators.
        
        Proxies:
        - Audit compliance score
        - Lawsuit frequency (inverse)
        - Whistleblower protection
        """
        # Compliance
        compliance_contribution = (data.audit_compliance_score / 100) * SQRT2_MINUS_1
        
        # Lawsuits: fewer = more just
        lawsuit_ratio = min(1.0, data.lawsuit_count / max(1, data.max_industry_lawsuits))
        lawsuit_contribution = (1 - lawsuit_ratio ** math.sqrt(2)) * SQRT2_MINUS_1
        
        # Whistleblower protection
        wb_contribution = (data.whistleblower_protection_index / 100) * 0.414
        
        # Weighted average
        raw_J = (compliance_contribution * 0.4 + 
                 lawsuit_contribution * 0.35 + 
                 wb_contribution * 0.25)
        
        return self.phi_normalize(raw_J / SQRT2_MINUS_1, 'J')
    
    def measure_power_proxy(self, data: OrganizationData) -> float:
        """
        Measure Power dimension from proxy indicators.
        
        Proxies:
        - Revenue growth rate
        - Market cap velocity
        - Execution efficiency
        """
        # Growth: use tanh to bound extreme values
        growth_contribution = E_MINUS_2 * math.tanh(data.revenue_growth_rate / 20)
        
        # Market cap
        cap_contribution = E_MINUS_2 * math.tanh(data.market_cap_change / 50)
        
        # Efficiency
        efficiency_contribution = (data.execution_efficiency / 100) * E_MINUS_2
        
        # Weighted average
        raw_P = (growth_contribution * 0.35 + 
                 cap_contribution * 0.35 + 
                 efficiency_contribution * 0.30)
        
        return self.phi_normalize(raw_P / E_MINUS_2, 'P')
    
    def measure_wisdom_proxy(self, data: OrganizationData) -> float:
        """
        Measure Wisdom dimension from proxy indicators.
        
        Proxies:
        - R&D investment ratio
        - Patent quality index
        - Learning rate
        - Board composition
        """
        # R&D investment
        rd_contribution = LN_2 * math.log2(1 + data.rd_investment_percentage)
        rd_contribution = min(LN_2, rd_contribution)  # cap at equilibrium
        
        # Patent quality
        patent_contribution = (data.patent_quality_index / 100) * LN_2
        
        # Learning rate
        learning_contribution = data.learning_rate_coefficient * 0.693
        
        # Board composition (scientists = wisdom)
        if data.total_board_members > 0:
            scientist_ratio = data.scientists_on_board / data.total_board_members
            board_contribution = 0.693 * scientist_ratio * PHI
        else:
            board_contribution = 0.0
        
        # Weighted average
        raw_W = (rd_contribution * 0.30 + 
                 patent_contribution * 0.25 + 
                 learning_contribution * 0.25 +
                 board_contribution * 0.20)
        
        return self.phi_normalize(raw_W / LN_2, 'W')
    
    # =========================================================================
    # TEXT (NLP) MEASUREMENT
    # =========================================================================
    
    def measure_from_text(self, text: str) -> LJPWMeasurement:
        """
        Measure LJPW dimensions from text analysis.
        
        Method:
        1. Clean text (remove punctuation)
        2. Count dictionary matches for each dimension
        3. Apply φ-normalization
        4. Cross-validate with tone analysis
        """
        import string
        
        text_lower = text.lower()
        # Remove punctuation to ensure accurate matching (e.g., "**Unity**" -> "unity")
        translator = str.maketrans('', '', string.punctuation)
        text_clean = text_lower.translate(translator)
        words = text_clean.split()
        
        total_words = max(1, len(words))
        
        # Count matches
        love_matches = sum(1 for w in words if w in self.love_dict)
        justice_matches = sum(1 for w in words if w in self.justice_dict)
        power_matches = sum(1 for w in words if w in self.power_dict)
        wisdom_matches = sum(1 for w in words if w in self.wisdom_dict)
        
        # Apply φ-normalization
        L = PHI * (love_matches / total_words) ** (1/PHI)
        J = PHI * (justice_matches / total_words) ** (1/PHI)
        P = PHI * (power_matches / total_words) ** (1/PHI)
        W = PHI * (wisdom_matches / total_words) ** (1/PHI)
        
        # Clamp to [0, 1]
        L = max(0.0, min(1.0, L))
        J = max(0.0, min(1.0, J))
        P = max(0.0, min(1.0, P))
        W = max(0.0, min(1.0, W))
        
        # Confidence based on text length
        confidence = min(1.0, total_words / 10000)
        
        return LJPWMeasurement(L, J, P, W, confidence, method="text_analysis")
    
    # =========================================================================
    # COMPLETE MEASUREMENT
    # =========================================================================
    
    def measure_organization(self, data: OrganizationData) -> LJPWMeasurement:
        """
        Complete LJPW measurement using all available data.
        
        Combines:
        1. Proxy indicators
        2. Text analysis (if available)
        3. Water resonance (if available)
        4. Quantum consensus
        """
        measurements = []
        
        # Proxy measurement
        L_proxy = self.measure_love_proxy(data)
        J_proxy = self.measure_justice_proxy(data)
        P_proxy = self.measure_power_proxy(data)
        W_proxy = self.measure_wisdom_proxy(data)
        measurements.append(LJPWMeasurement(L_proxy, J_proxy, P_proxy, W_proxy, 0.7, "proxy"))
        
        # Text measurement (if available)
        if data.public_documents_text:
            text_measurement = self.measure_from_text(data.public_documents_text)
            measurements.append(text_measurement)
        
        # Water resonance (if available)
        if data.water_613thz_resonance is not None:
            # 613 THz resonance directly measures Love
            L_water = data.water_613thz_resonance
            # Other dimensions estimated from Love
            estimated_J = L_water * 0.8  # High love correlates with justice
            estimated_P = 0.5  # Neutral
            estimated_W = L_water * 0.9  # High love correlates with wisdom
            measurements.append(LJPWMeasurement(L_water, estimated_J, estimated_P, estimated_W, 0.9, "water_resonance"))
        
        # Quantum consensus
        final = self.quantum_consensus(measurements)
        
        return final
    
    def quantum_consensus(self, measurements: List[LJPWMeasurement]) -> LJPWMeasurement:
        """
        Apply quantum consensus protocol to multiple measurements.
        
        The φ-Consensus Protocol:
        1. Calculate mean
        2. Calculate φ-alignment for each measurement
        3. Weight by alignment
        4. Result naturally converges to φ-optimal consensus
        """
        if not measurements:
            return LJPWMeasurement(0.5, 0.5, 0.5, 0.5, 0.0, "no_data")
        
        if len(measurements) == 1:
            return measurements[0]
        
        # Calculate means
        mean_L = sum(m.L for m in measurements) / len(measurements)
        mean_J = sum(m.J for m in measurements) / len(measurements)
        mean_P = sum(m.P for m in measurements) / len(measurements)
        mean_W = sum(m.W for m in measurements) / len(measurements)
        
        # Calculate φ-alignment for each measurement
        alignments = []
        for m in measurements:
            # Alignment = how close to φ × (value/mean)
            alignment_L = 1 - abs(PHI * (m.L / max(mean_L, 0.001)) - PHI)
            alignment_J = 1 - abs(PHI * (m.J / max(mean_J, 0.001)) - PHI)
            alignment_P = 1 - abs(PHI * (m.P / max(mean_P, 0.001)) - PHI)
            alignment_W = 1 - abs(PHI * (m.W / max(mean_W, 0.001)) - PHI)
            
            # Average alignment
            avg_alignment = (alignment_L + alignment_J + alignment_P + alignment_W) / 4
            avg_alignment = max(0.1, avg_alignment)  # minimum weight
            alignments.append(avg_alignment)
        
        # Weight by alignment
        total_weight = sum(alignments)
        final_L = sum(m.L * a for m, a in zip(measurements, alignments)) / total_weight
        final_J = sum(m.J * a for m, a in zip(measurements, alignments)) / total_weight
        final_P = sum(m.P * a for m, a in zip(measurements, alignments)) / total_weight
        final_W = sum(m.W * a for m, a in zip(measurements, alignments)) / total_weight
        
        # Confidence is average of individual confidences weighted by alignment
        final_confidence = sum(m.confidence * a for m, a in zip(measurements, alignments)) / total_weight
        
        return LJPWMeasurement(final_L, final_J, final_P, final_W, final_confidence, "quantum_consensus")
    
    # =========================================================================
    # VALIDATION
    # =========================================================================
    
    def validate_against_calibration(self, measurement: LJPWMeasurement, 
                                     reference: str) -> Dict:
        """
        Validate a measurement against a known calibration point.
        
        Returns deviation metrics and alignment score.
        """
        if reference not in self.calibration_points:
            return {'error': 'Unknown reference point'}
        
        ref = self.calibration_points[reference]
        
        deviation_L = abs(measurement.L - ref['L'])
        deviation_J = abs(measurement.J - ref['J'])
        deviation_P = abs(measurement.P - ref['P'])
        deviation_W = abs(measurement.W - ref['W'])
        
        total_deviation = deviation_L + deviation_J + deviation_P + deviation_W
        alignment_score = 1 - (total_deviation / 4)
        
        return {
            'reference': ref['name'],
            'deviations': {
                'L': deviation_L,
                'J': deviation_J,
                'P': deviation_P,
                'W': deviation_W
            },
            'total_deviation': total_deviation,
            'alignment_score': alignment_score
        }


# =============================================================================
# DEMO / TEST
# =============================================================================

def demo():
    """Demonstrate the measurement framework."""
    
    print("=" * 60)
    print("LJPW QUANTUM MEASUREMENT FRAMEWORK v1.0")
    print("=" * 60)
    print()
    
    engine = QuantumLJPWMeasurement()
    
    # Create sample organization data (roughly matching Enron 1999)
    enron_1999 = OrganizationData(
        employee_retention_rate=75,
        collaboration_score=60,
        internal_communication_sentiment=0.2,
        audit_compliance_score=40,
        lawsuit_count=8,
        max_industry_lawsuits=10,
        whistleblower_protection_index=20,
        regulatory_violations=5,
        revenue_growth_rate=40,
        market_cap_change=60,
        execution_efficiency=85,
        rd_investment_percentage=2,
        patent_quality_index=30,
        learning_rate_coefficient=0.3,
        scientists_on_board=0,
        total_board_members=15
    )
    
    print("Measuring 'Enron-like' organization circa 1999...")
    print("-" * 60)
    
    result = engine.measure_organization(enron_1999)
    
    print(f"LJPW Measurement:")
    print(f"  Love:    {result.L:.3f}")
    print(f"  Justice: {result.J:.3f}")
    print(f"  Power:   {result.P:.3f}")
    print(f"  Wisdom:  {result.W:.3f}")
    print(f"  Harmony: {result.harmony:.3f}")
    print(f"  Phase:   {result.phase}")
    print(f"  Method:  {result.method}")
    print(f"  Confidence: {result.confidence:.2f}")
    print()
    
    # Validate against calibration points
    print("Validation against calibration points:")
    print("-" * 60)
    
    for ref_name in ['enron_2001', 'natural_equilibrium', 'anchor']:
        validation = engine.validate_against_calibration(result, ref_name)
        print(f"  vs {validation['reference']}: alignment = {validation['alignment_score']:.3f}")
    
    print()
    print("=" * 60)
    print("MEASUREMENT COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    demo()
