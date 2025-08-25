# CLI Reference

Complete command-line interface reference for Neuron Daily Newsletter Automation. Every command, option, and flag explained with examples.

## 📋 Command Overview

The `neuron-automation` command provides access to all system functionality:

```bash
neuron-automation [OPTIONS] [COMMAND]
```

## 🚀 Basic Commands

### Core Operations

```bash
# Run automation (primary function)
neuron-automation

# Show version information
neuron-automation --version

# Display comprehensive help
neuron-automation --help

# System health check
neuron-automation --health-check
```

**Examples:**
```bash
$ neuron-automation --version
neuron-automation 1.5.0

$ neuron-automation --help
Neuron Daily Newsletter Automation

Usage: neuron-automation [OPTIONS]

Options:
  --version         Show version information
  --help           Show this help message
  --stats          Display reading statistics
  --health-check   Run system health check
  ...
```

## 📊 Information Commands

### Statistics & Status

```bash
# Complete reading statistics
neuron-automation --stats

# Database-specific statistics  
neuron-automation --db-stats

# Recent activity summary
neuron-automation --recent-activity

# System status overview
neuron-automation --status
```

**Sample Output:**
```bash
$ neuron-automation --stats
📊 Reading Statistics
==================================================
Total links encountered: 1,247
Blacklisted links: 892 (71.5%)
Active links: 355 (28.5%)
Automation runs: 156
Reading efficiency: 62.3%

🌐 Top Domains:
  youtu.be: 45 links
  reddit.com: 38 links
  techcrunch.com: 32 links

📈 Recent Activity (7 days):
  2025-08-25: 12 new, 8 opened
  2025-08-24: 15 new, 11 opened
  2025-08-23: 9 new, 6 opened
```

### Configuration Information

```bash
# Show effective configuration
neuron-automation --show-config

# Show configuration file location
neuron-automation --config-path

# Show database file location
neuron-automation --show-db-path

# Show log file location
neuron-automation --log-path
```

## 🔄 Link Management Commands

### Time Rewind Operations

```bash
# Preview rewind operation (safe)
neuron-automation --rewind-preview DAYS

# Perform rewind operation
neuron-automation --rewind DAYS

# Rewind with automatic backup
neuron-automation --rewind DAYS --backup

# Rewind without backup (dangerous)
neuron-automation --rewind DAYS --no-backup
```

**Examples:**
```bash
# See what 7-day rewind would do
$ neuron-automation --rewind-preview 7
🔍 Preview: Rewind 7 days
==========================
Cutoff date: 2025-08-18
Links to restore: 89
Restoration breakdown:
  • manual: 45 links
  • automatic: 44 links

# Actually perform the rewind
$ neuron-automation --rewind 7
⏪ Performing Rewind: 7 days
===========================
✅ Rewind complete!
   • Restored 89 links
   • Backup saved: backup_2025-08-25.db
```

### Blacklist Management

```bash
# Show recently blacklisted links
neuron-automation --recent-blacklisted [DAYS]

# Show all blacklisted links  
neuron-automation --list-blacklisted

# Manually blacklist a URL
neuron-automation --blacklist "https://example.com/article"

# Remove URL from blacklist
neuron-automation --unblacklist "https://example.com/article"

# Create blacklist backup
neuron-automation --backup-blacklist
```

**Examples:**
```bash
# Show last 10 days of blacklisted content
$ neuron-automation --recent-blacklisted 10
🕒 Recently Blacklisted Links (last 10 days)
============================================
📅 1 days ago (2025-08-24)
   🔗 https://example.com/article-1
   📂 Domain: example.com
   💭 Reason: automatic

# Manually blacklist a problematic link
$ neuron-automation --blacklist "https://spam-site.com/article"
✅ Blacklisted: https://spam-site.com/article
```

## 🛠️ System Management Commands

### Testing & Diagnostics

```bash
# Comprehensive system test
neuron-automation --system-test

# Test browser configuration
neuron-automation --test-browser

# Test network connectivity
neuron-automation --test-connection

# Test database operations
neuron-automation --test-db

# Validate configuration
neuron-automation --test-config
```

