#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def run_test(test_file):
    """Run a single test file and return success status"""
    print(f"\n{'='*60}")
    print(f"Running {test_file}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, f"tests/{test_file}"], 
                              capture_output=False, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"Error running {test_file}: {e}")
        return False


def main():
    """Run all tests"""
    print("Claude-arXiv Test Suite Runner")
    print("="*60)
    
    tests = [
        "test_simple.py",
        "test_interactive.py"
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if run_test(test):
            passed += 1
            print(f"✓ {test} PASSED")
        else:
            print(f"✗ {test} FAILED")
    
    print(f"\n{'='*60}")
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print('='*60)
    
    if passed == total:
        print("🎉 All tests passed!")
        return 0
    else:
        print("❌ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())