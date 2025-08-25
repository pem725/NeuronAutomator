# Manual Installation

For users who want full control over the installation process or don't use Python package managers, manual installation provides platform-specific installers with complete system integration.

## Platform-Specific Installation

=== "Linux (Ubuntu/Debian)"

    ### Prerequisites
    - Ubuntu 18.04+ or Debian 10+
    - Internet connection
    - Terminal access

    ### Installation Steps
    
    ```bash
    # 1. Clone the repository
    git clone https://github.com/pem725/NeuronAutomator.git
    cd NeuronAutomator
    
    # 2. Make installer executable
    chmod +x installers/install_linux.sh
    
    # 3. Run the installer
    ./installers/install_linux.sh
    ```

=== "macOS"

    ### Prerequisites
    - macOS 10.14+ (Mojave or later)
    - Internet connection
    - Terminal access

    ### Installation Steps
    
    ```bash
    # 1. Clone the repository
    git clone https://github.com/pem725/NeuronAutomator.git
    cd NeuronAutomator
    
    # 2. Make installer executable
    chmod +x installers/install_macos.sh
    
    # 3. Run the installer
    ./installers/install_macos.sh
    ```

=== "Windows"

    ### Prerequisites
    - Windows 10 or later
    - PowerShell 5.1 or later
    - Internet connection

    ### Installation Steps
    
    ```powershell
    # 1. Clone the repository (or download ZIP)
    git clone https://github.com/pem725/NeuronAutomator.git
    cd NeuronAutomator
    
    # 2. Set execution policy (run PowerShell as Administrator)
    Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
    
    # 3. Run the installer
    .\installers\install_windows.ps1
    ```

## What the Installer Does

The manual installer provides complete system integration:

### :material-download: Downloads & Installs
- **Python 3.9+** (if not present)
- **Google Chrome** (if not present) 
- **Package managers** (APT, Homebrew, Chocolatey)
- **System dependencies** (git, curl, etc.)

### :material-cog: Sets Up Environment
- **Virtual environment** with required Python packages
- **Configuration directory** (`~/.config/neuron-automation/`)
- **Log directories** with proper permissions
- **Data directories** for SQLite databases

### :material-clock: Configures Scheduling
- **Linux**: systemd service and timer files
- **macOS**: launchd plist configuration
- **Windows**: Task Scheduler entries

### :material-console: Installs Commands
- **neuron-automation**: Main automation command
- **blacklist-rewind**: Time rewind tool
- **System PATH**: Commands available globally

## Installation Verification

After installation, verify everything works:

```bash
# Check version
neuron-automation --version

# Test the automation
neuron-automation

# Check scheduled automation status
# Linux:
systemctl --user status neuron-automation.timer

# macOS:
launchctl list | grep neuron-automation

# Windows:
Get-ScheduledTask -TaskName "*neuron*"
```

## Manual Configuration

The installer creates default configurations, but you can customize:

### Configuration File Location
- **Linux/macOS**: `~/.config/neuron-automation/config.py`
- **Windows**: `%USERPROFILE%\.config\neuron-automation\config.py`

### Key Settings to Review
```python
# Scheduling (change automation times)
AUTOMATION_TIMES = ["05:30", "06:00", "06:30", "07:00"]

# Days to run (0=Monday, 6=Sunday)
ENABLED_DAYS = [0, 1, 2, 3, 4]  # Weekdays only

# Browser options
CHROME_OPTIONS = [
    "--no-sandbox",
    "--disable-dev-shm-usage"
]
```

## Post-Installation Tasks

### 1. Test Browser Integration
```bash
# Should open Chrome with newsletter tabs
neuron-automation
```

### 2. Configure Link Management
```bash
# View initial statistics (will be empty)
neuron-automation --stats

# Check blacklist configuration
cat ~/.config/neuron-automation/config.py | grep BLACKLIST
```

### 3. Set Up Monitoring
```bash
# View logs
tail -f ~/.config/neuron-automation/logs/neuron_automation.log

# Check service status regularly
# Linux: systemctl --user status neuron-automation.timer
# macOS: launchctl list | grep neuron
# Windows: Get-ScheduledTask | Where-Object {$_.TaskName -like "*neuron*"}
```

