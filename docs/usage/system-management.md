# System Management

Monitor, maintain, and troubleshoot your Neuron Daily Newsletter Automation system for optimal performance and reliability.

## 🔍 System Monitoring

### Health Check Dashboard

```bash
# Comprehensive system health check
neuron-automation --health-check

# Quick status overview
neuron-automation --stats | head -15
```

**Sample Health Check Output:**
```
🏥 System Health Check
════════════════════════════════════════

✅ Browser Configuration: OK
   - Chrome version: 120.0.6099.109
   - WebDriver: Compatible
   - Profile access: Available

✅ Database Status: OK
   - File size: 2.3 MB
   - Integrity: Verified
   - Recent writes: Successful

✅ Network Connectivity: OK
   - Newsletter site: Reachable
   - Response time: 245ms
   - SSL certificate: Valid

✅ System Integration: OK
   - Service status: Active
   - Next run: Today 06:00 AM
   - Permissions: Correct

⚠️  Storage Space: 89% Used
   - Free space: 2.1 GB
   - Recommendation: Monitor usage
```

### Monitoring Automation Status

```bash
# Check if automation service is running
neuron-automation --service-status

# View recent automation runs
neuron-automation --stats | grep -A 10 "Recent Activity"

# Monitor live log output  
neuron-automation --follow-logs
```

### Performance Monitoring

```bash
# System performance profile
neuron-automation --profile-performance

# Resource usage statistics
neuron-automation --memory-stats
neuron-automation --disk-usage

# Database performance metrics
neuron-automation --db-stats | grep -E "(size|queries|response)"
```

## 🛠️ Maintenance Tasks

### Daily Maintenance (Automated)

The system handles these tasks automatically:

- **Content change detection** via newsletter checksums
- **Database optimization** with automatic cleanup
- **Log rotation** to prevent disk space issues
- **Error recovery** with automatic retry mechanisms

### Weekly Maintenance (5 minutes)

```bash
#!/bin/bash
# weekly-maintenance.sh

echo "🔧 Weekly Neuron Automation Maintenance"
echo "========================================"

# 1. Backup critical data
echo "💾 Creating backups..."
neuron-automation --backup-db
neuron-automation --backup-blacklist

# 2. Database optimization
echo "⚡ Optimizing database..."
neuron-automation --vacuum-db
neuron-automation --optimize-db

# 3. Clean old files
echo "🧹 Cleaning old files..."
neuron-automation --clear-logs --older-than 14
neuron-automation --clean-temp

# 4. Health verification
echo "🏥 System health check..."
neuron-automation --health-check

echo "✅ Weekly maintenance complete!"
```

### Monthly Maintenance (10 minutes)

```bash
#!/bin/bash
# monthly-maintenance.sh

# 1. Full system verification
neuron-automation --system-test

# 2. Database integrity check
neuron-automation --check-db --repair-if-needed

# 3. Update system components
neuron-automation --check-updates
neuron-automation --update-service

# 4. Archive old data
neuron-automation --export-history "monthly_backup_$(date +%Y-%m).csv"
neuron-automation --cleanup --older-than 90

# 5. Performance benchmark
neuron-automation --benchmark > "benchmark_$(date +%Y-%m).txt"
```

## 🗄️ Database Management

### Database Health

```bash
# Check database integrity
neuron-automation --check-db

# Repair database if issues found
neuron-automation --repair-db

# Optimize database performance
neuron-automation --vacuum-db
neuron-automation --optimize-db

# Show database statistics
neuron-automation --db-stats
```

**Database Health Indicators:**

| Metric | Good Range | Action if Outside |
|--------|------------|-------------------|
| File Size | < 50 MB | Archive old data |
| Query Response | < 50ms | Optimize/vacuum |
| Integrity Errors | 0 | Repair immediately |
| Growth Rate | < 1 MB/week | Check for issues |

### Database Backup & Recovery

```bash
# Create database backup
neuron-automation --backup-db

# Restore from backup (emergency)
neuron-automation --restore-db backup_file.db

# Export data for external analysis
neuron-automation --export-csv full_data.csv

# Show backup history
ls -la ~/.config/neuron-automation/backups/
```

