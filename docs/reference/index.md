# Reference

Complete technical reference for Neuron Daily Newsletter Automation. Find commands, configuration options, and system information.

## 🚀 Quick Reference

### Essential Commands

| Command | Purpose | Example |
|---------|---------|---------|
| `neuron-automation` | Run automation | `neuron-automation` |
| `--stats` | View statistics | `neuron-automation --stats` |
| `--rewind N` | Restore N days of links | `neuron-automation --rewind 7` |
| `--recent-blacklisted N` | Show recent blacklisted | `neuron-automation --recent-blacklisted 10` |
| `--test` | Test system health | `neuron-automation --test` |
| `--version` | Show version info | `neuron-automation --version` |

### File Locations

| Platform | Configuration | Data | Logs |
|----------|---------------|------|------|
| **Linux** | `~/.config/neuron-automation/config.py` | `~/.config/neuron-automation/data/` | `~/.config/neuron-automation/logs/` |
| **macOS** | `~/.config/neuron-automation/config.py` | `~/.config/neuron-automation/data/` | `~/.config/neuron-automation/logs/` |
| **Windows** | `%USERPROFILE%\.config\neuron-automation\config.py` | `%USERPROFILE%\.config\neuron-automation\data\` | `%USERPROFILE%\.config\neuron-automation\logs\` |

## 📋 Command Line Interface

### Main Commands

```bash
# Basic operations
neuron-automation                    # Run automation
neuron-automation --help            # Show all options
neuron-automation --version         # Show version
neuron-automation --status          # System status

# Testing and diagnostics
neuron-automation --test            # Full system test
neuron-automation --dry-run         # Preview without action
neuron-automation --check-config    # Validate configuration
neuron-automation --health-check    # System health

# Statistics and monitoring
neuron-automation --stats           # Full statistics
neuron-automation --db-stats        # Database statistics
neuron-automation --show-config     # Current configuration
```

### Link Management

```bash
# Time rewind operations
neuron-automation --rewind N              # Restore N days
neuron-automation --rewind-preview N      # Preview restore
neuron-automation --recent-blacklisted N  # Show recent items

# Blacklist management
neuron-automation --show-blacklisted      # All blacklisted links
neuron-automation --clear-blacklist       # Clear all blacklisted
neuron-automation --export-blacklist      # Export to file

# Advanced filtering
neuron-automation --max-links N           # Limit links opened
neuron-automation --force                 # Ignore change detection
```

### System Management

```bash
# Configuration
neuron-automation --reset-config          # Reset to defaults
neuron-automation --backup-config         # Backup configuration
neuron-automation --setup                 # Initial system setup

# Database operations  
neuron-automation --backup-db             # Backup database
neuron-automation --vacuum-db             # Optimize database
neuron-automation --cleanup --days N      # Clean old entries

# Service control (Linux/macOS)
neuron-automation --start-service         # Start scheduled automation
neuron-automation --stop-service          # Stop scheduled automation
neuron-automation --restart-service       # Restart automation
```

### Standalone Tools

```bash
# Time rewind tool (advanced)
blacklist-rewind --help                   # Show options
blacklist-rewind --stats                  # Rewind statistics
blacklist-rewind --backup                 # Create backup
blacklist-rewind --rewind N               # Restore N days
```

## ⚙️ Configuration Reference

### Core Settings

```python
# Scheduling
AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00"]  # When to run
ENABLED_DAYS = [0, 1, 2, 3, 4]                          # Days (0=Mon)
TIMEZONE = "auto"                                        # Timezone

# Browser
CHROME_OPTIONS = ["--no-sandbox", "--disable-dev-shm-usage"]
BROWSER_PERSISTENCE = True                               # Keep tabs open
HEADLESS_MODE = False                                   # Show browser

# Link Management
RECENT_LINK_DAYS = 1                                    # Filter recent links
AUTO_BLACKLIST_AFTER_OPENING = True                     # Auto-blacklist
MAX_LINKS_PER_RUN = 50                                  # Link limit

# Logging
LOG_LEVEL = "INFO"                                      # DEBUG/INFO/WARNING/ERROR
LOG_RETENTION_DAYS = 30                                 # Keep logs N days
```

### Advanced Configuration

```python
# Performance
PAGE_LOAD_TIMEOUT = 30        # Page load timeout (seconds)  
MAX_RETRIES = 3              # Retry attempts
RETRY_DELAY = 5              # Delay between retries (seconds)

# Network
USER_AGENT = "auto"          # Browser user agent
REQUEST_TIMEOUT = 30         # HTTP timeout (seconds)
CONNECTION_POOL_SIZE = 10    # HTTP connection pool

# Database
DATABASE_PATH = "~/.config/neuron-automation/data/links.db"
BACKUP_RETENTION = 10        # Keep N backups
VACUUM_FREQUENCY = 30        # Optimize every N days
```

## 🗂️ File Structure

### Installation Directory

```
~/.config/neuron-automation/
├── config.py                    # Main configuration
├── neuron_automation.py         # Main automation script
├── link_manager.py              # Link management system
├── blacklist_rewind.py          # Time rewind tool
├── data/
│   ├── links.db                 # SQLite database
│   └── backups/                 # Database backups
├── logs/
│   ├── neuron_automation.log    # Application logs
│   └── debug.log               # Debug logs (if enabled)
└── venv/                       # Python virtual environment
    └── ...                     # Python packages
