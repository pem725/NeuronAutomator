# Configuration Reference

Complete configuration reference for Neuron Daily Newsletter Automation. Customize behavior, scheduling, and system settings.

## 📋 Configuration Overview

The system uses a hierarchical configuration approach with multiple sources:

1. **Default Configuration** (built-in defaults)
2. **User Configuration** (`config.py` file)
3. **Environment Variables** (runtime overrides)
4. **Command Line Arguments** (immediate overrides)

## 🔧 Core Configuration Settings

### Scheduling Configuration

```python
# config.py

class UserConfig:
    """User configuration overrides"""
    
    # Automation Schedule
    AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00"]  # Daily run times
    ENABLED_DAYS = [0, 1, 2, 3, 4]                          # Weekdays (0=Monday)
    TIMEZONE = "auto"                                        # System timezone
    
    # Weekend Behavior  
    WEEKEND_MODE = False                                     # Run on weekends
    HOLIDAY_SKIP = True                                      # Skip holidays
```

**Scheduling Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `AUTOMATION_TIMES` | List[str] | `["05:30", "06:00", "06:30", "07:00"]` | Daily execution times (24-hour format) |
| `ENABLED_DAYS` | List[int] | `[0,1,2,3,4]` | Days of week (0=Monday, 6=Sunday) |
| `TIMEZONE` | str | `"auto"` | Timezone (auto-detect or specific) |
| `WEEKEND_MODE` | bool | `False` | Enable weekend execution |
| `HOLIDAY_SKIP` | bool | `True` | Skip execution on holidays |

### Browser Configuration

```python
class UserConfig:
    # Browser Settings
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage", 
        "--disable-gpu"
    ]
    
    BROWSER_PERSISTENCE = True          # Keep browser open after automation
    HEADLESS_MODE = False              # Run browser in background
    WINDOW_SIZE = (1920, 1080)        # Browser window dimensions
    
    # Chrome Profile
    CHROME_PROFILE_PATH = "auto"       # Profile directory
    INCOGNITO_MODE = False            # Use private browsing
    
    # WebDriver Settings
    WEBDRIVER_TIMEOUT = 30            # Page load timeout (seconds)
    ELEMENT_WAIT_TIMEOUT = 15         # Element wait timeout (seconds)
    IMPLICIT_WAIT = 5                 # Implicit wait timeout (seconds)
```

**Browser Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `BROWSER_PERSISTENCE` | bool | `True` | Keep browser open after completion |
| `HEADLESS_MODE` | bool | `False` | Run without GUI (background mode) |
| `WINDOW_SIZE` | tuple | `(1920, 1080)` | Browser window dimensions |
| `WEBDRIVER_TIMEOUT` | int | `30` | Maximum page load time |
| `ELEMENT_WAIT_TIMEOUT` | int | `15` | Element location timeout |

### Link Management Configuration

```python
class UserConfig:
    # Link Processing  
    MAX_LINKS_PER_RUN = 50             # Maximum links to open per run
    RECENT_LINK_DAYS = 1               # Days to consider "recent"
    AUTO_BLACKLIST_AFTER_OPENING = True # Auto-blacklist opened links
    
    # Link Filtering
    MIN_LINK_TEXT_LENGTH = 5           # Minimum link text length
    EXCLUDED_DOMAINS = [               # Domains to skip
        "facebook.com",
        "twitter.com", 
        "instagram.com"
    ]
    
    # Content Detection
    ENABLE_CHANGE_DETECTION = True     # Check for content changes
    CONTENT_CHECK_TIMEOUT = 10         # Content check timeout (seconds)
    CACHE_CLEANUP_DAYS = 7            # Clean cache after N days
```

**Link Management Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `MAX_LINKS_PER_RUN` | int | `50` | Maximum links opened per execution |
| `AUTO_BLACKLIST_AFTER_OPENING` | bool | `True` | Automatically blacklist opened links |
| `EXCLUDED_DOMAINS` | List[str] | `[]` | Domains to never open |
| `MIN_LINK_TEXT_LENGTH` | int | `5` | Minimum characters in link text |
| `ENABLE_CHANGE_DETECTION` | bool | `True` | Only run when content changes |

### Database Configuration

```python
class UserConfig:
    # Database Settings
    DATABASE_PATH = "~/.config/neuron-automation/newsletter_links.db"
    DATABASE_TIMEOUT = 30              # SQLite timeout (seconds)
    
    # Performance
    VACUUM_FREQUENCY = 30              # Auto-optimize every N days
    BACKUP_RETENTION = 10              # Keep N database backups
    
    # Link Management Database
    LINK_MANAGEMENT_ENABLED = True     # Enable advanced link tracking
    LINK_DATABASE_NAME = "newsletter_links.db"
```

**Database Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `DATABASE_PATH` | str | `~/.config/neuron-automation/newsletter_links.db` | Database file location |
| `VACUUM_FREQUENCY` | int | `30` | Auto-optimization interval (days) |
| `BACKUP_RETENTION` | int | `10` | Number of backups to keep |
| `DATABASE_TIMEOUT` | int | `30` | SQLite operation timeout |

