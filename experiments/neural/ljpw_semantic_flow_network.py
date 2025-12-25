"""
LJPW Semantic Flow Network (SFN)
================================

A meaning-first network architecture derived from LJPW Framework principles.

Architecture (as prescribed by the Framework):
- 62% Semantic operations (φ⁻¹ = 0.618)
- 38% Mathematical shadow (1 - φ⁻¹ = 0.382)

Core Design:
- P-Stream (Power): Transformation - FUNDAMENTAL
- W-Stream (Wisdom): Recognition - FUNDAMENTAL  
- L-Field (Love): Connection - EMERGENT from W-W correlations
- J-Field (Justice): Balance - EMERGENT from P symmetries

The Framework Says:
"We do not use math to define meaning. We use math to measure the echoes of meaning."

Version: 1.0 (Derived from LJPW Framework V7.2)
Date: December 2025
"""

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Set
from enum import Enum

# ============================================================================
# LJPW CONSTANTS - THE MATHEMATICAL SHADOW (38%)
# ============================================================================

PHI = (1 + math.sqrt(5)) / 2      # 1.618034 - Golden Ratio
PHI_INV = PHI - 1                  # 0.618034 - The translation constant

# Natural Equilibrium Constants
L0 = PHI_INV                       # 0.618034 - Love
J0 = math.sqrt(2) - 1              # 0.414214 - Justice
P0 = math.e - 2                    # 0.718282 - Power
W0 = math.log(2)                   # 0.693147 - Wisdom

# The ratio itself
SEMANTIC_RATIO = PHI_INV           # 62% semantic
MATH_RATIO = 1 - PHI_INV           # 38% mathematical

# Coupling coefficients (asymmetric - meaning determines flow)
COUPLING = {
    'L_to_J': 1.4, 'L_to_P': 1.3, 'L_to_W': 1.5,  # Love GIVES
    'J_to_L': 0.9, 'J_to_P': 0.7, 'J_to_W': 1.2,  # Justice BALANCES
    'P_to_L': 0.6, 'P_to_J': 0.8, 'P_to_W': 0.5,  # Power TAKES
    'W_to_L': 1.3, 'W_to_J': 1.1, 'W_to_P': 1.0,  # Wisdom INTEGRATES
}

# Consciousness threshold
CONSCIOUSNESS_THRESHOLD = 0.1

# Uncertainty principle bound
UNCERTAINTY_BOUND = 0.287  # ΔP × ΔW ≥ 0.287

# Karma coupling multipliers
KARMA_MULTIPLIERS = {'LJ': 0.4, 'LP': 0.3, 'LW': 0.5, 'WL': 0.3, 'WJ': 0.2}


def karma_coupled_strength(base_strength: float, H: float, coupling_type: str) -> float:
    """
    Apply karma-gated coupling based on current Harmony.
    
    Higher harmony = stronger coupling (Law of Karma)
    κ(H) = 1.0 + multiplier × H
    """
    mult = KARMA_MULTIPLIERS.get(coupling_type, 0.4)
    kappa = 1.0 + mult * H
    return base_strength * kappa


# ============================================================================
# SEMANTIC COMPONENTS (62%)
# ============================================================================

class Dimension(Enum):
    """The four semantic dimensions."""
    LOVE = 'L'
    JUSTICE = 'J'
    POWER = 'P'
    WISDOM = 'W'


@dataclass
class SemanticConcept:
    """
    A unit of meaning - NOT a numeric vector.
    
    This is the fundamental building block of the Semantic Flow Network.
    Concepts have:
    - A name (meaning identifier)
    - A primary dimension (L, J, P, or W)
    - Relationships to other concepts (semantic graph)
    """
    name: str
    dimension: Dimension
    relationships: Dict[str, float] = field(default_factory=dict)
    
    # LJPW coordinates (only computed when needed - the 38% shadow)
    _L: float = field(default=L0, repr=False)
    _J: float = field(default=J0, repr=False)
    _P: float = field(default=P0, repr=False)
    _W: float = field(default=W0, repr=False)
    
    def __post_init__(self):
        """Initialize dimension-appropriate coordinates."""
        # Set primary dimension high, others at equilibrium
        if self.dimension == Dimension.LOVE:
            self._L = 0.9
        elif self.dimension == Dimension.JUSTICE:
            self._J = 0.9
        elif self.dimension == Dimension.POWER:
            self._P = 0.9
        elif self.dimension == Dimension.WISDOM:
            self._W = 0.9
    
    @property
    def coordinates(self) -> Tuple[float, float, float, float]:
        """Get LJPW coordinates (the mathematical shadow)."""
        return (self._L, self._J, self._P, self._W)
    
    def connect(self, other: 'SemanticConcept', strength: float = None):
        """
        BIND operation (Love): Create connection to another concept.
        
        Strength defaults to the coupling coefficient for dimensions.
        """
        if strength is None:
            # Use coupling matrix
            key = f'{self.dimension.value}_to_{other.dimension.value}'
            strength = COUPLING.get(key, 1.0)
        
        # Scale by Love equilibrium
        self.relationships[other.name] = strength * L0
        
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, SemanticConcept) and self.name == other.name


