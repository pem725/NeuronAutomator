#!/bin/bash
set -e

# Neuron Newsletter Automation - Installation Script
# ================================================

SCRIPT_NAME="neuron-automation"
INSTALL_DIR="/usr/local/bin"
SERVICE_DIR="/etc/systemd/system"
CONFIG_DIR="$HOME/.config/neuron-automation"

echo "🚀 Installing Neuron Newsletter Automation..."

# Check if running as root for system files
if [[ $EUID -eq 0 ]]; then
    echo "❌ Please run this script as a regular user (not root)"
    echo "   The script will ask for sudo privileges when needed"
    exit 1
fi

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Update system packages
echo "📦 Updating system packages..."
sudo apt update

# Install required system packages
echo "📦 Installing system dependencies..."
sudo apt install -y python3 python3-pip python3-venv wget curl unzip

# Install Google Chrome if not present
if ! command_exists google-chrome; then
    echo "🌐 Installing Google Chrome..."
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
    sudo apt update
    sudo apt install -y google-chrome-stable
else
    echo "✅ Google Chrome already installed"
fi

# Create configuration directory
echo "📁 Creating configuration directory..."
mkdir -p "$CONFIG_DIR"

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
# Neuron Newsletter Automation Wrapper Script

# Activate virtual environment
source "$CONFIG_DIR/venv/bin/activate"

# Set display for GUI applications
export DISPLAY=:0.0

# Run the Python script
python3 "$CONFIG_DIR/neuron_automation.py" "\$@"
EOF

sudo chmod +x "$INSTALL_DIR/$SCRIPT_NAME"

# Copy the Python scripts to config directory
echo "📄 Installing main scripts..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Check that all required files exist
REQUIRED_FILES=("neuron_automation.py" "config.py" "link_manager.py")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$file" ]; then
        echo "❌ Error: Required file $file not found in $SCRIPT_DIR"
        echo "   Please ensure all files are present and try again"
        exit 1
    fi
done

cp "$SCRIPT_DIR/neuron_automation.py" "$CONFIG_DIR/"
cp "$SCRIPT_DIR/config.py" "$CONFIG_DIR/"
cp "$SCRIPT_DIR/link_manager.py" "$CONFIG_DIR/"
cp "$SCRIPT_DIR/blacklist_rewind.py" "$CONFIG_DIR/"
chmod +x "$CONFIG_DIR/neuron_automation.py"
echo "✅ All Python scripts installed successfully"

# Create systemd service file
echo "⚙️ Creating systemd service..."
sudo tee "$SERVICE_DIR/$SCRIPT_NAME.service" > /dev/null << EOF
[Unit]
Description=Neuron Daily Newsletter Automation
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=$USER
Environment=HOME=$HOME
Environment=DISPLAY=:0
ExecStart=$INSTALL_DIR/$SCRIPT_NAME
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# Create systemd timer for weekday mornings
echo "⏰ Creating systemd timer..."
sudo tee "$SERVICE_DIR/$SCRIPT_NAME.timer" > /dev/null << EOF
[Unit]
Description=Run Neuron Newsletter Automation on weekday mornings
Requires=$SCRIPT_NAME.service

[Timer]
# Run Monday through Friday multiple times for optimal newsletter coverage
OnCalendar=Mon,Tue,Wed,Thu,Fri *-*-* 05:30:00
OnCalendar=Mon,Tue,Wed,Thu,Fri *-*-* 06:00:00  
OnCalendar=Mon,Tue,Wed,Thu,Fri *-*-* 06:30:00
OnCalendar=Mon,Tue,Wed,Thu,Fri *-*-* 07:00:00
Persistent=true
RandomizedDelaySec=300

[Install]
WantedBy=timers.target
EOF

# Enable and start the timer
echo "🔄 Enabling systemd timer..."
sudo systemctl daemon-reload
sudo systemctl enable "$SCRIPT_NAME.timer"
sudo systemctl start "$SCRIPT_NAME.timer"

# Create desktop launcher (optional)
DESKTOP_FILE="$HOME/.local/share/applications/$SCRIPT_NAME.desktop"
mkdir -p "$(dirname "$DESKTOP_FILE")"
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Name=Neuron Newsletter
Comment=Open Neuron Daily Newsletter with all articles
Exec=$INSTALL_DIR/$SCRIPT_NAME
Icon=web-browser
Terminal=false
Type=Application
Categories=Network;News;
EOF

