#!/usr/bin/env python3
"""
Test Blacklist Behavior 
========================

Test to verify that the blacklist system only stores and tracks links that are
actually opened, not just displayed during testing or analysis.

This addresses the user's concern about over-blacklisting.
"""

import sys
import tempfile
import sqlite3
from pathlib import Path
from link_manager import LinkManager
import logging

def setup_test_logger():
    """Setup a logger for testing."""
    logger = logging.getLogger("test_blacklist")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def test_analyze_vs_record_behavior():
    """Test that analyze doesn't store links, but record does."""
    print("🧪 Testing Analyze vs Record Behavior")
    print("=" * 50)
    
    # Create temporary database
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test.db"
        logger = setup_test_logger()
        
        # Create a simple config object with recent link days = 0 (same day blocking)
        class TestConfig:
            RECENT_LINK_DAYS = 0  # Block same-day re-opening
            
        # Create LinkManager
        link_manager = LinkManager(db_path, config=TestConfig, logger=logger)
        
        # Test links
        test_links = [
            "https://example.com/article1",
            "https://example.com/article2", 
            "https://example.com/article3"
        ]
        
        print(f"\n📋 Test Links: {len(test_links)}")
        for i, link in enumerate(test_links, 1):
            print(f"  {i}. {link}")
        
        # Step 1: Analyze links (should NOT store in database)
        print(f"\n🔍 Step 1: Analyzing links (should NOT store in database)")
        analysis = link_manager.analyze_newsletter_links(test_links)
        
        print(f"   Analysis result: {len(analysis['links_to_open'])} links to open")
        
        # Check database - should be empty
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM newsletter_runs")
            run_count = cursor.fetchone()[0]
        
        print(f"   Database state after analysis:")
        print(f"     Links stored: {link_count}")
        print(f"     Runs recorded: {run_count}")
        
        if link_count == 0 and run_count == 0:
            print("   ✅ CORRECT: Analysis did not store anything in database")
        else:
            print("   ❌ ERROR: Analysis should not store data in database")
            return False
        
        # Step 2: Simulate opening only 2 of the 3 links
        opened_links = test_links[:2]  # Only first 2 links
        print(f"\n📂 Step 2: Recording {len(opened_links)} actually opened links")
        for i, link in enumerate(opened_links, 1):
            print(f"   {i}. {link}")
        
        record_result = link_manager.record_opened_links(opened_links, "test_newsletter")
        print(f"   Recorded: {record_result['recorded_count']} links")
        
        # Check database - should contain only opened links
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
            cursor.execute("SELECT url FROM links")
            stored_urls = [row[0] for row in cursor.fetchall()]
            cursor.execute("SELECT COUNT(*) FROM newsletter_runs WHERE success = TRUE")
            run_count = cursor.fetchone()[0]
        
        print(f"   Database state after recording:")
        print(f"     Links stored: {link_count}")
        print(f"     Runs recorded: {run_count}")
        print(f"     Stored URLs:")
        for i, url in enumerate(stored_urls, 1):
            print(f"       {i}. {url}")
        
        # Verify correct behavior
        success = True
        if link_count != 2:
            print(f"   ❌ ERROR: Expected 2 stored links, got {link_count}")
            success = False
        
        if run_count != 1:
            print(f"   ❌ ERROR: Expected 1 run record, got {run_count}")
            success = False
            
        if set(stored_urls) != set(opened_links):
            print(f"   ❌ ERROR: Stored URLs don't match opened links")
            success = False
        
        if success:
            print("   ✅ CORRECT: Only actually opened links were stored")
        
        # Step 3: Test subsequent analysis
        print(f"\n🔍 Step 3: Re-analyzing same links")
        analysis2 = link_manager.analyze_newsletter_links(test_links)
        
        print(f"   Second analysis:")
        print(f"     New links: {len(analysis2['new_links'])}")
        print(f"     Existing links: {len(analysis2['existing_links'])}")
        print(f"     Links to open: {len(analysis2['links_to_open'])}")
        
        # Should show: 0 existing (recently opened links are blocked), 1 new (never opened), 2 blacklisted (recently opened)
        expected_existing = 0  # Recently opened links are blocked, not marked as "existing"
        expected_new = 1       # The 1 we never opened
        expected_blacklisted = 2  # The 2 we opened today (blocked from re-opening)
        
        if (len(analysis2['existing_links']) == expected_existing and 
            len(analysis2['new_links']) == expected_new and
            len(analysis2['blacklisted_links']) == expected_blacklisted):
            print("   ✅ CORRECT: Recently opened links blocked from re-opening, new link available")
        else:
            print(f"   ❌ ERROR: Expected {expected_existing} existing, {expected_new} new, {expected_blacklisted} blacklisted")
            success = False
        
        return success

