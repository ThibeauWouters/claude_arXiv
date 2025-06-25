#!/usr/bin/env python3

import sys
import os
import subprocess
import tempfile
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_interactive_mode_help():
    """Test that interactive mode help works"""
    print("=== Testing Interactive Mode Help ===")
    
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arxiv_simple.py")
    
    # Test help
    result = subprocess.run([sys.executable, script_path, "--help"], 
                           capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✓ Help text displays correctly")
        if "--interactive" in result.stdout and "-i" in result.stdout:
            print("✓ Interactive flags are documented")
            return True
        else:
            print("✗ Interactive flags not found in help")
            return False
    else:
        print("✗ Help command failed")
        return False


def test_argument_validation():
    """Test argument validation"""
    print("\n=== Testing Argument Validation ===")
    
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arxiv_simple.py")
    
    # Test missing arguments
    result = subprocess.run([sys.executable, script_path, "2404.11397"], 
                           capture_output=True, text=True)
    
    if result.returncode != 0 and "Either provide a question or use --interactive mode" in result.stderr:
        print("✓ Correctly rejects missing question without interactive flag")
    else:
        print("✗ Should reject missing question without interactive flag")
        return False
    
    # Test conflicting arguments
    result = subprocess.run([sys.executable, script_path, "2404.11397", "some question", "--interactive"], 
                           capture_output=True, text=True)
    
    if result.returncode != 0 and "Cannot use both question and --interactive mode" in result.stderr:
        print("✓ Correctly rejects conflicting arguments")
        return True
    else:
        print("✗ Should reject conflicting arguments")
        return False


def test_interactive_mode_initialization():
    """Test that interactive mode initializes correctly (without actually entering Claude)"""
    print("\n=== Testing Interactive Mode Initialization ===")
    
    script_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "arxiv_simple.py")
    
    # Create a test script that simulates the interactive mode but exits immediately
    test_script = f"""
import sys
sys.path.append('{os.path.dirname(os.path.dirname(os.path.abspath(__file__)))}')

from arxiv_client import ArxivClient
from cache_manager import CacheManager
from arxiv_simple import load_paper

# Test paper loading
client = ArxivClient("./test_cache")
cache = CacheManager("./test_cache")

try:
    metadata, tex_file = load_paper("2404.11397", client, cache)
    print(f"✓ Paper loaded: {{metadata['title'][:50]}}...")
    print(f"✓ TeX file found: {{tex_file.name}}")
    print("✓ Interactive mode would start successfully")
except Exception as e:
    print(f"✗ Error loading paper: {{e}}")
    sys.exit(1)
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script)
        test_file = f.name
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                               capture_output=True, text=True, cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        if result.returncode == 0:
            print("✓ Interactive mode initialization test passed")
            print(result.stdout.strip())
            return True
        else:
            print("✗ Interactive mode initialization failed")
            print("STDERR:", result.stderr)
            return False
    finally:
        os.unlink(test_file)


def main():
    """Run all interactive mode tests"""
    print("Interactive Mode Test Suite")
    print("="*50)
    
    tests = [
        test_interactive_mode_help,
        test_argument_validation,
        test_interactive_mode_initialization
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ Test failed with exception: {str(e)}")
    
    print(f"\n{'='*50}")
    print(f"Interactive Mode Tests: {passed}/{total} passed")
    
    if passed == total:
        print("✓ All interactive mode tests passed!")
        return 0
    else:
        print("✗ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())