# Create uninstall script
cat > "$CONFIG_DIR/uninstall.sh" << 'EOF'
#!/bin/bash
# Uninstall Neuron Newsletter Automation

echo "🗑️ Uninstalling Neuron Newsletter Automation..."

# Stop and disable timer
sudo systemctl stop neuron-automation.timer 2>/dev/null || true
sudo systemctl disable neuron-automation.timer 2>/dev/null || true

# Remove systemd files
sudo rm -f /etc/systemd/system/neuron-automation.service
sudo rm -f /etc/systemd/system/neuron-automation.timer

# Reload systemd
sudo systemctl daemon-reload

# Remove main script
sudo rm -f /usr/local/bin/neuron-automation

# Remove desktop file
rm -f "$HOME/.local/share/applications/neuron-automation.desktop"

# Remove config directory (ask user)
read -p "Remove configuration directory with logs? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -rf "$HOME/.config/neuron-automation"
    echo "✅ Configuration directory removed"
else
    echo "ℹ️ Configuration directory preserved at: $HOME/.config/neuron-automation"
fi

echo "✅ Uninstallation complete"
EOF

chmod +x "$CONFIG_DIR/uninstall.sh"

echo ""
echo "✅ Installation completed successfully!"
echo ""
echo "📋 Summary:"
echo "   • Service installed: $SCRIPT_NAME.service"
echo "   • Timer installed: $SCRIPT_NAME.timer (runs weekdays at 5:30, 6:00, 6:30, 7:00 AM)"
echo "   • Command: $SCRIPT_NAME"
echo "   • Config: $CONFIG_DIR"
echo "   • Logs: $CONFIG_DIR/neuron_automation.log"
echo ""
echo "🎮 Usage:"
echo "   • Manual run: $SCRIPT_NAME"
echo "   • Check timer: systemctl status $SCRIPT_NAME.timer"
echo "   • Check logs: journalctl -u $SCRIPT_NAME.service"
echo "   • View app logs: tail -f $CONFIG_DIR/neuron_automation.log"
echo ""
echo "⏰ The automation will run automatically at 5:30, 6:00, 6:30, 7:00 AM on weekdays"
echo "   (with up to 5 minutes random delay to avoid server load)"
echo ""
echo "🗑️ To uninstall: $CONFIG_DIR/uninstall.sh"
echo ""
echo "🧪 Test the installation: $SCRIPT_NAME"

# Configure shell integration
echo ""
echo "🐚 Configuring shell integration..."

# Detect user's shell and configuration files
USER_SHELL=$(basename "$SHELL")
echo "Detected shell: $USER_SHELL"

# Function to safely add PATH to shell config
add_to_shell_config() {
    local config_file="$1"
    local path_line='export PATH="/usr/local/bin:$PATH"'
    
    if [ -f "$config_file" ]; then
        if ! grep -q "/usr/local/bin" "$config_file"; then
            echo "Adding PATH to $config_file"
            echo "" >> "$config_file"
            echo "# Added by Neuron Automation installer" >> "$config_file" 
            echo "$path_line" >> "$config_file"
        else
            echo "PATH already configured in $config_file"
        fi
    fi
}

# Configure for different shells
case "$USER_SHELL" in
    zsh)
        echo "Configuring for Zsh..."
        add_to_shell_config "$HOME/.zshrc"
        
        # Check for Oh My Zsh
        if [ -d "$HOME/.oh-my-zsh" ]; then
            echo "Oh My Zsh detected - configuration added to .zshrc"
        fi
        
        # Also add to .zprofile if it exists
        add_to_shell_config "$HOME/.zprofile"
        ;;
    bash)
        echo "Configuring for Bash..."
        add_to_shell_config "$HOME/.bashrc"
        add_to_shell_config "$HOME/.bash_profile"
        ;;
    fish)
        echo "Fish shell detected - please manually add /usr/local/bin to your PATH"
        ;;
    *)
        echo "Unknown shell ($USER_SHELL) - adding to common config files..."
        add_to_shell_config "$HOME/.profile"
        ;;
esac

# Show timer status
echo ""
echo "📊 Timer status:"
systemctl status "$SCRIPT_NAME.timer" --no-pager -l || true