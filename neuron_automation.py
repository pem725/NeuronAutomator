#!/usr/bin/env python3
"""
Neuron Daily Newsletter Automation Script
=========================================

Automatically opens the latest Neuron Daily newsletter with all article links
in separate tabs every weekday morning.

Author: AI Assistant  
Created: 2025
License: MIT
Version: 1.4.0
"""

__version__ = "1.4.0"
__author__ = "AI Assistant"
__license__ = "MIT"

import os
import sys
import time
import hashlib
import logging
import requests
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional, Tuple
from urllib.parse import urljoin, urlparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException, TimeoutException, NoSuchElementException,
    ElementNotInteractableException
)
from webdriver_manager.chrome import ChromeDriverManager

# Import configuration
try:
    from config import ACTIVE_CONFIG
except ImportError:
    print("Warning: config.py not found, using defaults")
    # Fallback if config not found
    class DefaultConfig:
        ENABLE_CHANGE_DETECTION = True
        CONTENT_CHECK_TIMEOUT = 10
        CACHE_CLEANUP_DAYS = 7
    ACTIVE_CONFIG = DefaultConfig

# Import LinkManager with fallback
try:
    from link_manager import LinkManager
    LINK_MANAGER_AVAILABLE = True
except ImportError as e:
    print(f"Warning: LinkManager not available: {e}")
    print("Link management features will be disabled")
    LinkManager = None
    LINK_MANAGER_AVAILABLE = False


