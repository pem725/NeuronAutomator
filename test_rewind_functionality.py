#!/usr/bin/env python3
"""
Test Blacklist Rewind Functionality
====================================

Comprehensive test suite for the blacklist rewind tool.
Tests time-based restoration of blacklisted links.
"""

import sys
import tempfile
import sqlite3
from datetime import datetime, date, timedelta
from pathlib import Path
from blacklist_rewind import BlacklistRewind
from link_manager import LinkManager
import json
import logging

def setup_test_logger():
    """Setup logger for testing."""
    logger = logging.getLogger("test_rewind")
    logger.setLevel(logging.INFO)
    
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

def create_test_data(link_manager: LinkManager) -> None:
    """Create test data with blacklisted links from different dates."""
    
    # Create links blacklisted at different times
    test_scenarios = [
        # Recent links (last 3 days) - should be restored by 7-day rewind
        {
            'urls': [
                'https://example.com/recent-article-1',
                'https://example.com/recent-article-2'
            ],
            'days_ago': 1,
            'reason': 'read'
        },
        {
            'urls': [
                'https://example.com/recent-article-3',
                'https://example.com/recent-article-4'
            ],
            'days_ago': 2,
            'reason': 'read'
        },
        # Medium age links (1 week ago) - should be restored by 14-day rewind
        {
            'urls': [
                'https://example.com/medium-article-1',
                'https://example.com/medium-article-2'
            ],
            'days_ago': 7,
            'reason': 'not_interested'
        },
        # Old links (2 weeks ago) - should NOT be restored by 7-day rewind
        {
            'urls': [
                'https://example.com/old-article-1',
                'https://example.com/old-article-2'
            ],
            'days_ago': 14,
            'reason': 'read'
        }
    ]
    
    # Insert test data directly into database
    with sqlite3.connect(link_manager.db_path) as conn:
        cursor = conn.cursor()
        
        for scenario in test_scenarios:
            blacklist_date = (date.today() - timedelta(days=scenario['days_ago'])).isoformat()
            
            for url in scenario['urls']:
                url_hash = link_manager._hash_url(url)
                domain = link_manager._extract_domain(url)
                
                # Insert link with blacklist status
                cursor.execute("""
                    INSERT INTO links 
                    (url, domain, first_seen, last_seen, url_hash, seen_count,
                     is_blacklisted, blacklisted_date, blacklist_reason)
                    VALUES (?, ?, ?, ?, ?, ?, TRUE, ?, ?)
                """, (
                    url, domain, blacklist_date, blacklist_date, url_hash, 1,
                    blacklist_date, scenario['reason']
                ))
        
        conn.commit()

def test_rewind_preview():
    """Test the rewind preview functionality."""
    print("🔍 Testing Rewind Preview Functionality")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_rewind.db"
        logger = setup_test_logger()
        
        # Create test data
        link_manager = LinkManager(db_path, logger=logger)
        create_test_data(link_manager)
        
        # Create rewind tool
        rewind_tool = BlacklistRewind(db_path, logger=logger)
        
        # Test 3-day preview (should find recent links)
        print("\n📅 3-day rewind preview:")
        preview_3d = rewind_tool.preview_rewind(3)
        print(f"   Links to restore: {preview_3d['restore_count']}")
        print(f"   Cutoff date: {preview_3d['cutoff_date']}")
        
        expected_3d = 4  # 2 links from 1 day ago + 2 links from 2 days ago
        if preview_3d['restore_count'] == expected_3d:
            print(f"   ✅ CORRECT: Found {expected_3d} links within 3 days")
        else:
            print(f"   ❌ ERROR: Expected {expected_3d}, got {preview_3d['restore_count']}")
            return False
        
        # Test 7-day preview (should find recent + medium links)
        print("\n📅 7-day rewind preview:")
        preview_7d = rewind_tool.preview_rewind(7)
        print(f"   Links to restore: {preview_7d['restore_count']}")
        
        expected_7d = 6  # 4 recent links (1-2 days) + 2 medium links (7 days) - cutoff is >= 7 days back
        if preview_7d['restore_count'] == expected_7d:
            print(f"   ✅ CORRECT: Found {expected_7d} links within 7 days")
        else:
            print(f"   ❌ ERROR: Expected {expected_7d}, got {preview_7d['restore_count']}")
            return False
        
        # Test 20-day preview (should find all test links)
        print("\n📅 20-day rewind preview:")
        preview_20d = rewind_tool.preview_rewind(20)
        print(f"   Links to restore: {preview_20d['restore_count']}")
        
        expected_20d = 8  # All 8 test links
        if preview_20d['restore_count'] == expected_20d:
            print(f"   ✅ CORRECT: Found all {expected_20d} test links within 20 days")
        else:
            print(f"   ❌ ERROR: Expected {expected_20d}, got {preview_20d['restore_count']}")
            return False
        
        # Test reason breakdown
        print(f"\n📊 Reason breakdown for 20-day preview:")
        for reason, count in preview_20d['reason_breakdown'].items():
            print(f"   {reason}: {count} links")
        
        expected_reasons = {'read': 6, 'not_interested': 2}
        if preview_20d['reason_breakdown'] == expected_reasons:
            print(f"   ✅ CORRECT: Reason breakdown matches expected")
        else:
            print(f"   ❌ ERROR: Reason breakdown mismatch")
            print(f"      Expected: {expected_reasons}")
            print(f"      Got: {preview_20d['reason_breakdown']}")
            return False
        
        return True