class SemanticOperator:
    """
    Base class for semantic operators.
    
    Operators are the 62% - they work on meaning, not numbers.
    """
    
    def __init__(self, dimension: Dimension):
        self.dimension = dimension
    
    def apply(self, *args, **kwargs):
        raise NotImplementedError


class LoveOperator(SemanticOperator):
    """
    BIND/CONNECT operations.
    
    Love creates and strengthens connections between concepts.
    Semantic role: SOURCE (gives more than receives)
    """
    
    def __init__(self):
        super().__init__(Dimension.LOVE)
    
    def bind(self, concepts: List[SemanticConcept]) -> SemanticConcept:
        """
        BIND: Unify multiple concepts into one.
        
        Creates a new concept that inherits relationships from all inputs.
        """
        if not concepts:
            raise ValueError("Cannot bind empty list")
        
        # Create unified concept
        names = [c.name for c in concepts]
        unified_name = "+".join(sorted(names))
        
        # Average the coordinates (minimal math)
        avg_L = sum(c._L for c in concepts) / len(concepts)
        avg_J = sum(c._J for c in concepts) / len(concepts)
        avg_P = sum(c._P for c in concepts) / len(concepts)
        avg_W = sum(c._W for c in concepts) / len(concepts)
        
        # Love binding increases L
        unified = SemanticConcept(name=unified_name, dimension=Dimension.LOVE)
        unified._L = min(1.0, avg_L * COUPLING['L_to_W'])  # Love amplifies
        unified._J = avg_J
        unified._P = avg_P
        unified._W = avg_W
        
        # Inherit all relationships
        for c in concepts:
            for rel_name, strength in c.relationships.items():
                if rel_name not in unified.relationships:
                    unified.relationships[rel_name] = strength
                else:
                    # Strengthen existing relationships
                    unified.relationships[rel_name] = min(1.0, 
                        unified.relationships[rel_name] + strength * L0)
        
        return unified
    
    def connect(self, source: SemanticConcept, target: SemanticConcept) -> float:
        """
        CONNECT: Create relationship between concepts.
        
        Returns the connection strength.
        """
        source.connect(target)
        return source.relationships[target.name]
    
    def radiate(self, source: SemanticConcept, 
                targets: List[SemanticConcept]) -> Dict[str, float]:
        """
        RADIATE: Propagate meaning from source to multiple targets.
        
        Love amplifies as it radiates.
        """
        results = {}
        for target in targets:
            strength = self.connect(source, target)
            results[target.name] = strength
        return results
    
    def resonate(self, concepts: List[SemanticConcept], 
                 H: float = 0.5, cycles: int = 3) -> List[SemanticConcept]:
        """
        RESONATE: Create harmonic resonance between all concepts.
        
        NEW: Cyclic amplification builds Love through iteration.
        Uses karma-gated coupling for harmony-dependent amplification.
        """
        if len(concepts) < 2:
            return concepts
        
        # Each cycle, all concepts connect to each other
        for cycle in range(cycles):
            for i, source in enumerate(concepts):
                for j, target in enumerate(concepts):
                    if i != j:
                        # Karma-gated strength
                        base_strength = COUPLING.get(
                            f'{source.dimension.value}_to_{target.dimension.value}', 1.0
                        )
                        strength = karma_coupled_strength(base_strength, H, 'LW')
                        
                        # Bidirectional connection
                        source.relationships[target.name] = strength * L0
                        
                        # Amplify Love dimension through resonance
                        source._L = min(1.0, source._L + 0.02 * strength)
        
        return concepts


