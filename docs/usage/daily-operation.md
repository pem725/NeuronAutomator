# Daily Operation

Master the automatic daily workflow and optimize your reading routine with Neuron Daily Newsletter Automation.

## 🌅 Automatic Morning Workflow

### Schedule Overview

The system runs automatically at these times on weekdays:

```mermaid
timeline
    title Weekday Automation Schedule
    5:30 AM : Newsletter Check
            : Content Detection
            : Tab Opening
    6:00 AM : Change Detection  
            : New Content Opening
    6:30 AM : Final Check
            : Update Opening
    7:00 AM : Last Opportunity
            : Catch-up Opening
```

### What Happens Automatically

1. **Smart Content Detection**
   - Checks if newsletter content has changed since last run
   - Avoids duplicate tab opening
   - Respects your reading patterns

2. **Intelligent Link Extraction**
   - Finds relevant article links from the newsletter
   - Filters out navigation and promotional links
   - Prioritizes high-quality content

3. **Blacklist Management**
   - Skips previously opened/read links automatically
   - Prevents content duplication
   - Tracks your reading history

4. **Browser Integration**
   - Opens Chrome with article tabs
   - Preserves browser session for reading
   - Maintains tab organization

5. **Database Updates**
   - Records successfully opened links
   - Updates reading statistics
   - Maintains automation history

## ⏰ Morning Routine Optimization

### Early Bird Schedule (6:00 AM)

**Perfect for:** Commuters, early gym-goers, coffee shop readers

```bash
# Check if automation ran successfully
neuron-automation --stats | head -5

# Quick health check
neuron-automation --health-check
```

**Workflow:**
1. ☕ **Wake up** → Newsletter tabs already waiting
2. 📖 **Scan headlines** while having coffee
3. 🎯 **Read key articles** during commute
4. ❌ **Close finished tabs** throughout the day

### Standard Schedule (7:00 AM)

**Perfect for:** Traditional office schedules, work-from-home

```bash
# Review what's available
neuron-automation --stats

# Manual run if needed
neuron-automation --force
```

**Workflow:**
1. 🖥️ **Check device** → Newsletter tabs ready for browsing
2. 📰 **Browse content** that interests you
3. 📌 **Keep important tabs** open for deeper reading
4. 🔄 **System tracks** accessed content automatically

### Flexible Schedule (8:00 AM+)

**Perfect for:** Variable schedules, late risers, weekend readers

```bash
# See what you missed
neuron-automation --recent-blacklisted 10

# Restore recent content
neuron-automation --rewind 1

# Get fresh content
neuron-automation
```

**Workflow:**
1. 🔍 **Open browser** → Previous tabs still available
2. 📚 **Catch up** on morning's articles
3. ⏪ **Use time rewind** for older content if needed
4. 📈 **System adapts** to your preferred timing

## 📊 Daily Monitoring

### Quick Status Check

```bash
# Essential daily command
neuron-automation --stats
```

**Key metrics to watch:**

| Metric | Daily Target | Action if Outside Range |
|--------|--------------|------------------------|
| New links found | 5-15 | Check newsletter availability |
| Links opened | 3-10 | Adjust reading habits or rewind |
| Blacklist efficiency | 60-80% | Consider rewind or reset |
| Automation success | 100% | Check system health |

### Health Monitoring

```bash
# Daily system check
neuron-automation --health-check

# Browser test if issues
neuron-automation --test-browser

# Database integrity
neuron-automation --db-stats
```

## 🎯 Reading Patterns & Optimization

### Identifying Your Pattern

Track your reading behavior for 1-2 weeks:

```bash
# Week 1: Observe
neuron-automation --stats > weekly_stats_1.txt

# Week 2: Compare  
neuron-automation --stats > weekly_stats_2.txt

# Compare patterns
diff weekly_stats_1.txt weekly_stats_2.txt
```

### Common Patterns

=== "Speed Reader"

    **Characteristics:** Quick scanning, high volume consumption
    
    ```bash
    # Optimize for volume
    neuron-automation --max-links 25
    ```
    
    **Tips:**
    - Use larger link limits
    - Enable quick blacklisting
    - Regular rewind for second passes

=== "Deep Reader"

    **Characteristics:** Thorough reading, quality over quantity
    
    ```bash
    # Optimize for quality
    neuron-automation --max-links 10
    ```
    
    **Tips:**
    - Use smaller link limits
    - Longer reading sessions
    - Less frequent rewinds

=== "Time-Shift Reader"

    **Characteristics:** Irregular schedule, batch reading
    
    ```bash
    # Weekly batch restoration
    neuron-automation --rewind 7
    ```
    
    **Tips:**
    - Use weekend catch-up sessions
    - Aggressive time rewind usage
    - Export for mobile reading

## 🔄 Daily Maintenance Tasks

### Morning (2 minutes)

```bash
# Quick status and health check
neuron-automation --stats | grep -E "(Total|New|Blacklisted)"
neuron-automation --health-check --quiet
```

### Evening (1 minute)

```bash
# Review daily activity
neuron-automation --stats | tail -5

# Close finished tabs (manual)
# System automatically tracks closure
```

### Weekly (5 minutes)

```bash
# Database cleanup
neuron-automation --cleanup --older-than 30

# Export data backup
neuron-automation --export-csv weekly_backup.csv

# Review patterns
neuron-automation --stats
```

## 🚨 Daily Troubleshooting

### No New Content

```bash
# Force check bypass cache
neuron-automation --force --verbose

# Test newsletter connection
neuron-automation --test-connection

# Check automation history
neuron-automation --stats | grep "runs"
```

### Too Many/Few Links

```bash
# Adjust limits temporarily
neuron-automation --max-links 15

# Check blacklist efficiency
neuron-automation --stats | grep efficiency

# Consider rewind if too few
neuron-automation --rewind 2
```

### Browser Issues

```bash
# Test browser startup
neuron-automation --test-browser

# Check Chrome version
google-chrome --version

# Try headless mode test
neuron-automation --headless --dry-run
```

## 📱 Multi-Device Integration

### Reading Continuation

1. **Desktop Start** → Automation opens tabs
2. **Mobile Continuation** → Chrome sync carries links
3. **Tablet Reading** → Access same content anywhere
4. **Desktop Completion** → Close tabs when finished

### Remote Management

```bash
# SSH status check from mobile/work
ssh home-computer "neuron-automation --stats"

# Remote automation trigger
ssh home-computer "neuron-automation --force"
```

---

## Next Steps

Ready to dive deeper into manual controls and system management?

<div class="grid cards" markdown>

-   **Manual Commands**
    
    Complete reference for all available commands and advanced options.
    
    [:octicons-arrow-right-24: Command Reference](manual-commands.md)

-   **System Management**
    
    Monitor, maintain, and troubleshoot your automation system.
    
    [:octicons-arrow-right-24: System Management](system-management.md)

-   **Time Rewind Guide**
    
    Master advanced time rewind techniques for content optimization.
    
    [:octicons-arrow-right-24: Time Rewind Tool](../features/time-rewind.md)

</div>