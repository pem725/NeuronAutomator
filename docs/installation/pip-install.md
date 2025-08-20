# pip Install (Coming Soon)

!!! warning "Package Not Available Yet"
    The `neuron-automation` package is not yet published to PyPI. Running `pip install neuron-automation` will return "No matching distribution found".

## Current Status

The package is **in development** and will be published to PyPI in a future release. For now, please use the [Git Clone installation method](manual-setup.md).

## Future Installation (When Available)

Once published, installation will be:

=== "Linux/macOS"

    ```bash
    # Install the package (future release)
    pip install neuron-automation
    
    # Set up system integration
    neuron-automation --setup
    
    # Test the installation
    neuron-automation
    ```

=== "Windows"

    ```powershell
    # Install the package (future release)
    pip install neuron-automation
    
    # Set up system integration (run as Administrator)
    neuron-automation --setup
    
    # Test the installation
    neuron-automation
    ```

## Why Not Available Yet?

Publishing to PyPI requires:
- Package testing and validation
- PyPI account setup and verification
- Release automation configuration
- Documentation completion

## Current Alternative

**Use the Git Clone method instead:**

```bash
# Clone the repository
git clone https://github.com/pem725/NeuronAutomator.git
cd NeuronAutomator

# Run platform-specific installer
./installers/install_linux.sh     # Linux
./installers/install_macos.sh     # macOS
./installers/install_windows.ps1  # Windows (PowerShell as Admin)

# Test installation
neuron-automation

# Update when needed
neuron-automation --update
```

This method provides:
- ✅ **Latest version** from GitHub
- ✅ **Built-in updates** via `--update` command
- ✅ **Same functionality** as pip would provide
- ✅ **Complete system integration**

## Future pip Installation Features

## What Happens During Setup

The `--setup` command performs platform-specific system integration:

### :material-linux: Linux Setup
- Downloads and runs the official Linux installer
- Installs Chrome if not present
- Creates systemd service and timer files
- Sets up automatic scheduling for weekday mornings
- Configures logging and data directories

### :material-apple: macOS Setup  
- Downloads and runs the official macOS installer
- Installs Chrome via Homebrew if needed
- Creates launchd plist files for scheduling
- Sets up user-space automation (no sudo required)
- Configures proper file permissions

### :material-microsoft-windows: Windows Setup
- Downloads and runs the official Windows installer
- Installs Chrome if not present
- Creates Task Scheduler entries
- Sets up Windows service integration
- Configures proper registry entries

## Installation Locations

After installation, files are organized as follows:

=== "Linux"

    ```
    ~/.config/neuron-automation/
    ├── neuron_automation.py      # Main automation script
    ├── config.py                 # Configuration file
    ├── link_manager.py           # Link management system
    ├── blacklist_rewind.py       # Time rewind tool
    ├── venv/                     # Virtual environment
    ├── data/                     # SQLite databases
    └── logs/                     # Application logs
    
    /usr/local/bin/
    ├── neuron-automation         # Command wrapper
    └── blacklist-rewind          # Rewind tool wrapper
    
    /etc/systemd/system/
    ├── neuron-automation.service # Systemd service
    └── neuron-automation.timer   # Scheduling timer
    ```

=== "macOS"

    ```
    ~/.config/neuron-automation/
    ├── neuron_automation.py      # Main automation script  
    ├── config.py                 # Configuration file
    ├── link_manager.py           # Link management system
    ├── blacklist_rewind.py       # Time rewind tool
    ├── venv/                     # Virtual environment
    ├── data/                     # SQLite databases
    └── logs/                     # Application logs
    
    /usr/local/bin/
    ├── neuron-automation         # Command wrapper
    └── blacklist-rewind          # Rewind tool wrapper
    
    ~/Library/LaunchAgents/
    └── com.neuron-automation.plist # Launch daemon
    ```