## Advanced Manual Setup

### Custom Installation Directory

If you need to install in a custom location:

```bash
# Set custom directory
export NEURON_INSTALL_DIR="/opt/neuron-automation"

# Run installer with custom path
./installers/install_linux.sh --install-dir "$NEURON_INSTALL_DIR"
```

### Offline Installation

For systems without internet access:

1. **Download dependencies** on connected machine:
   ```bash
   pip download -r requirements.txt -d ./packages/
   ```

2. **Transfer files** to target machine

3. **Install offline**:
   ```bash
   ./installers/install_linux.sh --offline --package-dir ./packages/
   ```

### Enterprise Deployment

For deploying across multiple systems:

```bash
# Create deployment package
./installers/create_deployment_package.sh

# Deploy to multiple hosts
for host in server1 server2 server3; do
    scp deployment-package.tar.gz $host:/tmp/
    ssh $host "cd /tmp && tar -xf deployment-package.tar.gz && ./install.sh"
done
```

## Troubleshooting

### Permission Issues

```bash
# Fix file permissions
chmod -R 755 ~/.config/neuron-automation/
chown -R $USER:$USER ~/.config/neuron-automation/

# Fix executable permissions
chmod +x /usr/local/bin/neuron-automation
chmod +x /usr/local/bin/blacklist-rewind
```

### Service Registration Issues

=== "Linux"

    ```bash
    # Reload systemd daemon
    systemctl --user daemon-reload
    
    # Check service file
    systemctl --user cat neuron-automation.service
    
    # Manual service start
    systemctl --user start neuron-automation.service
    ```

=== "macOS"

    ```bash
    # Load launch agent manually
    launchctl load ~/Library/LaunchAgents/com.neuron-automation.plist
    
    # Check plist syntax
    plutil -lint ~/Library/LaunchAgents/com.neuron-automation.plist
    
    # View agent status
    launchctl print gui/$(id -u)/com.neuron-automation
    ```

=== "Windows"

    ```powershell
    # Check Task Scheduler manually
    Get-ScheduledTask -TaskName "NeuronAutomation*" | Get-ScheduledTaskInfo
    
    # Register task manually
    Register-ScheduledTask -Xml (Get-Content "task-definition.xml" | Out-String) -TaskName "NeuronAutomation"
    ```

### Dependency Issues

```bash
# Check Python installation
python3 --version
which python3

# Check Chrome installation
google-chrome --version
which google-chrome

# Reinstall Python packages
~/.config/neuron-automation/venv/bin/pip install -r requirements.txt --force-reinstall
```

## Uninstalling

To completely remove the manual installation:

=== "Linux"

    ```bash
    # Stop and disable services
    systemctl --user stop neuron-automation.timer
    systemctl --user disable neuron-automation.timer
    
    # Remove files
    rm -rf ~/.config/neuron-automation
    sudo rm /usr/local/bin/neuron-automation
    sudo rm /usr/local/bin/blacklist-rewind
    sudo rm ~/.config/systemd/user/neuron-automation.*
    
    # Reload systemd
    systemctl --user daemon-reload
    ```

=== "macOS"

    ```bash
    # Unload launch agent
    launchctl unload ~/Library/LaunchAgents/com.neuron-automation.plist
    
    # Remove files
    rm -rf ~/.config/neuron-automation
    sudo rm /usr/local/bin/neuron-automation  
    sudo rm /usr/local/bin/blacklist-rewind
    rm ~/Library/LaunchAgents/com.neuron-automation.plist
    ```

=== "Windows"

    ```powershell
    # Remove scheduled tasks
    Unregister-ScheduledTask -TaskName "NeuronAutomation*" -Confirm:$false
    
    # Remove files
    Remove-Item -Recurse -Force ~/.config/neuron-automation
    Remove-Item C:\Windows\System32\neuron-automation.bat
    Remove-Item C:\Windows\System32\blacklist-rewind.bat
    ```

---

**Next**: [Configure your installation](../configuration/index.md) to customize behavior and scheduling.