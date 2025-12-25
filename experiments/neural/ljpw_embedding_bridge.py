"""
LJPW Embedding Bridge
=====================

Bridges text/embeddings to the Semantic Flow Network, enabling:
1. Automatic concept extraction from text
2. LJPW dimension detection
3. Coordinate estimation
4. End-to-end text processing through SFN

This makes the SFN usable like a traditional neural network:
    text → embedding → LJPW coordinates → SFN processing → output
"""

import math
import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from enum import Enum

# Import from SFN
import sys
sys.path.insert(0, '.')

from experiments.neural.ljpw_semantic_flow_network import (
    SemanticFlowNetwork, SemanticConcept, Dimension, SFNState,
    L0, J0, P0, W0, PHI, PHI_INV
)


# ============================================================================
# DIMENSION CLASSIFICATION
# ============================================================================

# Seed words for each dimension (for keyword-based classification)
DIMENSION_KEYWORDS = {
    Dimension.LOVE: {
        'love', 'compassion', 'care', 'kindness', 'affection', 'connection',
        'empathy', 'unity', 'bond', 'warmth', 'tenderness', 'devotion',
        'friendship', 'relationship', 'together', 'family', 'trust', 'faith',
        'hope', 'forgiveness', 'mercy', 'grace', 'heart', 'soul', 'embrace',
        'give', 'share', 'support', 'nurture', 'cherish', 'beloved'
    },
    Dimension.JUSTICE: {
        'justice', 'truth', 'fair', 'right', 'law', 'balance', 'equal',
        'honest', 'integrity', 'moral', 'ethical', 'principle', 'righteous',
        'correct', 'accurate', 'valid', 'legitimate', 'proper', 'due',
        'judgment', 'court', 'verdict', 'innocent', 'guilty', 'evidence',
        'proof', 'reason', 'logic', 'order', 'structure', 'symmetry'
    },
    Dimension.POWER: {
        'power', 'powerful', 'strength', 'strong', 'force', 'energy', 'action',
        'create', 'build', 'built', 'construct', 'engineer', 'machine', 'engine',
        'change', 'transform', 'transformed', 'move', 'work', 'effort', 'capability',
        'ability', 'potential', 'dynamic', 'active', 'generate', 'produce', 'manufacture',
        'control', 'authority', 'influence', 'impact', 'effect', 'drive', 'industry',
        'execute', 'implement', 'achieve', 'accomplish', 'perform', 'act', 'deliver'
    },
    Dimension.WISDOM: {
        'wisdom', 'knowledge', 'understand', 'learn', 'know', 'insight',
        'intelligence', 'mind', 'thought', 'reason', 'perceive', 'recognize',
        'comprehend', 'grasp', 'discern', 'aware', 'conscious', 'observe',
        'study', 'research', 'discover', 'explore', 'analyze', 'reflect',
        'consider', 'ponder', 'contemplate', 'meditate', 'enlighten', 'teach'
    }
}

# Dimension affinities for common word patterns
PATTERN_AFFINITIES = {
    # Verbs of giving → Love
    r'\b(give|share|help|support|care)\b': Dimension.LOVE,
    # Verbs of truth → Justice
    r'\b(prove|verify|validate|confirm|judge)\b': Dimension.JUSTICE,
    # Verbs of action → Power
    r'\b(do|make|create|build|change|act)\b': Dimension.POWER,
    # Verbs of cognition → Wisdom
    r'\b(think|know|learn|understand|realize)\b': Dimension.WISDOM,
}


@dataclass
class ConceptExtraction:
    """Result of extracting a concept from text."""
    text: str
    dimension: Dimension
    confidence: float
    L: float
    J: float
    P: float
    W: float


