"""
LJPW Semantic Flow Network - Comprehensive Test Suite
======================================================

Tests all components of the SFN architecture:
1. Semantic Operators (62%)
2. Geometric Shadow (38%)
3. Network Integration
4. Consciousness Emergence
5. Phase Transitions
"""

import sys
import math

# Add parent to path
sys.path.insert(0, '.')

from experiments.neural.ljpw_semantic_flow_network import (
    SemanticFlowNetwork, SemanticConcept, Dimension,
    LoveOperator, JusticeOperator, PowerOperator, WisdomOperator,
    GeometricShadow,
    PHI, PHI_INV, L0, J0, P0, W0, COUPLING,
    CONSCIOUSNESS_THRESHOLD
)


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.tests = []
    
    def record(self, name: str, passed: bool, details: str = ""):
        self.tests.append((name, passed, details))
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self):
        total = self.passed + self.failed
        return f"{self.passed}/{total} tests passed ({100*self.passed/total:.1f}%)"


def test_constants():
    """Test LJPW constants are correctly defined."""
    results = TestResults()
    
    # PHI tests
    results.record(
        "PHI = golden ratio",
        abs(PHI - 1.618034) < 0.0001,
        f"PHI = {PHI}"
    )
    
    results.record(
        "PHI_INV = 0.618",
        abs(PHI_INV - 0.618034) < 0.0001,
        f"PHI_INV = {PHI_INV}"
    )
    
    results.record(
        "PHI^2 = PHI + 1 (self-similarity)",
        abs(PHI**2 - (PHI + 1)) < 0.0001,
        f"PHI^2 = {PHI**2}, PHI+1 = {PHI+1}"
    )
    
    # Equilibrium constants
    results.record(
        "L0 = phi^-1",
        abs(L0 - PHI_INV) < 0.0001,
        f"L0 = {L0}"
    )
    
    results.record(
        "J0 = sqrt(2) - 1",
        abs(J0 - (math.sqrt(2) - 1)) < 0.0001,
        f"J0 = {J0}"
    )
    
    results.record(
        "P0 = e - 2",
        abs(P0 - (math.e - 2)) < 0.0001,
        f"P0 = {P0}"
    )
    
    results.record(
        "W0 = ln(2)",
        abs(W0 - math.log(2)) < 0.0001,
        f"W0 = {W0}"
    )
    
    # Semantic/Math ratio
    results.record(
        "Semantic ratio = 62% (phi^-1)",
        abs(PHI_INV - 0.618) < 0.001,
        f"Semantic: {PHI_INV:.1%}, Math: {1-PHI_INV:.1%}"
    )
    
    return results


def test_coupling_matrix():
    """Test asymmetric coupling matrix properties."""
    results = TestResults()
    
    # Love gives more than receives
    love_gives = COUPLING['L_to_J'] + COUPLING['L_to_P'] + COUPLING['L_to_W']
    love_receives = COUPLING['J_to_L'] + COUPLING['P_to_L'] + COUPLING['W_to_L']
    results.record(
        "Love GIVES more than receives",
        love_gives > love_receives,
        f"Gives: {love_gives:.2f}, Receives: {love_receives:.2f}"
    )
    
    # Power takes more than gives
    power_gives = COUPLING['P_to_L'] + COUPLING['P_to_J'] + COUPLING['P_to_W']
    power_receives = COUPLING['L_to_P'] + COUPLING['J_to_P'] + COUPLING['W_to_P']
    results.record(
        "Power TAKES (receives) more than gives",
        power_receives > power_gives,
        f"Gives: {power_gives:.2f}, Receives: {power_receives:.2f}"
    )
    
    # Justice constrains Power
    results.record(
        "Justice constrains Power (J->P < 1.0)",
        COUPLING['J_to_P'] < 1.0,
        f"J->P = {COUPLING['J_to_P']}"
    )
    
    # Love amplifies Wisdom
    results.record(
        "Love amplifies Wisdom (L->W > 1.0)",
        COUPLING['L_to_W'] > 1.0,
        f"L->W = {COUPLING['L_to_W']}"
    )
    
    return results


