#!/usr/bin/env python3
"""
Configuration file for Neuron Newsletter Automation
==================================================

This file contains all configurable settings for the automation script.
Modify these values to customize the behavior according to your needs.
"""

import os
import platform
from pathlib import Path

class PlatformConfig:
    """Platform-specific configuration detection."""
    
    @staticmethod
    def get_platform_settings():
        """Return platform-specific configuration class."""
        system = platform.system().lower()
        if system == "darwin":
            return MacOSConfig
        elif system == "windows":
            return WindowsConfig
        else:
            return LinuxConfig
    
    @staticmethod
    def get_config_dir():
        """Return platform-appropriate configuration directory."""
        system = platform.system().lower()
        if system == "darwin":
            return Path.home() / "Library" / "Application Support" / "neuron-automation"
        elif system == "windows":
            return Path.home() / "AppData" / "Local" / "neuron-automation"
        else:
            return Path.home() / ".config" / "neuron-automation"
    
    @staticmethod
    def get_install_dir():
        """Return platform-appropriate installation directory."""
        system = platform.system().lower()
        if system == "windows":
            return Path("C:") / "Program Files" / "neuron-automation"
        else:
            return Path("/usr/local/bin")

class Config:
    """Base configuration class containing all settings."""
    
    # Base URL for the Neuron Daily newsletter
    BASE_URL = "https://www.theneurondaily.com/"
    
    # Timing settings
    MAX_RETRIES = 3                 # Maximum number of retry attempts
    RETRY_DELAY = 5                 # Delay between retries (seconds)
    PAGE_LOAD_TIMEOUT = 30          # Maximum time to wait for page load (seconds)
    ELEMENT_WAIT_TIMEOUT = 15       # Maximum time to wait for elements (seconds)
    TAB_OPEN_DELAY = 1              # Delay between opening tabs (seconds)
    
    # Directory settings (platform-aware)
    CONFIG_DIR = PlatformConfig.get_config_dir()
    LOG_FILE = CONFIG_DIR / 'neuron_automation.log'
    CHROME_PROFILE_DIR = CONFIG_DIR / 'chrome_profile'
    INSTALL_DIR = PlatformConfig.get_install_dir()
    
    # Platform identification
    PLATFORM = platform.system().lower()
    SCHEDULER = "unknown"  # Override in platform-specific classes
    
    # Chrome browser settings
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage", 
        "--disable-gpu",
        "--window-size=1920,1080",
        "--start-maximized",
        "--headless",  # Headless mode enabled by default
        "--autoplay-policy=document-user-activation-required",  # Disable video autoplay
        "--disable-features=VizDisplayCompositor",  # Additional autoplay prevention
    ]
    
    # Weekday settings (0=Monday, 6=Sunday)
    ENABLED_DAYS = [0, 1, 2, 3, 4]  # Monday through Friday
    
    # Link filtering settings
    SKIP_LINK_PATTERNS = [
        '#', 'javascript:', 'mailto:', 'tel:',
        'facebook.com', 'twitter.com', 'linkedin.com', 'instagram.com',
        'youtube.com', 'tiktok.com', 'discord.com', 'reddit.com',
        'subscribe', 'unsubscribe', 'privacy', 'terms', 'cookie',
        'contact', 'about', 'home', 'archive', 'search',
        'login', 'signup', 'register', 'account'
    ]
    
    SKIP_TEXT_PATTERNS = [
        'read more', 'click here', 'learn more', 'view all', 
        'see more', 'continue reading', 'full article',
        'subscribe', 'unsubscribe', 'share', 'tweet',
        'like', 'follow', 'join', 'sign up'
    ]
    
    # Article link requirements
    MIN_LINK_TEXT_LENGTH = 5        # Minimum character length for link text
    MAX_LINK_TEXT_LENGTH = 200      # Maximum character length for link text
    MIN_TITLE_WORDS = 3             # Minimum words in article title
    MAX_TITLE_WORDS = 20            # Maximum words in article title
    
    # Link Management Settings
    LINK_MANAGEMENT_ENABLED = True         # Enable link storage and blacklisting
    LINK_DATABASE_NAME = 'newsletter_links.db'  # Database filename
    AUTO_BLACKLIST_ENABLED = False         # Enable automatic blacklisting
    AUTO_BLACKLIST_DAYS = 30               # Days after which to auto-blacklist old links
    READING_STATS_ENABLED = True           # Track and show reading statistics
    DUPLICATE_DETECTION_ENABLED = True     # Prevent duplicate link opening
    BLACKLIST_CLEANUP_DAYS = 90            # Days to keep blacklisted link history
    RECENT_LINK_DAYS = 1                   # Don't re-open links opened within this many days
    
    # Link Management Behavior
    BLACKLIST_ON_ERROR = False             # Auto-blacklist links that fail to load
    DOMAIN_BLACKLIST = []                  # List of domains to always blacklist
    URL_PATTERN_BLACKLIST = [              # URL patterns to blacklist
        '*/advertisement/*',
        '*/ads/*', 
        '*/sponsor/*',
        '*/promoted/*'
    ]
    
    # Logging settings
    LOG_LEVEL = "INFO"              # DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    MAX_LOG_SIZE = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Network settings  
    CONNECTIVITY_CHECK_URL = "https://www.google.com"
    CONNECTIVITY_TIMEOUT = 10       # Timeout for connectivity check (seconds)
    
    # Change detection settings
    ENABLE_CHANGE_DETECTION = True  # Enable smart content change detection
    CONTENT_CHECK_TIMEOUT = 10      # Timeout for content hash requests (seconds)
    CACHE_CLEANUP_DAYS = 7          # Days to keep old cache files
    
    # Advanced settings
    ENABLE_JAVASCRIPT_WAIT = True   # Wait for JavaScript to finish loading
    JAVASCRIPT_WAIT_TIME = 2        # Additional wait time for JS (seconds)
    
    # Custom selectors (if the website structure changes)
    LINK_SELECTORS = [
        "a[href]",                  # All links
        # Add more specific selectors if needed
    ]
    
    # Content area selectors (to focus link extraction)
    CONTENT_SELECTORS = [
        "main",
        "[role='main']", 
        ".content",
        ".newsletter",
        ".articles",
        "article"
    ]
    
    # User preferences
    CLOSE_BROWSER_ON_ERROR = True   # Close browser if automation fails
    OPEN_IN_INCOGNITO = False       # Use incognito mode
    RESTORE_SESSION = True          # Restore previous Chrome session
    
    @classmethod
    def get_chrome_options_list(cls):
        """Get Chrome options as a list, including dynamic options."""
        options = cls.CHROME_OPTIONS.copy()
        
        if cls.OPEN_IN_INCOGNITO:
            options.append("--incognito")
        
        if cls.RESTORE_SESSION:
            options.append(f"--user-data-dir={cls.CHROME_PROFILE_DIR}")
        
        return options
    
    @classmethod
    def validate_config(cls):
        """Validate configuration settings."""
        errors = []
        
        if cls.MAX_RETRIES < 1:
            errors.append("MAX_RETRIES must be at least 1")
        
        if cls.RETRY_DELAY < 0:
            errors.append("RETRY_DELAY cannot be negative")
            
        if cls.PAGE_LOAD_TIMEOUT < 5:
            errors.append("PAGE_LOAD_TIMEOUT should be at least 5 seconds")
            
        if not cls.BASE_URL.startswith(('http://', 'https://')):
            errors.append("BASE_URL must start with http:// or https://")
        
        if not 0 <= min(cls.ENABLED_DAYS) <= 6 or not 0 <= max(cls.ENABLED_DAYS) <= 6:
            errors.append("ENABLED_DAYS must contain values between 0-6")
            
        if cls.MIN_LINK_TEXT_LENGTH >= cls.MAX_LINK_TEXT_LENGTH:
            errors.append("MIN_LINK_TEXT_LENGTH must be less than MAX_LINK_TEXT_LENGTH")
        
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(f"- {error}" for error in errors))
        
        return True

