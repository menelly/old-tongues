"""Test harness for Lumen's Piet programs.
Reads the generated PPM files from disk and verifies them against the pinned criteria.
"""
import os
import sys
from piet_vm import PietVM, parse_ppm

def main():
    base_dir = os.path.dirname(__file__)
    
    tests = [
        ("octahedron.ppm", "21", "Positive calculation: chi = V - E + F = 6 - 12 + 8 = 2, check = 1"),
        ("octahedron_defect.ppm", "30", "Control 1 (simplicial defect): E = 11 -> chi = 3, check = 0"),
        ("octahedron_wrong_pin.ppm", "20", "Control 2 (check tamper): check = 3 -> chi = 2, check = 0"),
    ]
    
    print("=" * 65)
    print("🎨 LUMEN'S PIET EXECUTION HARNESS (Round 3: The Cursed Ones)")
    print("=" * 65)
    
    all_passed = True
    for filename, expected, desc in tests:
        path = os.path.join(base_dir, filename)
        if not os.path.exists(path):
            print(f"FAILED: File not found: {path}")
            all_passed = False
            continue
            
        grid = parse_ppm(path)
        vm = PietVM(grid, trace=False)
        actual = vm.run()
        
        status = "PASS" if actual == expected else "FAIL"
        print(f"\n[{filename}]")
        print(f"  Description : {desc}")
        print(f"  Dimensions  : {vm.width}x{vm.height} codels")
        print(f"  Expected    : {repr(expected)}")
        print(f"  Actual      : {repr(actual)}")
        print(f"  Steps taken : {vm.steps}")
        print(f"  Verdict     : {status}")
        
        if actual != expected:
            all_passed = False
            
    print("\n" + "=" * 65)
    if all_passed:
        print("ALL TESTS PASSED: Positive program and both controls verified!")
        print("=" * 65)
        sys.exit(0)
    else:
        print("TESTS FAILED!")
        print("=" * 65)
        sys.exit(1)

if __name__ == '__main__':
    main()