class NeuronNewsletterAutomation:
    """Main class for automating Neuron Daily newsletter opening."""
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize the automation system."""
        self.config_path = config_path or Path.home() / '.config' / 'neuron-automation'
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        self.log_file = self.config_path / 'neuron_automation.log'
        self.setup_logging()
        
        # Configuration
        self.base_url = "https://www.theneurondaily.com/"
        self.max_retries = 3
        self.retry_delay = 5
        self.page_load_timeout = 30
        self.element_wait_timeout = 15
        
        # Initialize Link Manager for tracking and blacklisting (if available)
        if LINK_MANAGER_AVAILABLE and getattr(ACTIVE_CONFIG, 'LINK_MANAGEMENT_ENABLED', True):
            self.link_manager = LinkManager(
                database_path=self.config_path / getattr(ACTIVE_CONFIG, 'LINK_DATABASE_NAME', 'newsletter_links.db'),
                config=ACTIVE_CONFIG,
                logger=self.logger
            )
            self.logger.info("Link Management System initialized")
        else:
            self.link_manager = None
            self.logger.warning("Link Management System not available - running in legacy mode")
        
        self.logger.info("NeuronNewsletterAutomation initialized")
    
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def is_weekday(self) -> bool:
        """Check if today is a weekday (Monday-Friday)."""
        today = datetime.now().weekday()
        is_weekday = today < 5  # 0-4 are Monday-Friday
        self.logger.info(f"Today is {'a weekday' if is_weekday else 'weekend'}")
        return is_weekday
    
    def check_internet_connectivity(self) -> bool:
        """Check if internet connection is available."""
        try:
            response = requests.get("https://www.google.com", timeout=10)
            connected = response.status_code == 200
            self.logger.info(f"Internet connectivity: {'Available' if connected else 'Not available'}")
            return connected
        except requests.RequestException as e:
            self.logger.error(f"Internet connectivity check failed: {e}")
            return False
    
    def setup_chrome_driver(self) -> webdriver.Chrome:
        """Setup and return Chrome WebDriver with appropriate options."""
        self.logger.info("Setting up Chrome WebDriver to use regular browser")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Browser persistence options
        chrome_options.add_argument("--disable-extensions-except")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-default-apps")
        
        # Prevent browser from closing when automation ends
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
        # Enable remote debugging for connection attempts
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        try:
            # First try to connect to an existing Chrome instance
            try:
                self.logger.info("Attempting to connect to existing Chrome instance...")
                chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.set_page_load_timeout(self.page_load_timeout)
                self.logger.info("Connected to existing Chrome instance")
                return driver
            except Exception as e:
                self.logger.info(f"No existing Chrome instance found: {e}")
                
                # Fall back to starting new Chrome instance with regular profile
                self.logger.info("Starting new Chrome instance with regular profile...")
                chrome_options = Options()
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("--disable-dev-shm-usage")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--window-size=1920,1080")
                chrome_options.add_argument("--start-maximized")
                
                # Browser persistence options for fallback
                chrome_options.add_experimental_option("detach", True)
                chrome_options.add_experimental_option("useAutomationExtension", False)
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
                chrome_options.add_argument("--disable-blink-features=AutomationControlled")
                
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=chrome_options)
                driver.set_page_load_timeout(self.page_load_timeout)
                self.logger.info("New Chrome instance created with regular profile")
                return driver
                
        except Exception as e:
            self.logger.error(f"Failed to setup Chrome WebDriver: {e}")
            raise
    
    def wait_for_page_load(self, driver: webdriver.Chrome, timeout: int = None) -> bool:
        """Wait for page to fully load."""
        timeout = timeout or self.element_wait_timeout
        try:
            WebDriverWait(driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            # Additional wait for dynamic content
            time.sleep(2)
            return True
        except TimeoutException:
            self.logger.warning("Page load timeout reached")
            return False
    
    def find_latest_newsletter_url(self, driver: webdriver.Chrome) -> Optional[str]:
        """Find the URL of the latest daily newsletter post."""
        self.logger.info("Searching for latest newsletter post")
        
        try:
            # Look for the JSON data containing post information
            import json
            import re
            
            # Get the page source and extract JSON data
            page_source = driver.page_source
            
            # Look for paginatedPosts data in the page
            json_pattern = r'"paginatedPosts":\s*({[^}]*"posts":\s*\[[^\]]*\][^}]*})'
            match = re.search(json_pattern, page_source, re.DOTALL)
            
            if match:
                try:
                    # Extract and parse the posts data
                    posts_data = json.loads(match.group(1))
                    posts = posts_data.get('posts', [])
                    
                    if posts:
                        # Get the first (most recent) post
                        latest_post = posts[0]
                        post_slug = latest_post.get('parameterized_web_title') or latest_post.get('slug')
                        
                        if post_slug:
                            newsletter_url = f"{self.base_url}p/{post_slug}"
                            self.logger.info(f"Found latest newsletter: {latest_post.get('web_title', 'Unknown Title')}")
                            self.logger.info(f"Newsletter URL: {newsletter_url}")
                            return newsletter_url
                        else:
                            self.logger.error("Could not extract post slug from latest post")
                    else:
                        self.logger.error("No posts found in JSON data")
                        
                except json.JSONDecodeError as e:
                    self.logger.error(f"Failed to parse JSON data: {e}")
            else:
                self.logger.warning("Could not find paginatedPosts JSON in page source")
            
            # Fallback: Look for post links in the HTML
            self.logger.info("Trying fallback method: searching for post links in HTML")
            
            # Look for links that match the /p/ pattern
            post_links = driver.find_elements(By.CSS_SELECTOR, "a[href*='/p/']")
            
            if post_links:
                # Get the first post link
                latest_link = post_links[0]
                href = latest_link.get_attribute('href')
                
                if href and '/p/' in href:
                    self.logger.info(f"Found latest newsletter via HTML fallback: {href}")
                    return href
                    
        except Exception as e:
            self.logger.error(f"Error finding latest newsletter URL: {e}")
        
        self.logger.error("Could not find latest newsletter URL")
        return None
    
    def extract_newsletter_links(self, driver: webdriver.Chrome) -> List[str]:
        """Extract all relevant links from the newsletter page."""
        self.logger.info("Extracting newsletter links")
        links = []
        
        try:
            # Wait for the page content to load
            WebDriverWait(driver, self.element_wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # First, try to find the main content area of the newsletter post
            content_selectors = [
                "div[class*='post-content']",     # Common post content class
                "article[class*='post']",         # Article element
                "div[class*='newsletter']",       # Newsletter-specific content
                "div[class*='content']",          # General content div
                "main",                          # Main content element
                ".available-content"             # Substack-style container
            ]
            
            content_area = None
            for selector in content_selectors:
                try:
                    content_area = driver.find_element(By.CSS_SELECTOR, selector)
                    self.logger.info(f"Found content area using selector: {selector}")
                    break
                except:
                    continue
            
            if not content_area:
                self.logger.info("No specific content area found, using full page")
                content_area = driver.find_element(By.TAG_NAME, "body")
            
            # Look for links within the content area, prioritizing list items and paragraphs
            link_containers = []
            
            # Priority 1: Links in list items (most newsletter content is in lists)
            list_items = content_area.find_elements(By.TAG_NAME, "li")
            for li in list_items:
                link_containers.extend(li.find_elements(By.TAG_NAME, "a"))
            
            # Priority 2: Links in paragraphs
            paragraphs = content_area.find_elements(By.TAG_NAME, "p") 
            for p in paragraphs:
                link_containers.extend(p.find_elements(By.TAG_NAME, "a"))
            
            # Priority 3: All other links in content area (fallback)
            if not link_containers:
                link_containers = content_area.find_elements(By.TAG_NAME, "a")
            
            # Remove duplicate elements while preserving order
            seen_elements = set()
            unique_links = []
            for link in link_containers:
                element_id = id(link)
                if element_id not in seen_elements:
                    seen_elements.add(element_id)
                    unique_links.append(link)
            
            self.logger.info(f"Found {len(unique_links)} unique link elements in newsletter content")
            
            # Process each link
            for link_elem in unique_links:
                try:
                    href = link_elem.get_attribute("href")
                    text = link_elem.text.strip()
                    
                    if not href or not text:
                        continue
                    
                    # Filter for relevant newsletter article links
                    if self.is_relevant_article_link(href, text):
                        absolute_url = urljoin(self.base_url, href)
                        if absolute_url not in links:
                            links.append(absolute_url)
                            self.logger.debug(f"Added link: {text[:50]}... -> {absolute_url}")
                
                except Exception as e:
                    self.logger.debug(f"Error processing link element: {e}")
                    continue
            
            self.logger.info(f"Extracted {len(links)} relevant article links")
            return links
            
        except TimeoutException:
            self.logger.error("Timeout waiting for page content")
            return []
        except Exception as e:
            self.logger.error(f"Error extracting links: {e}")
            return []
    
    def is_relevant_article_link(self, href: str, text: str) -> bool:
        """Determine if a link is a relevant article link."""
        if not href or not text:
            return False
        
        # Skip obvious non-article links
        skip_patterns = [
            '#', 'javascript:', 'mailto:', 'tel:',
            'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com',
            'youtube.com', 'tiktok.com', 'discord.com',
            'subscribe', 'unsubscribe', 'privacy', 'terms',
            'contact', 'about', 'home', 'archive'
        ]
        
        href_lower = href.lower()
        text_lower = text.lower()
        
        for pattern in skip_patterns:
            if pattern in href_lower or pattern in text_lower:
                return False
        
        # Must have meaningful text (not just symbols or very short)
        if len(text.strip()) < 5:
            return False
        
        # Skip common navigation text
        nav_text = ['read more', 'click here', 'learn more', 'view all', 'see more']
        if any(nav in text_lower for nav in nav_text):
            return False
        
        # Prefer external links or links that look like articles
        if not href.startswith(self.base_url):
            return True
        
        # For internal links, look for article-like patterns
        article_indicators = ['article', 'post', 'news', 'story', 'blog']
        if any(indicator in href_lower for indicator in article_indicators):
            return True
        
        # If text looks like an article title (reasonable length, capitalized)
        words = text.split()
        if 3 <= len(words) <= 20 and any(word[0].isupper() for word in words):
            return True
        
        return False
    
    
    def get_content_hash(self, url: str = None) -> Optional[str]:
        """Get hash of key newsletter content areas for change detection."""
        try:
            target_url = url or self.base_url
            timeout = getattr(ACTIVE_CONFIG, 'CONTENT_CHECK_TIMEOUT', 10)
            response = requests.get(target_url, timeout=timeout, headers={
                'User-Agent': 'Mozilla/5.0 (compatible; NeuronAutomation/1.0)'
            })
            response.raise_for_status()
            
            # Import BeautifulSoup for content parsing
            try:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Focus on content areas likely to change with new newsletters
                content_selectors = [
                    'main', '.newsletter', '.content', 'article', 
                    '.post', '.entry', '.news-content', '[role="main"]'
                ]
                
                content_areas = []
                for selector in content_selectors:
                    elements = soup.select(selector)
                    content_areas.extend(elements)
                
                # If no specific content areas found, use body
                if not content_areas:
                    content_areas = soup.select('body')
                
                # Extract text content and create hash
                content_text = ' '.join([
                    area.get_text(strip=True) 
                    for area in content_areas
                ])
                
                # Create hash of content
                content_hash = hashlib.md5(content_text.encode('utf-8')).hexdigest()
                self.logger.debug(f"Content hash generated: {content_hash[:12]}...")
                return content_hash
                
            except ImportError:
                # Fallback: use raw HTML if BeautifulSoup not available
                content_hash = hashlib.md5(response.text.encode('utf-8')).hexdigest()
                self.logger.debug(f"Raw HTML hash generated: {content_hash[:12]}...")
                return content_hash
                
        except Exception as e:
            self.logger.warning(f"Failed to get content hash: {e}")
            return None
    
    def should_run_automation(self) -> bool:
        """Check if newsletter content has changed since last run today."""
        # Check if change detection is enabled
        if not getattr(ACTIVE_CONFIG, 'ENABLE_CHANGE_DETECTION', True):
            self.logger.debug("Change detection disabled - proceeding with automation")
            return True
        
        today = datetime.now().strftime("%Y-%m-%d")
        cache_file = self.config_path / f"last_run_{today}.txt"
        
        # Get current content hash
        current_hash = self.get_content_hash()
        if current_hash is None:
            self.logger.warning("Could not get content hash, proceeding with automation")
            return True
        
        # Check if we've run today and if content has changed
        if cache_file.exists():
            try:
                last_hash = cache_file.read_text(encoding='utf-8').strip()
                if current_hash == last_hash:
                    self.logger.info("No content changes detected since last run today")
                    return False
                else:
                    self.logger.info("Content changes detected since last run!")
                    # Update cache with new hash
                    cache_file.write_text(current_hash, encoding='utf-8')
                    return True
            except Exception as e:
                self.logger.warning(f"Error reading cache file: {e}")
                
        # First run of the day - save hash and proceed
        try:
            cache_file.write_text(current_hash, encoding='utf-8')
            self.logger.info("First run of the day - proceeding with automation")
        except Exception as e:
            self.logger.warning(f"Could not save content hash: {e}")
            
        return True
    
    def cleanup_old_cache_files(self) -> None:
        """Clean up old cache files to prevent directory bloat."""
        try:
            cleanup_days = getattr(ACTIVE_CONFIG, 'CACHE_CLEANUP_DAYS', 7)
            cutoff_time = datetime.now().timestamp() - (cleanup_days * 24 * 60 * 60)
            
            # Find old cache files
            for cache_file in self.config_path.glob("last_run_*.txt"):
                if cache_file.stat().st_mtime < cutoff_time:
                    cache_file.unlink()
                    self.logger.debug(f"Removed old cache file: {cache_file.name}")
                    
        except Exception as e:
            self.logger.warning(f"Error cleaning up cache files: {e}")
    
    def run_automation(self) -> bool:
        """Run the complete automation workflow."""
        self.logger.info("Starting Neuron Newsletter automation")
        
        # Check if it's a weekday
        if not self.is_weekday():
            self.logger.info("Not a weekday - skipping automation")
            return True
        
        # Check internet connectivity
        if not self.check_internet_connectivity():
            self.logger.error("No internet connection - cannot proceed")
            return False
        
        # Check if automation should run (content change detection)
        if not self.should_run_automation():
            self.logger.info("Skipping automation - no content changes detected")
            # Clean up old cache files before exiting
            self.cleanup_old_cache_files()
            return True
        
        # Retry mechanism for the main workflow
        for attempt in range(1, self.max_retries + 1):
            self.logger.info(f"Automation attempt {attempt}/{self.max_retries}")
            
            driver = None
            try:
                # Setup driver and load main page
                driver = self.setup_chrome_driver()
                self.logger.info(f"Loading main page: {self.base_url}")
                driver.get(self.base_url)
                
                if not self.wait_for_page_load(driver):
                    raise TimeoutException("Main page failed to load completely")
                
                # Find the latest newsletter post URL
                newsletter_url = self.find_latest_newsletter_url(driver)
                if not newsletter_url:
                    raise Exception("Could not find latest newsletter post")
                
                # Navigate to the specific newsletter post
                self.logger.info(f"Loading latest newsletter post: {newsletter_url}")
                driver.get(newsletter_url)
                
                if not self.wait_for_page_load(driver):
                    raise TimeoutException("Newsletter post failed to load completely")
                
                # Extract links from the newsletter post
                raw_links = self.extract_newsletter_links(driver)
                
                if not raw_links:
                    self.logger.warning("No newsletter links found")
                    self.logger.info("Keeping main newsletter page open")
                    # Keep driver open with just the main page
                    return True
                
                if self.link_manager:
                    # Analyze links through LinkManager (without storing in database yet)
                    self.logger.info(f"Analyzing {len(raw_links)} extracted links through LinkManager")
                    
                    # Analyze links to determine which ones should be opened
                    analysis_result = self.link_manager.analyze_newsletter_links(raw_links)
                    links_to_open = analysis_result['links_to_open']
                    stats = analysis_result['statistics']
                    
                    # Log link analysis summary
                    self.logger.info(f"Link Analysis: {stats['total_links']} total, "
                                   f"{stats['new_count']} new, "
                                   f"{stats['existing_count']} seen before, " 
                                   f"{stats['blacklisted_count']} blacklisted, "
                                   f"{len(links_to_open)} will be opened")
                    
                    if not links_to_open:
                        self.logger.info("No new links to open - all content previously seen or blacklisted")
                        self.logger.info("Keeping main newsletter page open")
                        return True
                else:
                    # Legacy mode: open all extracted links (no link management)
                    links_to_open = raw_links
                    self.logger.info("Link Management disabled - opening all extracted links (legacy mode)")
                
                # Open the determined article tabs
                self.logger.info(f"Opening {len(links_to_open)} article tabs")
                successfully_opened_links = []
                
                for i, link in enumerate(links_to_open, 1):
                    try:
                        self.logger.info(f"Opening tab {i}/{len(links_to_open)}: {link}")
                        driver.execute_script(f"window.open('{link}', '_blank');")
                        successfully_opened_links.append(link)
                        time.sleep(1)  # Small delay between tab openings
                    except Exception as e:
                        self.logger.error(f"Failed to open tab for {link}: {e}")
                        continue
                
                # Record successfully opened links in database (only now!)
                if self.link_manager and successfully_opened_links:
                    newsletter_hash = self.get_content_hash(newsletter_url) or "unknown"
                    record_result = self.link_manager.record_opened_links(successfully_opened_links, newsletter_hash)
                    self.logger.info(f"Recorded {record_result['recorded_count']} successfully opened links in database")
                
                # Switch back to the main newsletter tab
                driver.switch_to.window(driver.window_handles[0])
                
                # Detach from browser to keep it open after script ends
                self.logger.info(f"Successfully opened {len(successfully_opened_links)} article tabs")
                self.logger.info("Detaching from browser - tabs will remain open for reading")
                
                # Add a small delay to ensure all tabs are fully loaded
                time.sleep(2)
                
                # Important: Don't call driver.quit() - let Chrome detach naturally
                self.logger.info("🌅 Good morning! Your newsletter articles are ready to read.")
                self.logger.info(f"📖 {len(successfully_opened_links)} tabs opened in your browser")
                
                return True
                
            except Exception as e:
                self.logger.error(f"Attempt {attempt} failed: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                
                if attempt < self.max_retries:
                    self.logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)
                else:
                    self.logger.error("All retry attempts failed")
                    return False
        
        return False


def main():
    """Main entry point for the script."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Neuron Daily Newsletter Automation",
        prog="neuron-automation"
    )
    parser.add_argument("--version", action="version", 
                       version=f"%(prog)s {__version__}")
    parser.add_argument("--check-updates", action="store_true",
                       help="Check for available updates")
    
    # Link management commands
    parser.add_argument("--stats", action="store_true",
                       help="Show reading statistics and link analysis")
    parser.add_argument("--blacklist", type=str, metavar="URL",
                       help="Add a URL to the blacklist")
    parser.add_argument("--unblacklist", type=str, metavar="URL", 
                       help="Remove a URL from the blacklist")
    parser.add_argument("--list-blacklisted", action="store_true",
                       help="List all blacklisted URLs")
    parser.add_argument("--export-links", type=str, metavar="FILE",
                       help="Export all link data to JSON file")
    
    # Blacklist rewind commands
    parser.add_argument("--rewind-preview", type=int, metavar="DAYS",
                       help="Preview rewind operation for X days without making changes")
    parser.add_argument("--rewind", type=int, metavar="DAYS",
                       help="Rewind blacklist by X days (restores recently blacklisted links)")
    parser.add_argument("--backup-blacklist", action="store_true",
                       help="Create backup of current blacklist state")
    parser.add_argument("--recent-blacklisted", type=int, metavar="DAYS", default=7,
                       help="Show recently blacklisted links (default: 7 days)")
    parser.add_argument("--no-backup", action="store_true",
                       help="Skip automatic backup when performing rewind")
    
    args = parser.parse_args()
    
    if args.check_updates:
        print(f"Current version: {__version__}")
        print("To update, run: ./update.sh (Linux/macOS) or update.bat (Windows)")
        sys.exit(0)
    
    # Handle link management and rewind commands
    if any([args.stats, args.blacklist, args.unblacklist, args.list_blacklisted, args.export_links,
            args.rewind_preview, args.rewind, args.backup_blacklist, args.recent_blacklisted != 7]):
        if not LINK_MANAGER_AVAILABLE:
            print("❌ Link Management System not available.")
            print("   Please ensure link_manager.py is installed in the same directory.")
            sys.exit(1)
            
        automation = NeuronNewsletterAutomation()
        
        if not automation.link_manager:
            print("❌ Link Management System not initialized.")
            print("   Check configuration or installation.")
            sys.exit(1)
        
        if args.stats:
            stats = automation.link_manager.get_reading_statistics()
            print("\n📊 Reading Statistics")
            print("=" * 50)
            print(f"Total links encountered: {stats['total_links_encountered']}")
            print(f"Blacklisted links: {stats['blacklisted_links']}")
            print(f"Active links: {stats['active_links']}")
            print(f"Automation runs: {stats['total_automation_runs']}")
            print(f"Reading efficiency: {stats['reading_efficiency_percent']}%")
            
            print(f"\n🌐 Top Domains:")
            for domain, count in list(stats['top_domains'].items())[:5]:
                print(f"  {domain}: {count} links")
            
            print(f"\n📈 Recent Activity (last 7 days):")
            for activity in stats['recent_activity'][:7]:
                print(f"  {activity['date']}: {activity['new_links']} new, {activity['opened_links']} opened")
        
        if args.blacklist:
            if automation.link_manager.blacklist_url(args.blacklist, "manual"):
                print(f"✅ Blacklisted: {args.blacklist}")
            else:
                print(f"❌ URL not found in database: {args.blacklist}")
        
        if args.unblacklist:
            if automation.link_manager.unblacklist_url(args.unblacklist):
                print(f"✅ Removed from blacklist: {args.unblacklist}")
            else:
                print(f"❌ URL not found in database: {args.unblacklist}")
        
        if args.list_blacklisted:
            # Get blacklisted URLs
            with sqlite3.connect(automation.link_manager.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT url, blacklisted_date, blacklist_reason
                    FROM links 
                    WHERE is_blacklisted = TRUE
                    ORDER BY blacklisted_date DESC
                """)
                blacklisted = cursor.fetchall()
            
            if blacklisted:
                print(f"\n🚫 Blacklisted URLs ({len(blacklisted)} total)")
                print("=" * 60)
                for url, date, reason in blacklisted:
                    print(f"  {url}")
                    print(f"    Date: {date}, Reason: {reason or 'not specified'}\n")
            else:
                print("No blacklisted URLs found.")
        
        if args.export_links:
            export_path = Path(args.export_links)
            if automation.link_manager.export_data(export_path):
                print(f"✅ Links exported to: {export_path}")
            else:
                print(f"❌ Failed to export links")
        
        # Blacklist rewind commands
        if args.rewind_preview or args.rewind or args.backup_blacklist or args.recent_blacklisted != 7:
            # Import BlacklistRewind
            try:
                from blacklist_rewind import BlacklistRewind
                rewind_tool = BlacklistRewind(
                    automation.link_manager.db_path, 
                    config=ACTIVE_CONFIG,
                    logger=automation.logger
                )
            except ImportError:
                print("❌ Blacklist rewind functionality not available.")
                print("   Please ensure blacklist_rewind.py is installed in the same directory.")
                sys.exit(1)
            
            if args.rewind_preview:
                print(f"🔍 Preview: Rewind {args.rewind_preview} days")
                print("=" * 50)
                
                preview = rewind_tool.preview_rewind(args.rewind_preview)
                print(f"Cutoff date: {preview['cutoff_date']}")
                print(f"Links to restore: {preview['restore_count']}")
                
                if preview['restore_count'] > 0:
                    print(f"\n📊 Restoration breakdown:")
                    for reason, count in preview['reason_breakdown'].items():
                        print(f"  • {reason}: {count} links")
                    
                    print(f"\n📋 Links to restore (first 10):")
                    for link in preview['links_to_restore'][:10]:
                        print(f"  📅 {link['blacklisted_date']} - {link['url'][:60]}...")
                    
                    if len(preview['links_to_restore']) > 10:
                        print(f"  ... and {len(preview['links_to_restore']) - 10} more")
                else:
                    print("✅ No links would be restored")
            
            if args.rewind:
                print(f"⏪ Performing Rewind: {args.rewind} days")
                print("=" * 50)
                
                # Show preview first
                preview = rewind_tool.preview_rewind(args.rewind)
                print(f"This will restore {preview['restore_count']} links to available status")
                
                if preview['restore_count'] == 0:
                    print("✅ No links to restore - operation not needed")
                else:
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
                        print(f"\n🎯 These links are now available for opening again.")
                    else:
                        print("❌ Rewind operation failed")
            
            if args.backup_blacklist:
                print("💾 Creating Blacklist Backup")
                print("=" * 50)
                backup_file = rewind_tool.create_backup()
                print(f"✅ Backup created: {backup_file}")
            
            if args.recent_blacklisted != 7:
                print(f"🕒 Recently Blacklisted Links (last {args.recent_blacklisted} days)")
                print("=" * 60)
                
                recent_links = rewind_tool.list_recent_blacklists(args.recent_blacklisted)
                
                if not recent_links:
                    print("No links blacklisted in the specified period.")
                else:
                    for link in recent_links[:15]:  # Show top 15
                        print(f"📅 {link['days_ago']} days ago ({link['blacklisted_date']})")
                        print(f"   🔗 {link['url']}")
                        print(f"   📂 Domain: {link['domain']}")
                        print(f"   💭 Reason: {link['reason']}")
                        print()
                    
                    if len(recent_links) > 15:
                        print(f"... and {len(recent_links) - 15} more")
        
        sys.exit(0)
    
    try:
        automation = NeuronNewsletterAutomation()
        success = automation.run_automation()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()