# Basic Configuration

Get your automation working exactly how you want with these simple configuration changes. Most users only need these essential settings.

## 🚀 Quick Setup

### 1. Find Your Configuration File

=== "Linux/macOS"

    ```bash
    # Open configuration file
    nano ~/.config/neuron-automation/config.py
    
    # Or use your preferred editor
    code ~/.config/neuron-automation/config.py
    ```

=== "Windows"

    ```powershell
    # Open configuration file
    notepad %USERPROFILE%\.config\neuron-automation\config.py
    
    # Or use your preferred editor
    code %USERPROFILE%\.config\neuron-automation\config.py
    ```

### 2. Essential Settings

Copy and paste these common configurations:

#### ⏰ **Morning Person Setup**
```python
# Runs early for early risers
AUTOMATION_TIMES = ["05:00", "05:30", "06:00"]
ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only
```

#### 🌅 **Standard Setup** (Default)
```python
# Balanced timing for most users
AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00"] 
ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only
```

#### 🌤️ **Late Riser Setup**
```python
# Later start times
AUTOMATION_TIMES = ["07:00", "07:30", "08:00"]
ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only
```

#### 📅 **Every Day Setup**
```python
# Runs 7 days a week
AUTOMATION_TIMES = ["06:00", "06:30", "07:00"]
ENABLED_DAYS = [0, 1, 2, 3, 4, 5, 6]  # Every day
```

#### 🎯 **Weekend Only Setup**
```python
# Only runs on weekends
AUTOMATION_TIMES = ["08:00", "08:30"]
ENABLED_DAYS = [5, 6]  # Saturday & Sunday
```

## 🔧 Common Customizations

### Link Management
```python
# How many days to wait before showing links again
RECENT_LINK_DAYS = 1  # 1 day (recommended)
# RECENT_LINK_DAYS = 3  # 3 days (less frequent)
# RECENT_LINK_DAYS = 0  # No filtering (see everything)

# Automatically blacklist opened links
AUTO_BLACKLIST_AFTER_OPENING = True  # Recommended
# AUTO_BLACKLIST_AFTER_OPENING = False  # Keep showing same links
```

### Browser Behavior
```python
# Keep browser tabs open after automation
BROWSER_PERSISTENCE = True  # Recommended for reading
# BROWSER_PERSISTENCE = False  # Close browser when done

# Run without showing browser window (background only)
HEADLESS_MODE = False  # Show browser (recommended)
# HEADLESS_MODE = True  # Run in background
```

### Content Filtering
```python
# Skip links containing these words
SKIP_LINK_PATTERNS = [
    "advertisement",
    "promo", 
    "sponsor",
    "affiliate"
]

# Maximum links to open per run (prevents overwhelming)
MAX_LINKS_PER_RUN = 50  # Reasonable limit
# MAX_LINKS_PER_RUN = 20  # Conservative limit
# MAX_LINKS_PER_RUN = 100  # High limit
```

## 🎛️ Settings Explained

### Days of Week
```python
# Day numbers:
# 0 = Monday, 1 = Tuesday, 2 = Wednesday, 3 = Thursday
# 4 = Friday, 5 = Saturday, 6 = Sunday

ENABLED_DAYS = [0, 1, 2, 3, 4]      # Weekdays
ENABLED_DAYS = [5, 6]               # Weekends  
ENABLED_DAYS = [0, 2, 4]            # Mon, Wed, Fri
ENABLED_DAYS = [0, 1, 2, 3, 4, 5, 6] # Every day
```

### Time Format
```python
# Use 24-hour format (HH:MM)
AUTOMATION_TIMES = [
    "05:30",  # 5:30 AM
    "06:00",  # 6:00 AM
    "18:30",  # 6:30 PM
    "23:00"   # 11:00 PM
]
```

### Logging Levels
```python
LOG_LEVEL = "DEBUG"    # Everything (for troubleshooting)
LOG_LEVEL = "INFO"     # Normal operations (recommended)
LOG_LEVEL = "WARNING"  # Only warnings and errors
LOG_LEVEL = "ERROR"    # Only errors
```

## 💡 Configuration Tips

### For New Users
```python
# Start with these safe settings
AUTOMATION_TIMES = ["06:30"]  # Single time to test
ENABLED_DAYS = [1]            # Tuesday only
RECENT_LINK_DAYS = 1          # Filter duplicates
AUTO_BLACKLIST_AFTER_OPENING = True
BROWSER_PERSISTENCE = True
HEADLESS_MODE = False         # See what's happening
LOG_LEVEL = "INFO"
```

### For Power Users  
```python
# Advanced setup
AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00", "08:00"]
ENABLED_DAYS = [0, 1, 2, 3, 4]
RECENT_LINK_DAYS = 0          # No filtering
MAX_LINKS_PER_RUN = 100       # High limit
LOG_LEVEL = "DEBUG"           # Detailed logging
```

### For Servers (Headless)
```python
# No GUI server setup
HEADLESS_MODE = True
BROWSER_PERSISTENCE = False   # Don't keep browser open
CHROME_OPTIONS = [
    "--no-sandbox",
    "--disable-dev-shm-usage",
    "--headless",
    "--disable-gpu"
]
LOG_LEVEL = "WARNING"         # Minimal logging
```

## ✅ Apply Configuration Changes

After making changes:

### 1. Save the File
- **Linux/macOS**: `Ctrl + X` (nano), `Ctrl + S` (most editors)
- **Windows**: `Ctrl + S`

### 2. Restart the Service  
=== "Linux"

    ```bash
    # Restart automation service
    systemctl --user restart neuron-automation.service
    
    # Check status
    systemctl --user status neuron-automation.timer
    ```

=== "macOS"

    ```bash
    # Restart launch agent
    launchctl unload ~/Library/LaunchAgents/com.neuron-automation.plist
    launchctl load ~/Library/LaunchAgents/com.neuron-automation.plist
    ```

=== "Windows"

    ```powershell
    # Restart scheduled task
    Unregister-ScheduledTask -TaskName "NeuronAutomation" -Confirm:$false
    Register-ScheduledTask -Xml (Get-Content "task-definition.xml" | Out-String) -TaskName "NeuronAutomation"
    ```

### 3. Test Your Changes
```bash
# Test with current configuration
neuron-automation --dry-run

# Run once to test
neuron-automation
```

## 🛠️ Troubleshooting

### Configuration Not Working?

```bash
# Check configuration syntax
python -c "import sys; sys.path.append('~/.config/neuron-automation'); import config"

# View current configuration
neuron-automation --show-config

# Reset to defaults
neuron-automation --reset-config
```

### Service Not Running?

```bash
# Check if timer is active (Linux)
systemctl --user is-active neuron-automation.timer

# View service logs
journalctl --user -u neuron-automation.service -f
```

### Browser Not Opening?

```bash
# Test browser
neuron-automation --test-browser

# Check Chrome installation
google-chrome --version
```

---

Ready for more advanced configuration? Check out [Advanced Settings](advanced-settings.md) or jump to [Usage](../usage/) to start using your configured system!