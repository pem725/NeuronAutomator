# Manual Commands Reference

Complete command-line reference for Neuron Daily Newsletter Automation. All commands use the `neuron-automation` executable.

## 🎮 Basic Commands

### Core Operations

```bash
# Run automation manually (bypass schedule)
neuron-automation

# Show version information
neuron-automation --version

# Display help and available commands
neuron-automation --help

# Update to latest version from GitHub
neuron-automation --update

# Check for available updates
neuron-automation --check-updates
```

### System Information

```bash
# Show comprehensive statistics
neuron-automation --stats

# System health check
neuron-automation --health-check

# Test browser configuration
neuron-automation --test-browser

# Test network connectivity
neuron-automation --test-connection
```

## 📊 Statistics Commands

### Reading Analytics

```bash
# Full statistics report
neuron-automation --stats

# Database statistics only
neuron-automation --db-stats

# Export all data to CSV
neuron-automation --export-csv filename.csv

# Export all data to JSON  
neuron-automation --export-links filename.json

# Show recent activity summary
neuron-automation --recent-activity
```

**Sample Statistics Output:**
```
📊 Neuron Automation Statistics
════════════════════════════════════════

🔗 Link Management:
   Total links processed: 1,247
   Currently blacklisted: 892 (71.5%)
   Available for reading: 355 (28.5%)
   
📅 Recent Activity (7 days):
   Newsletter runs: 28
   New links found: 156
   Links opened: 89
   Blacklist efficiency: 57.1%

🌐 Top Domains:
   youtu.be: 45 links
   www.reddit.com: 38 links
   techcrunch.com: 32 links
   github.com: 28 links
   medium.com: 24 links
```

## 🚫 Blacklist Management

### View Blacklisted Content

```bash
# Show all blacklisted URLs
neuron-automation --list-blacklisted

# Show recently blacklisted (default: 7 days)
neuron-automation --recent-blacklisted

# Show recently blacklisted with custom days
neuron-automation --recent-blacklisted 14

# Show blacklisted from specific domain
neuron-automation --list-blacklisted | grep "domain.com"
```

### Manual Blacklist Control

```bash
# Blacklist a specific URL
neuron-automation --blacklist "https://example.com/article"

# Remove URL from blacklist
neuron-automation --unblacklist "https://example.com/article"

# Reset entire blacklist (dangerous!)
neuron-automation --reset-blacklist --confirm

# Backup current blacklist
neuron-automation --backup-blacklist
```

### Blacklist Analytics

```bash
# Show blacklist efficiency metrics
neuron-automation --stats | grep -A5 "Blacklist"

# Count blacklisted by domain
neuron-automation --list-blacklisted | cut -d'/' -f3 | sort | uniq -c | sort -nr

# Show blacklist growth over time
neuron-automation --blacklist-history
```

## ⏪ Time Rewind Commands

### Preview Operations (Safe)

```bash
# Preview 7-day rewind (no changes made)
neuron-automation --rewind-preview 7

# Preview 3-day rewind with details
neuron-automation --rewind-preview 3 --verbose

# Preview with specific cutoff date
neuron-automation --rewind-preview-date "2025-01-15"
```

### Rewind Operations

```bash
# Restore links from last 3 days
neuron-automation --rewind 3

# Restore links from last week
neuron-automation --rewind 7

# Restore with backup creation
neuron-automation --rewind 5 --backup

# Restore without automatic backup
neuron-automation --rewind 5 --no-backup

# Restore to specific date
neuron-automation --rewind-to-date "2025-01-10"
```

### Rewind Management

```bash
# Create blacklist backup before rewind
neuron-automation --backup-blacklist

# Show recent blacklisted items
neuron-automation --recent-blacklisted 20

# View rewind history
neuron-automation --rewind-history

# Undo last rewind operation
neuron-automation --undo-rewind
```

## 🛠️ Advanced Operations

### Custom Automation Runs

```bash
# Force run even if no new content detected
neuron-automation --force

# Run with custom link limit
neuron-automation --max-links 25

# Run in test mode (no browser opening)
neuron-automation --dry-run

# Run with detailed output
neuron-automation --verbose

# Run in headless mode (background)
neuron-automation --headless

# Run with specific browser profile
neuron-automation --profile "Profile 2"
```

### Database Operations

```bash
# Database integrity check
neuron-automation --check-db

# Repair database if corrupted
neuron-automation --repair-db

# Compact database (reclaim space)
neuron-automation --vacuum-db

# Backup database
neuron-automation --backup-db

# Restore database from backup
neuron-automation --restore-db backup_file.db

# Show database file location
neuron-automation --show-db-path
```

### Configuration Management

