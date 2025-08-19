# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a cross-platform Python-based automation system that opens the Neuron Daily newsletter with all article links in separate Chrome tabs every weekday morning. Supports Linux, macOS, and Windows with platform-specific scheduling integration (systemd, launchd, Task Scheduler).

## Architecture

**Main Components:**
- `neuron_automation.py` - Core automation script with `NeuronNewsletterAutomation` class
- `config.py` - Enhanced configuration with platform detection and environment classes
- `setup.py` - pip installable package configuration
- `installers/` - Platform-specific installation scripts
  - `install_linux.sh` - Linux (Ubuntu/Debian) installer
  - `install_macos.sh` - macOS installer with Homebrew integration
  - `install_windows.ps1` - Windows PowerShell installer

**Cross-Platform Architecture:**
- Platform detection via `PlatformConfig` class
- Automatic config directory selection per platform
- Platform-specific scheduling integration:
  - Linux: systemd service/timer
  - macOS: launchd LaunchAgent
  - Windows: Task Scheduler
- Chrome profile isolation in platform-appropriate directories

## Development Commands

**Package Installation:**
```bash
pip install -e .  # Development install
pip install neuron-automation  # Production install
```

**Platform-Specific Installation:**
```bash
# Linux
./installers/install_linux.sh

# macOS  
./installers/install_macos.sh

# Windows (PowerShell as Admin)
.\installers\install_windows.ps1
```

**Testing:**
```bash
# Platform-specific tests
./installers/test_linux.sh      # Linux
./installers/test_macos.sh      # macOS
# (Windows test script TBD)
```

**Manual Execution:**
```bash
neuron-automation
```

**Development Testing:**
```bash
# Activate virtual environment
source ~/.config/neuron-automation/venv/bin/activate

# Run script directly
python3 ~/.config/neuron-automation/neuron_automation.py
```

**System Service Management:**
```bash
# Check timer status
systemctl status neuron-automation.timer

# View service logs
journalctl -u neuron-automation.service

# View application logs
tail -f ~/.config/neuron-automation/neuron_automation.log
```

## Configuration Architecture

The system uses a multi-layered configuration system:

**Platform Detection:**
- `PlatformConfig` class automatically detects OS and returns appropriate config
- Platform-specific directory paths and scheduling mechanisms
- Cross-platform Chrome options and WebDriver integration

**Environment Configurations:**
- `LinuxConfig`, `MacOSConfig`, `WindowsConfig` - Platform-specific settings
- `DevelopmentConfig` - Daily execution with verbose logging  
- `TestConfig` - Minimal retries for testing

Active configuration auto-selected via `PlatformConfig.get_platform_settings()`.

## Key Technical Details

**Dependencies:**
- selenium>=4.0.0
- webdriver-manager>=3.8.0  
- requests>=2.28.0
- beautifulsoup4>=4.11.0

**Chrome Integration:**
- Uses WebDriver Manager for automatic ChromeDriver management
- Isolated Chrome profile in `~/.config/neuron-automation/chrome_profile/`
- Configurable Chrome options including headless mode support

**Error Handling:**
- Comprehensive retry mechanisms with configurable attempts
- Network connectivity validation before execution
- Detailed logging to both systemd journal and application log file

**Security Considerations:**
- Runs as regular user (not root)
- Chrome profile isolation
- No sensitive data exposure in logs or configuration