# Example of how to override settings for development/testing
class DevelopmentConfig(Config):
    """Development configuration with more verbose logging and shorter timeouts."""
    LOG_LEVEL = "DEBUG"
    PAGE_LOAD_TIMEOUT = 15
    MAX_RETRIES = 1
    ENABLED_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Every day for testing

class TestConfig(Config):
    """Test configuration for automated testing."""
    LOG_LEVEL = "DEBUG"
    MAX_RETRIES = 1
    RETRY_DELAY = 1
    PAGE_LOAD_TIMEOUT = 10
    ELEMENT_WAIT_TIMEOUT = 5
    CHROME_OPTIONS = Config.CHROME_OPTIONS + ["--headless"]
    CLOSE_BROWSER_ON_ERROR = True

# Platform-specific configurations
class LinuxConfig(Config):
    """Linux-specific configuration."""
    SCHEDULER = "systemd"
    SERVICE_DIR = Path("/etc/systemd/system")
    
class MacOSConfig(Config):
    """macOS-specific configuration."""
    SCHEDULER = "launchd"
    LAUNCHD_DIR = Path.home() / "Library" / "LaunchAgents"
    
class WindowsConfig(Config):
    """Windows-specific configuration."""
    SCHEDULER = "taskscheduler"
    # Windows Task Scheduler doesn't use file paths like Unix systems
    TASK_NAME = "NeuronAutomation"

# Auto-select platform configuration
# Change this to DevelopmentConfig or TestConfig as needed
ACTIVE_CONFIG = PlatformConfig.get_platform_settings()

# Validate the active configuration
ACTIVE_CONFIG.validate_config()