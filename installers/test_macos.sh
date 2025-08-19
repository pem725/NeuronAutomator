#!/bin/bash

# Neuron Newsletter Automation - macOS Test and Validation Script
# ===============================================================

set -e

SCRIPT_NAME="neuron-automation"
CONFIG_DIR="$HOME/Library/Application Support/neuron-automation"
INSTALL_DIR="/usr/local/bin"
LAUNCHD_DIR="$HOME/Library/LaunchAgents"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test result tracking
TESTS_PASSED=0
TESTS_FAILED=0

# Helper functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
    ((TESTS_PASSED++))
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
    ((TESTS_FAILED++))
}

test_command() {
    local cmd="$1"
    local description="$2"
    
    if command -v "$cmd" >/dev/null 2>&1; then
        log_success "$description"
        return 0
    else
        log_error "$description"
        return 1
    fi
}

test_file_exists() {
    local file="$1"
    local description="$2"
    
    if [[ -f "$file" ]]; then
        log_success "$description"
        return 0
    else
        log_error "$description"
        return 1
    fi
}

test_directory_exists() {
    local dir="$1"
    local description="$2"
    
    if [[ -d "$dir" ]]; then
        log_success "$description"
        return 0
    else
        log_error "$description"
        return 1
    fi
}

test_python_import() {
    local module="$1"
    local description="$2"
    local venv_python="$CONFIG_DIR/venv/bin/python"
    
    if [[ -f "$venv_python" ]] && "$venv_python" -c "import $module" 2>/dev/null; then
        log_success "$description"
        return 0
    else
        log_error "$description"
        return 1
    fi
}

echo "🧪 Neuron Newsletter Automation - macOS System Test"
echo "===================================================="
echo

# Test 1: System Dependencies
log_info "Testing system dependencies..."
test_command "python3" "Python 3 is installed"
test_command "pip3" "pip3 is installed"
test_command "brew" "Homebrew is installed"

# Check for Chrome
if [[ -d "/Applications/Google Chrome.app" ]] || command -v google-chrome >/dev/null 2>&1; then
    log_success "Google Chrome is installed"
else
    log_error "Google Chrome is not installed"
fi

# Test 2: Installation Files
echo
log_info "Testing installation files..."
test_file_exists "$INSTALL_DIR/$SCRIPT_NAME" "Main command script exists"
test_file_exists "$CONFIG_DIR/neuron_automation.py" "Python script exists"
test_file_exists "$CONFIG_DIR/config.py" "Configuration file exists"
test_directory_exists "$CONFIG_DIR/venv" "Virtual environment exists"
test_file_exists "$CONFIG_DIR/venv/bin/python" "Virtual environment Python exists"

# Test 3: LaunchAgent Integration
echo
log_info "Testing LaunchAgent integration..."
test_file_exists "$LAUNCHD_DIR/com.neuron.automation.plist" "LaunchAgent plist file exists"

# Check if LaunchAgent is loaded
if launchctl list | grep -q "com.neuron.automation"; then
    log_success "LaunchAgent is loaded"
else
    log_error "LaunchAgent is not loaded"
fi

# Test 4: Python Dependencies
echo
log_info "Testing Python dependencies..."
test_python_import "selenium" "Selenium is installed"
test_python_import "webdriver_manager" "WebDriver Manager is installed"
test_python_import "requests" "Requests is installed"
test_python_import "bs4" "BeautifulSoup4 is installed"

# Test 5: Configuration Validation
echo
log_info "Testing configuration..."
if [[ -f "$CONFIG_DIR/venv/bin/python" ]]; then
    if "$CONFIG_DIR/venv/bin/python" -c "
import sys
sys.path.insert(0, '$CONFIG_DIR')
from config import ACTIVE_CONFIG
try:
    ACTIVE_CONFIG.validate_config()
    print('Configuration validation passed')
except Exception as e:
    print(f'Configuration validation failed: {e}')
    sys.exit(1)