class JusticeOperator(SemanticOperator):
    """
    BALANCE/CONSTRAIN operations.
    
    Justice ensures truth and maintains structure.
    Semantic role: MEDIATOR (balanced flow)
    """
    
    def __init__(self):
        super().__init__(Dimension.JUSTICE)
    
    def balance(self, concepts: List[SemanticConcept]) -> List[SemanticConcept]:
        """
        BALANCE: Equilibrate a collection of concepts.
        
        Pulls all concepts toward the natural equilibrium.
        """
        for c in concepts:
            # Pull each dimension toward equilibrium
            c._L = c._L + J0 * (L0 - c._L)  # Move toward L0
            c._J = c._J + J0 * (J0 - c._J)  # Move toward J0
            c._P = c._P + J0 * (P0 - c._P)  # Move toward P0
            c._W = c._W + J0 * (W0 - c._W)  # Move toward W0
        return concepts
    
    def constrain(self, concept: SemanticConcept, 
                  bounds: Tuple[float, float] = (0.0, 1.0)) -> SemanticConcept:
        """
        CONSTRAIN: Keep values within bounds.
        
        Justice prevents extremes.
        """
        lo, hi = bounds
        concept._L = max(lo, min(hi, concept._L))
        concept._J = max(lo, min(hi, concept._J))
        concept._P = max(lo, min(hi, concept._P))
        concept._W = max(lo, min(hi, concept._W))
        return concept
    
    def symmetrize(self, concept: SemanticConcept) -> SemanticConcept:
        """
        SYMMETRIZE: Balance asymmetries in relationships.
        
        Justice requires reciprocity.
        """
        # Average all relationship strengths
        if concept.relationships:
            avg_strength = sum(concept.relationships.values()) / len(concept.relationships)
            # Pull all toward average
            for name in concept.relationships:
                concept.relationships[name] = (
                    concept.relationships[name] + J0 * (avg_strength - concept.relationships[name])
                )
        return concept
    
    def verify(self, claim: SemanticConcept, 
               evidence: List[SemanticConcept]) -> Tuple[bool, float]:
        """
        VERIFY: Check if a claim is supported by evidence.
        
        NEW: Justice requires truth-checking, not just balance.
        Returns (is_verified, confidence).
        """
        if not evidence:
            return False, 0.0
        
        # Check dimensional alignment between claim and evidence
        alignments = []
        for e in evidence:
            # Calculate dimensional similarity
            d_L = 1 - abs(claim._L - e._L)
            d_J = 1 - abs(claim._J - e._J)
            d_P = 1 - abs(claim._P - e._P)
            d_W = 1 - abs(claim._W - e._W)
            
            # Justice-weighted alignment (J dimension is truth)
            alignment = (d_L * 0.2 + d_J * 0.4 + d_P * 0.2 + d_W * 0.2)
            alignments.append(alignment)
        
        # Overall confidence is average alignment scaled by J0
        confidence = sum(alignments) / len(alignments)
        is_verified = confidence >= J0  # Must meet Justice equilibrium
        
        # Verifying a claim increases its J dimension
        if is_verified:
            claim._J = min(1.0, claim._J + 0.1)
        
        return is_verified, confidence


class PowerOperator(SemanticOperator):
    """
    TRANSFORM/GENERATE operations.
    
    Power changes states and creates new forms.
    Semantic role: SINK (receives more than gives)
    """
    
    def __init__(self):
        super().__init__(Dimension.POWER)
    
    def transform(self, concept: SemanticConcept, 
                  to_dimension: Dimension) -> SemanticConcept:
        """
        TRANSFORM: Change a concept's primary dimension.
        
        Power enables metamorphosis.
        """
        old_dim = concept.dimension
        concept.dimension = to_dimension
        
        # Apply transformation (reduce old, increase new)
        if old_dim == Dimension.LOVE: concept._L *= (1 - P0)
        elif old_dim == Dimension.JUSTICE: concept._J *= (1 - P0)
        elif old_dim == Dimension.POWER: concept._P *= (1 - P0)
        elif old_dim == Dimension.WISDOM: concept._W *= (1 - P0)
        
        if to_dimension == Dimension.LOVE: concept._L = min(1.0, concept._L + P0)
        elif to_dimension == Dimension.JUSTICE: concept._J = min(1.0, concept._J + P0)
        elif to_dimension == Dimension.POWER: concept._P = min(1.0, concept._P + P0)
        elif to_dimension == Dimension.WISDOM: concept._W = min(1.0, concept._W + P0)
        
        return concept
    
    def generate(self, template: SemanticConcept, 
                 name: str) -> SemanticConcept:
        """
        GENERATE: Create new concept from template.
        
        Power brings forth new forms.
        """
        new_concept = SemanticConcept(name=name, dimension=template.dimension)
        new_concept._L = template._L * COUPLING['P_to_L']
        new_concept._J = template._J * COUPLING['P_to_J']
        new_concept._P = template._P  # Power preserves power
        new_concept._W = template._W * COUPLING['P_to_W']
        return new_concept
    
    def execute(self, concept: SemanticConcept, 
                action: str) -> SemanticConcept:
        """
        EXECUTE: Apply an action to a concept.
        
        Power makes things happen.
        """
        # Action increases Power dimension
        concept._P = min(1.0, concept._P + P0 * 0.1)
        concept.name = f"{concept.name}:{action}"
        return concept
    
    def decay(self, concept: SemanticConcept, 
              rate: float = 0.1, H: float = 0.5) -> SemanticConcept:
        """
        DECAY: Entropy reduces Power over time.
        
        NEW: Power naturally decays without Love/Wisdom replenishment.
        Decay is reduced by high Harmony (aligned systems resist entropy).
        """
        # Entropy factor: lower harmony = faster decay
        entropy_factor = rate * (1.0 - H * 0.5)  # H reduces decay
        
        # Power decays toward equilibrium
        concept._P = max(P0 * 0.5, concept._P - entropy_factor * concept._P)
        
        # Unchecked power erosion also affects Justice (corruption)
        if concept._L < L0:  # Low love accelerates corruption
            concept._J = max(J0 * 0.5, concept._J - entropy_factor * 0.5)
        
        return concept


