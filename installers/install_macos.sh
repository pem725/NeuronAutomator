#!/bin/bash
set -e

# Neuron Newsletter Automation - macOS Installation Script
# ========================================================

SCRIPT_NAME="neuron-automation"
INSTALL_DIR="/usr/local/bin"
CONFIG_DIR="$HOME/Library/Application Support/neuron-automation"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"

echo "🍎 Installing Neuron Newsletter Automation for macOS..."

# Check if running as root
if [[ $EUID -eq 0 ]]; then
    echo "❌ Please run this script as a regular user (not root)"
    echo "   The script will ask for sudo privileges when needed"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for Homebrew and install if needed
if ! command_exists brew; then
    echo "🍺 Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    # Add Homebrew to PATH for current session
    eval "$(/opt/homebrew/bin/brew shellenv)" 2>/dev/null || eval "$(/usr/local/bin/brew shellenv)"
fi

# Update Homebrew
echo "📦 Updating Homebrew..."
brew update

# Install required packages
echo "📦 Installing system dependencies..."
brew install python3

# Install Google Chrome if not present
if ! command_exists google-chrome && ! [ -d "/Applications/Google Chrome.app" ]; then
    echo "🌐 Installing Google Chrome..."
    brew install --cask google-chrome
else
    echo "✅ Google Chrome already installed"
fi

# Create configuration directory
echo "📁 Creating configuration directory..."
mkdir -p "$CONFIG_DIR"
mkdir -p "$LAUNCHD_DIR"

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
VENV_DIR="$CONFIG_DIR/venv"

# Remove existing virtual environment if it exists
if [ -d "$VENV_DIR" ]; then
    echo "   Removing existing virtual environment..."
    rm -rf "$VENV_DIR"
fi

# Create fresh virtual environment
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install Python dependencies
echo "📦 Installing Python packages..."
pip install --upgrade pip
pip install selenium webdriver-manager requests beautifulsoup4

# Create requirements.txt for future reference
cat > "$CONFIG_DIR/requirements.txt" << EOF
selenium>=4.0.0
webdriver-manager>=3.8.0
requests>=2.28.0
beautifulsoup4>=4.11.0
EOF

# Create wrapper script
echo "📝 Creating wrapper script..."
sudo tee "$INSTALL_DIR/$SCRIPT_NAME" > /dev/null << EOF
#!/bin/bash
# Neuron Newsletter Automation Wrapper Script for macOS

# Activate virtual environment
source "$CONFIG_DIR/venv/bin/activate"

# Run the Python script
python3 "$CONFIG_DIR/neuron_automation.py" "\$@"
EOF

sudo chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# Copy the Python script to config directory
echo "📄 Installing main script..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cp "$SCRIPT_DIR/neuron_automation.py" "$CONFIG_DIR/"
cp "$SCRIPT_DIR/config.py" "$CONFIG_DIR/"
chmod +x "$CONFIG_DIR/neuron_automation.py"

# Create launchd plist file
echo "⏰ Creating launchd configuration..."
cat > "$LAUNCHD_DIR/com.neuron.automation.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.neuron.automation</string>
    <key>ProgramArguments</key>
    <array>
        <string>$INSTALL_DIR/$SCRIPT_NAME</string>
    </array>
    <key>StartCalendarInterval</key>
    <array>
        <dict>
            <key>Weekday</key>
            <integer>1</integer>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key>
            <integer>2</integer>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key>
            <integer>3</integer>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key>
            <integer>4</integer>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
        <dict>
            <key>Weekday</key>
            <integer>5</integer>
            <key>Hour</key>
            <integer>6</integer>
            <key>Minute</key>
            <integer>0</integer>
        </dict>
    </array>
    <key>StandardOutPath</key>
    <string>$CONFIG_DIR/launchd.log</string>
    <key>StandardErrorPath</key>
    <string>$CONFIG_DIR/launchd.log</string>
    <key>RunAtLoad</key>
    <false/>
</dict>
</plist>
EOF

# Load the launchd job
echo "🔄 Loading launchd job..."
launchctl load "$LAUNCHD_DIR/com.neuron.automation.plist"

# Create uninstall script
cat > "$CONFIG_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
# Uninstall Neuron Newsletter Automation for macOS

echo "🗑️ Uninstalling Neuron Newsletter Automation..."

# Unload launchd job
launchctl unload "$HOME/Library/LaunchAgents/com.neuron.automation.plist" 2>/dev/null || true

# Remove launchd plist
rm -f "$HOME/Library/LaunchAgents/com.neuron.automation.plist"

# Remove main script
sudo rm -f /usr/local/bin/neuron-automation

# Remove config directory (ask user)
read -p "Remove configuration directory with logs? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/Library/Application Support/neuron-automation"
    echo "✅ Configuration directory removed"
else
    echo "ℹ️ Configuration directory preserved at: $HOME/Library/Application Support/neuron-automation"
fi

echo "✅ Uninstallation complete"
EOF

chmod +x "$CONFIG_DIR/uninstall.sh"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "📋 Summary:"
echo "   • Command: $SCRIPT_NAME"
echo "   • Config: $CONFIG_DIR"
echo "   • Logs: $CONFIG_DIR/neuron_automation.log"
echo "   • LaunchAgent: com.neuron.automation"
echo ""
echo "🎮 Usage:"
echo "   • Manual run: $SCRIPT_NAME"
echo "   • Check schedule: launchctl list | grep neuron"
echo "   • View logs: tail -f '$CONFIG_DIR/neuron_automation.log'"
echo ""
echo "⏰ The automation will run automatically every weekday at 6:00 AM"
echo ""
echo "🗑️ To uninstall: $CONFIG_DIR/uninstall.sh"
echo ""
echo "🧪 Test the installation: $SCRIPT_NAME"

# Show launchd job status
echo ""
echo "📊 LaunchAgent status:"
launchctl list | grep neuron || echo "LaunchAgent registered but not currently running (will start at scheduled time)"