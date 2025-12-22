#!/usr/bin/env python3
"""
Run all tests for intelligentOne
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from tests import test_core, test_discovery, test_executor, test_os_layer


def run_all_tests():
    """Run all test modules"""
    print("=" * 60)
    print("Running intelligentOne Test Suite")
    print("=" * 60)
    print()
    
    test_modules = [
        ("Core Tests", test_core),
        ("Discovery Tests", test_discovery),
        ("Executor Tests", test_executor),
        ("OS Layer Tests", test_os_layer)
    ]
    
    passed = 0
    failed = 0
    
    for name, module in test_modules:
        print(f"\n{name}...")
        print("-" * 60)
        try:
            # Get all test functions
            test_functions = [
                getattr(module, attr) for attr in dir(module)
                if attr.startswith('test_') and callable(getattr(module, attr))
            ]
            
            for test_func in test_functions:
                try:
                    test_func()
                    print(f"  ✓ {test_func.__name__}")
                    passed += 1
                except Exception as e:
                    print(f"  ✗ {test_func.__name__}: {e}")
                    failed += 1
                    
        except Exception as e:
            print(f"  Error running {name}: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
