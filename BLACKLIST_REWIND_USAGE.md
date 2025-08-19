# Blacklist Time Rewind Tool 📅

The **Blacklist Time Rewind Tool** allows you to "go back in time" and restore previously blacklisted links, making them available for reading again. This is perfect for testing disruptions in learning material, re-introducing content for review, or recovering from over-blacklisting.

## 🎯 Use Cases

- **Testing Learning Disruptions**: Remove blacklisted links to simulate new content exposure
- **Content Review**: Re-introduce previously read articles for reinforcement  
- **Experimentation**: Test different content exposure patterns and timing
- **Recovery**: Undo accidental over-blacklisting of important content
- **Content Rotation**: Manage long-term content availability cycles

## 🚀 Quick Start

### Preview Before Acting
```bash
# See what a 7-day rewind would do (without making changes)
neuron-automation --rewind-preview 7

# Preview a 3-day rewind
neuron-automation --rewind-preview 3
```

### Perform Time Rewind
```bash
# Rewind blacklist by 5 days (restores links blacklisted in last 5 days)
neuron-automation --rewind 5

# Rewind 2 days without creating backup
neuron-automation --rewind 2 --no-backup
```

### Manage Blacklist History
```bash
# Show recently blacklisted links
neuron-automation --recent-blacklisted 10

# Create backup of current blacklist state
neuron-automation --backup-blacklist

# View current blacklist statistics
neuron-automation --stats
```

## 📋 Command Reference

### Main Commands

| Command | Description | Example |
|---------|-------------|---------|
| `--rewind-preview DAYS` | Preview rewind operation without changes | `--rewind-preview 7` |
| `--rewind DAYS` | Restore blacklisted links from last X days | `--rewind 5` |
| `--backup-blacklist` | Create backup of current blacklist state | `--backup-blacklist` |
| `--recent-blacklisted DAYS` | Show recently blacklisted links | `--recent-blacklisted 10` |

### Options

| Option | Description | Example |
|--------|-------------|---------|
| `--no-backup` | Skip automatic backup during rewind | `--rewind 3 --no-backup` |
| `--database PATH` | Specify database path (auto-detected) | `--database /path/to/links.db` |

## 🔧 Detailed Examples

### Example 1: Testing Content Re-exposure

**Scenario**: You want to test how re-introducing content from 5 days ago affects your learning.

```bash
# 1. Preview what would be restored
neuron-automation --rewind-preview 5

# Output:
# 🔍 Preview: Rewind 5 days
# Cutoff date: 2025-08-14
# Links to restore: 12
# 
# 📊 Restoration breakdown:
#   • read: 10 links
#   • not_interested: 2 links

# 2. Perform the rewind
neuron-automation --rewind 5

# Output:
# ⏪ Performing Rewind: 5 days
# This will restore 12 links to available status
# ✅ Rewind complete!
#    • Restored 12 links
#    • Cutoff date: 2025-08-14
#    • Backup saved: /path/to/backups/blacklist_backup_20250819_143022.json
```

### Example 2: Gradual Content Introduction

**Scenario**: Gradually re-introduce content starting with most recently blacklisted.

```bash
# Start with just 1 day
neuron-automation --rewind-preview 1
# Shows: 3 links from yesterday

neuron-automation --rewind 1
# Restores yesterday's content

# Next day, expand to 3 days  
neuron-automation --rewind-preview 3
# Shows: 8 links from last 3 days (including newly blacklisted)

neuron-automation --rewind 3
# Restores 3-day content
```

### Example 3: Content Analysis and Recovery

**Scenario**: Analyze blacklist patterns and recover accidentally blacklisted content.

```bash
# 1. View recent blacklist activity
neuron-automation --recent-blacklisted 14

# Output shows links with reasons and dates:
# 📅 2 days ago (2025-08-17)
#    🔗 https://techcrunch.com/important-ai-breakthrough
#    📂 Domain: techcrunch.com
#    💭 Reason: read
#
# 📅 5 days ago (2025-08-14) 
#    🔗 https://nature.com/critical-research-paper
#    📂 Domain: nature.com
#    💭 Reason: read

# 2. Create backup before making changes
neuron-automation --backup-blacklist

# 3. Restore important content from last week
neuron-automation --rewind 7
```

### Example 4: Experimental Learning Patterns

**Scenario**: Test different content exposure cycles for optimal learning.

