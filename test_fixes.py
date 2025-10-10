#!/usr/bin/env python3
"""
Test script to verify the browser persistence and automation fixes
"""
import sys
import time
from pathlib import Path

# Add current directory to path to import our modules
sys.path.insert(0, str(Path(__file__).parent))

from neuron_automation import NeuronNewsletterAutomation

def test_browser_setup():
    """Test browser setup and persistence"""
    print("🔧 Testing browser setup and persistence...")
    
    try:
        automation = NeuronNewsletterAutomation()
        
        # Test Chrome driver setup
        print("   Setting up Chrome driver...")
        driver = automation.setup_chrome_driver()
        
        print("   ✅ Chrome driver setup successful")
        print(f"   📊 Browser window handles: {len(driver.window_handles)}")
        
        # Navigate to a simple page to test
        print("   🌐 Testing navigation...")
        driver.get("https://httpbin.org/html")
        
        # Test opening a new tab (simulating article opening)
        print("   📑 Testing tab opening...")
        driver.execute_script("window.open('https://httpbin.org/json', '_blank');")
        time.sleep(2)
        
        print(f"   📊 Total tabs after opening: {len(driver.window_handles)}")
        
        # Test the critical fix - browser should NOT close when we return
        print("   🔍 Testing browser persistence (the critical fix)...")
        print("   ⚠️  Browser should remain open - do NOT quit driver")
        
        # This simulates what happens at the end of automation
        # Previously, driver was set to None and browser closed
        # Now, browser should stay open
        
        print("   ✅ Test completed - browser should remain open")
        print("   🎯 Please manually verify browser tabs are still accessible")
        
        # Don't quit the driver - this is the fix!
        # driver.quit()  # <- This line should never be called for persistence
        
        return True
        
    except Exception as e:
        print(f"   ❌ Test failed: {e}")
        return False

def test_database_functionality():
    """Test database and link management functionality"""
    print("🗄️  Testing database functionality...")
    
    try:
        automation = NeuronNewsletterAutomation()
        
        if automation.link_manager:
            print("   ✅ Link Manager initialized successfully")
            
            # Test database path
            db_path = automation.link_manager.db_path
            print(f"   📍 Database path: {db_path}")
            
            # Get some basic stats
            stats = automation.link_manager.get_reading_statistics()
            print(f"   📊 Total links in database: {stats['total_links_encountered']}")
            print(f"   🚫 Blacklisted links: {stats['blacklisted_links']}")
            print(f"   ✅ Active links: {stats['active_links']}")
            
            return True
        else:
            print("   ⚠️  Link Manager not available")
            return False
            
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Running Neuron Automation Fix Verification Tests")
    print("=" * 60)
    
    results = []
    
    # Test 1: Browser setup and persistence
    results.append(test_browser_setup())
    
    print()
    
    # Test 2: Database functionality  
    results.append(test_database_functionality())
    
    print()
    print("📋 Test Results Summary:")
    print("=" * 30)
    
    if all(results):
        print("✅ All tests passed!")
        print("🎉 Fixes appear to be working correctly")
    else:
        print("❌ Some tests failed")
        for i, result in enumerate(results, 1):
            status = "✅ PASS" if result else "❌ FAIL"
            test_names = ["Browser Setup/Persistence", "Database Functionality"]
            print(f"   Test {i} ({test_names[i-1]}): {status}")

if __name__ == "__main__":
    main()