### Logging Configuration

```python
class UserConfig:
    # Logging Behavior
    LOG_LEVEL = "INFO"                 # DEBUG, INFO, WARNING, ERROR
    LOG_TO_FILE = True                 # Write logs to file
    LOG_TO_CONSOLE = True              # Display logs in terminal
    
    # Log Management
    LOG_RETENTION_DAYS = 30            # Keep logs for N days
    LOG_MAX_SIZE_MB = 10               # Max log file size
    LOG_BACKUP_COUNT = 5               # Number of log backups
    
    # Debug Settings
    DEBUG_BROWSER = False              # Extra browser debugging
    DEBUG_DATABASE = False             # Database operation logging
    DEBUG_NETWORK = False              # Network request logging
```

**Logging Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `LOG_LEVEL` | str | `"INFO"` | Minimum log level (DEBUG/INFO/WARNING/ERROR) |
| `LOG_RETENTION_DAYS` | int | `30` | Days to keep log files |
| `LOG_MAX_SIZE_MB` | int | `10` | Maximum individual log file size |
| `DEBUG_BROWSER` | bool | `False` | Enable detailed browser logging |

### Network Configuration

```python
class UserConfig:
    # HTTP Settings
    REQUEST_TIMEOUT = 30               # HTTP request timeout (seconds)
    MAX_RETRIES = 3                   # Network retry attempts
    RETRY_DELAY = 5                   # Delay between retries (seconds)
    
    # Connection Pool
    CONNECTION_POOL_SIZE = 10          # HTTP connection pool size
    CONNECTION_POOL_MAXSIZE = 10       # Max connections per host
    
    # User Agent
    USER_AGENT = "Mozilla/5.0 (compatible; NeuronAutomation/1.5.0)"
    
    # Proxy Settings (if needed)
    HTTP_PROXY = None                  # HTTP proxy URL
    HTTPS_PROXY = None                 # HTTPS proxy URL
```

**Network Options:**

| Setting | Type | Default | Description |
|---------|------|---------|-------------|
| `REQUEST_TIMEOUT` | int | `30` | HTTP request timeout |
| `MAX_RETRIES` | int | `3` | Network retry attempts |
| `CONNECTION_POOL_SIZE` | int | `10` | HTTP connection pool size |
| `USER_AGENT` | str | Auto-generated | Browser user agent string |

## 🌍 Environment Variables

Override any configuration setting using environment variables with the `NEURON_` prefix:

### Scheduling Variables

```bash
# Scheduling
export NEURON_AUTOMATION_TIMES="06:00,07:00,08:00"
export NEURON_ENABLED_DAYS="1,2,3,4,5"  # Monday-Friday
export NEURON_TIMEZONE="America/New_York"

# Weekend behavior
export NEURON_WEEKEND_MODE="true" 
export NEURON_HOLIDAY_SKIP="false"
```

### Browser Variables

```bash
# Browser behavior
export NEURON_BROWSER_PERSISTENCE="true"
export NEURON_HEADLESS_MODE="false"
export NEURON_WINDOW_SIZE="1920,1080"

# Timeouts
export NEURON_WEBDRIVER_TIMEOUT="45"
export NEURON_ELEMENT_WAIT_TIMEOUT="20"
```

### Link Management Variables

```bash
# Link processing
export NEURON_MAX_LINKS="25"
export NEURON_AUTO_BLACKLIST="true"
export NEURON_RECENT_LINK_DAYS="2"

# Content detection
export NEURON_ENABLE_CHANGE_DETECTION="true"
export NEURON_CONTENT_CHECK_TIMEOUT="15"
```

### System Variables

```bash
# Paths
export NEURON_CONFIG_DIR="/custom/config/path"
export NEURON_DATA_DIR="/custom/data/path"
export NEURON_LOG_DIR="/custom/log/path"

# Database
export NEURON_DATABASE_PATH="/custom/db/location.db"
export NEURON_BACKUP_RETENTION="15"

# Logging
export NEURON_LOG_LEVEL="DEBUG"
export NEURON_LOG_RETENTION_DAYS="14"
```

## 📁 Configuration File Locations

### Default Locations

| Platform | Configuration Directory |
|----------|------------------------|
| **Linux** | `~/.config/neuron-automation/` |
| **macOS** | `~/.config/neuron-automation/` |
| **Windows** | `%USERPROFILE%\.config\neuron-automation\` |

### Configuration Files

```
~/.config/neuron-automation/
├── config.py              # Main user configuration
├── local_config.py        # Machine-specific overrides
├── .env                   # Environment variables
└── backups/
    ├── config_backup.py   # Configuration backups
    └── ...