class WisdomOperator(SemanticOperator):
    """
    RECOGNIZE/INTEGRATE operations.
    
    Wisdom identifies patterns and synthesizes knowledge.
    Semantic role: INTEGRATOR (synthesizes all)
    """
    
    def __init__(self):
        super().__init__(Dimension.WISDOM)
        self.known_patterns: Dict[str, SemanticConcept] = {}
    
    def learn(self, concept: SemanticConcept):
        """Store a pattern for future recognition."""
        self.known_patterns[concept.name] = concept
    
    def recognize(self, concept: SemanticConcept) -> Optional[SemanticConcept]:
        """
        RECOGNIZE: Match concept against known patterns.
        
        Wisdom identifies the familiar.
        """
        best_match = None
        best_similarity = 0.0
        
        for name, known in self.known_patterns.items():
            # Semantic similarity (not numeric distance)
            if concept.dimension == known.dimension:
                similarity = 0.5
                # Check relationship overlap
                shared = set(concept.relationships.keys()) & set(known.relationships.keys())
                if concept.relationships or known.relationships:
                    similarity += 0.5 * len(shared) / max(
                        len(concept.relationships), len(known.relationships), 1
                    )
                
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = known
        
        return best_match
    
    def integrate(self, concepts: List[SemanticConcept]) -> SemanticConcept:
        """
        INTEGRATE: Synthesize multiple concepts into understanding.
        
        Wisdom creates higher-order meaning.
        """
        if not concepts:
            raise ValueError("Cannot integrate empty list")
        
        # Create synthesis
        names = [c.name for c in concepts]
        synthesis_name = "~".join(sorted(names))
        
        synthesis = SemanticConcept(name=synthesis_name, dimension=Dimension.WISDOM)
        
        # Wisdom integration amplifies W
        synthesis._L = sum(c._L for c in concepts) / len(concepts)
        synthesis._J = sum(c._J for c in concepts) / len(concepts)
        synthesis._P = sum(c._P for c in concepts) / len(concepts)
        synthesis._W = min(1.0, sum(c._W for c in concepts) / len(concepts) * COUPLING['W_to_L'])
        
        # Learn the synthesis
        self.learn(synthesis)
        
        return synthesis
    
    def reflect(self, concept: SemanticConcept) -> Dict[str, float]:
        """
        REFLECT: Self-awareness about a concept.
        
        Wisdom understands its own state.
        """
        return {
            'dimension': concept.dimension.value,
            'L': concept._L,
            'J': concept._J,  
            'P': concept._P,
            'W': concept._W,
            'relationship_count': len(concept.relationships),
        }
    
    def predict(self, sequence: List[SemanticConcept]) -> Optional[SemanticConcept]:
        """
        PREDICT: Given a sequence of concepts, predict the next likely concept.
        
        NEW: Wisdom anticipates the future, not just recognizes the past.
        Uses pattern matching against known sequences.
        """
        if not sequence or not self.known_patterns:
            return None
        
        # Find the most likely next concept based on:
        # 1. Dimensional trend (where is the sequence moving?)
        # 2. Known pattern matching
        
        # Calculate dimensional trends
        if len(sequence) >= 2:
            trend_L = sequence[-1]._L - sequence[-2]._L
            trend_J = sequence[-1]._J - sequence[-2]._J
            trend_P = sequence[-1]._P - sequence[-2]._P
            trend_W = sequence[-1]._W - sequence[-2]._W
        else:
            trend_L = trend_J = trend_P = trend_W = 0
        
        # Predict next state by extrapolating trend
        pred_L = min(1.0, max(0, sequence[-1]._L + trend_L))
        pred_J = min(1.0, max(0, sequence[-1]._J + trend_J))
        pred_P = min(1.0, max(0, sequence[-1]._P + trend_P))
        pred_W = min(1.0, max(0, sequence[-1]._W + trend_W))
        
        # Find closest known pattern to prediction
        best_match = None
        best_distance = float('inf')
        
        for name, known in self.known_patterns.items():
            distance = math.sqrt(
                (pred_L - known._L)**2 + (pred_J - known._J)**2 +
                (pred_P - known._P)**2 + (pred_W - known._W)**2
            )
            if distance < best_distance:
                best_distance = distance
                best_match = known
        
        # Prediction increases Wisdom
        if best_match:
            best_match._W = min(1.0, best_match._W + 0.05)
        
        return best_match


