# Installation Overview

Get Neuron Daily Newsletter Automation running on your system in just a few minutes. We support multiple installation methods to fit your preferences and technical comfort level.

## Choose Your Installation Method

=== "pip Install (Recommended)"

    **Best for**: Most users, especially those familiar with Python

    - :material-check-circle: Simplest installation process
    - :material-check-circle: Automatic dependency management  
    - :material-check-circle: Easy updates via pip
    - :material-check-circle: Works on all platforms

    [Get Started with pip :octicons-arrow-right-24:](pip-install.md){ .md-button .md-button--primary }

=== "Manual Installation"

    **Best for**: Users who want full control or don't use Python package managers

    - :material-check-circle: Complete system integration
    - :material-check-circle: Platform-specific optimizations
    - :material-check-circle: Includes all dependencies
    - :material-check-circle: No Python knowledge required

    [Manual Setup Guide :octicons-arrow-right-24:](manual-setup.md){ .md-button .md-button--primary }

## System Requirements

Before installing, ensure your system meets these minimum requirements:

### Operating Systems

| Platform | Minimum Version | Recommended |
|----------|----------------|-------------|
| **Linux** | Ubuntu 18.04+ / Debian 10+ | Ubuntu 22.04+ |
| **macOS** | macOS 10.14+ (Mojave) | macOS 12+ (Monterey) |
| **Windows** | Windows 10 | Windows 11 |

### Software Dependencies

| Component | Minimum Version | Purpose |
|-----------|----------------|---------|
| **Python** | 3.6+ | Runtime environment |
| **Chrome** | Latest stable | Browser automation |
| **Internet** | Broadband | Newsletter fetching |

!!! note "Automatic Installation"
    Our installers will automatically install missing dependencies, including Python and Chrome if needed.

## Installation Time

| Method | Time Required | Technical Level |
|--------|--------------|-----------------|
| **pip install** | 2-3 minutes | Beginner |
| **Manual install** | 5-10 minutes | Beginner |

## What Gets Installed

The installation process sets up:

- :material-file-code: Core automation scripts
- :material-cog: Configuration files  
- :material-clock: Automatic scheduling (systemd/launchd/Task Scheduler)
- :material-folder: Virtual environment with dependencies
- :material-console: Command-line tools (`neuron-automation`, `blacklist-rewind`)
- :material-file-document: Log files and data directories

## Post-Installation

After installation, you can:

1. **Test the system**: `neuron-automation`
2. **Check version**: `neuron-automation --version`
3. **View statistics**: `neuron-automation --stats`
4. **Configure settings**: Edit `~/.config/neuron-automation/config.py`

## Need Help?

If you run into issues during installation:

- :material-wrench: Check our [Troubleshooting Guide](troubleshooting.md)
- :material-github: Report bugs on [GitHub Issues](https://github.com/pem725/NeuronAutomator/issues)
- :material-book: Read the [Configuration Guide](../configuration/) for customization options

---

Ready to get started? Choose your preferred installation method above!