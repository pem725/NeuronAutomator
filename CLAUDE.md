# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based automation system that opens the Neuron Daily newsletter with all article links in separate Chrome tabs every weekday morning on Ubuntu. The system uses Selenium WebDriver for browser automation and integrates with systemd for scheduled execution.

## Architecture

**Main Components:**
- `neuron_automation.py` - Core automation script with `NeuronNewsletterAutomation` class
- `config.py` - Configuration management with different environment classes (Production, Development, Test)
- `install.sh` - Complete system installation script
- `test_installation.sh` - Comprehensive testing and validation script

**System Integration:**
- Uses systemd service and timer for automatic weekday execution
- Creates virtual environment in `~/.config/neuron-automation/`
- Installs system command wrapper at `/usr/local/bin/neuron-automation`
- Chrome profile isolation in dedicated directory

## Development Commands

**Installation and Setup:**
```bash
chmod +x install.sh
./install.sh
```

**Testing:**
```bash
chmod +x test_installation.sh
./test_installation.sh
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

The system uses a class-based configuration system with three environments:
- `ProductionConfig` - Default weekday-only execution
- `DevelopmentConfig` - Daily execution with verbose logging
- `TestConfig` - Minimal retries for testing

Active configuration is controlled by `ACTIVE_CONFIG` variable in `config.py`.

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