```

## 🎛️ Platform-Specific Configuration

### Linux Configuration

```python
class LinuxConfig:
    # Service Integration
    SYSTEMD_SERVICE = True             # Use systemd scheduling
    SERVICE_USER = "current"           # Run as current user
    
    # System Paths
    CHROME_EXECUTABLE = "/usr/bin/google-chrome"
    PYTHON_EXECUTABLE = "/usr/bin/python3"
    
    # Desktop Integration
    DESKTOP_NOTIFICATIONS = True       # Show desktop notifications
    TRAY_ICON = False                 # System tray integration
```

### macOS Configuration

```python
class MacOSConfig:
    # Service Integration  
    LAUNCHD_SERVICE = True             # Use launchd scheduling
    LAUNCH_AGENT_PATH = "~/Library/LaunchAgents/"
    
    # System Paths
    CHROME_EXECUTABLE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    PYTHON_EXECUTABLE = "/usr/local/bin/python3"
    
    # Integration
    NOTIFICATION_CENTER = True         # macOS notifications
    DOCK_INTEGRATION = False          # Dock badge/icon
```

### Windows Configuration

```python
class WindowsConfig:
    # Service Integration
    TASK_SCHEDULER = True              # Use Windows Task Scheduler
    RUN_AS_SERVICE = False            # Run as Windows service
    
    # System Paths  
    CHROME_EXECUTABLE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    PYTHON_EXECUTABLE = r"C:\Python\python.exe"
    
    # Integration
    WINDOWS_NOTIFICATIONS = True       # Windows 10/11 notifications
    STARTUP_SHORTCUT = False          # Add to startup folder
```

## 🔧 Advanced Configuration Examples

### High-Performance Configuration

```python
# config.py - High performance setup
class UserConfig:
    # Fast execution
    MAX_LINKS_PER_RUN = 30
    WEBDRIVER_TIMEOUT = 20
    ELEMENT_WAIT_TIMEOUT = 10
    
    # Minimal logging
    LOG_LEVEL = "WARNING"
    DEBUG_BROWSER = False
    
    # Aggressive caching
    ENABLE_CHANGE_DETECTION = True
    CACHE_CLEANUP_DAYS = 1
    
    # Optimized browser
    CHROME_OPTIONS = [
        "--no-sandbox",
        "--disable-dev-shm-usage",
        "--disable-gpu", 
        "--disable-extensions",
        "--disable-images"  # Skip image loading
    ]
```

### Privacy-Focused Configuration

```python
# config.py - Privacy-focused setup
class UserConfig:
    # Private browsing
    INCOGNITO_MODE = True
    CHROME_PROFILE_PATH = None  # No persistent profile
    
    # Minimal data collection
    USER_AGENT = "Mozilla/5.0 (compatible)"  # Generic UA
    
    # Limited logging
    LOG_LEVEL = "ERROR"
    LOG_RETENTION_DAYS = 1
    
    # No external connections for optimization
    VACUUM_FREQUENCY = 0  # Manual only
    BACKUP_RETENTION = 1
```

### Development Configuration

```python
# config.py - Development/testing setup
class UserConfig:
    # Testing behavior
    AUTOMATION_TIMES = ["09:00"]  # Single daily run
    MAX_LINKS_PER_RUN = 5        # Limited links
    
    # Verbose logging
    LOG_LEVEL = "DEBUG"
    DEBUG_BROWSER = True
    DEBUG_DATABASE = True
    DEBUG_NETWORK = True
    
    # Development features
    HEADLESS_MODE = False        # Always show browser
    BROWSER_PERSISTENCE = True   # Keep for debugging
    
    # Fast testing
    WEBDRIVER_TIMEOUT = 10
    CONTENT_CHECK_TIMEOUT = 5
```

## 🔍 Configuration Validation

### Validate Current Configuration

```bash
# Check configuration validity
neuron-automation --test-config

# Show effective configuration
neuron-automation --show-config

# Test specific components
neuron-automation --test-browser
neuron-automation --test-database
neuron-automation --test-scheduling
```

### Configuration Diagnostics

```bash
# Full system test with config validation
neuron-automation --system-test

# Check for config conflicts
neuron-automation --check-config-conflicts

# Validate environment variables
neuron-automation --validate-env
```

## 🔄 Configuration Migration

### Migrating Between Versions

```bash
# Backup current configuration
neuron-automation --backup-config

# Migrate to new version format
neuron-automation --migrate-config --from-version 1.4.0

# Verify migration
neuron-automation --test-config
```

### Configuration Reset

```bash
# Reset to defaults (with backup)
neuron-automation --reset-config

# Reset specific sections
neuron-automation --reset-config --section browser
neuron-automation --reset-config --section scheduling
```

---

## Next Steps

<div class="grid cards" markdown>

-   **Basic Configuration**
    
    Get started with essential configuration settings.
    
    [:octicons-arrow-right-24: Basic Config Guide](../configuration/basic-config.md)

-   **CLI Reference**
    
    Complete command-line interface documentation.
    
    [:octicons-arrow-right-24: CLI Reference](cli-reference.md)

-   **System Management**
    
    Monitor and maintain your configured system.
    
    [:octicons-arrow-right-24: System Management](../usage/system-management.md)

</div>