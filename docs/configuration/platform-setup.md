# Platform Setup

Platform-specific configuration and optimization for Linux, macOS, and Windows. Customize system integration and performance for your operating system.

## 🐧 Linux Configuration

### System Integration

Linux provides the most comprehensive automation capabilities through systemd:

```bash
# Check systemd service status
systemctl status neuron-automation.service

# Check timer schedule
systemctl status neuron-automation.timer

# View service logs
journalctl -u neuron-automation.service -f
```

### Linux-Specific Settings

```python
# config.py - Linux optimizations

class LinuxConfig:
    # System service configuration
    SYSTEMD_SERVICE = True
    SERVICE_USER = os.getenv('USER')
    
    # Performance optimizations
    USE_SYSTEM_CHROME = True
    CHROME_EXECUTABLE = "/usr/bin/google-chrome"
    
    # File system paths
    CONFIG_BASE = os.path.expanduser("~/.config/neuron-automation")
    LOG_DIRECTORY = os.path.expanduser("~/.config/neuron-automation/logs")
    
    # Desktop integration
    DESKTOP_NOTIFICATIONS = True
    SHOW_BROWSER_ON_DESKTOP = True
```

### Ubuntu/Debian Optimization

```bash
# Install additional performance packages
sudo apt install preload iotop htop

# Configure Chrome for automation
sudo mkdir -p /opt/chrome-automation
sudo chown $USER:$USER /opt/chrome-automation

# Optimize systemd service
sudo systemctl edit neuron-automation.service
```

Add to the service override:
```ini
[Service]
IOSchedulingClass=3
IOSchedulingPriority=7
CPUSchedulingPolicy=2
Nice=10
```

### Arch Linux Configuration

```bash
# Use AUR package manager for Chrome
yay -S google-chrome

# Systemd user services
systemctl --user enable neuron-automation.service
systemctl --user start neuron-automation.timer
```

## 🍎 macOS Configuration

### LaunchAgent Integration

macOS uses LaunchAgents for scheduling automation:

```bash
# Check LaunchAgent status
launchctl list | grep neuron

# View LaunchAgent configuration
cat ~/Library/LaunchAgents/com.neuron-automation.plist

# Manually load/unload
launchctl load ~/Library/LaunchAgents/com.neuron-automation.plist
launchctl unload ~/Library/LaunchAgents/com.neuron-automation.plist
```

### macOS-Specific Settings

```python
# config.py - macOS optimizations

class MacOSConfig:
    # LaunchAgent configuration
    LAUNCHD_SERVICE = True
    LAUNCH_AGENT_PATH = os.path.expanduser("~/Library/LaunchAgents")
    
    # macOS paths
    CHROME_EXECUTABLE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    CONFIG_BASE = os.path.expanduser("~/Library/Application Support/neuron-automation")
    
    # macOS integration
    NOTIFICATION_CENTER = True
    DOCK_BADGE_UPDATES = False
    MENU_BAR_ICON = False  # Future feature
    
    # Power management
    RESPECT_POWER_SETTINGS = True
    PREVENT_SLEEP_DURING_AUTOMATION = True
```

### Homebrew Integration

```bash
# Ensure Homebrew is properly configured
brew doctor

# Install Chrome via Homebrew if not present
brew install --cask google-chrome

# Optional: Install monitoring tools
brew install htop glances
```

### macOS Security Configuration

```bash
# Add automation to accessibility permissions
# System Preferences > Security & Privacy > Privacy > Accessibility

# Allow Chrome automation
# System Preferences > Security & Privacy > Privacy > Automation

# Configure Gatekeeper (if needed)
sudo spctl --master-disable  # Only if necessary for testing
```

## 🪟 Windows Configuration

### Task Scheduler Integration

Windows uses Task Scheduler for automation:

```powershell
# Check scheduled task status
Get-ScheduledTask -TaskName "NeuronAutomation*"

# View task details
Get-ScheduledTaskInfo -TaskName "NeuronAutomationDaily"

# Run task manually
Start-ScheduledTask -TaskName "NeuronAutomationDaily"
```

### Windows-Specific Settings

```python
# config.py - Windows optimizations

class WindowsConfig:
    # Task Scheduler configuration
    TASK_SCHEDULER = True
    TASK_USER = os.getenv('USERNAME')
    
    # Windows paths
    CHROME_EXECUTABLE = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    CONFIG_BASE = os.path.expanduser(r"~\.config\neuron-automation")
    
    # Windows integration
    WINDOWS_NOTIFICATIONS = True
    TASKBAR_PROGRESS = False  # Future feature
    
    # Performance
    PROCESS_PRIORITY = "below_normal"
    MEMORY_OPTIMIZATION = True
```

### PowerShell Configuration

```powershell
# Set execution policy (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install Chrome (if not present)
winget install Google.Chrome

# Optional: Install monitoring tools
winget install Microsoft.Sysinternals.ProcessMonitor
```

### Windows Defender Configuration

```powershell
# Add exclusion for automation directory (optional)
Add-MpPreference -ExclusionPath "$env:USERPROFILE\.config\neuron-automation"

# Add exclusion for Python processes (if needed)
Add-MpPreference -ExclusionProcess "python.exe"
Add-MpPreference -ExclusionProcess "chrome.exe"
```

## 🔧 Cross-Platform Optimization

### Network Configuration

```python
# config.py - Network optimizations for all platforms

class NetworkConfig:
    # DNS configuration
    DNS_SERVERS = ["1.1.1.1", "8.8.8.8"]  # Fast DNS servers
    
    # Connection settings
    CONNECTION_TIMEOUT = 10
    READ_TIMEOUT = 15
    MAX_RETRIES = 3
    
    # Proxy configuration (if needed)
    HTTP_PROXY = None   # "http://proxy:8080"
    HTTPS_PROXY = None  # "https://proxy:8080"
    NO_PROXY = "localhost,127.0.0.1"
```