**Example Output:**
```bash
$ neuron-automation --system-test
🧪 System Test Results
======================
✅ Browser Configuration: OK
✅ Network Connectivity: OK  
✅ Database Operations: OK
✅ Configuration Valid: OK
✅ Service Integration: OK

System Status: All tests passed!
```

### Database Operations

```bash
# Check database integrity
neuron-automation --check-db

# Repair database (if corrupted)
neuron-automation --repair-db

# Optimize database performance
neuron-automation --vacuum-db

# Create database backup
neuron-automation --backup-db

# Restore from backup
neuron-automation --restore-db BACKUP_FILE
```

### Service Management

```bash
# Install system service
neuron-automation --install-service

# Uninstall system service
neuron-automation --uninstall-service

# Check service status
neuron-automation --service-status

# Start/stop/restart service
neuron-automation --start-service
neuron-automation --stop-service
neuron-automation --restart-service
```

## 🎛️ Execution Control Commands

### Automation Behavior

```bash
# Force run (ignore change detection)
neuron-automation --force

# Dry run (preview without action)
neuron-automation --dry-run

# Run with link limit
neuron-automation --max-links NUMBER

# Run in headless mode
neuron-automation --headless

# Run with verbose output
neuron-automation --verbose
```

**Examples:**
```bash
# Preview what would happen without actually running
$ neuron-automation --dry-run
🔍 Dry Run Mode - No changes will be made
=========================================
✓ Would open 12 new article links
✓ Would blacklist 8 previously seen links
✓ Browser would remain open for reading

# Force run even if no new content detected
$ neuron-automation --force --verbose
🔄 Force mode enabled - bypassing change detection
Loading newsletter content...
Found 15 potential article links...
Opening tabs in browser...
✅ Force automation completed successfully
```

### Performance Options

```bash
# Run with custom timeouts
neuron-automation --timeout SECONDS

# Run with retry limits
neuron-automation --max-retries NUMBER

# Run with specific browser profile
neuron-automation --profile PROFILE_NAME

# Run with custom user agent
neuron-automation --user-agent "Custom Agent String"
```

## 📤 Export & Import Commands

### Data Export

```bash
# Export all data to CSV
neuron-automation --export-csv FILENAME

# Export all data to JSON
neuron-automation --export-links FILENAME

# Export configuration
neuron-automation --export-config FILENAME

# Export reading history
neuron-automation --export-history FILENAME
```

**Examples:**
```bash
# Export all link data to CSV for analysis
$ neuron-automation --export-csv my_links.csv
✅ Links exported to: my_links.csv
   Total records: 1,247
   File size: 2.3 MB

# Export configuration for backup
$ neuron-automation --export-config config_backup.json  
✅ Configuration exported to: config_backup.json
```

### Data Import

```bash
# Import configuration
neuron-automation --import-config FILENAME

# Import blacklist from file
neuron-automation --import-blacklist FILENAME

# Import reading history
neuron-automation --import-history FILENAME
```

## 🧹 Maintenance Commands

### Cleanup Operations

```bash
# Clean old log files
neuron-automation --clear-logs --older-than DAYS

# Clean temporary files
neuron-automation --clean-temp

# Clean browser cache/data
neuron-automation --clear-browser-data

# Database cleanup
neuron-automation --cleanup --older-than DAYS
```

### Reset Operations

```bash
# Reset configuration to defaults
neuron-automation --reset-config --confirm

# Reset blacklist (clear all)
neuron-automation --reset-blacklist --confirm

# Emergency system reset
neuron-automation --emergency-reset --confirm
```

**Safety Note:** Reset operations require `--confirm` flag to prevent accidental data loss.

## 🔄 Update Commands

```bash
# Check for available updates
neuron-automation --check-updates

# Update to latest version
neuron-automation --update

# Update system integration
neuron-automation --update-service

# Update from specific source
neuron-automation --update --source github
```

**Example:**
```bash
$ neuron-automation --check-updates
Current version: 1.5.0
Latest version: 1.5.1
Update available! Run --update to install.

$ neuron-automation --update
📥 Downloading latest version...
✅ Update completed successfully!
New version: 1.5.1
🔄 Please restart any running services.
```

## 🐛 Debug & Logging Commands

### Debug Options