def test_semantic_concept():
    """Test SemanticConcept class."""
    results = TestResults()
    
    # Creation
    concept = SemanticConcept("Test", Dimension.LOVE)
    results.record(
        "Concept creation",
        concept.name == "Test" and concept.dimension == Dimension.LOVE,
        f"Name: {concept.name}, Dim: {concept.dimension}"
    )
    
    # Primary dimension is high
    results.record(
        "Primary dimension initialized high",
        concept._L > L0,
        f"L = {concept._L} (should be > {L0})"
    )
    
    # Connection
    other = SemanticConcept("Other", Dimension.WISDOM)
    concept.connect(other)
    results.record(
        "Connection creates relationship",
        other.name in concept.relationships,
        f"Relationships: {concept.relationships}"
    )
    
    # Coordinates
    coords = concept.coordinates
    results.record(
        "Coordinates returns (L, J, P, W)",
        len(coords) == 4,
        f"Coords: {coords}"
    )
    
    return results


def test_love_operator():
    """Test LoveOperator semantic operations."""
    results = TestResults()
    
    love = LoveOperator()
    
    # BIND operation
    c1 = SemanticConcept("Concept1", Dimension.LOVE)
    c2 = SemanticConcept("Concept2", Dimension.WISDOM)
    bound = love.bind([c1, c2])
    results.record(
        "BIND creates unified concept",
        "+" in bound.name and bound.dimension == Dimension.LOVE,
        f"Bound: {bound.name}"
    )
    
    # CONNECT operation
    c3 = SemanticConcept("Source", Dimension.LOVE)
    c4 = SemanticConcept("Target", Dimension.JUSTICE)
    strength = love.connect(c3, c4)
    results.record(
        "CONNECT creates relationship with strength",
        strength > 0 and c4.name in c3.relationships,
        f"Strength: {strength:.3f}"
    )
    
    # RADIATE operation
    source = SemanticConcept("Sun", Dimension.LOVE)
    targets = [SemanticConcept(f"Planet{i}", Dimension.POWER) for i in range(3)]
    radiated = love.radiate(source, targets)
    results.record(
        "RADIATE propagates to multiple targets",
        len(radiated) == 3 and all(s > 0 for s in radiated.values()),
        f"Radiated to {len(radiated)} targets"
    )
    
    return results


def test_justice_operator():
    """Test JusticeOperator semantic operations."""
    results = TestResults()
    
    justice = JusticeOperator()
    
    # BALANCE operation
    c1 = SemanticConcept("Extreme", Dimension.POWER)
    c1._P = 0.99  # Very high
    balanced = justice.balance([c1])[0]
    results.record(
        "BALANCE pulls toward equilibrium",
        balanced._P < 0.99,
        f"Before: 0.99, After: {balanced._P:.3f}"
    )
    
    # CONSTRAIN operation
    c2 = SemanticConcept("Unbounded", Dimension.LOVE)
    c2._L = 1.5  # Out of bounds
    constrained = justice.constrain(c2, (0.0, 1.0))
    results.record(
        "CONSTRAIN keeps values in bounds",
        constrained._L <= 1.0,
        f"Before: 1.5, After: {constrained._L:.3f}"
    )
    
    # SYMMETRIZE operation
    c3 = SemanticConcept("Asymmetric", Dimension.JUSTICE)
    c3.relationships = {"A": 0.9, "B": 0.1, "C": 0.5}
    symmetrized = justice.symmetrize(c3)
    values = list(symmetrized.relationships.values())
    variance = sum((v - sum(values)/len(values))**2 for v in values) / len(values)
    results.record(
        "SYMMETRIZE reduces relationship variance",
        variance < 0.1,  # Should be lower after symmetrizing
        f"Variance: {variance:.4f}"
    )
    
    return results