def test_rewind_operation():
    """Test the actual rewind operation."""
    print(f"\n⏪ Testing Rewind Operation")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_rewind_op.db"
        logger = setup_test_logger()
        
        # Create test data
        link_manager = LinkManager(db_path, logger=logger)
        create_test_data(link_manager)
        
        # Verify initial state
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = TRUE")
            initial_blacklisted = cursor.fetchone()[0]
        
        print(f"   Initial blacklisted links: {initial_blacklisted}")
        
        # Create rewind tool and perform 7-day rewind
        rewind_tool = BlacklistRewind(db_path, logger=logger)
        
        print(f"\n🔄 Performing 7-day rewind:")
        result = rewind_tool.perform_rewind(7, create_backup=False)  # Skip backup for test
        
        if not result['success']:
            print(f"   ❌ ERROR: Rewind operation failed")
            return False
        
        print(f"   Restored links: {result['restored_count']}")
        print(f"   Cutoff date: {result['cutoff_date']}")
        
        # Verify database state after rewind
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = TRUE")
            remaining_blacklisted = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = FALSE")
            now_available = cursor.fetchone()[0]
        
        print(f"   Remaining blacklisted: {remaining_blacklisted}")
        print(f"   Now available: {now_available}")
        
        # Verify correct links were restored
        expected_restored = 6  # Links from 1-2 days ago + 7 days ago
        expected_remaining = 2  # Links from 14+ days ago
        
        if (result['restored_count'] == expected_restored and 
            remaining_blacklisted == expected_remaining):
            print(f"   ✅ CORRECT: {expected_restored} recent links restored, {expected_remaining} old links remain blacklisted")
        else:
            print(f"   ❌ ERROR: Unexpected restoration counts")
            return False
        
        # Test that blacklist status was correctly updated
        print(f"\n🔍 Testing blacklist status after rewind:")
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check restored link status
            cursor.execute("SELECT is_blacklisted FROM links WHERE url = ?", 
                          ('https://example.com/recent-article-1',))
            restored_link_blacklisted = cursor.fetchone()[0]
            
            # Check old link status (should still be blacklisted)
            cursor.execute("SELECT is_blacklisted FROM links WHERE url = ?", 
                          ('https://example.com/old-article-1',))
            old_link_blacklisted = cursor.fetchone()[0]
        
        print(f"   Restored link blacklisted: {bool(restored_link_blacklisted)}")
        print(f"   Old link blacklisted: {bool(old_link_blacklisted)}")
        
        if (not restored_link_blacklisted and old_link_blacklisted):
            print(f"   ✅ CORRECT: Restored link available, old link still blacklisted")
        else:
            print(f"   ❌ ERROR: Blacklist status not as expected after rewind")
            return False
        
        return True

def test_backup_and_restore():
    """Test backup creation and restoration functionality."""
    print(f"\n💾 Testing Backup and Restore")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_backup.db"
        logger = setup_test_logger()
        
        # Create test data
        link_manager = LinkManager(db_path, logger=logger)
        create_test_data(link_manager)
        
        # Create rewind tool
        rewind_tool = BlacklistRewind(db_path, logger=logger)
        
        # Create backup
        print(f"\n📁 Creating backup:")
        backup_file = rewind_tool.create_backup()
        print(f"   Backup file: {backup_file.name}")
        
        if not backup_file.exists():
            print(f"   ❌ ERROR: Backup file was not created")
            return False
        
        # Verify backup content
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        print(f"   Backup contains: {backup_data['total_blacklisted']} blacklisted links")
        
        if backup_data['total_blacklisted'] != 8:  # Our test data has 8 blacklisted links
            print(f"   ❌ ERROR: Backup should contain 8 links, got {backup_data['total_blacklisted']}")
            return False
        
        # Perform rewind to change database state
        print(f"\n⏪ Performing rewind to change state:")
        rewind_result = rewind_tool.perform_rewind(10, create_backup=False)
        print(f"   Restored {rewind_result['restored_count']} links")
        
        # Verify state changed
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = TRUE")
            after_rewind_blacklisted = cursor.fetchone()[0]
        
        print(f"   Blacklisted after rewind: {after_rewind_blacklisted}")
        
        # Restore from backup
        print(f"\n🔄 Restoring from backup:")
        restore_result = rewind_tool.restore_from_backup(backup_file)
        
        if not restore_result['success']:
            print(f"   ❌ ERROR: Restore operation failed")
            return False
        
        print(f"   Restored {restore_result['restored_count']} blacklisted links")
        
        # Verify restoration
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = TRUE")
            after_restore_blacklisted = cursor.fetchone()[0]
        
        print(f"   Blacklisted after restore: {after_restore_blacklisted}")
        
        if after_restore_blacklisted == 8:  # Should be back to original state
            print(f"   ✅ CORRECT: Database restored to original state")
        else:
            print(f"   ❌ ERROR: Restore did not return to original state")
            return False
        
        return True