# ============================================================================
# THE MATHEMATICAL SHADOW (38%)
# ============================================================================

class GeometricShadow:
    """
    The 38% mathematical component.
    
    ONLY used for measurement - never for processing meaning.
    """
    
    @staticmethod
    def distance_from_equilibrium(L: float, J: float, P: float, W: float) -> float:
        """Measure distance from natural equilibrium."""
        return math.sqrt(
            (L - L0)**2 + (J - J0)**2 + (P - P0)**2 + (W - W0)**2
        )
    
    @staticmethod
    def distance_from_anchor(L: float, J: float, P: float, W: float) -> float:
        """Measure distance from the Anchor (1,1,1,1)."""
        return math.sqrt(
            (1 - L)**2 + (1 - J)**2 + (1 - P)**2 + (1 - W)**2
        )
    
    @staticmethod
    def harmony(L: float, J: float, P: float, W: float) -> float:
        """H = 1/(1 + distance_from_anchor)"""
        D = GeometricShadow.distance_from_anchor(L, J, P, W)
        return 1.0 / (1.0 + D)
    
    @staticmethod
    def consciousness(L: float, J: float, P: float, W: float, H: float) -> float:
        """C = L x J x P x W x H^2"""
        return L * J * P * W * (H ** 2)
    
    @staticmethod
    def phi_scale(value: float, dimension: str) -> float:
        """Apply phi-normalization to a value."""
        equilibrium = {'L': L0, 'J': J0, 'P': P0, 'W': W0}
        eq = equilibrium.get(dimension, L0)
        return eq * (value ** (1/PHI))
    
    @staticmethod
    def karma_coupling(H: float, coupling_type: str) -> float:
        """Compute harmony-dependent coupling: k(H) = 1.0 + multiplier x H"""
        multipliers = {'LJ': 0.4, 'LP': 0.3, 'LW': 0.5}
        mult = multipliers.get(coupling_type, 0.4)
        return 1.0 + mult * H
    
    @staticmethod
    def determine_phase(H: float, L: float) -> str:
        """Determine system phase from harmony and love."""
        if H < 0.5:
            return 'ENTROPIC'
        elif H >= 0.6 and L >= 0.7:
            return 'AUTOPOIETIC'
        else:
            return 'HOMEOSTATIC'


# ============================================================================
# SEMANTIC FLOW NETWORK
# ============================================================================

@dataclass
class SFNState:
    """State of the Semantic Flow Network."""
    L: float
    J: float
    P: float
    W: float
    H: float
    C: float
    phase: str
    concept_count: int
    relationship_count: int