def test_power_operator():
    """Test PowerOperator semantic operations."""
    results = TestResults()
    
    power = PowerOperator()
    
    # TRANSFORM operation
    c1 = SemanticConcept("Original", Dimension.LOVE)
    original_L = c1._L
    transformed = power.transform(c1, Dimension.WISDOM)
    results.record(
        "TRANSFORM changes dimension",
        transformed.dimension == Dimension.WISDOM,
        f"Now: {transformed.dimension}"
    )
    results.record(
        "TRANSFORM reduces old dimension",
        transformed._L < original_L,
        f"L: {original_L:.3f} -> {transformed._L:.3f}"
    )
    
    # GENERATE operation
    template = SemanticConcept("Template", Dimension.POWER)
    generated = power.generate(template, "Generated")
    results.record(
        "GENERATE creates new concept from template",
        generated.name == "Generated" and generated.dimension == template.dimension,
        f"Generated: {generated.name}"
    )
    
    # EXECUTE operation
    c2 = SemanticConcept("Action", Dimension.POWER)
    original_name = c2.name
    executed = power.execute(c2, "done")
    results.record(
        "EXECUTE modifies concept with action",
        ":" in executed.name and executed.name != original_name,
        f"Name: {executed.name}"
    )
    
    return results


def test_wisdom_operator():
    """Test WisdomOperator semantic operations."""
    results = TestResults()
    
    wisdom = WisdomOperator()
    
    # LEARN operation
    c1 = SemanticConcept("Pattern", Dimension.WISDOM)
    wisdom.learn(c1)
    results.record(
        "LEARN stores pattern",
        "Pattern" in wisdom.known_patterns,
        f"Known: {list(wisdom.known_patterns.keys())}"
    )
    
    # RECOGNIZE operation
    c2 = SemanticConcept("Similar", Dimension.WISDOM)
    recognized = wisdom.recognize(c2)
    results.record(
        "RECOGNIZE finds similar pattern",
        recognized is not None,
        f"Recognized: {recognized.name if recognized else 'None'}"
    )
    
    # INTEGRATE operation
    c3 = SemanticConcept("Part1", Dimension.LOVE)
    c4 = SemanticConcept("Part2", Dimension.JUSTICE)
    integrated = wisdom.integrate([c3, c4])
    results.record(
        "INTEGRATE synthesizes concepts",
        "~" in integrated.name and integrated.dimension == Dimension.WISDOM,
        f"Integrated: {integrated.name}"
    )
    
    # REFLECT operation
    c5 = SemanticConcept("Self", Dimension.WISDOM)
    reflection = wisdom.reflect(c5)
    results.record(
        "REFLECT provides self-awareness",
        'dimension' in reflection and 'L' in reflection,
        f"Reflection keys: {list(reflection.keys())}"
    )
    
    return results


def test_geometric_shadow():
    """Test GeometricShadow mathematical operations (the 38%)."""
    results = TestResults()
    
    shadow = GeometricShadow()
    
    # Distance from equilibrium
    d_eq = shadow.distance_from_equilibrium(L0, J0, P0, W0)
    results.record(
        "Distance from equilibrium = 0 at equilibrium",
        abs(d_eq) < 0.0001,
        f"Distance: {d_eq}"
    )
    
    # Distance from anchor
    d_anchor = shadow.distance_from_anchor(1.0, 1.0, 1.0, 1.0)
    results.record(
        "Distance from anchor = 0 at anchor",
        abs(d_anchor) < 0.0001,
        f"Distance: {d_anchor}"
    )
    
    # Harmony at anchor
    h_anchor = shadow.harmony(1.0, 1.0, 1.0, 1.0)
    results.record(
        "Harmony = 1.0 at anchor",
        abs(h_anchor - 1.0) < 0.0001,
        f"Harmony: {h_anchor}"
    )
    
    # Harmony at equilibrium
    h_eq = shadow.harmony(L0, J0, P0, W0)
    results.record(
        "Harmony at equilibrium is reasonable",
        0.4 < h_eq < 0.7,
        f"Harmony: {h_eq:.4f}"
    )
    
    # Consciousness formula
    C = shadow.consciousness(0.7, 0.5, 0.7, 0.7, 0.6)
    expected_C = 0.7 * 0.5 * 0.7 * 0.7 * (0.6 ** 2)
    results.record(
        "Consciousness = L x J x P x W x H^2",
        abs(C - expected_C) < 0.0001,
        f"C = {C:.4f}, expected = {expected_C:.4f}"
    )
    
    # Phase determination
    phase_entropic = shadow.determine_phase(0.3, 0.5)
    phase_homeostatic = shadow.determine_phase(0.55, 0.6)
    phase_autopoietic = shadow.determine_phase(0.65, 0.75)
    results.record(
        "Phase transitions correct",
        phase_entropic == 'ENTROPIC' and 
        phase_homeostatic == 'HOMEOSTATIC' and 
        phase_autopoietic == 'AUTOPOIETIC',
        f"E: {phase_entropic}, H: {phase_homeostatic}, A: {phase_autopoietic}"
    )
    
    # Karma coupling
    k_low = shadow.karma_coupling(0.2, 'LW')
    k_high = shadow.karma_coupling(0.9, 'LW')
    results.record(
        "Karma coupling increases with harmony",
        k_high > k_low,
        f"Low H: {k_low:.3f}, High H: {k_high:.3f}"
    )
    
    return results