### Browser Optimization

```python
# config.py - Cross-platform browser settings

class BrowserConfig:
    # Memory management
    CHROME_OPTIONS = [
        "--memory-pressure-off",
        "--max_old_space_size=512",
        "--disable-background-timer-throttling",
        "--disable-renderer-backgrounding",
        "--disable-backgrounding-occluded-windows"
    ]
    
    # Performance flags
    PERFORMANCE_OPTIONS = [
        "--enable-fast-unload",
        "--enable-aggressive-domstorage-flushing",
        "--enable-parallel-downloading",
        "--disable-ipc-flooding-protection"
    ]
```

## 📊 Platform-Specific Monitoring

### Linux Monitoring

```bash
# Resource monitoring
htop -p $(pgrep -f neuron-automation)

# I/O monitoring
sudo iotop -p $(pgrep -f neuron-automation)

# Network monitoring
sudo netstat -tulpn | grep chrome

# Systemd journal monitoring
journalctl -u neuron-automation.service --since "1 hour ago"
```

### macOS Monitoring

```bash
# Activity Monitor via command line
top -pid $(pgrep -f neuron-automation)

# Network activity
nettop -p $(pgrep -f chrome)

# Console logs
log show --predicate 'subsystem == "com.neuron.automation"' --info
```

### Windows Monitoring

```powershell
# Process monitoring
Get-Process -Name "*neuron*" | Select-Object CPU,WorkingSet,PagedMemorySize

# Network monitoring
netstat -an | Select-String "chrome"

# Event log monitoring
Get-WinEvent -LogName Application | Where-Object {$_.ProviderName -like "*neuron*"}
```

## 🚀 Performance Tuning by Platform

### Linux Performance Tuning

```bash
# I/O scheduler optimization (for SSD)
echo mq-deadline | sudo tee /sys/block/sda/queue/scheduler

# Swappiness optimization
echo 'vm.swappiness=10' | sudo tee -a /etc/sysctl.conf

# File descriptor limits
echo 'fs.file-max = 65536' | sudo tee -a /etc/sysctl.conf

# Network buffer optimization
echo 'net.core.rmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
echo 'net.core.wmem_max = 16777216' | sudo tee -a /etc/sysctl.conf
```

### macOS Performance Tuning

```bash
# Increase file descriptor limits
sudo launchctl limit maxfiles 65536 200000

# Optimize network settings
sudo sysctl -w net.inet.tcp.delayed_ack=0

# Memory pressure monitoring
memory_pressure
```

### Windows Performance Tuning

```powershell
# Increase virtual memory if needed
$cs = Get-WmiObject -Class Win32_ComputerSystem
$TotalPhysicalMemory = [Math]::Round($cs.TotalPhysicalMemory / 1GB)
$PageFileSize = $TotalPhysicalMemory * 1.5

# Optimize power settings for performance
powercfg /setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c  # High performance

# Disable Windows Search indexing for automation directory
Remove-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows Search\Crawlmgr\Extensions\Web" -Name "*.log" -ErrorAction SilentlyContinue
```

## 🔒 Platform Security Considerations

### Linux Security

```bash
# AppArmor profile (Ubuntu)
sudo nano /etc/apparmor.d/neuron-automation

# SELinux context (RHEL/CentOS)
sudo setsebool -P httpd_can_network_connect 1

# Firewall configuration
sudo ufw allow out 443/tcp
sudo ufw allow out 80/tcp
```

### macOS Security

```bash
# System Integrity Protection considerations
csrutil status

# Code signing verification
codesign -dv /Applications/Google\ Chrome.app

# Keychain integration (future feature)
security add-generic-password -s "neuron-automation" -a "$USER"
```

### Windows Security

```powershell
# Windows Defender exclusions
Add-MpPreference -ExclusionPath "$env:USERPROFILE\.config"

# User Account Control settings
# Manual: Control Panel > User Accounts > Change User Account Control settings

# Execution policy
Get-ExecutionPolicy -List
```

## 🛠️ Troubleshooting Platform Issues

### Common Linux Issues

```bash
# Permission issues
sudo chown -R $USER:$USER ~/.config/neuron-automation
chmod -R 755 ~/.config/neuron-automation

# Chrome not found
which google-chrome || which chromium-browser || which chrome

# Display issues (headless servers)
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

### Common macOS Issues

```bash
# LaunchAgent not loading
launchctl load -w ~/Library/LaunchAgents/com.neuron-automation.plist

# Chrome permissions
tccutil reset SystemPolicyDesktopFolder com.google.Chrome

# Path issues
echo $PATH | tr ':' '\n' | grep -E "(local|opt)"
```

### Common Windows Issues

```powershell
# Task Scheduler issues
schtasks /query /tn "NeuronAutomation*" /v

# Path issues
$env:PATH -split ';' | Where-Object {$_ -like "*Chrome*"}

# PowerShell execution issues
Get-ExecutionPolicy
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Next Steps

<div class="grid cards" markdown>

-   **Basic Configuration**
    
    Start with essential settings before platform optimization.
    
    [:octicons-arrow-right-24: Basic Config](basic-config.md)

-   **Advanced Settings**
    
    Fine-tune performance and behavior for your platform.
    
    [:octicons-arrow-right-24: Advanced Settings](advanced-settings.md)

-   **Troubleshooting**
    
    Platform-specific troubleshooting guides.
    
    [:octicons-arrow-right-24: Troubleshooting](../installation/troubleshooting.md)

</div>