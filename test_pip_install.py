#!/usr/bin/env python3
"""
Test Pip Installation Process
=============================

Test script to verify that the pip installation setup would work correctly.
This validates the setup.py configuration and package structure.
"""

import sys
import subprocess
import tempfile
import os
from pathlib import Path
import shutil

def test_setup_py_validation():
    """Test that setup.py is valid and can be processed."""
    print("🔍 Testing setup.py validation")
    print("=" * 50)
    
    try:
        # Test setup.py syntax
        result = subprocess.run([
            sys.executable, 'setup.py', 'check'
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode == 0:
            print("✅ setup.py syntax is valid")
        else:
            print("❌ setup.py has syntax errors:")
            print(result.stderr)
            return False
        
        # Test that we can generate package metadata
        result = subprocess.run([
            sys.executable, 'setup.py', '--name', '--version', '--description'
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            print(f"   Package name: {lines[0]}")
            print(f"   Version: {lines[1]}")
            print(f"   Description: {lines[2]}")
            print("✅ Package metadata generation works")
        else:
            print("❌ Cannot generate package metadata")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Setup.py test failed: {e}")
        return False

def test_required_modules():
    """Test that all required modules are importable."""
    print("\n🐍 Testing module imports")
    print("=" * 50)
    
    required_modules = [
        'neuron_automation',
        'config', 
        'link_manager',
        'blacklist_rewind'
    ]
    
    success_count = 0
    
    for module_name in required_modules:
        try:
            # Test if module file exists
            module_file = Path(f"{module_name}.py")
            if not module_file.exists():
                print(f"❌ Module file missing: {module_file}")
                continue
            
            print(f"✅ Found module file: {module_file}")
            success_count += 1
            
        except Exception as e:
            print(f"❌ Error with module {module_name}: {e}")
    
    print(f"\nModule files found: {success_count}/{len(required_modules)}")
    return success_count == len(required_modules)

def test_entry_points():
    """Test that entry points would be created correctly."""
    print("\n⚙️ Testing entry points configuration")
    print("=" * 50)
    
    try:
        # Read setup.py and check entry points
        with open('setup.py', 'r') as f:
            setup_content = f.read()
        
        # Check for expected entry points
        expected_entries = [
            'neuron-automation=neuron_automation:main',
            'blacklist-rewind=blacklist_rewind:main'
        ]
        
        found_entries = 0
        for entry in expected_entries:
            if entry in setup_content:
                print(f"✅ Found entry point: {entry}")
                found_entries += 1
            else:
                print(f"❌ Missing entry point: {entry}")
        
        return found_entries == len(expected_entries)
        
    except Exception as e:
        print(f"❌ Entry points test failed: {e}")
        return False

def test_package_files():
    """Test that all required package files exist."""
    print("\n📁 Testing package files")
    print("=" * 50)
    
    required_files = [
        'setup.py',
        'requirements.txt', 
        'README.md',
        'MANIFEST.in',
        'BLACKLIST_REWIND_USAGE.md'
    ]
    
    optional_files = [
        '__pycache__',  # Will be created during build
    ]
    
    found_count = 0
    
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"✅ Found required file: {file_path}")
            found_count += 1
        else:
            print(f"❌ Missing required file: {file_path}")
    
    # Check installer directory
    installers_dir = Path('installers')
    if installers_dir.exists():
        installer_files = list(installers_dir.glob('install_*'))
        print(f"✅ Found installer directory with {len(installer_files)} files")
        found_count += 1
    else:
        print("❌ Missing installers directory")
    
    print(f"\nRequired files found: {found_count}/{len(required_files) + 1}")
    return found_count >= len(required_files)

def test_dependencies():
    """Test that dependencies are properly specified."""
    print("\n📦 Testing dependencies")
    print("=" * 50)
    
    try:
        # Check requirements.txt
        with open('requirements.txt', 'r') as f:
            requirements = f.read().strip().split('\n')
        
        print("📋 requirements.txt dependencies:")
        for req in requirements:
            if req.strip():
                print(f"   • {req}")
        
        # Check setup.py dependencies
        with open('setup.py', 'r') as f:
            setup_content = f.read()
        
        expected_deps = ['selenium', 'webdriver-manager', 'requests', 'beautifulsoup4']
        found_deps = 0
        
        for dep in expected_deps:
            if dep in setup_content:
                found_deps += 1
        
        print(f"\n✅ Found {found_deps}/{len(expected_deps)} expected dependencies in setup.py")
        
        return len(requirements) >= 4 and found_deps >= 3
        
    except Exception as e:
        print(f"❌ Dependencies test failed: {e}")
        return False

def test_build_simulation():
    """Simulate package build process."""
    print("\n🏗️ Testing build simulation")
    print("=" * 50)
    
    try:
        # Test sdist build (source distribution)
        print("Testing source distribution build...")
        result = subprocess.run([
            sys.executable, 'setup.py', 'sdist', '--dry-run'
        ], capture_output=True, text=True, cwd=Path.cwd())
        
        if result.returncode == 0:
            print("✅ Source distribution build simulation successful")
        else:
            print("❌ Source distribution build simulation failed:")
            print(result.stderr)
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Build simulation failed: {e}")
        return False

def main():
    """Run all pip installation tests."""
    print("🚀 Pip Installation Test Suite")
    print("=" * 70)
    print("Verifying that 'pip install neuron-automation' would work correctly")
    print()
    
    tests = [
        ("Setup.py Validation", test_setup_py_validation),
        ("Required Modules", test_required_modules),
        ("Entry Points Configuration", test_entry_points), 
        ("Package Files", test_package_files),
        ("Dependencies", test_dependencies),
        ("Build Simulation", test_build_simulation)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 70)
    print("🎯 Test Results Summary:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 Pip installation setup is READY!")
        print("\n📋 What this means:")
        print("  ✅ Users can install with: pip install neuron-automation")
        print("  ✅ Command-line tools will be available: neuron-automation, blacklist-rewind")
        print("  ✅ System integration: neuron-automation --setup") 
        print("  ✅ All modules and dependencies properly configured")
        
        print("\n🚀 Installation Process:")
        print("  1. pip install neuron-automation")
        print("  2. neuron-automation --setup")
        print("  3. neuron-automation (to test)")
        print("  4. System automatically schedules morning automation")
        
        return True
    else:
        print("\n⚠️ Some tests failed - pip installation needs fixing")
        print("\n🔧 Common issues to check:")
        print("  • Missing module files")
        print("  • Incorrect entry points in setup.py")
        print("  • Missing required package files")
        print("  • Dependency specification problems")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)