" 2>/dev/null; then
        log_success "Configuration validation passed"
    else
        log_error "Configuration validation failed"
    fi
else
    log_error "Cannot test configuration - Python virtual environment not found"
fi

# Test 6: File Permissions
echo
log_info "Testing file permissions..."
if [[ -x "$INSTALL_DIR/$SCRIPT_NAME" ]]; then
    log_success "Main script is executable"
else
    log_error "Main script is not executable"
fi

if [[ -x "$CONFIG_DIR/neuron_automation.py" ]]; then
    log_success "Python script is executable"
else
    log_error "Python script is not executable"
fi

# Test 7: Network Connectivity
echo
log_info "Testing network connectivity..."
if curl -s --head https://www.theneurondaily.com/ | grep -q "200 OK"; then
    log_success "Can reach Neuron Daily website"
elif curl -s --head https://www.theneurondaily.com/ | grep -q "HTTP"; then
    log_warning "Neuron Daily website is reachable but returned non-200 status"
    ((TESTS_PASSED++))  # Still count as passed since site is reachable
else
    log_error "Cannot reach Neuron Daily website"
fi

if curl -s --head https://www.google.com/ | grep -q "200 OK"; then
    log_success "Internet connectivity is working"
else
    log_error "Internet connectivity test failed"
fi

# Test 8: Chrome WebDriver Test
echo
log_info "Testing Chrome WebDriver..."
if [[ -f "$CONFIG_DIR/venv/bin/python" ]]; then
    WEBDRIVER_TEST_OUTPUT=$("$CONFIG_DIR/venv/bin/python" -c "
import sys
import os
sys.path.insert(0, '$CONFIG_DIR')

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get('https://www.google.com')
    
    if 'Google' in driver.title:
        print('WebDriver test successful')
        driver.quit()
    else:
        print('WebDriver test failed - could not load Google')
        driver.quit()
        sys.exit(1)
        
except Exception as e:
    print(f'WebDriver test failed: {e}')
    sys.exit(1)
" 2>&1)

    if echo "$WEBDRIVER_TEST_OUTPUT" | grep -q "WebDriver test successful"; then
        log_success "Chrome WebDriver test passed"
    else
        log_error "Chrome WebDriver test failed"
        echo "Error details: $WEBDRIVER_TEST_OUTPUT"
    fi
else
    log_error "Cannot test WebDriver - Python virtual environment not found"
fi

# Test 9: Log Directory and Permissions
echo
log_info "Testing logging setup..."
if [[ -d "$CONFIG_DIR" ]]; then
    if touch "$CONFIG_DIR/test_log.tmp" 2>/dev/null; then
        rm -f "$CONFIG_DIR/test_log.tmp"
        log_success "Log directory is writable"
    else
        log_error "Log directory is not writable"
    fi
else
    log_error "Configuration directory does not exist"
fi

# Summary
echo
echo "🏁 Test Summary"
echo "==============="
echo "Tests passed: $TESTS_PASSED"
echo "Tests failed: $TESTS_FAILED"
echo

if [[ $TESTS_FAILED -eq 0 ]]; then
    log_success "All tests passed! The installation appears to be working correctly."
    echo
    echo "🚀 Next steps:"
    echo "   • Run manually: $SCRIPT_NAME"
    echo "   • Check LaunchAgent: launchctl list | grep neuron"
    echo "   • View logs: tail -f '$CONFIG_DIR/neuron_automation.log'"
    exit 0
elif [[ $TESTS_FAILED -lt 3 ]]; then
    log_warning "Most tests passed, but there are some minor issues."
    echo "   The automation should still work, but you may want to investigate the failures."
    exit 0
else
    log_error "Multiple tests failed. The installation may not be working correctly."
    echo
    echo "🔧 Troubleshooting steps:"
    echo "   1. Re-run the installation: ./installers/install_macos.sh"
    echo "   2. Check system requirements"
    echo "   3. Verify internet connectivity"
    echo "   4. Check the installation log for errors"
    exit 1
fi