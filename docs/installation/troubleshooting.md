# Installation Troubleshooting

Common installation issues and their solutions. Most problems can be resolved quickly with these troubleshooting steps.

## 🔍 Quick Diagnostics

### Check System Status
```bash
# Test basic functionality
neuron-automation --test

# Check version and installation
neuron-automation --version

# Validate configuration
neuron-automation --check-config
```

## 🐧 Linux Issues

### Permission Denied Errors
```bash
# Fix file permissions
chmod +x ~/.config/neuron-automation/neuron_automation.py
sudo chmod +x /usr/local/bin/neuron-automation

# Fix ownership
sudo chown -R $USER:$USER ~/.config/neuron-automation/
```

### Systemd Service Issues
```bash
# Check service status
systemctl --user status neuron-automation.timer

# Reload systemd configuration
systemctl --user daemon-reload

# Enable and start service
systemctl --user enable neuron-automation.timer
systemctl --user start neuron-automation.timer

# View service logs
journalctl --user -u neuron-automation.service -f
```

### Chrome Installation Issues
```bash
# Install Chrome on Ubuntu/Debian
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main"
sudo apt update && sudo apt install google-chrome-stable

# Verify installation
google-chrome --version
```

## 🍎 macOS Issues

### Homebrew Installation
```bash
# Install Homebrew if missing
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Chrome via Homebrew
brew install --cask google-chrome

# Verify installation
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version
```

### Launch Agent Issues
```bash
# Check launch agent status
launchctl list | grep neuron-automation

# Unload and reload launch agent
launchctl unload ~/Library/LaunchAgents/com.neuron-automation.plist
launchctl load ~/Library/LaunchAgents/com.neuron-automation.plist

# Check plist file syntax
plutil -lint ~/Library/LaunchAgents/com.neuron-automation.plist
```

### Permission Issues
```bash
# Fix script permissions
chmod +x ~/.config/neuron-automation/neuron_automation.py
sudo chmod +x /usr/local/bin/neuron-automation

# Fix launch agent permissions
chmod 644 ~/Library/LaunchAgents/com.neuron-automation.plist
```

## 🪟 Windows Issues

### PowerShell Execution Policy
```powershell
# Check current policy
Get-ExecutionPolicy

# Set execution policy (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Task Scheduler Issues
```powershell
# Check scheduled tasks
Get-ScheduledTask -TaskName "*neuron*"

# Get detailed task information
Get-ScheduledTask -TaskName "NeuronAutomation" | Get-ScheduledTaskInfo

# Manually run task for testing
Start-ScheduledTask -TaskName "NeuronAutomation"
```

### Chrome Installation
```powershell
# Install Chrome via Chocolatey (if available)
choco install googlechrome

# Or download manually
# Visit: https://www.google.com/chrome/
```

## 🐍 Python Issues

### Python Version Problems
```bash
# Check Python version (need 3.6+)
python --version
python3 --version

# Install Python 3 on Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip

# Install Python 3 on macOS via Homebrew
brew install python3

# Windows: Download from python.org
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf ~/.config/neuron-automation/venv
python3 -m venv ~/.config/neuron-automation/venv

# Activate and reinstall dependencies
source ~/.config/neuron-automation/venv/bin/activate
pip install -r ~/.config/neuron-automation/requirements.txt
```

### Package Installation Failures
```bash
# Upgrade pip first
pip install --upgrade pip

# Install with verbose output
pip install -v selenium webdriver-manager requests beautifulsoup4

# Clear pip cache if needed
pip cache purge
```

## 🌐 Network Issues

### Connection Problems
```bash
# Test internet connectivity
ping -c 4 www.theneurondaily.com

# Test SSL/HTTPS
curl -I https://www.theneurondaily.com/

# Check DNS resolution
nslookup www.theneurondaily.com
```

### Proxy/Firewall Issues
```bash
# Test with proxy settings
export https_proxy=http://your-proxy:port
neuron-automation --test

# Configure Chrome for proxy
# Add to config.py:
CHROME_OPTIONS = [
    "--proxy-server=http://your-proxy:port"
]
```

## 🔧 Common Error Messages

### "selenium.common.exceptions.WebDriverException"
**Solution**: Update Chrome and webdriver-manager
```bash
# Update Chrome to latest version
# Then update webdriver-manager
pip install --upgrade webdriver-manager

# Clear webdriver cache
rm -rf ~/.wdm/
```

### "ModuleNotFoundError: No module named 'selenium'"
**Solution**: Reinstall Python packages
```bash
source ~/.config/neuron-automation/venv/bin/activate
pip install -r requirements.txt
```

### "Permission denied: '/usr/local/bin/neuron-automation'"
**Solution**: Fix executable permissions
```bash
sudo chmod +x /usr/local/bin/neuron-automation
```

### "Database is locked"
**Solution**: Stop automation service first
```bash
# Linux/macOS
systemctl --user stop neuron-automation.timer

# Run operation
neuron-automation --your-command

# Restart service
systemctl --user start neuron-automation.timer
```

## 🛠️ Advanced Troubleshooting

### Enable Debug Logging
```python
# Edit ~/.config/neuron-automation/config.py
LOG_LEVEL = "DEBUG"
```

### Manual Testing
```bash
# Test each component individually
cd ~/.config/neuron-automation
source venv/bin/activate

# Test browser
python3 -c "from selenium import webdriver; driver = webdriver.Chrome(); driver.get('https://google.com'); driver.quit()"

# Test network access
python3 -c "import requests; print(requests.get('https://www.theneurondaily.com/').status_code)"

# Test configuration
python3 -c "import config; print('Config loaded successfully')"
```

### Reset Everything
```bash
# Complete reset (nuclear option)
systemctl --user stop neuron-automation.timer
rm -rf ~/.config/neuron-automation
sudo rm /usr/local/bin/neuron-automation
sudo rm /usr/local/bin/blacklist-rewind

# Reinstall
pip install neuron-automation
neuron-automation --setup
```

## 📞 Getting More Help

### Log File Locations
- **Linux/macOS**: `~/.config/neuron-automation/logs/neuron_automation.log`
- **Windows**: `%USERPROFILE%\.config\neuron-automation\logs\neuron_automation.log`

### Collect System Information
```bash
# Generate system info for bug reports
neuron-automation --system-info > system_info.txt
```

### Create Bug Report
When reporting issues, include:

1. **Operating System** and version
2. **Python version**: `python --version`
3. **Chrome version**: `google-chrome --version`
4. **Error messages** (full text)
5. **Log files** (recent entries)
6. **Steps to reproduce** the issue

### Community Support
- **GitHub Issues**: [Report bugs and get help](https://github.com/pem725/NeuronAutomator/issues)
- **GitHub Discussions**: [Ask questions](https://github.com/pem725/NeuronAutomator/discussions)

---

**Still having issues?** Don't hesitate to [create an issue](https://github.com/pem725/NeuronAutomator/issues/new) with your system information and error details. The community is here to help!