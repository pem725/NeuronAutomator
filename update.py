#!/usr/bin/env python3
"""
Neuron Automation Update Script
==============================

Easily update the Neuron Daily Newsletter Automation system to the latest version
from GitHub while preserving user configurations and settings.
"""

import os
import sys
import json
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any
import platform

__version__ = "1.0.0"

class NeuronAutomationUpdater:
    """Handles updating the Neuron Automation system."""
    
    def __init__(self):
        self.current_dir = Path(__file__).parent.absolute()
        self.platform = platform.system().lower()
        self.github_url = "https://github.com/pem725/NeuronAutomator.git"
        
        # Platform-specific paths
        if self.platform == "windows":
            self.config_dir = Path.home() / "AppData" / "Local" / "neuron-automation"
            self.install_dir = Path("C:") / "Program Files" / "neuron-automation"
        elif self.platform == "darwin":
            self.config_dir = Path.home() / "Library" / "Application Support" / "neuron-automation"
            self.install_dir = Path("/usr/local/bin")
        else:  # Linux
            self.config_dir = Path.home() / ".config" / "neuron-automation"
            self.install_dir = Path("/usr/local/bin")
    
    def get_current_version(self) -> Optional[str]:
        """Get the current installed version."""
        try:
            # Try to get version from neuron_automation.py
            main_script = self.config_dir / "neuron_automation.py"
            if main_script.exists():
                with open(main_script, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.strip().startswith('__version__'):
                            return line.split('"')[1]
            
            # Fallback: try current directory
            local_script = self.current_dir / "neuron_automation.py"
            if local_script.exists():
                with open(local_script, 'r', encoding='utf-8') as f:
                    content = f.read()
                    for line in content.split('\n'):
                        if line.strip().startswith('__version__'):
                            return line.split('"')[1]
            
            return None
        except Exception as e:
            print(f"Warning: Could not determine current version: {e}")
            return None
    
    def backup_user_config(self) -> Optional[Path]:
        """Backup user configuration files."""
        if not self.config_dir.exists():
            print("No existing configuration found - fresh installation")
            return None
        
        backup_dir = Path(tempfile.mkdtemp(prefix="neuron_backup_"))
        print(f"📦 Backing up configuration to: {backup_dir}")
        
        try:
            # Files to preserve
            preserve_files = [
                "neuron_automation.log",
                "last_run_*.txt",  # Cache files
                "chrome_profile/",  # Chrome profile data
                "custom_config.py"  # User customizations
            ]
            
            for pattern in preserve_files:
                if "*" in pattern:
                    # Handle glob patterns
                    for file_path in self.config_dir.glob(pattern):
                        if file_path.is_file():
                            shutil.copy2(file_path, backup_dir / file_path.name)
                        elif file_path.is_dir():
                            shutil.copytree(file_path, backup_dir / file_path.name, dirs_exist_ok=True)
                else:
                    file_path = self.config_dir / pattern
                    if file_path.exists():
                        if file_path.is_file():
                            shutil.copy2(file_path, backup_dir / pattern)
                        elif file_path.is_dir():
                            shutil.copytree(file_path, backup_dir / pattern, dirs_exist_ok=True)
            
            return backup_dir
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return None
    
    def download_latest_version(self) -> Optional[Path]:
        """Download the latest version from GitHub."""
        temp_dir = Path(tempfile.mkdtemp(prefix="neuron_update_"))
        
        print("🌐 Downloading latest version from GitHub...")
        try:
            # Clone the repository
            result = subprocess.run([
                "git", "clone", self.github_url, str(temp_dir)
            ], capture_output=True, text=True, check=True)
            
            print("✅ Download completed successfully")
            return temp_dir
        except subprocess.CalledProcessError as e:
            print(f"❌ Git clone failed: {e.stderr}")
            return None
        except FileNotFoundError:
            print("❌ Git not found. Please install git or download manually.")
            return None
    
    def install_update(self, source_dir: Path, backup_dir: Optional[Path]) -> bool:
        """Install the update from source directory."""
        try:
            print("🔧 Installing update...")
            
            # Run the appropriate installer
            installer_map = {
                "linux": source_dir / "installers" / "install_linux.sh",
                "darwin": source_dir / "installers" / "install_macos.sh", 
                "windows": source_dir / "installers" / "install_windows.ps1"
            }
            
            installer = installer_map.get(self.platform)
            if not installer or not installer.exists():
                print(f"❌ No installer found for platform: {self.platform}")
                return False
            
            # Change to source directory and run installer
            original_dir = Path.cwd()
            try:
                os.chdir(source_dir)
                
                if self.platform == "windows":
                    # PowerShell execution
                    result = subprocess.run([
                        "powershell", "-ExecutionPolicy", "RemoteSigned", "-File", str(installer)
                    ], check=True)
                else:
                    # Bash execution
                    result = subprocess.run([
                        "bash", str(installer)
                    ], check=True)
                
                print("✅ Installation completed successfully")
                return True
                
            finally:
                os.chdir(original_dir)
                
        except subprocess.CalledProcessError as e:
            print(f"❌ Installation failed: {e}")
            return False
        except Exception as e:
            print(f"❌ Installation error: {e}")
            return False
    
    def restore_user_data(self, backup_dir: Optional[Path]) -> bool:
        """Restore user data from backup."""
        if not backup_dir or not backup_dir.exists():
            return True
        
        try:
            print("📂 Restoring user data...")
            
            # Restore files
            for backup_file in backup_dir.iterdir():
                target_path = self.config_dir / backup_file.name
                
                if backup_file.is_file():
                    shutil.copy2(backup_file, target_path)
                elif backup_file.is_dir():
                    if target_path.exists():
                        shutil.rmtree(target_path)
                    shutil.copytree(backup_file, target_path)
            
            print("✅ User data restored successfully")
            return True
            
        except Exception as e:
            print(f"❌ Failed to restore user data: {e}")
            return False
    
    def cleanup(self, temp_dirs: list) -> None:
        """Clean up temporary directories."""
        for temp_dir in temp_dirs:
            if temp_dir and temp_dir.exists():
                try:
                    shutil.rmtree(temp_dir)
                except Exception as e:
                    print(f"Warning: Could not clean up {temp_dir}: {e}")
    
    def run_update(self, force: bool = False) -> bool:
        """Run the complete update process."""
        print("🚀 Neuron Automation Updater v{__version__}")
        print("=" * 50)
        
        current_version = self.get_current_version()
        if current_version:
            print(f"📋 Current version: {current_version}")
        else:
            print("📋 Current version: Unknown")
        
        if not force:
            response = input("\n🤔 Proceed with update? (y/N): ").lower()
            if response not in ['y', 'yes']:
                print("Update cancelled by user")
                return False
        
        temp_dirs = []
        
        try:
            # Step 1: Backup user configuration
            backup_dir = self.backup_user_config()
            if backup_dir:
                temp_dirs.append(backup_dir)
            
            # Step 2: Download latest version
            source_dir = self.download_latest_version()
            if not source_dir:
                return False
            temp_dirs.append(source_dir)
            
            # Step 3: Install update
            if not self.install_update(source_dir, backup_dir):
                return False
            
            # Step 4: Restore user data
            if not self.restore_user_data(backup_dir):
                print("⚠️ Update completed but user data restoration had issues")
            
            # Step 5: Verify installation
            new_version = self.get_current_version()
            if new_version and new_version != current_version:
                print(f"🎉 Update successful! New version: {new_version}")
            else:
                print("✅ Update completed")
            
            return True
            
        except KeyboardInterrupt:
            print("\n❌ Update interrupted by user")
            return False
        except Exception as e:
            print(f"❌ Update failed with error: {e}")
            return False
        finally:
            # Cleanup temporary directories
            self.cleanup(temp_dirs)

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Update Neuron Automation system")
    parser.add_argument("--force", action="store_true", 
                       help="Skip confirmation prompts")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    
    args = parser.parse_args()
    
    updater = NeuronAutomationUpdater()
    success = updater.run_update(force=args.force)
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()