### Database Analysis

```bash
# Detailed database analysis
sqlite3 ~/.config/neuron-automation/newsletter_links.db << EOF
.headers on
.mode column

-- Table sizes
SELECT name, COUNT(*) as rows FROM sqlite_master 
  LEFT JOIN (SELECT 'links' as name, COUNT(*) as cnt FROM links 
            UNION SELECT 'newsletter_runs', COUNT(*) FROM newsletter_runs) 
  ON sqlite_master.name = name WHERE type='table';

-- Recent activity
SELECT DATE(run_date) as date, COUNT(*) as runs, 
       SUM(opened_links) as total_opened
FROM newsletter_runs 
WHERE run_date >= DATE('now', '-30 days')
GROUP BY DATE(run_date)
ORDER BY date DESC
LIMIT 10;
EOF
```

## 🔧 System Troubleshooting

### Common Issues & Solutions

#### Issue: Automation Not Running

```bash
# 1. Check service status
neuron-automation --service-status

# 2. Verify schedule configuration
crontab -l | grep neuron
# or (macOS)
launchctl list | grep neuron

# 3. Test manual execution
neuron-automation --force --verbose

# 4. Check permissions
ls -la ~/.config/neuron-automation/
```

#### Issue: Browser Not Opening

```bash
# 1. Test browser configuration
neuron-automation --test-browser

# 2. Check Chrome installation
which google-chrome
google-chrome --version

# 3. Test WebDriver
neuron-automation --debug-browser

# 4. Try headless mode
neuron-automation --headless --dry-run
```

#### Issue: Database Errors

```bash
# 1. Check database file
ls -la ~/.config/neuron-automation/newsletter_links.db

# 2. Verify integrity
neuron-automation --check-db

# 3. Attempt repair
neuron-automation --repair-db

# 4. Restore from backup if needed
neuron-automation --restore-db latest_backup.db
```

#### Issue: Network/Connection Problems

```bash
# 1. Test connectivity
neuron-automation --test-connection

# 2. Check DNS resolution
nslookup www.theneurondaily.com

# 3. Test HTTP access
curl -I https://www.theneurondaily.com/

# 4. Check firewall/proxy settings
neuron-automation --debug-network
```

### Advanced Troubleshooting

#### Debug Mode Analysis

```bash
# Full debug run with output capture
neuron-automation --debug --verbose > debug_full.log 2>&1

# Analyze common error patterns
grep -i error debug_full.log
grep -i failed debug_full.log  
grep -i timeout debug_full.log

# Component-specific debugging
neuron-automation --debug-browser > browser_debug.log 2>&1
neuron-automation --debug-database > db_debug.log 2>&1
```

#### Log Analysis

```bash
# View recent errors
neuron-automation --show-logs | grep -i error | tail -10

# Analyze automation patterns
grep "automation" ~/.config/neuron-automation/neuron_automation.log | tail -20

# Check browser startup issues
grep -E "(Chrome|WebDriver|selenium)" ~/.config/neuron-automation/neuron_automation.log
```

#### Performance Diagnostics

```bash
# System resource usage during automation
top -p $(pgrep -f neuron-automation) &
neuron-automation --force
kill %1

# Disk I/O monitoring
iotop -p $(pgrep -f neuron-automation) &
neuron-automation --force  
kill %1

# Network traffic analysis
netstat -i before && neuron-automation --force && netstat -i after
```

## 🔄 System Updates & Upgrades

### Update Management

```bash
# Check for updates
neuron-automation --check-updates

# Update to latest version
neuron-automation --update

# Update system integration components
neuron-automation --update-service

# Verify update success
neuron-automation --version
neuron-automation --health-check
```

### Version Control

```bash
# Show current version
neuron-automation --version

# Show version history
neuron-automation --version-history

# Rollback to previous version (if available)
neuron-automation --rollback-version

# Update from specific source
neuron-automation --update --source github
```

### Configuration Migration

