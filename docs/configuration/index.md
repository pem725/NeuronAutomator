# Configuration

Customize Neuron Daily Newsletter Automation to match your preferences and schedule. The system is designed to work perfectly out-of-the-box, but offers extensive customization options.

## Quick Configuration

Most users only need to adjust these basic settings:

=== "Schedule Times"

    **Change when automation runs:**
    ```python
    # Edit ~/.config/neuron-automation/config.py
    AUTOMATION_TIMES = [
        "05:30",  # Early morning
        "06:00",  # Primary time  
        "06:30",  # Late catch
        "07:00"   # Final safety net
    ]
    ```

=== "Days to Run"

    **Customize which days:**
    ```python
    # 0=Monday, 6=Sunday
    ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only
    # ENABLED_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Every day
    ```

=== "Link Management"

    **Blacklist behavior:**
    ```python
    # How long to wait before showing links again
    RECENT_LINK_DAYS = 1  # Skip links opened yesterday
    
    # Auto-blacklist after opening
    AUTO_BLACKLIST_AFTER_OPENING = True
    ```

## Configuration File Location

Find your config file at:

| Platform | Location |
|----------|----------|
| **Linux** | `~/.config/neuron-automation/config.py` |
| **macOS** | `~/.config/neuron-automation/config.py` |  
| **Windows** | `%USERPROFILE%\.config\neuron-automation\config.py` |

## Essential Settings

### 🕐 Scheduling Configuration

```python
# When to run automation (24-hour format)
AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00"]

# Which days (0=Monday, 6=Sunday)
ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only

# Timezone (auto-detected by default)
TIMEZONE = "auto"  # or "America/New_York", "Europe/London", etc.
```

### 🌐 Browser Configuration

```python
# Chrome browser options
CHROME_OPTIONS = [
    "--no-sandbox",           # Required for some systems
    "--disable-dev-shm-usage" # Prevents memory issues
]

# Keep browser open after automation
BROWSER_PERSISTENCE = True

# Headless mode (no GUI)
HEADLESS_MODE = False  # Set True for server environments
```

### 🔗 Link Management

```python
# Days to wait before reshowing links
RECENT_LINK_DAYS = 1

# Auto-blacklist opened links
AUTO_BLACKLIST_AFTER_OPENING = True

# Maximum links to open per run
MAX_LINKS_PER_RUN = 50

# Skip patterns (URLs containing these)
SKIP_LINK_PATTERNS = [
    "advertisement",
    "promo", 
    "sponsor"
]
```

### 📝 Logging Configuration

```python
# Logging level
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR

# Log file retention (days)
LOG_RETENTION_DAYS = 30

# Max log file size (MB)
MAX_LOG_SIZE_MB = 10
```

## Advanced Configuration

### Custom URL Filtering

```python
# Advanced link filtering
LINK_FILTER_CONFIG = {
    'min_url_length': 10,
    'max_url_length': 500,
    'allowed_domains': [],     # Empty = allow all
    'blocked_domains': [       # Block these domains
        'ads.example.com',
        'tracking.example.com'
    ],
    'require_https': False     # Only allow HTTPS URLs
}
```

### Performance Tuning

```python
# Performance settings
PERFORMANCE_CONFIG = {
    'page_load_timeout': 30,    # Seconds to wait for page load
    'max_retries': 3,          # Retry attempts on failure
    'retry_delay': 5,          # Seconds between retries
    'concurrent_tabs': False   # Open tabs simultaneously
}
```

### Database Configuration

```python
# SQLite database settings
DATABASE_CONFIG = {
    'db_path': '~/.config/neuron-automation/data/links.db',
    'backup_enabled': True,
    'backup_frequency': 7,     # Days between automatic backups
    'vacuum_frequency': 30     # Days between database optimization
}
```

## Configuration Profiles

Switch between different configurations easily:

### Development Profile
```python
class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"
    ENABLED_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Every day
    AUTOMATION_TIMES = ["09:00"]  # Single test time
    HEADLESS_MODE = False
```

### Production Profile  
```python
class ProductionConfig(Config):
    LOG_LEVEL = "INFO" 
    ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only
    AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00"]
    BROWSER_PERSISTENCE = True
```

### Server Profile
```python
class ServerConfig(Config):
    LOG_LEVEL = "WARNING"
    HEADLESS_MODE = True      # No GUI on servers
    BROWSER_PERSISTENCE = False
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage", 
        "--headless",
        "--disable-gpu"
    ]
```

**Switch profiles:**
```python
# At the end of config.py
ACTIVE_CONFIG = ProductionConfig  # Change this line
```

## Environment Variables

Override settings with environment variables:

```bash
# Set environment variables
export NEURON_LOG_LEVEL="DEBUG"
export NEURON_HEADLESS_MODE="true"
export NEURON_AUTOMATION_TIMES="06:00,07:00"

# Run with custom settings
neuron-automation
```

## Validation & Testing

### Validate Configuration
```bash
# Check configuration syntax
neuron-automation --check-config

# Test with current settings
neuron-automation --dry-run

# View effective configuration
neuron-automation --show-config
```

### Reset to Defaults
```bash
# Reset all settings to defaults
neuron-automation --reset-config

# Reset specific sections
neuron-automation --reset-config --section=scheduling
```

## Troubleshooting Configuration

### Common Issues

!!! warning "Configuration Syntax Error"
    If you see Python syntax errors:
    ```bash
    # Validate syntax
    python -m py_compile ~/.config/neuron-automation/config.py
    
    # Reset to working configuration
    neuron-automation --reset-config
    ```

!!! warning "Times Not Working"
    If automation doesn't run at scheduled times:
    ```bash
    # Check system service status
    systemctl --user status neuron-automation.timer
    
    # View service logs  
    journalctl --user -u neuron-automation.service
    ```

!!! warning "Browser Issues"
    If Chrome doesn't open or behaves strangely:
    ```bash
    # Test browser configuration
    neuron-automation --test-browser
    
    # Reset browser settings
    neuron-automation --reset-config --section=browser
    ```

---

## Next Steps

<div class="grid cards" markdown>

-   **Advanced Settings**
    
    Explore platform-specific configurations and power-user features.
    
    [:octicons-arrow-right-24: Advanced Configuration](advanced-settings.md)

-   **Basic Usage**
    
    Learn how to use the configured automation system.
    
    [:octicons-arrow-right-24: Usage Guide](../usage/index.md)

-   **Platform Setup**
    
    Platform-specific configuration details and optimization.
    
    [:octicons-arrow-right-24: Platform Configuration](platform-setup.md)

-   **Troubleshooting**
    
    Solve common configuration issues and get help.
    
    [:octicons-arrow-right-24: Installation Troubleshooting](../installation/troubleshooting.md)

</div>