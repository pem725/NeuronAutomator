#!/usr/bin/env python3
"""
Neuron Daily Newsletter Automation Script
=========================================

Automatically opens the latest Neuron Daily newsletter with all article links
in separate tabs every weekday morning.

Author: AI Assistant  
Created: 2025
License: MIT
Version: 1.3.0
"""

__version__ = "1.3.0"
__author__ = "AI Assistant"
__license__ = "MIT"

import os
import sys
import time
import hashlib
import logging
import requests
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
    # Fallback if config not found
    class DefaultConfig:
        ENABLE_CHANGE_DETECTION = True
        CONTENT_CHECK_TIMEOUT = 10
        CACHE_CLEANUP_DAYS = 7
    ACTIVE_CONFIG = DefaultConfig()


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
        
        # Enable remote debugging to connect to existing Chrome instances
        chrome_options.add_argument("--remote-debugging-port=9222")
        
        # Use regular Chrome profile instead of isolated one
        # This allows tabs to open in your existing Chrome browser
        chrome_options.add_experimental_option("useAutomationExtension", False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        
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
                
                # Don't specify user-data-dir to use default Chrome profile
                chrome_options.add_experimental_option("useAutomationExtension", False)
                chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
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
    
    def extract_newsletter_links(self, driver: webdriver.Chrome) -> List[str]:
        """Extract all relevant links from the newsletter page."""
        self.logger.info("Extracting newsletter links")
        links = []
        
        try:
            # Wait for the page content to load
            WebDriverWait(driver, self.element_wait_timeout).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Find all links on the page
            link_elements = driver.find_elements(By.TAG_NAME, "a")
            self.logger.info(f"Found {len(link_elements)} total links on page")
            
            # Filter for relevant article links
            for link_elem in link_elements:
                try:
                    href = link_elem.get_attribute("href")
                    text = link_elem.text.strip()
                    
                    if not href or not text:
                        continue
                    
                    # Skip internal navigation and non-article links
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
    
    
    def get_content_hash(self) -> Optional[str]:
        """Get hash of key newsletter content areas for change detection."""
        try:
            timeout = getattr(ACTIVE_CONFIG, 'CONTENT_CHECK_TIMEOUT', 10)
            response = requests.get(self.base_url, timeout=timeout, headers={
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
                self.logger.info(f"Loading newsletter page: {self.base_url}")
                driver.get(self.base_url)
                
                if not self.wait_for_page_load(driver):
                    raise TimeoutException("Page failed to load completely")
                
                # Extract links from the newsletter
                links = self.extract_newsletter_links(driver)
                
                if not links:
                    self.logger.warning("No newsletter links found")
                    self.logger.info("Keeping main newsletter page open")
                    # Keep driver open with just the main page
                    return True
                
                # Open article tabs in the same browser instance
                self.logger.info(f"Opening {len(links)} article tabs in current browser")
                for i, link in enumerate(links, 1):
                    try:
                        self.logger.info(f"Opening tab {i}/{len(links)}: {link}")
                        driver.execute_script(f"window.open('{link}', '_blank');")
                        time.sleep(1)  # Small delay between tab openings
                    except Exception as e:
                        self.logger.error(f"Failed to open tab for {link}: {e}")
                        continue
                
                # Switch back to the main newsletter tab
                driver.switch_to.window(driver.window_handles[0])
                
                # Don't close the driver - let user interact with tabs
                self.logger.info(f"Successfully opened {len(links)} tabs - browser will remain open")
                self.logger.info("Automation completed successfully")
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
    
    args = parser.parse_args()
    
    if args.check_updates:
        print(f"Current version: {__version__}")
        print("To update, run: ./update.sh (Linux/macOS) or update.bat (Windows)")
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