```

### System Integration Files

=== "Linux"

    ```
    /etc/systemd/system/
    ├── neuron-automation.service    # Systemd service
    └── neuron-automation.timer      # Scheduling timer
    
    /usr/local/bin/
    ├── neuron-automation           # Command wrapper
    └── blacklist-rewind            # Rewind tool wrapper
    ```

=== "macOS"

    ```
    ~/Library/LaunchAgents/
    └── com.neuron-automation.plist  # Launch agent
    
    /usr/local/bin/
    ├── neuron-automation           # Command wrapper  
    └── blacklist-rewind            # Rewind tool wrapper
    ```

=== "Windows"

    ```
    # Task Scheduler entries (no files)
    C:\Windows\System32\
    ├── neuron-automation.bat       # Command wrapper
    └── blacklist-rewind.bat        # Rewind tool wrapper
    ```

## 📊 Database Schema

### Links Table
```sql
CREATE TABLE links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE NOT NULL,
    url_hash TEXT UNIQUE NOT NULL,
    title TEXT,
    first_seen DATE NOT NULL,
    last_seen DATE NOT NULL,
    is_blacklisted BOOLEAN DEFAULT FALSE,
    blacklisted_date DATE,
    blacklist_reason TEXT,
    times_opened INTEGER DEFAULT 0,
    newsletter_hash TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Operations Log Table
```sql
CREATE TABLE operations_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    operation_type TEXT NOT NULL,
    operation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    links_affected INTEGER DEFAULT 0,
    success BOOLEAN DEFAULT TRUE
);
```

### Rewind History Table  
```sql
CREATE TABLE rewind_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    rewind_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    days_rewound INTEGER NOT NULL,
    links_affected INTEGER NOT NULL,
    backup_created TEXT,
    operation_type TEXT DEFAULT 'rewind'
);
```

## 🌐 Environment Variables

Override configuration with environment variables:

```bash
# Scheduling
export NEURON_AUTOMATION_TIMES="06:00,07:00"
export NEURON_ENABLED_DAYS="1,2,3,4,5"

# Behavior  
export NEURON_HEADLESS_MODE="true"
export NEURON_BROWSER_PERSISTENCE="false"
export NEURON_MAX_LINKS="25"

# Paths
export NEURON_CONFIG_DIR="/custom/path"
export NEURON_DATA_DIR="/custom/data"
export NEURON_LOG_DIR="/custom/logs"

# Logging
export NEURON_LOG_LEVEL="DEBUG"
export NEURON_LOG_RETENTION="7"
```

## 🔧 API Reference (Python Module)

### Import and Basic Usage
```python
from neuron_automation import NeuronNewsletterAutomation
from link_manager import LinkManager
from blacklist_rewind import BlacklistRewind

# Initialize automation
automation = NeuronNewsletterAutomation()

# Run automation
result = automation.run_automation()

# Link management
link_mgr = LinkManager()
stats = link_mgr.get_statistics()

# Time rewind  
rewind_tool = BlacklistRewind()
preview = rewind_tool.preview_rewind(days=7)
```

### Key Classes and Methods

#### NeuronNewsletterAutomation
```python
class NeuronNewsletterAutomation:
    def run_automation(self) -> dict           # Main automation
    def test_browser_config(self) -> bool      # Test browser
    def check_internet_connectivity(self) -> bool  # Test connection
    def get_system_info(self) -> dict          # System information
```

#### LinkManager  
```python
class LinkManager:
    def analyze_newsletter_links(self, links: List[str]) -> dict
    def record_opened_links(self, links: List[str]) -> dict
    def get_statistics(self) -> dict
    def get_recent_blacklisted(self, limit: int) -> List[dict]
```

#### BlacklistRewind
```python
class BlacklistRewind:
    def preview_rewind(self, days: int) -> dict
    def perform_rewind(self, days: int, backup: bool = True) -> dict
    def get_rewind_statistics(self) -> dict
    def create_backup(self) -> str
```

---

## Next Steps

<div class="grid cards" markdown>

-   **CLI Reference**
    
    Complete command-line interface documentation with examples.
    
    [:octicons-arrow-right-24: CLI Reference](cli-reference.md)

-   **Configuration Reference**  
    
    Detailed configuration options and advanced settings.
    
    [:octicons-arrow-right-24: Config Reference](config-reference.md)

-   **Usage Guide**
    
    Learn how to use all these commands effectively.
    
    [:octicons-arrow-right-24: Usage Guide](../usage/index.md)

-   **Troubleshooting**
    
    Solve common issues and get help with problems.
    
    [:octicons-arrow-right-24: Troubleshooting](../installation/troubleshooting.md)

</div>