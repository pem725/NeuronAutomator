#!/bin/bash
# Neuron Automation Update Script Wrapper
# ========================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
UPDATE_SCRIPT="$SCRIPT_DIR/update.py"

echo "🔄 Neuron Automation Update Utility"
echo "===================================="

# Check if Python script exists
if [[ ! -f "$UPDATE_SCRIPT" ]]; then
    echo "❌ Update script not found: $UPDATE_SCRIPT"
    exit 1
fi

# Check Python availability
if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD="python3"
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD="python"
else
    echo "❌ Python not found. Please install Python 3.6+ to use the updater."
    exit 1
fi

# Run the update script with all arguments
"$PYTHON_CMD" "$UPDATE_SCRIPT" "$@"