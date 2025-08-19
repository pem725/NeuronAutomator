#!/usr/bin/env python3
"""
Blacklist Time Rewind Tool
===========================

Allows users to "rewind" the blacklist to a previous state by removing
blacklist entries that were added within the last X days.

This is useful for:
- Testing disruptions in learning material
- Re-introducing previously read content for review
- Experimenting with different content exposure patterns
- Recovering from accidental over-blacklisting

Author: AI Assistant
Created: 2025
License: MIT
Version: 1.4.0
"""

import sys
import sqlite3
import argparse
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import json
import logging

# Try to import LinkManager for database access
try:
    from link_manager import LinkManager
    from config import ACTIVE_CONFIG
    LINK_MANAGER_AVAILABLE = True
except ImportError:
    LINK_MANAGER_AVAILABLE = False
    ACTIVE_CONFIG = None


class BlacklistRewind:
    """
    Tool for rewinding blacklist state to a previous point in time.
    
    Allows users to restore access to links that were blacklisted within
    the last X days, effectively "rewinding" their reading history.
    """
    
    def __init__(self, database_path: Path, config=None, logger: Optional[logging.Logger] = None):
        """Initialize the rewind tool."""
        self.db_path = database_path
        self.config = config
        self.logger = logger or self._setup_logger()
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Database not found at {self.db_path}")
            
        self.logger.info(f"BlacklistRewind initialized with database: {self.db_path}")
    
    def _setup_logger(self) -> logging.Logger:
        """Setup default logger."""
        logger = logging.getLogger("blacklist_rewind")
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stdout)
            formatter = logging.Formatter('%(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def get_blacklist_statistics(self) -> Dict:
        """Get current blacklist statistics."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Total blacklisted links
            cursor.execute("SELECT COUNT(*) FROM links WHERE is_blacklisted = TRUE")
            total_blacklisted = cursor.fetchone()[0]
            
            # Blacklisted by date (last 30 days)
            cursor.execute("""
                SELECT blacklisted_date, COUNT(*) as count
                FROM links 
                WHERE is_blacklisted = TRUE 
                AND blacklisted_date >= date('now', '-30 days')
                GROUP BY blacklisted_date
                ORDER BY blacklisted_date DESC
            """)
            
            recent_blacklists = [
                {'date': row[0], 'count': row[1]} 
                for row in cursor.fetchall()
            ]
            
            # Blacklist reasons summary
            cursor.execute("""
                SELECT blacklist_reason, COUNT(*) as count
                FROM links 
                WHERE is_blacklisted = TRUE
                GROUP BY blacklist_reason
                ORDER BY count DESC
            """)
            
            blacklist_reasons = [
                {'reason': row[0] or 'not specified', 'count': row[1]}
                for row in cursor.fetchall()
            ]
            
            return {
                'total_blacklisted': total_blacklisted,
                'recent_blacklists': recent_blacklists,
                'blacklist_reasons': blacklist_reasons
            }
    
    def preview_rewind(self, days: int) -> Dict:
        """
        Preview what would happen if we rewind X days.
        
        Args:
            days: Number of days to rewind
            
        Returns:
            Dict with preview information
        """
        cutoff_date = date.today() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Find links that would be restored (un-blacklisted)
            cursor.execute("""
                SELECT url, blacklisted_date, blacklist_reason, domain, seen_count
                FROM links 
                WHERE is_blacklisted = TRUE 
                AND blacklisted_date >= ?
                ORDER BY blacklisted_date DESC
            """, (cutoff_date,))
            
            restore_candidates = []
            for row in cursor.fetchall():
                restore_candidates.append({
                    'url': row[0],
                    'blacklisted_date': row[1],
                    'reason': row[2] or 'not specified',
                    'domain': row[3],
                    'seen_count': row[4]
                })
            
            # Count by reason
            reason_counts = {}
            for candidate in restore_candidates:
                reason = candidate['reason']
                reason_counts[reason] = reason_counts.get(reason, 0) + 1
            
            # Count by domain
            domain_counts = {}
            for candidate in restore_candidates:
                domain = candidate['domain']
                domain_counts[domain] = domain_counts.get(domain, 0) + 1
            
            return {
                'cutoff_date': cutoff_date.isoformat(),
                'days_back': days,
                'links_to_restore': restore_candidates,
                'restore_count': len(restore_candidates),
                'reason_breakdown': reason_counts,
                'domain_breakdown': domain_counts
            }
    
    def create_backup(self) -> Path:
        """
        Create a backup of current blacklist state.
        
        Returns:
            Path to backup file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.db_path.parent / "backups"
        backup_dir.mkdir(exist_ok=True)
        
        backup_file = backup_dir / f"blacklist_backup_{timestamp}.json"
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Export all blacklisted links
            cursor.execute("""
                SELECT url, blacklisted_date, blacklist_reason, domain, 
                       first_seen, last_seen, seen_count, url_hash
                FROM links 
                WHERE is_blacklisted = TRUE
            """)
            
            blacklist_data = []
            for row in cursor.fetchall():
                blacklist_data.append({
                    'url': row[0],
                    'blacklisted_date': row[1],
                    'blacklist_reason': row[2],
                    'domain': row[3],
                    'first_seen': row[4],
                    'last_seen': row[5],
                    'seen_count': row[6],
                    'url_hash': row[7]
                })
        
        backup_content = {
            'backup_date': datetime.now().isoformat(),
            'database_path': str(self.db_path),
            'total_blacklisted': len(blacklist_data),
            'blacklisted_links': blacklist_data
        }
        
        with open(backup_file, 'w') as f:
            json.dump(backup_content, f, indent=2, default=str)
        
        self.logger.info(f"Backup created: {backup_file}")
        return backup_file
    
    def perform_rewind(self, days: int, create_backup: bool = True) -> Dict:
        """
        Perform the actual rewind operation.
        
        Args:
            days: Number of days to rewind
            create_backup: Whether to create backup before operation
            
        Returns:
            Dict with operation results
        """
        if create_backup:
            backup_file = self.create_backup()
        else:
            backup_file = None
        
        cutoff_date = date.today() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get links that will be restored for reporting
            cursor.execute("""
                SELECT url, blacklisted_date, blacklist_reason
                FROM links 
                WHERE is_blacklisted = TRUE 
                AND blacklisted_date >= ?
            """, (cutoff_date,))
            
            restored_links = [
                {'url': row[0], 'blacklisted_date': row[1], 'reason': row[2]}
                for row in cursor.fetchall()
            ]
            
            # Perform the rewind - remove blacklist status for recent entries
            cursor.execute("""
                UPDATE links 
                SET is_blacklisted = FALSE,
                    blacklisted_date = NULL,
                    blacklist_reason = NULL
                WHERE is_blacklisted = TRUE 
                AND blacklisted_date >= ?
            """, (cutoff_date,))
            
            restored_count = cursor.rowcount
            conn.commit()
        
        self.logger.info(f"Rewind complete: {restored_count} links restored to available status")
        
        return {
            'success': True,
            'cutoff_date': cutoff_date.isoformat(),
            'days_rewound': days,
            'restored_count': restored_count,
            'restored_links': restored_links,
            'backup_file': str(backup_file) if backup_file else None
        }
    
    def restore_from_backup(self, backup_file: Path) -> Dict:
        """
        Restore blacklist from a backup file.
        
        Args:
            backup_file: Path to backup JSON file
            
        Returns:
            Dict with restoration results
        """
        if not backup_file.exists():
            raise FileNotFoundError(f"Backup file not found: {backup_file}")
        
        with open(backup_file, 'r') as f:
            backup_data = json.load(f)
        
        blacklisted_links = backup_data.get('blacklisted_links', [])
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            restored_count = 0
            for link_data in blacklisted_links:
                url_hash = link_data['url_hash']
                
                # Update the link to restore blacklist status
                cursor.execute("""
                    UPDATE links 
                    SET is_blacklisted = TRUE,
                        blacklisted_date = ?,
                        blacklist_reason = ?
                    WHERE url_hash = ?
                """, (
                    link_data['blacklisted_date'],
                    link_data['blacklist_reason'],
                    url_hash
                ))
                
                if cursor.rowcount > 0:
                    restored_count += 1
            
            conn.commit()
        
        self.logger.info(f"Restored {restored_count} blacklisted links from backup")
        
        return {
            'success': True,
            'backup_file': str(backup_file),
            'backup_date': backup_data.get('backup_date'),
            'restored_count': restored_count,
            'total_in_backup': len(blacklisted_links)
        }
    
    def list_recent_blacklists(self, days: int = 7) -> List[Dict]:
        """List recently blacklisted links for review."""
        cutoff_date = date.today() - timedelta(days=days)
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT url, blacklisted_date, blacklist_reason, domain, seen_count
                FROM links 
                WHERE is_blacklisted = TRUE 
                AND blacklisted_date >= ?
                ORDER BY blacklisted_date DESC
            """, (cutoff_date,))
            
            recent_blacklists = []
            for row in cursor.fetchall():
                recent_blacklists.append({
                    'url': row[0],
                    'blacklisted_date': row[1],
                    'reason': row[2] or 'not specified',
                    'domain': row[3],
                    'seen_count': row[4],
                    'days_ago': (date.today() - datetime.strptime(row[1], '%Y-%m-%d').date()).days
                })
            
            return recent_blacklists


def main():
    """Main CLI interface for blacklist rewind tool."""
    parser = argparse.ArgumentParser(
        description="Blacklist Time Rewind Tool - Restore previously blacklisted links",
        epilog="""
Examples:
  %(prog)s --preview 7           # Preview what would happen with 7-day rewind
  %(prog)s --rewind 3            # Rewind blacklist by 3 days
  %(prog)s --stats               # Show current blacklist statistics
  %(prog)s --recent 5            # Show links blacklisted in last 5 days
  %(prog)s --backup              # Create backup of current state
  %(prog)s --restore backup.json # Restore from backup file
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument("--preview", type=int, metavar="DAYS",
                       help="Preview rewind operation for X days without making changes")
    parser.add_argument("--rewind", type=int, metavar="DAYS", 
                       help="Perform rewind operation for X days")
    parser.add_argument("--stats", action="store_true",
                       help="Show current blacklist statistics")
    parser.add_argument("--recent", type=int, metavar="DAYS", default=7,
                       help="Show recently blacklisted links (default: 7 days)")
    parser.add_argument("--backup", action="store_true",
                       help="Create backup of current blacklist state")
    parser.add_argument("--restore", type=str, metavar="BACKUP_FILE",
                       help="Restore blacklist from backup file")
    parser.add_argument("--database", type=str, metavar="DB_PATH",
                       help="Path to newsletter database (auto-detected if not specified)")
    parser.add_argument("--no-backup", action="store_true",
                       help="Skip automatic backup when performing rewind")
    parser.add_argument("-y", "--yes", action="store_true",
                       help="Auto-confirm operations (non-interactive mode)")
    
    args = parser.parse_args()
    
    # Determine database path
    if args.database:
        db_path = Path(args.database)
    else:
        # Try to auto-detect database location
        possible_paths = [
            Path.home() / '.config' / 'neuron-automation' / 'newsletter_links.db',
            Path.home() / 'Library' / 'Application Support' / 'neuron-automation' / 'newsletter_links.db',
            Path.home() / 'AppData' / 'Local' / 'neuron-automation' / 'newsletter_links.db',
            Path.cwd() / 'newsletter_links.db'
        ]
        
        db_path = None
        for path in possible_paths:
            if path.exists():
                db_path = path
                break
        
        if not db_path:
            print("❌ Could not find newsletter database.")
            print("   Please specify path with --database option")
            print(f"   Searched locations:")
            for path in possible_paths:
                print(f"     • {path}")
            sys.exit(1)
    
    try:
        rewind_tool = BlacklistRewind(db_path, config=ACTIVE_CONFIG)
        
        # Handle different operations
        if args.stats:
            print("📊 Blacklist Statistics")
            print("=" * 50)
            
            stats = rewind_tool.get_blacklist_statistics()
            print(f"Total blacklisted links: {stats['total_blacklisted']}")
            
            print(f"\n📅 Recent blacklists (last 30 days):")
            for entry in stats['recent_blacklists'][:10]:
                print(f"  {entry['date']}: {entry['count']} links")
            
            print(f"\n📋 Blacklist reasons:")
            for reason in stats['blacklist_reasons'][:5]:
                print(f"  {reason['reason']}: {reason['count']} links")
        
        elif args.recent:
            print(f"🕒 Recently Blacklisted Links (last {args.recent} days)")
            print("=" * 60)
            
            recent_links = rewind_tool.list_recent_blacklists(args.recent)
            
            if not recent_links:
                print("No links blacklisted in the specified period.")
            else:
                for link in recent_links[:20]:  # Show top 20
                    print(f"📅 {link['days_ago']} days ago ({link['blacklisted_date']})")
                    print(f"   🔗 {link['url']}")
                    print(f"   📂 Domain: {link['domain']}")
                    print(f"   📊 Seen: {link['seen_count']} times")
                    print(f"   💭 Reason: {link['reason']}")
                    print()
                
                if len(recent_links) > 20:
                    print(f"... and {len(recent_links) - 20} more")
        
        elif args.preview is not None:
            print(f"🔍 Preview: Rewind {args.preview} days")
            print("=" * 50)
            
            preview = rewind_tool.preview_rewind(args.preview)
            
            print(f"Cutoff date: {preview['cutoff_date']}")
            print(f"Links to restore: {preview['restore_count']}")
            
            if preview['restore_count'] == 0:
                print("✅ No links would be restored (no recent blacklists found)")
            else:
                print(f"\n📊 Restoration breakdown:")
                print(f"By reason:")
                for reason, count in preview['reason_breakdown'].items():
                    print(f"  • {reason}: {count} links")
                
                print(f"By domain:")
                for domain, count in list(preview['domain_breakdown'].items())[:5]:
                    print(f"  • {domain}: {count} links")
                
                print(f"\n📋 Links to restore (showing first 10):")
                for link in preview['links_to_restore'][:10]:
                    print(f"  📅 {link['blacklisted_date']} - {link['url'][:60]}...")
                
                if len(preview['links_to_restore']) > 10:
                    print(f"  ... and {len(preview['links_to_restore']) - 10} more")
        
        elif args.rewind is not None:
            print(f"⏪ Performing Rewind: {args.rewind} days")
            print("=" * 50)
            
            # Show preview first
            preview = rewind_tool.preview_rewind(args.rewind)
            print(f"This will restore {preview['restore_count']} links to available status")
            
            if preview['restore_count'] == 0:
                print("✅ No links to restore - operation not needed")
                sys.exit(0)
            
            # Confirm operation
            if not args.yes:
                print(f"\n⚠️  This operation will:")
                print(f"   • Remove blacklist status from {preview['restore_count']} links")
                print(f"   • Make these links available for opening again")
                print(f"   • Create backup (unless --no-backup specified)")
                
                response = input("\nProceed with rewind? (y/N): ")
                if response.lower() != 'y':
                    print("Operation cancelled.")
                    sys.exit(0)
            
            # Perform rewind
            result = rewind_tool.perform_rewind(
                args.rewind, 
                create_backup=not args.no_backup
            )
            
            if result['success']:
                print(f"✅ Rewind complete!")
                print(f"   • Restored {result['restored_count']} links")
                print(f"   • Cutoff date: {result['cutoff_date']}")
                if result['backup_file']:
                    print(f"   • Backup saved: {result['backup_file']}")
                
                print(f"\n🎯 These links are now available for opening again in future newsletter runs.")
            else:
                print("❌ Rewind operation failed")
                sys.exit(1)
        
        elif args.backup:
            print("💾 Creating Blacklist Backup")
            print("=" * 50)
            
            backup_file = rewind_tool.create_backup()
            print(f"✅ Backup created successfully: {backup_file}")
        
        elif args.restore:
            backup_file = Path(args.restore)
            print(f"📁 Restoring from Backup: {backup_file}")
            print("=" * 60)
            
            if not backup_file.exists():
                print(f"❌ Backup file not found: {backup_file}")
                sys.exit(1)
            
            # Confirm operation
            if not args.yes:
                print(f"⚠️  This operation will restore blacklist state from backup.")
                print(f"   Current blacklisted links may be affected.")
                
                response = input("Proceed with restoration? (y/N): ")
                if response.lower() != 'y':
                    print("Operation cancelled.")
                    sys.exit(0)
            
            result = rewind_tool.restore_from_backup(backup_file)
            
            if result['success']:
                print(f"✅ Restoration complete!")
                print(f"   • Restored {result['restored_count']} blacklisted links")
                print(f"   • From backup: {result['backup_date']}")
            else:
                print("❌ Restoration failed")
                sys.exit(1)
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()