```bash
# Enable debug mode
neuron-automation --debug

# Component-specific debugging
neuron-automation --debug-browser
neuron-automation --debug-database
neuron-automation --debug-network

# Save debug output to file
neuron-automation --debug > debug.log 2>&1
```

### Log Management

```bash
# Show recent log entries
neuron-automation --show-logs [--lines NUMBER]

# Follow live logs
neuron-automation --follow-logs

# Clear old logs
neuron-automation --clear-logs --older-than DAYS

# Set log level
neuron-automation --log-level DEBUG|INFO|WARNING|ERROR
```

## 🔧 Advanced Options

### Browser Control

```bash
# Specific browser executable
neuron-automation --chrome-path "/path/to/chrome"

# Custom browser profile
neuron-automation --profile-path "/path/to/profile"

# Additional Chrome options
neuron-automation --chrome-options "--option1 --option2"

# Window size
neuron-automation --window-size WIDTHxHEIGHT
```

### Network Options

```bash
# Custom timeout
neuron-automation --timeout 45

# Proxy settings
neuron-automation --proxy "http://proxy:8080"

# Custom user agent
neuron-automation --user-agent "Custom Agent"

# Request headers
neuron-automation --headers "Header: Value"
```

## 🔗 Command Chaining & Scripting

### Common Command Combinations

```bash
# Daily maintenance routine
neuron-automation --stats && \
neuron-automation --health-check && \
neuron-automation

# Weekly maintenance
neuron-automation --backup-db && \
neuron-automation --vacuum-db && \
neuron-automation --clear-logs --older-than 7

# Troubleshooting sequence
neuron-automation --test-browser && \
neuron-automation --test-connection && \
neuron-automation --debug --dry-run
```

### Script Integration

```bash
#!/bin/bash
# automation-wrapper.sh

# Check if automation should run
if neuron-automation --dry-run | grep -q "new content"; then
    echo "🔄 Running automation - new content detected"
    neuron-automation --verbose
    
    # Log results
    neuron-automation --stats | head -10 >> daily_log.txt
else
    echo "⏭️ Skipping automation - no new content"
fi
```

## 📋 Exit Codes

Commands return standard exit codes for scripting:

| Exit Code | Meaning | Action |
|-----------|---------|---------|
| `0` | Success | Continue normally |
| `1` | General error | Check error message and logs |
| `2` | Invalid arguments | Verify command syntax |
| `3` | Browser error | Test browser configuration |
| `4` | Network error | Check internet connectivity |
| `5` | Database error | Run database integrity check |
| `6` | Configuration error | Validate configuration |
| `7` | Service error | Check system service status |

**Example Script Usage:**
```bash
#!/bin/bash
neuron-automation --health-check
case $? in
    0) echo "✅ System healthy" ;;
    3) echo "❌ Browser issue - check Chrome installation" ;;
    4) echo "❌ Network issue - check internet connection" ;;
    *) echo "❌ Unknown error - check logs" ;;
esac
```

## 📖 Quick Reference Cards

### Daily Commands
```bash
neuron-automation                    # Run automation
neuron-automation --stats            # Check status
neuron-automation --health-check     # System health
```

### Weekly Maintenance
```bash
neuron-automation --backup-db        # Backup database
neuron-automation --vacuum-db        # Optimize performance
neuron-automation --clear-logs --older-than 7  # Clean logs
```

### Troubleshooting
```bash
neuron-automation --test-browser     # Test browser
neuron-automation --test-connection  # Test network
neuron-automation --debug           # Debug mode
```

### Time Management
```bash
neuron-automation --rewind-preview 7    # Preview rewind
neuron-automation --rewind 3           # Restore 3 days
neuron-automation --recent-blacklisted 10  # Recent items
```

---

## Next Steps

<div class="grid cards" markdown>

-   **Configuration Reference**
    
    Detailed configuration options and settings.
    
    [:octicons-arrow-right-24: Config Reference](config-reference.md)

-   **Usage Guide**
    
    Learn effective usage patterns and workflows.
    
    [:octicons-arrow-right-24: Usage Guide](../usage/index.md)

-   **System Management**
    
    Advanced system monitoring and maintenance.
    
    [:octicons-arrow-right-24: System Management](../usage/system-management.md)

</div>