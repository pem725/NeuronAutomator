# Neuron Daily Newsletter Automation

**Cross-platform automation system** that automatically opens the latest Neuron Daily newsletter with all article links in separate tabs every weekday morning.

**Supported Platforms:** Linux, macOS, Windows

## Features

- ✅ **Smart Multi-Run System**: Multiple scheduled runs with intelligent change detection
- ✅ **Optimal Newsletter Coverage**: Catches newsletters regardless of publication time (5:00-7:00 AM)
- ✅ **Intelligent Link Extraction**: Finds and filters relevant article links
- ✅ **Error Recovery**: Robust retry mechanisms and comprehensive error handling
- ✅ **Cross-Platform**: Works on Linux, macOS, and Windows
- ✅ **System Integration**: Automatic scheduling (systemd/launchd/Task Scheduler)
- ✅ **Easy Installation**: Platform-specific installers or pip install
- ✅ **Logging**: Detailed logging for troubleshooting
- ✅ **Configuration**: Easily customizable settings
- ✅ **Chrome Integration**: Opens tabs in your regular Chrome browser (preserves existing tabs)
- ✅ **Network Resilience**: Checks connectivity before running

## Quick Start

### Option 1: pip Install (Recommended)

```bash
pip install neuron-automation
neuron-automation --setup
```

### Option 2: Manual Installation

1. **Clone or Download**
```bash
git clone https://github.com/pem725/NeuronAutomator.git
cd NeuronAutomator
```

2. **Run Platform-Specific Installer**

#### Linux (Ubuntu/Debian)
```bash
chmod +x installers/install_linux.sh
./installers/install_linux.sh
```

#### macOS
```bash
chmod +x installers/install_macos.sh
./installers/install_macos.sh
```

#### Windows
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\installers\install_windows.ps1
```

The installer will:
- Install system dependencies (Python, Chrome, package managers)
- Create a virtual environment with required packages
- Set up automatic scheduling (systemd/launchd/Task Scheduler)
- Configure the system to run multiple times each weekday morning (5:30, 6:00, 6:30, 7:00 AM)

### 3. Test the Installation

Test that everything works:

```bash
neuron-automation
```

This should open Chrome with the Neuron Daily newsletter and article tabs.

## Usage

### Automatic Operation
The script runs automatically at 5:30, 6:00, 6:30, and 7:00 AM on weekdays, with smart detection to prevent redundant executions.

### Manual Operation
Run manually anytime:
```bash
neuron-automation
```

Check version:
```bash
neuron-automation --version
```

Check for updates:
```bash
neuron-automation --check-updates
```

## How It Works: Smart Multi-Run System

The automation uses a sophisticated **Phase 2** approach that combines multiple scheduled runs with intelligent content detection:

### **📅 Daily Schedule**
- **5:30 AM**: Early check (catches early publications)
- **6:00 AM**: Primary window (most common publication time)  
- **6:30 AM**: Late catch (for delayed publications)
- **7:00 AM**: Final safety net (covers very late publications)

### **🧠 Smart Detection Logic**

**Scenario 1: Normal Publication (6:15 AM)**
- 5:30 AM → Finds old content → Proceeds (user gets yesterday's articles temporarily)
- 6:00 AM → Same old content → **SKIPS** (smart detection prevents redundancy)
- 6:30 AM → **NEW content detected!** → Proceeds (user gets today's articles)
- 7:00 AM → Same new content → **SKIPS** (already got today's content)

**Scenario 2: Late Publication (6:45 AM)**
- 5:30 AM, 6:00 AM, 6:30 AM → All skip old content after first run
- 7:00 AM → **NEW content detected!** → Proceeds (catches late publication)

**Result: Perfect coverage with zero redundancy** ✨

### **🌐 Chrome Browser Integration**

The automation now uses your **regular Chrome browser** instead of creating isolated instances:

**✅ Benefits:**
- **Persistent Tabs**: Newsletter tabs remain open until you manually close them
- **No Interruption**: If you get up late, your tabs from 5:30 AM are still there
- **Regular Profile**: Uses your bookmarks, extensions, and settings
- **Existing Windows**: Adds tabs to current Chrome windows when possible

**📖 Reading Scenarios:**
- **Early Bird (6:00 AM)**: Get fresh tabs, read immediately
- **Late Riser (8:00 AM)**: Earlier tabs still open and waiting
- **Multiple Runs**: Later runs add to existing tabs (smart detection prevents duplicates)

### System Management

Check if the timer is active:
```bash
systemctl status neuron-automation.timer
```

View service logs:
```bash
journalctl -u neuron-automation.service
```

View application logs:
```bash
tail -f ~/.config/neuron-automation/neuron_automation.log
```

Stop the automatic timer:
```bash
sudo systemctl stop neuron-automation.timer
sudo systemctl disable neuron-automation.timer
```

Re-enable the timer:
```bash
sudo systemctl enable neuron-automation.timer
sudo systemctl start neuron-automation.timer
```

## Configuration

The script can be customized by editing the configuration file:

```bash
nano ~/.config/neuron-automation/config.py
```

### Key Settings

| Setting | Description | Default |
|---------|-------------|---------|
| `BASE_URL` | Newsletter URL | `https://www.theneurondaily.com/` |
| `ENABLED_DAYS` | Days to run (0=Monday, 6=Sunday) | `[0,1,2,3,4]` (weekdays) |
| `MAX_RETRIES` | Retry attempts on failure | `3` |
| `PAGE_LOAD_TIMEOUT` | Page load timeout (seconds) | `30` |
| `CHROME_OPTIONS` | Chrome browser options | See config.py |
| `LOG_LEVEL` | Logging verbosity | `INFO` |