```bash
# Before major updates, backup configuration
neuron-automation --export-config backup_config.json

# After update, verify configuration
neuron-automation --test-config

# Migrate settings if needed
neuron-automation --migrate-config --from-version 1.4.0
```

## 🔒 Security & Privacy

### Security Monitoring

```bash
# Check file permissions
ls -la ~/.config/neuron-automation/

# Verify no sensitive data in logs
grep -E "(password|token|key)" ~/.config/neuron-automation/neuron_automation.log

# Check browser security settings
neuron-automation --test-browser --security-check
```

### Privacy Maintenance

```bash
# Clear browsing data from automation profile
neuron-automation --clear-browser-data

# Anonymize exported data
neuron-automation --export-csv --anonymize data.csv

# Review data collection settings
neuron-automation --show-config | grep -E "(track|collect|send)"
```

### Access Control

```bash
# Set proper file permissions
chmod 700 ~/.config/neuron-automation/
chmod 600 ~/.config/neuron-automation/*.db
chmod 600 ~/.config/neuron-automation/*.log

# Review system access
ps aux | grep neuron-automation
lsof -c neuron-automation
```

## 📊 Reporting & Analytics

### System Reports

```bash
# Generate monthly system report
neuron-automation --generate-report --month 2025-01

# Performance summary report
neuron-automation --report-performance --days 30

# Usage analytics report  
neuron-automation --report-usage --detailed
```

### Custom Monitoring Scripts

```bash
#!/bin/bash
# custom-monitoring.sh

# Daily system health email
{
  echo "Subject: Neuron Automation Daily Report"
  echo ""
  neuron-automation --health-check
  echo ""
  neuron-automation --stats | head -20
} | sendmail admin@example.com

# Resource usage alert
if neuron-automation --disk-usage | grep -q "90%"; then
  echo "Warning: Disk usage high" | logger -t neuron-automation
fi
```

## 🚨 Emergency Procedures

### System Recovery

```bash
# Emergency system reset (last resort)
neuron-automation --emergency-reset --confirm

# Restore from last known good state
neuron-automation --restore-backup --latest

# Minimal restart procedure
sudo systemctl stop neuron-automation
neuron-automation --repair-db
neuron-automation --test-config
sudo systemctl start neuron-automation
```

### Data Recovery

```bash
# Recover from corrupted database
cp ~/.config/neuron-automation/newsletter_links.db corrupted_backup.db
neuron-automation --restore-db backup_file.db

# Rebuild database from logs
neuron-automation --rebuild-db --from-logs

# Extract data from backup
neuron-automation --extract-backup backup_file.db
```

---

## Monitoring Automation Script

Create a comprehensive monitoring script:

```bash
#!/bin/bash
# system-monitor.sh

LOG_FILE="$HOME/.config/neuron-automation/monitoring.log"

echo "$(date): Starting system monitoring check" >> "$LOG_FILE"

# Health check
if ! neuron-automation --health-check --quiet; then
    echo "$(date): Health check failed!" >> "$LOG_FILE"
    # Send alert (email, notification, etc.)
fi

# Disk space check
DISK_USAGE=$(neuron-automation --disk-usage | grep -o '[0-9]*%' | head -1)
if [[ "${DISK_USAGE%\%}" -gt 85 ]]; then
    echo "$(date): Disk usage warning: $DISK_USAGE" >> "$LOG_FILE"
fi

# Service status check
if ! neuron-automation --service-status --quiet; then
    echo "$(date): Service status issue detected" >> "$LOG_FILE"
fi

echo "$(date): Monitoring check completed" >> "$LOG_FILE"
```

---

## Next Steps

<div class="grid cards" markdown>

-   **Configuration Guide**
    
    Customize system behavior and advanced settings.
    
    [:octicons-arrow-right-24: Configuration](../configuration/basic-config.md)

-   **Troubleshooting**
    
    Detailed troubleshooting guides for common issues.
    
    [:octicons-arrow-right-24: Troubleshooting](../installation/troubleshooting.md)

-   **Daily Operation**
    
    Return to daily workflow optimization.
    
    [:octicons-arrow-right-24: Daily Workflow](daily-operation.md)

</div>