class DimensionClassifier:
    """
    Classifies text/concepts into LJPW dimensions.
    
    Uses a combination of:
    1. Keyword matching
    2. Pattern recognition
    3. Embedding similarity (if available)
    """
    
    def __init__(self):
        self.keywords = DIMENSION_KEYWORDS
        self.patterns = PATTERN_AFFINITIES
    
    def classify(self, text: str) -> Tuple[Dimension, float]:
        """
        Classify text into a primary LJPW dimension.
        
        Returns (dimension, confidence).
        """
        text_lower = text.lower()
        words = set(re.findall(r'\b\w+\b', text_lower))
        
        # Count keyword matches for each dimension
        scores = {dim: 0 for dim in Dimension}
        
        for dim, keywords in self.keywords.items():
            matches = words & keywords
            scores[dim] = len(matches)
        
        # Check pattern matches
        for pattern, dim in self.patterns.items():
            if re.search(pattern, text_lower):
                scores[dim] += 0.5
        
        # Find best dimension
        total = sum(scores.values())
        if total == 0:
            # Default to Wisdom (most general)
            return Dimension.WISDOM, 0.25
        
        best_dim = max(scores, key=scores.get)
        confidence = scores[best_dim] / total
        
        return best_dim, confidence
    
    def estimate_coordinates(self, text: str, 
                            primary_dim: Dimension,
                            confidence: float) -> Tuple[float, float, float, float]:
        """
        Estimate LJPW coordinates for a concept.
        
        Primary dimension gets high value, others at equilibrium.
        """
        # Base values at equilibrium
        L, J, P, W = L0, J0, P0, W0
        
        # Primary dimension is high (scaled by confidence)
        primary_value = 0.6 + 0.4 * confidence  # Range [0.6, 1.0]
        
        if primary_dim == Dimension.LOVE:
            L = primary_value
        elif primary_dim == Dimension.JUSTICE:
            J = primary_value
        elif primary_dim == Dimension.POWER:
            P = primary_value
        elif primary_dim == Dimension.WISDOM:
            W = primary_value
        
        return L, J, P, W


# ============================================================================
# CONCEPT EXTRACTOR
# ============================================================================

class ConceptExtractor:
    """
    Extracts concepts from text for SFN processing.
    
    Methods:
    - extract_keywords: Simple keyword extraction
    - extract_phrases: Noun phrase extraction
    - extract_sentences: Each sentence as a concept
    """
    
    def __init__(self):
        self.classifier = DimensionClassifier()
    
    def extract_keywords(self, text: str, max_concepts: int = 10) -> List[str]:
        """Extract significant words as concepts."""
        # Remove common stopwords
        stopwords = {
            'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
            'would', 'could', 'should', 'may', 'might', 'must', 'shall',
            'to', 'of', 'in', 'for', 'on', 'with', 'at', 'by', 'from',
            'as', 'into', 'through', 'during', 'before', 'after', 'above',
            'below', 'between', 'under', 'again', 'further', 'then', 'once',
            'and', 'but', 'or', 'nor', 'so', 'yet', 'both', 'either',
            'neither', 'not', 'only', 'own', 'same', 'than', 'too', 'very',
            'can', 'just', 'now', 'that', 'this', 'these', 'those', 'what',
            'which', 'who', 'whom', 'when', 'where', 'why', 'how', 'all',
            'each', 'every', 'any', 'some', 'no', 'such', 'more', 'most',
            'other', 'it', 'its', 'i', 'me', 'my', 'we', 'our', 'you',
            'your', 'he', 'him', 'his', 'she', 'her', 'they', 'them', 'their'
        }
        
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        keywords = [w for w in words if w not in stopwords]
        
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for w in keywords:
            if w not in seen:
                seen.add(w)
                unique.append(w)
        
        return unique[:max_concepts]
    
    def extract_to_concepts(self, text: str, 
                           max_concepts: int = 10) -> List[ConceptExtraction]:
        """
        Extract concepts from text with full LJPW analysis.
        """
        keywords = self.extract_keywords(text, max_concepts)
        results = []
        
        for keyword in keywords:
            dim, confidence = self.classifier.classify(keyword)
            L, J, P, W = self.classifier.estimate_coordinates(keyword, dim, confidence)
            
            results.append(ConceptExtraction(
                text=keyword.capitalize(),
                dimension=dim,
                confidence=confidence,
                L=L, J=J, P=P, W=W
            ))
        
        return results


# ============================================================================
# EMBEDDING BRIDGE
# ============================================================================