### Customizing the Schedule

To change when the script runs, edit the systemd timer:

```bash
sudo systemctl edit neuron-automation.timer
```

Add your custom schedule:
```ini
[Timer]
# Add an additional run at 7:30 AM
OnCalendar=Mon,Tue,Wed,Thu,Fri *-*-* 07:30:00
```

Common schedule formats:
- `*-*-* 09:00:00` - Daily at 9:00 AM
- `Mon *-*-* 05:30:00` - Mondays only at 5:30 AM  
- `*-*-01 05:30:00` - First day of every month

## Troubleshooting

### Common Issues

**Chrome not opening:**
```bash
# Check if Chrome is installed
google-chrome --version

# Check Chrome driver
~/.config/neuron-automation/venv/bin/python -c "from selenium import webdriver; print('Selenium OK')"
```

**Permission errors:**
```bash
# Fix permissions
chmod +x /usr/local/bin/neuron-automation
sudo chown -R $USER:$USER ~/.config/neuron-automation/
```

**Service not running:**
```bash
# Check service status
systemctl status neuron-automation.service

# View recent logs
journalctl -u neuron-automation.service -n 50
```

**Network issues:**
```bash
# Test connectivity
curl -I https://www.theneurondaily.com/
```

### Debug Mode

Enable debug logging by editing the config:
```python
LOG_LEVEL = "DEBUG"
```

Or use the development configuration:
```python
ACTIVE_CONFIG = DevelopmentConfig
```

### Manual Testing

Test individual components:

```bash
# Activate the virtual environment
source ~/.config/neuron-automation/venv/bin/activate

# Test the script directly
cd ~/.config/neuron-automation
python3 neuron_automation.py
```

## File Structure

```
~/.config/neuron-automation/
├── neuron_automation.py      # Main script
├── config.py                 # Configuration file
├── venv/                     # Python virtual environment
├── neuron_automation.log     # Application logs
├── requirements.txt          # Python dependencies
└── uninstall.sh             # Uninstallation script

/usr/local/bin/
└── neuron-automation        # System command wrapper

/etc/systemd/system/
├── neuron-automation.service # Systemd service
└── neuron-automation.timer   # Systemd timer
```

## Advanced Usage

### Running in Different Modes

**Test mode** (minimal retries, debug logging):
```bash
# Edit config.py and change:
ACTIVE_CONFIG = TestConfig
```

**Development mode** (verbose logging, runs every day):
```bash
# Edit config.py and change:
ACTIVE_CONFIG = DevelopmentConfig
```

### Custom Link Filtering