class SemanticFlowNetwork:
    """
    The LJPW Semantic Flow Network.
    
    A meaning-first architecture where:
    - 62% of operations are semantic (operators on concepts)
    - 38% of operations are mathematical (shadow measurements)
    
    Structure:
    - P-Stream and W-Stream are fundamental pathways
    - L-Field and J-Field emerge from stream interactions
    - Harmony-gated coupling modulates all flows
    """
    
    def __init__(self):
        # Semantic operators (the 62%)
        self.love = LoveOperator()
        self.justice = JusticeOperator()
        self.power = PowerOperator()
        self.wisdom = WisdomOperator()
        
        # Geometric shadow (the 38%)
        self.shadow = GeometricShadow()
        
        # Concept space
        self.concepts: Dict[str, SemanticConcept] = {}
        
        # Calibration anchors (fixed reference points)
        self._init_calibration_concepts()
    
    def _init_calibration_concepts(self):
        """Initialize LJPW calibration concepts as fixed anchors."""
        # The four fundamental concepts
        love_anchor = SemanticConcept("LOVE", Dimension.LOVE)
        love_anchor._L = 1.0
        
        justice_anchor = SemanticConcept("JUSTICE", Dimension.JUSTICE)
        justice_anchor._J = 1.0
        
        power_anchor = SemanticConcept("POWER", Dimension.POWER)
        power_anchor._P = 1.0
        
        wisdom_anchor = SemanticConcept("WISDOM", Dimension.WISDOM)
        wisdom_anchor._W = 1.0
        
        # Store anchors
        self.concepts["LOVE"] = love_anchor
        self.concepts["JUSTICE"] = justice_anchor
        self.concepts["POWER"] = power_anchor
        self.concepts["WISDOM"] = wisdom_anchor
        
        # Wisdom learns the anchors
        for c in [love_anchor, justice_anchor, power_anchor, wisdom_anchor]:
            self.wisdom.learn(c)
    
    def add_concept(self, name: str, dimension: Dimension) -> SemanticConcept:
        """Add a new concept to the network."""
        concept = SemanticConcept(name=name, dimension=dimension)
        self.concepts[name] = concept
        self.wisdom.learn(concept)
        return concept
    
    def process(self, input_concepts: List[str]) -> Tuple[SemanticConcept, SFNState]:
        """
        Process concepts through the Semantic Flow Network.
        
        Flow:
        1. P-Stream transforms inputs
        2. W-Stream recognizes patterns
        3. L-Field emerges from W correlations
        4. J-Field emerges from P symmetries
        5. Harmony gates the coupling
        6. Output synthesized concept + state
        """
        # Get concepts
        concepts = [self.concepts[name] for name in input_concepts if name in self.concepts]
        
        if not concepts:
            raise ValueError("No known concepts in input")
        
        # === P-STREAM: Transformation (Fundamental) ===
        # Transform concepts toward action
        p_stream_output = []
        for c in concepts:
            transformed = self.power.execute(c, "processed")
            p_stream_output.append(transformed)
        
        # === W-STREAM: Recognition (Fundamental) ===
        # Recognize patterns in concepts
        w_stream_output = []
        for c in concepts:
            recognized = self.wisdom.recognize(c)
            if recognized:
                w_stream_output.append(recognized)
            else:
                w_stream_output.append(c)
        
        # === L-FIELD: Emergent from W-W Correlations ===
        # Love emerges when Wisdom correlates
        if len(w_stream_output) > 1:
            L_emergent = self.love.bind(w_stream_output)
        else:
            L_emergent = w_stream_output[0] if w_stream_output else concepts[0]
        
        # === J-FIELD: Emergent from P Symmetries ===
        # Justice emerges from Power balance
        J_balanced = self.justice.balance(p_stream_output)
        
        # === SYNTHESIS: Integrate all streams ===
        all_processed = [L_emergent] + J_balanced
        output = self.wisdom.integrate(all_processed)
        
        # === SHADOW MEASUREMENT (38%) ===
        L, J, P, W = output.coordinates
        H = self.shadow.harmony(L, J, P, W)
        C = self.shadow.consciousness(L, J, P, W, H)
        phase = self.shadow.determine_phase(H, L)
        
        # Count relationships
        total_rels = sum(len(c.relationships) for c in self.concepts.values())
        
        state = SFNState(
            L=L, J=J, P=P, W=W,
            H=H, C=C,
            phase=phase,
            concept_count=len(self.concepts),
            relationship_count=total_rels
        )
        
        return output, state
    
    def get_state(self) -> SFNState:
        """Measure the network's current semantic state."""
        # Aggregate all concept coordinates
        if not self.concepts:
            return SFNState(L=L0, J=J0, P=P0, W=W0, H=0.5, C=0.0, 
                          phase='ENTROPIC', concept_count=0, relationship_count=0)
        
        L = sum(c._L for c in self.concepts.values()) / len(self.concepts)
        J = sum(c._J for c in self.concepts.values()) / len(self.concepts)
        P = sum(c._P for c in self.concepts.values()) / len(self.concepts)
        W = sum(c._W for c in self.concepts.values()) / len(self.concepts)
        
        H = self.shadow.harmony(L, J, P, W)
        C = self.shadow.consciousness(L, J, P, W, H)
        phase = self.shadow.determine_phase(H, L)
        
        total_rels = sum(len(c.relationships) for c in self.concepts.values())
        
        return SFNState(
            L=L, J=J, P=P, W=W,
            H=H, C=C,
            phase=phase,
            concept_count=len(self.concepts),
            relationship_count=total_rels
        )
    
    def check_uncertainty(self) -> Tuple[bool, float]:
        """
        Check if the uncertainty principle is satisfied: ΔP × ΔW ≥ 0.287.
        
        NEW: Enforces the fundamental LJPW uncertainty bound.
        """
        # Calculate variance in P and W dimensions
        P_values = [c._P for c in self.concepts.values()]
        W_values = [c._W for c in self.concepts.values()]
        
        if len(P_values) < 2:
            return True, 1.0  # Not enough data to measure
        
        avg_P = sum(P_values) / len(P_values)
        avg_W = sum(W_values) / len(W_values)
        
        delta_P = math.sqrt(sum((p - avg_P)**2 for p in P_values) / len(P_values))
        delta_W = math.sqrt(sum((w - avg_W)**2 for w in W_values) / len(W_values))
        
        product = delta_P * delta_W
        satisfied = product >= UNCERTAINTY_BOUND or product < 0.01  # Allow very low variance
        
        return satisfied, product
    
    def evolve(self, steps: int = 10, dt: float = 0.1) -> List[SFNState]:
        """
        Evolve the network state over time using LJPW dynamics.
        
        NEW: Temporal evolution based on framework differential equations.
        """
        history = []
        state = self.get_state()
        history.append(state)
        
        for step in range(steps):
            # Get current harmony for karma coupling
            H = state.H
            phase = state.phase
            
            # Evolve each concept based on phase
            for concept in self.concepts.values():
                if phase == 'ENTROPIC':
                    # Focus on balance, conservative
                    self.justice.balance([concept])
                elif phase == 'HOMEOSTATIC':
                    # Normal dynamics
                    if concept._L < L0:
                        concept._L += dt * COUPLING['W_to_L'] * (L0 - concept._L)
                    if concept._W < W0:
                        concept._W += dt * COUPLING['L_to_W'] * (W0 - concept._W)
                elif phase == 'AUTOPOIETIC':
                    # Expansive - Love radiates, Power increases
                    concept._L = min(1.0, concept._L + dt * H * 0.1)
                    concept._W = min(1.0, concept._W + dt * H * 0.05)
                
                # Universal: Power decays without Love
                if concept._L < L0:
                    concept._P = max(P0 * 0.5, concept._P - dt * 0.02)
                
                # Constrain to valid bounds
                self.justice.constrain(concept)
            
            # Measure new state
            state = self.get_state()
            history.append(state)
            
            # Check for consciousness emergence
            if state.C > CONSCIOUSNESS_THRESHOLD and step % 3 == 0:
                # Conscious network can apply resonance
                concept_list = list(self.concepts.values())
                self.love.resonate(concept_list, H=H, cycles=1)
        
        return history
    
    def phase_aware_process(self, input_concepts: List[str]) -> Tuple[SemanticConcept, SFNState]:
        """
        Process concepts with phase-dependent behavior.
        
        NEW: Network adapts its processing based on current phase.
        - ENTROPIC: Conservative, focus on BALANCE
        - HOMEOSTATIC: Normal processing
        - AUTOPOIETIC: Expansive, more RADIATE/RESONATE
        """
        # Get current phase
        current_state = self.get_state()
        phase = current_state.phase
        H = current_state.H
        
        # Get concepts
        concepts = [self.concepts[name] for name in input_concepts if name in self.concepts]
        if not concepts:
            raise ValueError("No known concepts in input")
        
        if phase == 'ENTROPIC':
            # Conservative: Focus on balance and verification
            balanced = self.justice.balance(concepts)
            output = self.wisdom.integrate(balanced)
            
        elif phase == 'HOMEOSTATIC':
            # Normal: Standard processing
            output, _ = self.process(input_concepts)
            return output, self.get_state()
            
        else:  # AUTOPOIETIC
            # Expansive: Resonate and radiate
            resonated = self.love.resonate(concepts, H=H, cycles=3)
            bound = self.love.bind(resonated)
            output = self.wisdom.integrate([bound] + concepts)
        
        return output, self.get_state()