```bash
# Week 1: Normal operation (links get blacklisted)
# ... content accumulates in blacklist

# Week 2: 3-day review cycle - rewind every 3 days
neuron-automation --rewind 3  # Monday
# ... automation runs, some content gets re-blacklisted
neuron-automation --rewind 3  # Thursday  
# ... cycle continues

# Week 3: 7-day review cycle - rewind weekly
neuron-automation --rewind 7  # Monday
# ... all week's content available again

# Analysis: Compare learning effectiveness between cycles
neuron-automation --stats
```

## ⚙️ How It Works

### Time-Based Restoration

The rewind tool works by:

1. **Calculating Cutoff Date**: `today - X days = cutoff_date`
2. **Finding Eligible Links**: Links blacklisted on or after the cutoff date
3. **Removing Blacklist Status**: Sets `is_blacklisted = FALSE` for eligible links
4. **Preserving History**: Keeps original blacklist dates in history for analysis

### Database Changes

**Before Rewind:**
```sql
-- Link blacklisted 3 days ago
is_blacklisted: TRUE
blacklisted_date: 2025-08-16
blacklist_reason: 'read'
```

**After 5-Day Rewind:**  
```sql
-- Link restored to available status
is_blacklisted: FALSE
blacklisted_date: NULL
blacklist_reason: NULL
```

### Safety Features

- **Automatic Backups**: Created before each rewind operation
- **Preview Mode**: See exactly what will be restored before committing
- **Selective Restoration**: Only affects links within specified timeframe  
- **Backup Recovery**: Restore previous blacklist state from backup files

## 📊 Integration with Automation

The rewind tool integrates seamlessly with the main newsletter automation:

### Morning Automation Flow
1. **6:30 AM**: Automation runs, analyzes newsletter links
2. **Link Analysis**: Restored links are now available again  
3. **Tab Opening**: Previously blacklisted content opens in new tabs
4. **New Blacklisting**: Content gets re-blacklisted after opening (if read)

### Rewind Timing Strategies

**Daily Review Pattern:**
```bash
# Every morning before automation
neuron-automation --rewind 1  # Yesterday's content
# Then normal automation runs
```

**Weekly Deep Review:**
```bash  
# Sunday evening
neuron-automation --rewind 7  # Last week's content
# Monday morning automation includes restored content
```

**Monthly Content Rotation:**
```bash
# First of month
neuron-automation --rewind 30  # Last month's content
```

## 🛠️ Standalone Tool

You can also use the rewind tool independently:

```bash
# Direct tool usage (more options)
python3 blacklist_rewind.py --preview 10
python3 blacklist_rewind.py --rewind 5 --yes  # Non-interactive
python3 blacklist_rewind.py --stats
python3 blacklist_rewind.py --restore backup_file.json
```

## 🎯 Best Practices

### 1. **Always Preview First**
```bash
# Good practice
neuron-automation --rewind-preview 7
neuron-automation --rewind 7

# Risky (no preview)  
neuron-automation --rewind 30  # Could restore too much
```

### 2. **Create Backups for Large Operations**
```bash
# For big rewinds, backup first
neuron-automation --backup-blacklist
neuron-automation --rewind 14
```

### 3. **Monitor Recent Activity**
```bash
# Regular monitoring
neuron-automation --recent-blacklisted 5
# Understand patterns before rewinding
```

### 4. **Gradual Introduction**
```bash
# Start small, expand gradually
neuron-automation --rewind 1  # Day 1
neuron-automation --rewind 3  # Day 3
neuron-automation --rewind 7  # Day 7
```

### 5. **Document Experiments**
```bash
# Keep notes on what works
echo "$(date): Tested 5-day rewind cycle" >> learning_experiments.log
neuron-automation --rewind 5
```

## 🔍 Troubleshooting

### Database Not Found
```bash
# Specify database path explicitly
neuron-automation --rewind 5 --database ~/.config/neuron-automation/newsletter_links.db
```

### No Links to Restore
```bash
# Check what's available first
neuron-automation --recent-blacklisted 14
neuron-automation --stats
```

### Backup Recovery
```bash
# If rewind went wrong, restore from backup
python3 blacklist_rewind.py --restore path/to/backup.json
```

## 📈 Monitoring & Analytics

### View Impact of Rewinds
```bash
# Before rewind
neuron-automation --stats
# Note: "Total blacklisted: 150"

neuron-automation --rewind 7

# After rewind  
neuron-automation --stats
# Note: "Total blacklisted: 120" (30 restored)
```

### Track Patterns
```bash
# Weekly pattern analysis
neuron-automation --recent-blacklisted 7 | grep "Domain:"
# See which domains get blacklisted most
```

This powerful time rewind feature gives you complete control over your content exposure timeline, enabling sophisticated learning pattern experimentation and content management strategies.