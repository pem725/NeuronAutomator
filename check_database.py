#!/usr/bin/env python3
"""
Script to examine database details after test run
"""
import sqlite3
from pathlib import Path
from datetime import datetime

def examine_database():
    """Examine the database structure and contents"""
    
    db_path = Path.home() / '.config' / 'neuron-automation' / 'newsletter_links.db'
    
    if not db_path.exists():
        print(f"❌ Database not found at: {db_path}")
        return
    
    print(f"📊 Database Analysis: {db_path}")
    print("=" * 60)
    
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            
            # Check database schema
            print("🗂️  Database Schema:")
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table'")
            for table_sql in cursor.fetchall():
                print(f"   {table_sql[0]}")
            
            print("\n📋 Table: links")
            print("-" * 40)
            
            # Get table info
            cursor.execute("PRAGMA table_info(links)")
            columns = cursor.fetchall()
            print("   Columns:")
            for col in columns:
                print(f"     • {col[1]} ({col[2]})")
            
            # Get row count
            cursor.execute("SELECT COUNT(*) FROM links")
            total_rows = cursor.fetchone()[0]
            print(f"\n   📊 Total records: {total_rows}")
            
            # Get recent records
            print("\n   📑 Recent Records (last 10):")
            cursor.execute("""
                SELECT url, first_seen, last_seen, seen_count, is_blacklisted, domain
                FROM links 
                ORDER BY first_seen DESC 
                LIMIT 10
            """)
            
            recent = cursor.fetchall()
            for record in recent:
                url, first_seen, last_seen, seen_count, blacklisted, domain = record
                status = "🚫 BLACKLISTED" if blacklisted else "✅ ACTIVE"
                print(f"     {status} | {domain}")
                print(f"       URL: {url[:60]}...")
                print(f"       First seen: {first_seen}")
                print(f"       Last seen: {last_seen}")
                print(f"       Seen count: {seen_count}")
                print()
            
            # Statistics by domain
            print("\n   🌐 Links by Domain:")
            cursor.execute("""
                SELECT domain, COUNT(*) as count, 
                       SUM(CASE WHEN is_blacklisted = 1 THEN 1 ELSE 0 END) as blacklisted_count
                FROM links 
                GROUP BY domain 
                ORDER BY count DESC 
                LIMIT 10
            """)
            
            domains = cursor.fetchall()
            for domain, count, blacklisted in domains:
                print(f"     {domain}: {count} links ({blacklisted} blacklisted)")
            
            # Check automation runs table if it exists
            print("\n📋 Table: newsletter_runs")
            print("-" * 40)
            
            cursor.execute("SELECT COUNT(*) FROM newsletter_runs")
            run_count = cursor.fetchone()[0]
            print(f"   📊 Total newsletter runs: {run_count}")
            
            if run_count > 0:
                print("\n   📑 Recent Runs (last 5):")
                cursor.execute("""
                    SELECT run_date, new_links, opened_links, newsletter_hash
                    FROM newsletter_runs 
                    ORDER BY run_date DESC 
                    LIMIT 5
                """)
                
                runs = cursor.fetchall()
                for run_date, new_links, opened_links, newsletter_hash in runs:
                    print(f"     📅 {run_date}")
                    print(f"       New links: {new_links}, Opened: {opened_links}")
                    print(f"       Newsletter hash: {newsletter_hash[:12]}...")
                    print()
            
    except sqlite3.Error as e:
        print(f"❌ Database error: {e}")
    
    # Check file size
    file_size = db_path.stat().st_size
    print(f"\n💾 Database file size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
    
    # Check last modified
    mtime = datetime.fromtimestamp(db_path.stat().st_mtime)
    print(f"🕐 Last modified: {mtime}")

if __name__ == "__main__":
    examine_database()