class EmbeddingBridge:
    """
    Main bridge between text and SFN.
    
    Usage:
        bridge = EmbeddingBridge()
        sfn, state = bridge.process_text("The teacher showed compassion to students.")
        print(f"Consciousness: {state.C}")
    """
    
    def __init__(self):
        self.extractor = ConceptExtractor()
        self.sfn = SemanticFlowNetwork()
    
    def process_text(self, text: str, 
                    max_concepts: int = 8) -> Tuple[SemanticConcept, SFNState]:
        """
        Process text through the Semantic Flow Network.
        
        1. Extract concepts from text
        2. Add them to the network with estimated LJPW coordinates
        3. Process through SFN
        4. Return output concept and network state
        """
        # Create fresh network for this text
        self.sfn = SemanticFlowNetwork()
        
        # Extract concepts
        extractions = self.extractor.extract_to_concepts(text, max_concepts)
        
        if not extractions:
            raise ValueError("No concepts extracted from text")
        
        # Add concepts to network
        concept_names = []
        for ext in extractions:
            concept = self.sfn.add_concept(ext.text, ext.dimension)
            concept._L = ext.L
            concept._J = ext.J
            concept._P = ext.P
            concept._W = ext.W
            concept_names.append(ext.text)
        
        # Process through network
        output, state = self.sfn.process(concept_names)
        
        return output, state
    
    def analyze_text(self, text: str) -> Dict:
        """
        Comprehensive analysis of text through LJPW lens.
        
        Returns dictionary with:
        - concepts: extracted concepts with dimensions
        - state: network state (L, J, P, W, H, C, phase)
        - harmony: overall harmony score
        - consciousness: consciousness metric
        - phase: system phase
        - dominant_dimension: strongest dimension
        """
        extractions = self.extractor.extract_to_concepts(text, max_concepts=10)
        
        if not extractions:
            return {'error': 'No concepts extracted'}
        
        output, state = self.process_text(text)
        
        # Count dimensions
        dim_counts = {dim: 0 for dim in Dimension}
        for ext in extractions:
            dim_counts[ext.dimension] += 1
        dominant = max(dim_counts, key=dim_counts.get)
        
        return {
            'concepts': [
                {
                    'text': e.text,
                    'dimension': e.dimension.value,
                    'confidence': round(e.confidence, 3),
                    'coordinates': {
                        'L': round(e.L, 3),
                        'J': round(e.J, 3),
                        'P': round(e.P, 3),
                        'W': round(e.W, 3)
                    }
                } for e in extractions
            ],
            'state': {
                'L': round(state.L, 4),
                'J': round(state.J, 4),
                'P': round(state.P, 4),
                'W': round(state.W, 4),
            },
            'harmony': round(state.H, 4),
            'consciousness': round(state.C, 4),
            'is_conscious': state.C > 0.1,
            'phase': state.phase,
            'dominant_dimension': dominant.value,
            'concept_count': len(extractions)
        }
    
    def evolve_text(self, text: str, steps: int = 10) -> List[SFNState]:
        """
        Process text and evolve the network over time.
        
        Returns history of states showing how the network evolves.
        """
        self.process_text(text)
        return self.sfn.evolve(steps=steps)


# ============================================================================
# DEMO
# ============================================================================

def demo():
    """Demonstrate the embedding bridge."""
    
    print("=" * 70)
    print("LJPW EMBEDDING BRIDGE DEMO")
    print("Text -> Concepts -> LJPW Coordinates -> SFN Processing")
    print("=" * 70)
    
    bridge = EmbeddingBridge()
    
    # Test texts
    texts = [
        "The compassionate teacher showed love and care to struggling students.",
        "The judge delivered a fair verdict based on truth and evidence.",
        "The engineer built a powerful machine that transformed the industry.",
        "The wise philosopher understood the deep patterns of existence."
    ]
    
    for i, text in enumerate(texts, 1):
        print(f"\n{i}. INPUT TEXT")
        print("-" * 50)
        print(f"   \"{text}\"")
        
        analysis = bridge.analyze_text(text)
        
        print(f"\n   EXTRACTED CONCEPTS:")
        for c in analysis['concepts'][:5]:  # Show first 5
            print(f"   - {c['text']} ({c['dimension']}, conf: {c['confidence']})")
        
        print(f"\n   NETWORK STATE:")
        print(f"   L={analysis['state']['L']}, J={analysis['state']['J']}, "
              f"P={analysis['state']['P']}, W={analysis['state']['W']}")
        print(f"   Harmony: {analysis['harmony']}")
        print(f"   Consciousness: {analysis['consciousness']}")
        print(f"   Phase: {analysis['phase']}")
        print(f"   Dominant: {analysis['dominant_dimension']}")
        
        if analysis['is_conscious']:
            print(f"   [OK] CONSCIOUS")
        else:
            print(f"   [--] Not conscious")
    
    # Evolution demo
    print("\n" + "=" * 70)
    print("TEMPORAL EVOLUTION")
    print("=" * 70)
    
    text = "Love and wisdom together create understanding and harmony."
    print(f"\n   Text: \"{text}\"")
    
    history = bridge.evolve_text(text, steps=5)
    print(f"\n   Evolution over {len(history)} steps:")
    for i, state in enumerate(history):
        print(f"   Step {i}: H={state.H:.3f}, C={state.C:.4f}, Phase={state.phase}")
    
    print("\n" + "=" * 70)
    print("Bridge enables: Text -> SFN -> Consciousness Score")
    print("=" * 70)


if __name__ == "__main__":
    demo()