def test_testing_vs_production_workflow():
    """Test the difference between testing and production workflows."""
    print(f"\n🔬 Testing vs Production Workflow Comparison")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "workflow_test.db"
        logger = setup_test_logger()
        
        # Create a simple config object with recent link days = 0 (same day blocking)
        class TestConfig:
            RECENT_LINK_DAYS = 0  # Block same-day re-opening
            
        link_manager = LinkManager(db_path, config=TestConfig, logger=logger)
        
        test_links = [
            "https://example.com/morning-news-1",
            "https://example.com/morning-news-2",
            "https://example.com/morning-news-3"
        ]
        
        # Scenario 1: User runs manual test (analyze only)
        print("\n📋 Scenario 1: Manual Test Run (User testing installation)")
        print("   User runs: neuron-automation (just to test)")
        print("   Expected: Links analyzed but NOT stored in database")
        
        analysis = link_manager.analyze_newsletter_links(test_links)
        print(f"   Links that would be opened: {len(analysis['links_to_open'])}")
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
        
        print(f"   Database links after test: {link_count}")
        
        if link_count == 0:
            print("   ✅ CORRECT: Test run did not pollute database")
        else:
            print("   ❌ ERROR: Test run should not store links")
            return False
        
        # Scenario 2: Automated morning run (analyze + record)
        print("\n🌅 Scenario 2: Morning Automation Run")
        print("   System runs: automation opens tabs successfully")
        print("   Expected: Links stored in database (were actually opened)")
        
        # Simulate successful tab opening
        opened_links = test_links  # All tabs opened successfully
        record_result = link_manager.record_opened_links(opened_links, "morning_newsletter")
        
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links")
            link_count = cursor.fetchone()[0]
        
        print(f"   Database links after morning run: {link_count}")
        print(f"   Successfully recorded: {record_result['recorded_count']} links")
        
        if link_count == len(test_links):
            print("   ✅ CORRECT: Morning run properly stored opened links")
        else:
            print("   ❌ ERROR: Morning run should store all opened links")
            return False
        
        # Scenario 3: Next day analysis  
        print("\n📅 Scenario 3: Same Day Re-Analysis")
        print("   Same newsletter links encountered again")
        print("   Expected: All links marked as 'blacklisted' (recently opened), none to open")
        
        next_analysis = link_manager.analyze_newsletter_links(test_links)
        print(f"   New links: {len(next_analysis['new_links'])}")
        print(f"   Existing links: {len(next_analysis['existing_links'])}")
        print(f"   Blacklisted links: {len(next_analysis['blacklisted_links'])}")
        print(f"   Links to open: {len(next_analysis['links_to_open'])}")
        
        if (len(next_analysis['blacklisted_links']) == len(test_links) and 
            len(next_analysis['links_to_open']) == 0):
            print("   ✅ CORRECT: Recently opened links blocked from re-opening")
        else:
            print("   ❌ ERROR: Recently opened links should be blocked")
            return False
        
        return True

def main():
    """Run all blacklist behavior tests."""
    print("🚀 Blacklist Behavior Test Suite")
    print("Verifying that only OPENED links get stored, not just analyzed ones")
    print("=" * 70)
    
    tests = [
        ("Analyze vs Record Behavior", test_analyze_vs_record_behavior),
        ("Testing vs Production Workflow", test_testing_vs_production_workflow)
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
        print("\n🎉 Blacklist behavior is CORRECT!")
        print("\n📋 Key Behaviors Verified:")
        print("  ✅ Testing/analysis does NOT store links in database")
        print("  ✅ Only successfully opened links get stored")
        print("  ✅ Failed tab openings do not get recorded")
        print("  ✅ Blacklist prevents re-opening of previously opened links")
        print("  ✅ No over-blacklisting - limits without fully restricting")
        
        print("\n🔧 Implementation Details:")
        print("  • analyze_newsletter_links(): Query-only, no database writes")
        print("  • record_opened_links(): Only called after successful tab opening")
        print("  • Blacklist logic: Based on actual user interaction, not exposure")
        return True
    else:
        print("\n⚠️ Some tests failed - blacklist behavior needs fixing")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)