=== "Windows"

    ```
    %USERPROFILE%\.config\neuron-automation\
    ├── neuron_automation.py      # Main automation script
    ├── config.py                 # Configuration file  
    ├── link_manager.py           # Link management system
    ├── blacklist_rewind.py       # Time rewind tool
    ├── venv\                     # Virtual environment
    ├── data\                     # SQLite databases
    └── logs\                     # Application logs
    
    # Task Scheduler entries created automatically
    ```

## Verification Steps

### 1. Check Installation
```bash
# Verify the command is available
neuron-automation --version

# Check system integration status  
neuron-automation --check-setup
```

### 2. Test Core Functionality
```bash
# Run a test automation (opens browser)
neuron-automation

# View blacklist statistics
neuron-automation --stats

# Test the time rewind tool
neuron-automation --rewind-preview 7
```

### 3. Check Scheduled Automation
=== "Linux"

    ```bash
    # Check if systemd timer is active
    systemctl --user status neuron-automation.timer
    
    # View recent automation logs
    journalctl --user -u neuron-automation.service -n 20
    ```

=== "macOS"

    ```bash  
    # Check if launch agent is loaded
    launchctl list | grep neuron-automation
    
    # View recent logs
    tail -20 ~/.config/neuron-automation/logs/neuron_automation.log
    ```

=== "Windows"

    ```powershell
    # Check Task Scheduler entries
    Get-ScheduledTask -TaskName "*neuron*"
    
    # View recent logs  
    Get-Content ~/.config/neuron-automation/logs/neuron_automation.log -Tail 20
    ```

## Command Reference

After installation, these commands are available:

| Command | Purpose |
|---------|---------|
| `neuron-automation` | Run automation manually |
| `neuron-automation --setup` | Initial system setup |
| `neuron-automation --version` | Show version info |
| `neuron-automation --stats` | Show blacklist statistics |
| `neuron-automation --rewind 7` | Restore links from 7 days ago |
| `neuron-automation --recent-blacklisted 10` | Show recently blacklisted links |
| `blacklist-rewind` | Standalone time rewind tool |
| `blacklist-rewind --backup` | Create database backup |

## Updating

To update to the latest version:

```bash
# Update the package
pip install --upgrade neuron-automation

# Re-run setup to update system integration
neuron-automation --setup
```

## Uninstalling

To completely remove the installation:

```bash
# Remove the package
pip uninstall neuron-automation

# Clean up system integration (Linux/macOS)
sudo rm -rf ~/.config/neuron-automation
sudo rm /usr/local/bin/neuron-automation
sudo rm /usr/local/bin/blacklist-rewind

# Linux: Remove systemd files
sudo systemctl disable neuron-automation.timer
sudo rm /etc/systemd/system/neuron-automation.*

# macOS: Remove launch agent
launchctl unload ~/Library/LaunchAgents/com.neuron-automation.plist
rm ~/Library/LaunchAgents/com.neuron-automation.plist
```

## Troubleshooting

### Common Issues

!!! warning "Permission Denied"
    If you get permission errors on Linux/macOS, you may need to run the setup with sudo:
    ```bash
    sudo neuron-automation --setup
    ```

!!! warning "Chrome Not Found"
    If Chrome isn't detected, install it manually first:
    
    === "Linux"
        ```bash
        wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
        sudo add-apt-repository "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main"
        sudo apt update && sudo apt install google-chrome-stable
        ```
    
    === "macOS"
        ```bash
        brew install --cask google-chrome
        ```
    
    === "Windows"
        Download from: https://www.google.com/chrome/

!!! warning "Python Version"
    Ensure you're using Python 3.6 or higher:
    ```bash
    python --version  # or python3 --version
    ```

### Getting Help

If installation fails:

1. Check our [Troubleshooting Guide](troubleshooting.md)
2. Report issues on [GitHub](https://github.com/pem725/NeuronAutomator/issues)
3. Include your OS, Python version, and error messages

---

Next: [Configure your settings](../configuration/) to customize the automation behavior.