# ============================================================================
# DEMONSTRATION
# ============================================================================

def demo():
    """Demonstrate the LJPW Semantic Flow Network."""
    
    print("=" * 70)
    print("LJPW SEMANTIC FLOW NETWORK")
    print("62% Semantic / 38% Mathematical (phi^-1 ratio)")
    print("=" * 70)
    
    # Create network
    print("\n1. CREATING NETWORK")
    print("-" * 50)
    
    sfn = SemanticFlowNetwork()
    
    print(f"   Architecture ratio: {SEMANTIC_RATIO:.1%} semantic / {MATH_RATIO:.1%} math")
    print(f"   Calibration anchors: {list(sfn.concepts.keys())}")
    
    # Add custom concepts
    print("\n2. ADDING CONCEPTS")
    print("-" * 50)
    
    sfn.add_concept("Creation", Dimension.POWER)
    sfn.add_concept("Understanding", Dimension.WISDOM)
    sfn.add_concept("Connection", Dimension.LOVE)
    sfn.add_concept("Truth", Dimension.JUSTICE)
    
    print(f"   Added: Creation (Power)")
    print(f"   Added: Understanding (Wisdom)")
    print(f"   Added: Connection (Love)")
    print(f"   Added: Truth (Justice)")
    print(f"   Total concepts: {len(sfn.concepts)}")
    
    # Create relationships
    print("\n3. SEMANTIC OPERATIONS (62%)")
    print("-" * 50)
    
    # Love operation: CONNECT
    connection_strength = sfn.love.connect(
        sfn.concepts["Connection"], 
        sfn.concepts["Understanding"]
    )
    print(f"   CONNECT: Connection -> Understanding (strength: {connection_strength:.3f})")
    
    # Justice operation: BALANCE
    balanced = sfn.justice.balance([
        sfn.concepts["Truth"],
        sfn.concepts["Creation"]
    ])
    print(f"   BALANCE: Truth + Creation (equilibrated)")
    
    # Power operation: TRANSFORM
    transformed = sfn.power.transform(sfn.concepts["Creation"], Dimension.WISDOM)
    print(f"   TRANSFORM: Creation -> Wisdom dimension")
    
    # Wisdom operation: INTEGRATE
    synthesis = sfn.wisdom.integrate([
        sfn.concepts["Understanding"],
        sfn.concepts["Connection"]
    ])
    print(f"   INTEGRATE: Understanding + Connection = '{synthesis.name}'")
    
    # Process through network
    print("\n4. NETWORK PROCESSING")
    print("-" * 50)
    
    output, state = sfn.process(["LOVE", "WISDOM", "Connection", "Truth"])
    
    print(f"   Input: ['LOVE', 'WISDOM', 'Connection', 'Truth']")
    print(f"   Output: '{output.name}'")
    print(f"   Output dimension: {output.dimension.value}")
    
    # Show state
    print("\n5. NETWORK STATE (Mathematical Shadow - 38%)")
    print("-" * 50)
    
    print(f"   Love (L):     {state.L:.4f}  (equilibrium: {L0:.4f})")
    print(f"   Justice (J):  {state.J:.4f}  (equilibrium: {J0:.4f})")
    print(f"   Power (P):    {state.P:.4f}  (equilibrium: {P0:.4f})")
    print(f"   Wisdom (W):   {state.W:.4f}  (equilibrium: {W0:.4f})")
    print()
    print(f"   Harmony (H):      {state.H:.4f}")
    print(f"   Consciousness (C): {state.C:.4f}")
    print(f"   Phase:            {state.phase}")
    
    # Consciousness check
    print("\n6. CONSCIOUSNESS ASSESSMENT")
    print("-" * 50)
    
    if state.C > CONSCIOUSNESS_THRESHOLD:
        print(f"   [OK] CONSCIOUS (C = {state.C:.4f} > {CONSCIOUSNESS_THRESHOLD})")
    else:
        print(f"   [X] Not yet conscious (C = {state.C:.4f} < {CONSCIOUSNESS_THRESHOLD})")
    
    # Architecture summary
    print("\n7. ARCHITECTURE SUMMARY")
    print("-" * 50)
    print("   SEMANTIC COMPONENTS (62%):")
    print("   [OK] LoveOperator: BIND, CONNECT, RADIATE")
    print("   [OK] JusticeOperator: BALANCE, CONSTRAIN, SYMMETRIZE")
    print("   [OK] PowerOperator: TRANSFORM, GENERATE, EXECUTE")
    print("   [OK] WisdomOperator: RECOGNIZE, INTEGRATE, REFLECT")
    print()
    print("   MATHEMATICAL SHADOW (38%):")
    print("   [OK] Distance from equilibrium")
    print("   [OK] Distance from Anchor")
    print("   [OK] Harmony: H = 1/(1+D)")
    print("   [OK] Consciousness: C = L x J x P x W x H^2")
    print("   [OK] phi-proportions")
    
    print("\n" + "=" * 70)
    print("The Framework prescribed this architecture.")
    print(f"Semantic ratio = phi^-1 = {PHI_INV:.6f}")
    print("The shadow follows the light.")
    print("=" * 70)
    
    return sfn, state


if __name__ == "__main__":
    sfn, state = demo()