```bash
# Show current configuration
neuron-automation --show-config

# Test configuration validity
neuron-automation --test-config

# Reset to default configuration
neuron-automation --reset-config --confirm

# Show configuration file location
neuron-automation --config-path
```

## 🔧 Debugging & Troubleshooting

### Debug Mode

```bash
# Run with maximum debugging output
neuron-automation --debug

# Debug specific component
neuron-automation --debug-browser
neuron-automation --debug-database  
neuron-automation --debug-network

# Save debug output to file
neuron-automation --debug > debug_output.txt 2>&1
```

### Log Management

```bash
# Show recent log entries
neuron-automation --show-logs

# Show specific number of log lines
neuron-automation --show-logs --lines 50

# Follow live logs
neuron-automation --follow-logs

# Clear old logs
neuron-automation --clear-logs --older-than 30

# Show log file location
neuron-automation --log-path
```

### System Testing

```bash
# Comprehensive system test
neuron-automation --system-test

# Test browser functionality
neuron-automation --test-browser --verbose

# Test network connectivity
neuron-automation --test-connection

# Test newsletter parsing
neuron-automation --test-parsing

# Test database operations
neuron-automation --test-db
```

## 🚀 Performance & Optimization

### Performance Commands

```bash
# Performance profile of last run
neuron-automation --profile-performance

# Optimize database performance
neuron-automation --optimize-db

# Show cache statistics
neuron-automation --cache-stats

# Clear cache
neuron-automation --clear-cache

# Benchmark system performance
neuron-automation --benchmark
```

### Resource Management

```bash
# Show memory usage
neuron-automation --memory-stats

# Show disk usage
neuron-automation --disk-usage

# Clean temporary files
neuron-automation --clean-temp

# Show resource limits
neuron-automation --show-limits
```

## 🔄 Integration Commands

### System Integration

```bash
# Install system service (Linux/macOS)
neuron-automation --install-service

# Uninstall system service
neuron-automation --uninstall-service

# Check service status
neuron-automation --service-status

# Update system integration
neuron-automation --update-service
```

### Import/Export

```bash
# Export configuration
neuron-automation --export-config config.json

# Import configuration
neuron-automation --import-config config.json

# Export reading history
neuron-automation --export-history history.csv

# Import blacklist from file
neuron-automation --import-blacklist blacklist.txt
```

## 📋 Command Combinations

### Daily Workflow Examples

```bash
# Morning routine
neuron-automation --stats && neuron-automation --health-check && neuron-automation

# Weekly maintenance  
neuron-automation --backup-db && neuron-automation --vacuum-db && neuron-automation --clear-logs --older-than 7

# Problem investigation
neuron-automation --debug --test-browser --test-connection
```

### Batch Operations

```bash
# Backup everything
neuron-automation --backup-db && neuron-automation --backup-blacklist && neuron-automation --export-config backup_config.json

# Full system reset (emergency)
neuron-automation --reset-blacklist --confirm && neuron-automation --clear-cache && neuron-automation --reset-config --confirm
```

## 📖 Command Reference Quick Cards

### Essential Daily Commands
```bash
neuron-automation              # Run automation
neuron-automation --stats      # Check status  
neuron-automation --rewind 3   # Restore 3 days
```

### Weekly Maintenance
```bash
neuron-automation --backup-db       # Backup database
neuron-automation --vacuum-db       # Optimize storage
neuron-automation --clear-logs --older-than 7  # Clean logs
```

### Troubleshooting
```bash
neuron-automation --health-check    # System health
neuron-automation --test-browser    # Browser test
neuron-automation --debug          # Debug mode
```

### Advanced Features
```bash
neuron-automation --dry-run         # Test run
neuron-automation --force           # Force execution
neuron-automation --export-csv data.csv  # Export data
```

---

## Command Exit Codes

| Exit Code | Meaning | Action |
|-----------|---------|---------|
| 0 | Success | Continue normally |
| 1 | General error | Check error message |
| 2 | Invalid arguments | Check command syntax |
| 3 | Browser error | Test browser setup |
| 4 | Network error | Check connectivity |
| 5 | Database error | Check database integrity |

---

## Next Steps

<div class="grid cards" markdown>

-   **Daily Operation**
    
    Master the automatic daily workflow and reading optimization.
    
    [:octicons-arrow-right-24: Daily Workflow](daily-operation.md)

-   **System Management**
    
    Monitor, maintain, and troubleshoot your automation system.
    
    [:octicons-arrow-right-24: System Management](system-management.md)

-   **Configuration Guide**
    
    Customize system behavior and advanced settings.
    
    [:octicons-arrow-right-24: Configuration](../configuration/basic-config.md)

</div>