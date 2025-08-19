#!/usr/bin/env python3
"""
Link Management System for Neuron Newsletter Automation
=====================================================

Handles storage, tracking, and blacklisting of newsletter links to prevent
duplicate reading and provide reading analytics.

Author: AI Assistant
Created: 2025
License: MIT
Version: 1.4.0
"""

import sqlite3
import hashlib
import json
import fnmatch
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Set, Tuple
from urllib.parse import urlparse
import logging

__version__ = "1.4.0"


class LinkManager:
    """
    Manages newsletter links with SQLite database storage.
    
    Features:
    - Store and track all encountered links
    - Prevent duplicate link opening
    - Blacklist management (manual and automatic)
    - Reading analytics and statistics
    - Link history and change detection
    """
    
    def __init__(self, database_path: Path, config=None, logger: Optional[logging.Logger] = None):
        """Initialize LinkManager with database path and configuration."""
        self.db_path = database_path
        self.config = config
        self.logger = logger or logging.getLogger(__name__)
        
        # Ensure parent directory exists
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._init_database()
        
        self.logger.info(f"LinkManager initialized with database: {self.db_path}")
    
    def _init_database(self) -> None:
        """Initialize the SQLite database with required tables."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create links table - stores all unique links ever encountered
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS links (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT UNIQUE NOT NULL,
                    title TEXT,
                    domain TEXT NOT NULL,
                    first_seen DATE NOT NULL,
                    last_seen DATE NOT NULL,
                    seen_count INTEGER DEFAULT 1,
                    is_blacklisted BOOLEAN DEFAULT FALSE,
                    blacklisted_date DATE,
                    blacklist_reason TEXT,
                    url_hash TEXT UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Create newsletter_runs table - tracks each automation execution
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS newsletter_runs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    run_date DATE NOT NULL,
                    run_time TIMESTAMP NOT NULL,
                    newsletter_hash TEXT,
                    links_found INTEGER DEFAULT 0,
                    new_links INTEGER DEFAULT 0,
                    existing_links INTEGER DEFAULT 0,
                    blacklisted_links INTEGER DEFAULT 0,
                    opened_links INTEGER DEFAULT 0,
                    success BOOLEAN DEFAULT TRUE,
                    notes TEXT
                );
            """)
            
            # Create link_appearances table - many-to-many relationship
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS link_appearances (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    link_id INTEGER NOT NULL,
                    run_id INTEGER NOT NULL,
                    position INTEGER,
                    extraction_context TEXT,
                    FOREIGN KEY (link_id) REFERENCES links(id),
                    FOREIGN KEY (run_id) REFERENCES newsletter_runs(id),
                    UNIQUE(link_id, run_id)
                );
            """)
            
            # Create indexes for better performance
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_url_hash ON links(url_hash);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_domain ON links(domain);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_links_blacklisted ON links(is_blacklisted);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_newsletter_runs_date ON newsletter_runs(run_date);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_link_appearances_link_id ON link_appearances(link_id);")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_link_appearances_run_id ON link_appearances(run_id);")
            
            conn.commit()
            self.logger.info("Database schema initialized successfully")
    
    def _hash_url(self, url: str) -> str:
        """Create a consistent hash for URL deduplication."""
        # Normalize URL for consistent hashing
        parsed = urlparse(url.lower().strip())
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return hashlib.md5(normalized.encode()).hexdigest()
    
    def _extract_domain(self, url: str) -> str:
        """Extract domain from URL."""
        try:
            return urlparse(url).netloc.lower()
        except Exception as e:
            self.logger.warning(f"Failed to extract domain from {url}: {e}")
            return "unknown"
    
    def _should_auto_blacklist_url(self, url: str) -> Optional[str]:
        """Check if URL should be automatically blacklisted based on configuration."""
        if not self.config:
            return None
            
        domain = self._extract_domain(url)
        
        # Check domain blacklist
        domain_blacklist = getattr(self.config, 'DOMAIN_BLACKLIST', [])
        if domain in domain_blacklist:
            return "domain_blacklisted"
        
        # Check URL pattern blacklist
        url_patterns = getattr(self.config, 'URL_PATTERN_BLACKLIST', [])
        for pattern in url_patterns:
            if fnmatch.fnmatch(url.lower(), pattern.lower()):
                return f"pattern_match: {pattern}"
        
        return None
    
    def _auto_blacklist_old_links(self) -> int:
        """Auto-blacklist old links based on configuration."""
        if not self.config or not getattr(self.config, 'AUTO_BLACKLIST_ENABLED', False):
            return 0
            
        days_old = getattr(self.config, 'AUTO_BLACKLIST_DAYS', 30)
        cutoff_date = date.today() - timedelta(days=days_old)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE links 
                SET is_blacklisted = TRUE, 
                    blacklisted_date = ?, 
                    blacklist_reason = 'auto_aged'
                WHERE last_seen < ? 
                AND is_blacklisted = FALSE
            """, (date.today(), cutoff_date))
            
            count = cursor.rowcount
            if count > 0:
                self.logger.info(f"Auto-blacklisted {count} links older than {days_old} days")
            
            return count
    
    def process_newsletter_links(self, links: List[str], newsletter_hash: str = None) -> Dict:
        """
        Process a list of newsletter links and return categorized results.
        
        Args:
            links: List of URLs from newsletter
            newsletter_hash: Optional hash of newsletter content
            
        Returns:
            Dictionary with categorized link lists and statistics
        """
        today = date.today()
        now = datetime.now()
        
        # Initialize result structure
        result = {
            'new_links': [],
            'existing_links': [],
            'blacklisted_links': [],
            'links_to_open': [],  # Links that should be opened in browser
            'statistics': {
                'total_links': len(links),
                'new_count': 0,
                'existing_count': 0,
                'blacklisted_count': 0,
                'opened_count': 0
            }
        }
        
        if not links:
            self.logger.info("No links provided to process")
            return result
        
        # Run auto-blacklisting for old links if enabled
        aged_count = self._auto_blacklist_old_links()
        if aged_count > 0:
            result['statistics']['auto_blacklisted_aged'] = aged_count
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create newsletter run record
            cursor.execute("""
                INSERT INTO newsletter_runs 
                (run_date, run_time, newsletter_hash, links_found)
                VALUES (?, ?, ?, ?)
            """, (today, now, newsletter_hash, len(links)))
            
            run_id = cursor.lastrowid
            
            # Process each link
            for position, url in enumerate(links, 1):
                try:
                    url_hash = self._hash_url(url)
                    domain = self._extract_domain(url)
                    
                    # Check if URL should be auto-blacklisted based on patterns
                    auto_blacklist_reason = self._should_auto_blacklist_url(url)
                    
                    # Check if link already exists
                    cursor.execute("""
                        SELECT id, is_blacklisted, seen_count
                        FROM links WHERE url_hash = ?
                    """, (url_hash,))
                    
                    existing_link = cursor.fetchone()
                    
                    if existing_link:
                        link_id, is_blacklisted, seen_count = existing_link
                        
                        # Update existing link
                        cursor.execute("""
                            UPDATE links 
                            SET last_seen = ?, seen_count = seen_count + 1
                            WHERE id = ?
                        """, (today, link_id))
                        
                        if is_blacklisted:
                            result['blacklisted_links'].append(url)
                            result['statistics']['blacklisted_count'] += 1
                        else:
                            result['existing_links'].append(url)
                            result['statistics']['existing_count'] += 1
                    
                    else:
                        # Create new link record
                        is_auto_blacklisted = bool(auto_blacklist_reason)
                        
                        cursor.execute("""
                            INSERT INTO links 
                            (url, domain, first_seen, last_seen, url_hash, 
                             is_blacklisted, blacklisted_date, blacklist_reason)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """, (url, domain, today, today, url_hash,
                              is_auto_blacklisted, 
                              today if is_auto_blacklisted else None,
                              auto_blacklist_reason))
                        
                        link_id = cursor.lastrowid
                        
                        if is_auto_blacklisted:
                            result['blacklisted_links'].append(url)
                            result['statistics']['blacklisted_count'] += 1
                            self.logger.info(f"Auto-blacklisted new link: {url} ({auto_blacklist_reason})")
                        else:
                            result['new_links'].append(url)
                            result['statistics']['new_count'] += 1
                            result['links_to_open'].append(url)
                    
                    # Record link appearance in this run
                    cursor.execute("""
                        INSERT OR IGNORE INTO link_appearances
                        (link_id, run_id, position)
                        VALUES (?, ?, ?)
                    """, (link_id, run_id, position))
                
                except Exception as e:
                    self.logger.error(f"Error processing link {url}: {e}")
                    continue
            
            # Update run statistics
            result['statistics']['opened_count'] = len(result['links_to_open'])
            
            cursor.execute("""
                UPDATE newsletter_runs
                SET new_links = ?, existing_links = ?, blacklisted_links = ?, opened_links = ?
                WHERE id = ?
            """, (
                result['statistics']['new_count'],
                result['statistics']['existing_count'], 
                result['statistics']['blacklisted_count'],
                result['statistics']['opened_count'],
                run_id
            ))
            
            conn.commit()
        
        # Log summary
        stats = result['statistics']
        self.logger.info(f"Processed {stats['total_links']} links: "
                        f"{stats['new_count']} new, "
                        f"{stats['existing_count']} existing, " 
                        f"{stats['blacklisted_count']} blacklisted, "
                        f"{stats['opened_count']} to open")
        
        return result
    
    def analyze_newsletter_links(self, links: List[str]) -> Dict:
        """
        Analyze newsletter links without storing them in the database.
        This determines which links should be opened without committing to database storage.
        
        Args:
            links: List of URLs to analyze
            
        Returns:
            Dict with categorized links and statistics for decision making
        """
        if not links:
            return {
                'new_links': [],
                'existing_links': [],
                'blacklisted_links': [],
                'links_to_open': [],
                'statistics': {'total_links': 0, 'new_count': 0, 'existing_count': 0, 'blacklisted_count': 0}
            }
        
        result = {
            'new_links': [],
            'existing_links': [],
            'blacklisted_links': [],
            'links_to_open': [],
            'statistics': {
                'total_links': len(links),
                'new_count': 0,
                'existing_count': 0,
                'blacklisted_count': 0
            }
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Analyze each link without storing
            for url in links:
                try:
                    url_hash = self._hash_url(url)
                    
                    # Check if URL should be auto-blacklisted based on patterns
                    auto_blacklist_reason = self._should_auto_blacklist_url(url)
                    if auto_blacklist_reason:
                        result['blacklisted_links'].append(url)
                        result['statistics']['blacklisted_count'] += 1
                        continue
                    
                    # Check if link already exists and its status
                    cursor.execute("""
                        SELECT id, is_blacklisted, last_seen
                        FROM links WHERE url_hash = ?
                    """, (url_hash,))
                    
                    existing_link = cursor.fetchone()
                    
                    if existing_link:
                        link_id, is_blacklisted, last_seen_str = existing_link
                        
                        if is_blacklisted:
                            result['blacklisted_links'].append(url)
                            result['statistics']['blacklisted_count'] += 1
                        else:
                            # Check if link was opened recently (within last few days)
                            from datetime import datetime, date
                            
                            # Parse last_seen date
                            if last_seen_str:
                                try:
                                    if isinstance(last_seen_str, str):
                                        last_seen_date = datetime.strptime(last_seen_str, '%Y-%m-%d').date()
                                    else:
                                        last_seen_date = last_seen_str
                                    
                                    days_since_opened = (date.today() - last_seen_date).days
                                    
                                    # Don't re-open links that were opened recently
                                    recent_days_threshold = getattr(self.config, 'RECENT_LINK_DAYS', 3)
                                    
                                    if days_since_opened <= recent_days_threshold:
                                        result['blacklisted_links'].append(url)
                                        result['statistics']['blacklisted_count'] += 1
                                        self.logger.debug(f"Skipping recently opened link ({days_since_opened} days ago): {url}")
                                    else:
                                        result['existing_links'].append(url)
                                        result['statistics']['existing_count'] += 1
                                        result['links_to_open'].append(url)
                                        
                                except (ValueError, TypeError):
                                    # If date parsing fails, treat as normal existing link
                                    result['existing_links'].append(url)
                                    result['statistics']['existing_count'] += 1
                                    result['links_to_open'].append(url)
                            else:
                                # No last_seen date, treat as normal existing link
                                result['existing_links'].append(url)
                                result['statistics']['existing_count'] += 1
                                result['links_to_open'].append(url)
                    else:
                        # New link - add to open list
                        result['new_links'].append(url)
                        result['statistics']['new_count'] += 1
                        result['links_to_open'].append(url)
                
                except Exception as e:
                    self.logger.error(f"Error analyzing link {url}: {e}")
                    continue
            
            self.logger.info(f"Analyzed {len(links)} links: {result['statistics']['new_count']} new, "
                           f"{result['statistics']['existing_count']} existing, "
                           f"{result['statistics']['blacklisted_count']} blacklisted, "
                           f"{len(result['links_to_open'])} to open")
            
            return result
    
    def record_opened_links(self, links: List[str], newsletter_hash: str = None) -> Dict:
        """
        Record links that were actually opened in the browser.
        This should only be called AFTER links have been successfully opened.
        
        Args:
            links: List of URLs that were successfully opened
            newsletter_hash: Optional hash of newsletter content for change tracking
            
        Returns:
            Dict with recording statistics
        """
        if not links:
            self.logger.info("No links to record as opened")
            return {'recorded_count': 0}
        
        today = date.today()
        now = datetime.now()
        
        # Run auto-blacklisting for old links if enabled
        aged_count = self._auto_blacklist_old_links()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create newsletter run record
            cursor.execute("""
                INSERT INTO newsletter_runs 
                (run_date, run_time, newsletter_hash, links_found, opened_links, success)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (today, now, newsletter_hash, len(links), len(links), True))
            
            run_id = cursor.lastrowid
            recorded_count = 0
            
            # Process each opened link
            for position, url in enumerate(links, 1):
                try:
                    url_hash = self._hash_url(url)
                    domain = self._extract_domain(url)
                    
                    # Check if link already exists
                    cursor.execute("""
                        SELECT id, seen_count
                        FROM links WHERE url_hash = ?
                    """, (url_hash,))
                    
                    existing_link = cursor.fetchone()
                    
                    if existing_link:
                        link_id, seen_count = existing_link
                        
                        # Update existing link - increment seen count for opened links
                        cursor.execute("""
                            UPDATE links 
                            SET last_seen = ?, seen_count = seen_count + 1
                            WHERE id = ?
                        """, (today, link_id))
                        
                    else:
                        # Create new link record (only for successfully opened links)
                        cursor.execute("""
                            INSERT INTO links 
                            (url, domain, first_seen, last_seen, url_hash)
                            VALUES (?, ?, ?, ?, ?)
                        """, (url, domain, today, today, url_hash))
                        
                        link_id = cursor.lastrowid
                    
                    # Record link appearance in this run
                    cursor.execute("""
                        INSERT OR IGNORE INTO link_appearances
                        (link_id, run_id, position)
                        VALUES (?, ?, ?)
                    """, (link_id, run_id, position))
                    
                    recorded_count += 1
                
                except Exception as e:
                    self.logger.error(f"Error recording opened link {url}: {e}")
                    continue
            
            conn.commit()
            
            self.logger.info(f"Recorded {recorded_count} successfully opened links in database")
            if aged_count > 0:
                self.logger.info(f"Auto-blacklisted {aged_count} old links during cleanup")
            
            return {
                'recorded_count': recorded_count,
                'auto_blacklisted_aged': aged_count
            }
    
    def blacklist_url(self, url: str, reason: str = "read") -> bool:
        """
        Add a URL to the blacklist.
        
        Args:
            url: URL to blacklist
            reason: Reason for blacklisting (e.g., 'read', 'not_interested')
            
        Returns:
            True if successfully blacklisted, False if URL not found
        """
        url_hash = self._hash_url(url)
        today = date.today()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE links 
                SET is_blacklisted = TRUE, blacklisted_date = ?, blacklist_reason = ?
                WHERE url_hash = ?
            """, (today, reason, url_hash))
            
            if cursor.rowcount > 0:
                self.logger.info(f"Blacklisted URL: {url} (reason: {reason})")
                return True
            else:
                self.logger.warning(f"URL not found for blacklisting: {url}")
                return False
    
    def unblacklist_url(self, url: str) -> bool:
        """Remove a URL from the blacklist."""
        url_hash = self._hash_url(url)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE links 
                SET is_blacklisted = FALSE, blacklisted_date = NULL, blacklist_reason = NULL
                WHERE url_hash = ?
            """, (url_hash,))
            
            if cursor.rowcount > 0:
                self.logger.info(f"Removed from blacklist: {url}")
                return True
            else:
                self.logger.warning(f"URL not found for un-blacklisting: {url}")
                return False
    
    def get_reading_statistics(self) -> Dict:
        """Get comprehensive reading statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Basic counts
            cursor.execute("SELECT COUNT(*) FROM links")
            total_links = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = TRUE")
            blacklisted_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM newsletter_runs")
            total_runs = cursor.fetchone()[0]
            
            # Domain statistics
            cursor.execute("""
                SELECT domain, COUNT(*) as count
                FROM links 
                GROUP BY domain 
                ORDER BY count DESC 
                LIMIT 10
            """)
            top_domains = dict(cursor.fetchall())
            
            # Recent activity
            cursor.execute("""
                SELECT run_date, SUM(new_links) as new_links, SUM(opened_links) as opened_links
                FROM newsletter_runs
                WHERE run_date >= date('now', '-7 days')
                GROUP BY run_date
                ORDER BY run_date DESC
            """)
            recent_activity = [
                {'date': row[0], 'new_links': row[1], 'opened_links': row[2]}
                for row in cursor.fetchall()
            ]
            
            # Calculate reading efficiency
            reading_efficiency = 0
            if total_links > 0:
                reading_efficiency = (blacklisted_count / total_links) * 100
            
            return {
                'total_links_encountered': total_links,
                'blacklisted_links': blacklisted_count,
                'active_links': total_links - blacklisted_count,
                'total_automation_runs': total_runs,
                'reading_efficiency_percent': round(reading_efficiency, 1),
                'top_domains': top_domains,
                'recent_activity': recent_activity
            }
    
    def export_data(self, export_path: Path, format: str = 'json') -> bool:
        """Export link data to file."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get all links with metadata
                cursor.execute("""
                    SELECT url, title, domain, first_seen, last_seen, 
                           seen_count, is_blacklisted, blacklisted_date, blacklist_reason
                    FROM links
                    ORDER BY first_seen DESC
                """)
                
                links_data = [
                    {
                        'url': row[0],
                        'title': row[1],
                        'domain': row[2],
                        'first_seen': row[3],
                        'last_seen': row[4],
                        'seen_count': row[5],
                        'is_blacklisted': bool(row[6]),
                        'blacklisted_date': row[7],
                        'blacklist_reason': row[8]
                    }
                    for row in cursor.fetchall()
                ]
                
                # Export data
                if format.lower() == 'json':
                    with open(export_path, 'w') as f:
                        json.dump({
                            'export_date': datetime.now().isoformat(),
                            'total_links': len(links_data),
                            'links': links_data
                        }, f, indent=2, default=str)
                
                self.logger.info(f"Exported {len(links_data)} links to {export_path}")
                return True
                
        except Exception as e:
            self.logger.error(f"Failed to export data: {e}")
            return False
    
    def cleanup_old_data(self, days_to_keep: int = 90) -> int:
        """Remove old data beyond specified days."""
        cutoff_date = date.today().replace(day=1)  # Keep at least current month
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Remove old newsletter runs
            cursor.execute("""
                DELETE FROM newsletter_runs 
                WHERE run_date < date('now', '-{} days')
            """.format(days_to_keep))
            
            removed_count = cursor.rowcount
            conn.commit()
            
            self.logger.info(f"Cleaned up {removed_count} old records")
            return removed_count


# Utility functions for command-line usage
def create_link_manager(config_dir: Path, logger: logging.Logger = None) -> LinkManager:
    """Factory function to create LinkManager instance."""
    db_path = config_dir / 'newsletter_links.db'
    return LinkManager(db_path, logger)


if __name__ == "__main__":
    # Basic testing/demo functionality
    import tempfile
    import sys
    
    # Create temporary database for testing
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp:
        test_db_path = Path(tmp.name)
    
    print(f"Testing LinkManager with database: {test_db_path}")
    
    # Initialize LinkManager
    lm = LinkManager(test_db_path)
    
    # Test with sample links
    sample_links = [
        "https://example.com/article1",
        "https://example.com/article2", 
        "https://news.com/story1",
        "https://example.com/article1",  # Duplicate
    ]
    
    print("\\nProcessing sample links...")
    result = lm.process_newsletter_links(sample_links, "sample_hash_123")
    
    print(f"Result: {result}")
    
    print("\\nBlacklisting first article...")
    lm.blacklist_url(sample_links[0], "test_read")
    
    print("\\nProcessing links again...")
    result2 = lm.process_newsletter_links(sample_links, "sample_hash_124")
    print(f"Result: {result2}")
    
    print("\\nReading statistics:")
    stats = lm.get_reading_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Cleanup
    test_db_path.unlink()
    print(f"\\nTest completed successfully!")