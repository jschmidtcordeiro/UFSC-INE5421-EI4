import json
import pytest
from pathlib import Path
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.grammar import Grammar

def load_test_cases(filename):
    test_cases_dir = Path(__file__).parent / "test_cases"
    with open(test_cases_dir / filename) as f:
        return json.load(f)

@pytest.mark.parametrize("test_case", load_test_cases("first_follow_sets.json"))
def test_first_follow_sets(test_case):
    print(f"\nTesting: {test_case['name']}")
    
    # Create grammar from input string
    grammar = Grammar.from_string_EI4(test_case["input"])
    
    # Calculate FIRST sets
    grammar.calculate_first_set()
    
    # Verify FIRST sets
    for non_terminal, expected_first in test_case["expected_first_sets"].items():
        assert set(grammar.first_set[non_terminal]) == set(expected_first), \
            f"FIRST set mismatch for {non_terminal}. Expected {expected_first}, got {grammar.first_set[non_terminal]}"
    
    # Calculate FOLLOW sets
    grammar.calculate_follow_set()
    
    # Verify FOLLOW sets
    for non_terminal, expected_follow in test_case["expected_follow_sets"].items():
        assert set(grammar.follow_set[non_terminal]) == set(expected_follow), \
            f"FOLLOW set mismatch for {non_terminal}. Expected {expected_follow}, got {grammar.follow_set[non_terminal]}"