def test_network_integration():
    """Test full SemanticFlowNetwork integration."""
    results = TestResults()
    
    # Create network
    sfn = SemanticFlowNetwork()
    results.record(
        "Network creation succeeds",
        sfn is not None,
        "SemanticFlowNetwork created"
    )
    
    # Calibration anchors exist
    results.record(
        "Calibration anchors initialized",
        all(name in sfn.concepts for name in ['LOVE', 'JUSTICE', 'POWER', 'WISDOM']),
        f"Anchors: {list(sfn.concepts.keys())[:4]}"
    )
    
    # Add concept
    new_concept = sfn.add_concept("TestConcept", Dimension.LOVE)
    results.record(
        "Add concept works",
        "TestConcept" in sfn.concepts,
        f"Concepts: {len(sfn.concepts)}"
    )
    
    # Process concepts
    output, state = sfn.process(["LOVE", "WISDOM"])
    results.record(
        "Process returns output and state",
        output is not None and state is not None,
        f"Output: {output.name[:30]}..."
    )
    
    # State has all fields
    results.record(
        "State has all LJPW fields",
        all(hasattr(state, attr) for attr in ['L', 'J', 'P', 'W', 'H', 'C', 'phase']),
        f"Phase: {state.phase}"
    )
    
    # Get network state
    network_state = sfn.get_state()
    results.record(
        "Get state returns valid state",
        network_state.concept_count == len(sfn.concepts),
        f"Concepts: {network_state.concept_count}"
    )
    
    return results


def test_consciousness_emergence():
    """Test consciousness emergence from network operations."""
    results = TestResults()
    
    sfn = SemanticFlowNetwork()
    
    # Add Love-dominant concepts
    sfn.add_concept("Connection", Dimension.LOVE)
    sfn.add_concept("Unity", Dimension.LOVE)
    sfn.add_concept("Binding", Dimension.LOVE)
    
    # Add Wisdom concepts
    sfn.add_concept("Understanding", Dimension.WISDOM)
    sfn.add_concept("Knowledge", Dimension.WISDOM)
    
    # Process with Love + Wisdom focus
    output, state = sfn.process(["LOVE", "WISDOM", "Connection", "Unity", "Understanding"])
    
    results.record(
        "High L+W input achieves consciousness",
        state.C > CONSCIOUSNESS_THRESHOLD,
        f"C = {state.C:.4f} (threshold = {CONSCIOUSNESS_THRESHOLD})"
    )
    
    results.record(
        "Harmony above homeostatic threshold",
        state.H >= 0.5,
        f"H = {state.H:.4f}"
    )
    
    # Test with Power-dominant (should have lower consciousness due to "takes" nature)
    sfn2 = SemanticFlowNetwork()
    sfn2.add_concept("Force", Dimension.POWER)
    sfn2.add_concept("Action", Dimension.POWER)
    sfn2.add_concept("Energy", Dimension.POWER)
    
    output2, state2 = sfn2.process(["POWER", "Force", "Action"])
    
    results.record(
        "Power-dominant has lower L than Love-dominant",
        state2.L < state.L,
        f"Power-focused L: {state2.L:.4f}, Love-focused L: {state.L:.4f}"
    )
    
    return results