Modify link filtering by editing these config variables:
```python
SKIP_LINK_PATTERNS = [
    # Add patterns to skip
    'advertisement', 'promo', 'sponsor'
]

SKIP_TEXT_PATTERNS = [
    # Add text patterns to skip
    'buy now', 'limited time'
]
```

### Headless Mode

Run without opening browser windows:
```python
CHROME_OPTIONS = [
    "--headless",
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
```

### Custom Selectors

If the website structure changes, update selectors:
```python
CONTENT_SELECTORS = [
    ".newsletter-content",  # Add site-specific selectors
    ".article-list"
]
```

## Security Considerations

- The script opens tabs in your regular Chrome browser, using your existing profile and settings
- When possible, it connects to existing Chrome instances rather than creating new ones
- Logs may contain URLs visited - review log files if sharing system access  
- The script only accesses the specified newsletter URL and extracted links
- Browser tabs remain open until you manually close them, allowing you to read at your own pace

## Performance

**Resource Usage:**
- Memory: ~100-200MB during execution
- CPU: Low (brief spike during Chrome startup)
- Disk: ~50MB for virtual environment and dependencies
- Network: Minimal (loads newsletter page once, then opens tabs)

**Optimization Tips:**
- Use headless mode to reduce resource usage
- Adjust `PAGE_LOAD_TIMEOUT` for slower connections
- Reduce `MAX_RETRIES` if network is reliable

## Uninstallation

To completely remove the automation:

```bash
~/.config/neuron-automation/uninstall.sh
```

This will:
- Stop and disable the systemd timer
- Remove all system files
- Optionally remove configuration and logs

## Contributing

### Development Setup

1. Fork the project
2. Create a development environment:
```bash
python3 -m venv dev-env
source dev-env/bin/activate
pip install -r requirements.txt
```

3. Use the test configuration:
```python
ACTIVE_CONFIG = TestConfig
```

### Testing

Run tests with different configurations:
```bash
# Test with current site
python3 neuron_automation.py

# Test connectivity
python3 -c "from neuron_automation import NeuronNewsletterAutomation; n=NeuronNewsletterAutomation(); print(n.check_internet_connectivity())"
```

## Changelog

### Version 1.0.0
- Initial release
- Automated weekday newsletter opening
- Intelligent link extraction
- Systemd integration
- Comprehensive error handling
- Configurable settings

## License

MIT License - feel free to modify and distribute.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review logs in `~/.config/neuron-automation/neuron_automation.log`
3. Test manually with debug logging enabled
4. Check systemd service status and logs

**System Requirements:**
- Ubuntu 18.04+ (or compatible Debian-based distribution)
- Python 3.6+
- Internet connection
- X11 display server (for GUI Chrome)

**Tested On:**
- Ubuntu 20.04 LTS
- Ubuntu 22.04 LTS
- Ubuntu 24.04 LTS

## Updating

The system includes an automatic update mechanism to easily upgrade to newer versions while preserving your configuration.

### Easy Update Method

**Linux/macOS:**
```bash
./update.sh
```

**Windows:**
```batch
update.bat
```

### Update Process
The updater will:
1. 📦 **Backup** your current configuration and logs
2. 🌐 **Download** the latest version from GitHub
3. 🔧 **Install** the new version using platform-specific installers
4. 📂 **Restore** your preserved settings and data
5. ✅ **Verify** the update completed successfully

### What's Preserved
- Configuration files and customizations  
- Application logs
- Content change detection cache

### Manual Update
If the automatic updater doesn't work:

1. **Download latest version:**
   ```bash
   git clone https://github.com/pem725/NeuronAutomator.git neuron-update
   cd neuron-update
   ```

2. **Run installer:**
   ```bash
   # Linux
   ./installers/install_linux.sh
   
   # macOS
   ./installers/install_macos.sh
   
   # Windows (PowerShell as Admin)
   .\installers\install_windows.ps1
   ```

### Version Management
- Check current version: `neuron-automation --version`
- Check for updates: `neuron-automation --check-updates`
- View update history on [GitHub Releases](https://github.com/pem725/NeuronAutomator/releases)