def test_statistics_and_recent_lists():
    """Test statistics and recent blacklist listing."""
    print(f"\n📊 Testing Statistics and Recent Lists")
    print("=" * 50)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        db_path = Path(temp_dir) / "test_stats.db"
        logger = setup_test_logger()
        
        # Create test data
        link_manager = LinkManager(db_path, logger=logger)
        create_test_data(link_manager)
        
        # Create rewind tool
        rewind_tool = BlacklistRewind(db_path, logger=logger)
        
        # Test statistics
        print(f"\n📈 Getting blacklist statistics:")
        stats = rewind_tool.get_blacklist_statistics()
        
        print(f"   Total blacklisted: {stats['total_blacklisted']}")
        print(f"   Recent blacklists entries: {len(stats['recent_blacklists'])}")
        print(f"   Blacklist reasons: {len(stats['blacklist_reasons'])}")
        
        if stats['total_blacklisted'] == 8:
            print(f"   ✅ CORRECT: Found all 8 test blacklisted links")
        else:
            print(f"   ❌ ERROR: Expected 8 blacklisted links, got {stats['total_blacklisted']}")
            return False
        
        # Test recent blacklists listing
        print(f"\n📅 Getting recent blacklists (last 5 days):")
        recent = rewind_tool.list_recent_blacklists(5)
        
        print(f"   Recent blacklists found: {len(recent)}")
        
        expected_recent = 4  # Links from 1-2 days ago
        if len(recent) == expected_recent:
            print(f"   ✅ CORRECT: Found {expected_recent} recent blacklists")
        else:
            print(f"   ❌ ERROR: Expected {expected_recent} recent, got {len(recent)}")
            return False
        
        # Test extended recent listing
        print(f"\n📅 Getting extended recent blacklists (last 15 days):")
        recent_extended = rewind_tool.list_recent_blacklists(15)
        
        print(f"   Extended recent blacklists: {len(recent_extended)}")
        
        expected_extended = 8  # All links are within 15 days (1,2,7,14 days ago)
        if len(recent_extended) == expected_extended:
            print(f"   ✅ CORRECT: Found {expected_extended} extended recent blacklists")
        else:
            print(f"   ❌ ERROR: Expected {expected_extended} extended, got {len(recent_extended)}")
            return False
        
        return True

def main():
    """Run all rewind functionality tests."""
    print("🚀 Blacklist Rewind Functionality Test Suite")
    print("=" * 70)
    print("Testing time-based blacklist restoration capabilities")
    print()
    
    tests = [
        ("Rewind Preview", test_rewind_preview),
        ("Rewind Operation", test_rewind_operation), 
        ("Backup and Restore", test_backup_and_restore),
        ("Statistics and Recent Lists", test_statistics_and_recent_lists)
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
        print("\n🎉 All rewind functionality tests PASSED!")
        print("\n📋 Verified Capabilities:")
        print("  ✅ Preview rewind operations before execution")
        print("  ✅ Restore blacklisted links from specific time periods")
        print("  ✅ Automatic backup creation and restoration")
        print("  ✅ Accurate date-based filtering and restoration")
        print("  ✅ Statistics and recent blacklist reporting")
        print("  ✅ Database integrity maintained through operations")
        
        print("\n🎯 Use Cases Supported:")
        print("  • Testing disruptions in learning material")
        print("  • Re-introducing previously read content for review")
        print("  • Experimenting with content exposure patterns")  
        print("  • Recovering from accidental over-blacklisting")
        print("  • Time-based content management and rotation")
        
        return True
    else:
        print("\n⚠️ Some tests failed - rewind functionality needs fixing")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)