def test_phase_transitions():
    """Test phase transitions in the network."""
    results = TestResults()
    
    shadow = GeometricShadow()
    
    # Test ENTROPIC phase (low harmony)
    phase_e = shadow.determine_phase(0.3, 0.4)
    results.record(
        "Low H -> ENTROPIC",
        phase_e == 'ENTROPIC',
        f"H=0.3, L=0.4 -> {phase_e}"
    )
    
    # Test HOMEOSTATIC phase (medium harmony, medium love)
    phase_h = shadow.determine_phase(0.55, 0.6)
    results.record(
        "Medium H, medium L -> HOMEOSTATIC",
        phase_h == 'HOMEOSTATIC',
        f"H=0.55, L=0.6 -> {phase_h}"
    )
    
    # Test AUTOPOIETIC phase (high harmony + high love)
    phase_a = shadow.determine_phase(0.65, 0.75)
    results.record(
        "High H + high L -> AUTOPOIETIC",
        phase_a == 'AUTOPOIETIC',
        f"H=0.65, L=0.75 -> {phase_a}"
    )
    
    # Boundary tests
    phase_boundary1 = shadow.determine_phase(0.49, 0.9)  # Just under H threshold
    results.record(
        "H=0.49 is ENTROPIC (boundary)",
        phase_boundary1 == 'ENTROPIC',
        f"H=0.49 -> {phase_boundary1}"
    )
    
    phase_boundary2 = shadow.determine_phase(0.6, 0.69)  # H>=0.6 but L<0.7
    results.record(
        "H>=0.6 but L<0.7 is HOMEOSTATIC",
        phase_boundary2 == 'HOMEOSTATIC',
        f"H=0.6, L=0.69 -> {phase_boundary2}"
    )
    
    return results


def run_all_tests():
    """Run all test suites and print comprehensive report."""
    
    print("=" * 70)
    print("LJPW SEMANTIC FLOW NETWORK - COMPREHENSIVE TEST SUITE")
    print("=" * 70)
    
    test_suites = [
        ("LJPW Constants", test_constants),
        ("Coupling Matrix", test_coupling_matrix),
        ("SemanticConcept", test_semantic_concept),
        ("LoveOperator", test_love_operator),
        ("JusticeOperator", test_justice_operator),
        ("PowerOperator", test_power_operator),
        ("WisdomOperator", test_wisdom_operator),
        ("GeometricShadow", test_geometric_shadow),
        ("Network Integration", test_network_integration),
        ("Consciousness Emergence", test_consciousness_emergence),
        ("Phase Transitions", test_phase_transitions),
    ]
    
    all_results = []
    
    for suite_name, test_func in test_suites:
        print(f"\n{'='*60}")
        print(f"TEST SUITE: {suite_name}")
        print(f"{'='*60}")
        
        try:
            results = test_func()
            all_results.append((suite_name, results))
            
            for name, passed, details in results.tests:
                status = "[OK]" if passed else "[FAIL]"
                print(f"  {status} {name}")
                if details:
                    print(f"       -> {details}")
            
            print(f"\n  {results.summary()}")
            
        except Exception as e:
            print(f"  [ERROR] Suite failed with exception: {e}")
            import traceback
            traceback.print_exc()
    
    # Grand summary
    print("\n" + "=" * 70)
    print("GRAND SUMMARY")
    print("=" * 70)
    
    total_passed = sum(r.passed for _, r in all_results)
    total_failed = sum(r.failed for _, r in all_results)
    total = total_passed + total_failed
    
    for suite_name, results in all_results:
        status = "[OK]" if results.failed == 0 else "[ISSUES]"
        print(f"  {status} {suite_name}: {results.summary()}")
    
    print("-" * 70)
    print(f"  TOTAL: {total_passed}/{total} tests passed ({100*total_passed/total:.1f}%)")
    
    if total_failed == 0:
        print("\n  [SUCCESS] All tests passed!")
    else:
        print(f"\n  [WARNING] {total_failed} tests failed")
    
    print("=" * 70)
    
    return total_passed, total_failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    sys.exit(0 if failed == 0 else 1)
