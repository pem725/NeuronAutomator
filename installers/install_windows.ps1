# Neuron Newsletter Automation - Windows Installation Script
# =========================================================

param(
    [switch]$Force = $false
)

$ErrorActionPreference = "Stop"

$SCRIPT_NAME = "neuron-automation"
$INSTALL_DIR = "C:\Program Files\neuron-automation"
$CONFIG_DIR = "$env:LOCALAPPDATA\neuron-automation"
$TASK_NAME = "NeuronAutomation"

Write-Host "🪟 Installing Neuron Newsletter Automation for Windows..." -ForegroundColor Cyan

# Check if running as administrator
$currentUser = [System.Security.Principal.WindowsIdentity]::GetCurrent()
$principal = New-Object System.Security.Principal.WindowsPrincipal($currentUser)
$isAdmin = $principal.IsInRole([System.Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "❌ This script requires administrator privileges" -ForegroundColor Red
    Write-Host "   Please run PowerShell as Administrator and try again" -ForegroundColor Yellow
    exit 1
}

# Function to check if command exists
function Test-Command {
    param($Command)
    $oldPreference = $ErrorActionPreference
    $ErrorActionPreference = "stop"
    try {
        if(Get-Command $Command) { return $true }
    }
    catch { return $false }
    finally { $ErrorActionPreference = $oldPreference }
}

# Check for Chocolatey and install if needed
if (-not (Test-Command "choco")) {
    Write-Host "🍫 Installing Chocolatey package manager..." -ForegroundColor Yellow
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    refreshenv
}

# Install Python if not present
if (-not (Test-Command "python")) {
    Write-Host "🐍 Installing Python..." -ForegroundColor Yellow
    choco install python3 -y
    refreshenv
}

# Install Google Chrome if not present
$chromePath = "${env:ProgramFiles}\Google\Chrome\Application\chrome.exe"
$chromePathx86 = "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe"
if (-not (Test-Path $chromePath) -and -not (Test-Path $chromePathx86)) {
    Write-Host "🌐 Installing Google Chrome..." -ForegroundColor Yellow
    choco install googlechrome -y
} else {
    Write-Host "✅ Google Chrome already installed" -ForegroundColor Green
}

# Create directories
Write-Host "📁 Creating directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Path $INSTALL_DIR -Force | Out-Null
New-Item -ItemType Directory -Path $CONFIG_DIR -Force | Out-Null

# Create virtual environment
Write-Host "🐍 Setting up Python virtual environment..." -ForegroundColor Yellow
$VENV_DIR = "$CONFIG_DIR\venv"

# Remove existing virtual environment if it exists
if (Test-Path $VENV_DIR) {
    Write-Host "   Removing existing virtual environment..." -ForegroundColor Yellow
    Remove-Item $VENV_DIR -Recurse -Force
}

# Create fresh virtual environment
python -m venv "$VENV_DIR"
& "$VENV_DIR\Scripts\Activate.ps1"

# Install Python packages
Write-Host "📦 Installing Python packages..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install selenium webdriver-manager requests beautifulsoup4

# Create requirements.txt
@"
selenium>=4.0.0
webdriver-manager>=3.8.0
requests>=2.28.0
beautifulsoup4>=4.11.0
"@ | Out-File "$CONFIG_DIR\requirements.txt" -Encoding utf8

# Create batch wrapper script
Write-Host "📝 Creating wrapper script..." -ForegroundColor Yellow
@"
@echo off
REM Neuron Newsletter Automation Wrapper Script for Windows

REM Activate virtual environment
call "$CONFIG_DIR\venv\Scripts\activate.bat"

REM Run the Python script
python "$CONFIG_DIR\neuron_automation.py" %*
"@ | Out-File "$INSTALL_DIR\$SCRIPT_NAME.bat" -Encoding ascii

# Copy Python scripts
Write-Host "📄 Installing main scripts..." -ForegroundColor Yellow
$SCRIPT_DIR = Split-Path -Parent $PSScriptRoot
Copy-Item "$SCRIPT_DIR\neuron_automation.py" "$CONFIG_DIR\" -Force
Copy-Item "$SCRIPT_DIR\config.py" "$CONFIG_DIR\" -Force

# Create Task Scheduler XML configuration
Write-Host "⏰ Creating Task Scheduler configuration..." -ForegroundColor Yellow
$taskXml = @"
<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.4" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>$(Get-Date -Format "yyyy-MM-ddTHH:mm:ss")</Date>
    <Author>$env:USERNAME</Author>
    <Description>Automatically opens Neuron Daily newsletter with article links every weekday morning</Description>
  </RegistrationInfo>
  <Triggers>
    <!-- 5:30 AM Trigger -->
    <CalendarTrigger>
      <StartBoundary>$(Get-Date -Date "05:30" -Format "yyyy-MM-ddTHH:mm:ss")</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Monday />
          <Tuesday />
          <Wednesday />
          <Thursday />
          <Friday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
    <!-- 6:00 AM Trigger -->
    <CalendarTrigger>
      <StartBoundary>$(Get-Date -Date "06:00" -Format "yyyy-MM-ddTHH:mm:ss")</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Monday />
          <Tuesday />
          <Wednesday />
          <Thursday />
          <Friday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
    <!-- 6:30 AM Trigger -->
    <CalendarTrigger>
      <StartBoundary>$(Get-Date -Date "06:30" -Format "yyyy-MM-ddTHH:mm:ss")</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Monday />
          <Tuesday />
          <Wednesday />
          <Thursday />
          <Friday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
    <!-- 7:00 AM Trigger -->
    <CalendarTrigger>
      <StartBoundary>$(Get-Date -Date "07:00" -Format "yyyy-MM-ddTHH:mm:ss")</StartBoundary>
      <Enabled>true</Enabled>
      <ScheduleByWeek>
        <DaysOfWeek>
          <Monday />
          <Tuesday />
          <Wednesday />
          <Thursday />
          <Friday />
        </DaysOfWeek>
        <WeeksInterval>1</WeeksInterval>
      </ScheduleByWeek>
    </CalendarTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>$env:USERNAME</UserId>
      <LogonType>InteractiveToken</LogonType>
      <RunLevel>LeastPrivilege</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>false</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>true</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>false</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>false</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT1H</ExecutionTimeLimit>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>"$INSTALL_DIR\$SCRIPT_NAME.bat"</Command>
      <WorkingDirectory>$CONFIG_DIR</WorkingDirectory>
    </Exec>
  </Actions>
</Task>
"@

$taskXml | Out-File "$CONFIG_DIR\task.xml" -Encoding utf8

# Register the scheduled task
Write-Host "🔄 Registering scheduled task..." -ForegroundColor Yellow
schtasks /create /tn $TASK_NAME /xml "$CONFIG_DIR\task.xml" /f

# Add to PATH (system-wide)
$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
if ($currentPath -notlike "*$INSTALL_DIR*") {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$INSTALL_DIR", "Machine")
    Write-Host "✅ Added to system PATH" -ForegroundColor Green
}

# Create uninstall script
Write-Host "📝 Creating uninstall script..." -ForegroundColor Yellow
@"
# Uninstall Neuron Newsletter Automation for Windows

Write-Host "🗑️ Uninstalling Neuron Newsletter Automation..." -ForegroundColor Cyan

# Remove scheduled task
schtasks /delete /tn "$TASK_NAME" /f 2>``$null

# Remove from PATH
``$currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
``$newPath = ``$currentPath -replace ";?``$INSTALL_DIR", ""
[Environment]::SetEnvironmentVariable("Path", ``$newPath, "Machine")

# Remove installation directory
Remove-Item "$INSTALL_DIR" -Recurse -Force -ErrorAction SilentlyContinue

# Ask about config directory
``$response = Read-Host "Remove configuration directory with logs? (y/N)"
if (``$response -eq "y" -or ``$response -eq "Y") {
    Remove-Item "$CONFIG_DIR" -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "✅ Configuration directory removed" -ForegroundColor Green
} else {
    Write-Host "ℹ️ Configuration directory preserved at: $CONFIG_DIR" -ForegroundColor Blue
}

Write-Host "✅ Uninstallation complete" -ForegroundColor Green
"@ | Out-File "$CONFIG_DIR\uninstall.ps1" -Encoding utf8

Write-Host ""
Write-Host "✅ Installation completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Summary:" -ForegroundColor Cyan
Write-Host "   • Command: $SCRIPT_NAME" -ForegroundColor White
Write-Host "   • Config: $CONFIG_DIR" -ForegroundColor White
Write-Host "   • Logs: $CONFIG_DIR\neuron_automation.log" -ForegroundColor White
Write-Host "   • Task: $TASK_NAME" -ForegroundColor White
Write-Host ""
Write-Host "🎮 Usage:" -ForegroundColor Cyan
Write-Host "   • Manual run: $SCRIPT_NAME" -ForegroundColor White
Write-Host "   • Check task: schtasks /query /tn $TASK_NAME" -ForegroundColor White
Write-Host "   • View logs: type `"$CONFIG_DIR\neuron_automation.log`"" -ForegroundColor White
Write-Host ""
Write-Host "⏰ The automation will run automatically at 5:30, 6:00, 6:30, 7:00 AM on weekdays" -ForegroundColor Yellow
Write-Host ""
Write-Host "🗑️ To uninstall: PowerShell -File `"$CONFIG_DIR\uninstall.ps1`"" -ForegroundColor Red
Write-Host ""
Write-Host "🧪 Test the installation: $SCRIPT_NAME" -ForegroundColor Green

# Show task status
Write-Host ""
Write-Host "📊 Scheduled Task status:" -ForegroundColor Cyan
schtasks /query /tn $TASK_NAME /fo table