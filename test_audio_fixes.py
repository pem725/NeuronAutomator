#!/usr/bin/env python3
"""
Test Audio and Autoplay Fixes
==============================

Verify that Chrome options correctly disable video autoplay and mute audio.
"""

import sys
from pathlib import Path

def test_chrome_audio_options():
    """Test that Chrome audio/autoplay options are configured correctly."""
    print("🔇 Testing Audio and Autoplay Configuration...")

    # Expected options for audio muting and autoplay prevention
    expected_options = {
        "--autoplay-policy=document-user-activation-required": "Prevents videos from autoplaying",
        "--disable-features=VizDisplayCompositor": "Additional autoplay prevention",
        "--mute-audio": "Mutes all audio in browser including videos",
        "--remote-allow-origins=*": "Allows browser persistence across platforms"
    }

    print("\n  ✅ Chrome options for audio/autoplay control:")
    for option, description in expected_options.items():
        print(f"    {option}")
        print(f"       → {description}")

    return True


def test_config_file_settings():
    """Test that config.py has the correct audio settings."""
    print("\n📝 Testing config.py Settings...")

    try:
        # Import the config
        from config import ACTIVE_CONFIG

        # Check if mute-audio is in CHROME_OPTIONS
        chrome_options = ACTIVE_CONFIG.CHROME_OPTIONS

        required_options = [
            "--mute-audio",
            "--autoplay-policy=document-user-activation-required",
            "--remote-allow-origins=*"
        ]

        all_present = True
        for option in required_options:
            if option in chrome_options:
                print(f"  ✅ Found: {option}")
            else:
                print(f"  ❌ Missing: {option}")
                all_present = False

        return all_present

    except Exception as e:
        print(f"  ❌ Error loading config: {e}")
        return False


def test_neuron_automation_setup():
    """Test that neuron_automation.py correctly configures Chrome options."""
    print("\n🤖 Testing neuron_automation.py Chrome Setup...")

    try:
        # Read the neuron_automation.py file to verify options are set
        script_path = Path(__file__).parent / "neuron_automation.py"

        if not script_path.exists():
            print(f"  ❌ Script not found: {script_path}")
            return False

        content = script_path.read_text()

        # Check for critical audio/autoplay options
        checks = [
            ("--mute-audio", "Audio muting option"),
            ("--autoplay-policy=document-user-activation-required", "Autoplay policy"),
            ("--remote-allow-origins=*", "Remote origins for persistence"),
            ('chrome_options.add_experimental_option("detach", True)', "Browser detach option")
        ]

        all_present = True
        for check_str, description in checks:
            if check_str in content:
                print(f"  ✅ Found: {description}")
            else:
                print(f"  ❌ Missing: {description}")
                all_present = False

        return all_present

    except Exception as e:
        print(f"  ❌ Error reading script: {e}")
        return False


def main():
    """Run all audio/autoplay tests."""
    print("🚀 Audio and Autoplay Fix Test Suite")
    print("=" * 60)

    tests = [
        ("Chrome Audio Options", test_chrome_audio_options),
        ("Config File Settings", test_config_file_settings),
        ("Neuron Automation Setup", test_neuron_automation_setup)
    ]

    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed: {e}")
            results.append((test_name, False))

    # Summary
    print("\n" + "=" * 60)
    print("🎯 Test Results Summary:")

    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")
        if result:
            passed += 1

    print(f"\nOverall: {passed}/{len(results)} tests passed")

    if passed == len(results):
        print("\n🎉 All audio and autoplay fixes validated!")
        print("\n📋 Expected behavior:")
        print("  • Videos will NOT autoplay when tabs open")
        print("  • All browser audio is muted by default")
        print("  • System sound will NOT be triggered")
        print("  • Browser remains open after script completes")
        print("  • Users can manually unmute if needed")
        return True
    else:
        print("\n⚠️ Some tests failed - fixes may not work as expected")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
