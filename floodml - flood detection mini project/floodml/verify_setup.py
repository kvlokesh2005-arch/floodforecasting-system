#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FloodML Dashboard - Setup Verification Script
Checks all dependencies and configurations before running the dashboard
"""

import sys
import os
from pathlib import Path
import json
import platform

# Fix encoding for Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def print_status(check, status, message=""):
    """Print status of a check"""
    symbol = "✅" if status else "❌"
    status_text = "PASS" if status else "FAIL"
    print(f"{symbol} {check:<40} [{status_text}]")
    if message:
        print(f"  → {message}")

def check_python():
    """Check Python version"""
    version = sys.version_info
    required = (3, 8)
    check_pass = (version.major, version.minor) >= required
    print_status(
        "Python Version",
        check_pass,
        f"Python {version.major}.{version.minor}.{version.micro}"
    )
    return check_pass

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        # Try to get version
        try:
            module = sys.modules[import_name]
            version = getattr(module, '__version__', 'Unknown')
            print_status(package_name, True, f"version {version}")
        except:
            print_status(package_name, True)
        return True
    except ImportError:
        print_status(package_name, False, "Not installed")
        return False

def check_file(file_path, description):
    """Check if a file exists"""
    exists = os.path.exists(file_path)
    print_status(description, exists, file_path if exists else "Missing")
    return exists

def check_directory(dir_path, description):
    """Check if a directory exists"""
    exists = os.path.isdir(dir_path)
    print_status(description, exists, dir_path if exists else "Missing")
    return exists

def check_config_json():
    """Check configuration file"""
    config_file = "dashboard_config.json"
    if not os.path.exists(config_file):
        print_status("Configuration File", False, f"{config_file} not found")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        required_keys = ['app_name', 'model', 'satellites', 'processing']
        all_present = all(key in config for key in required_keys)
        
        if all_present:
            print_status("Configuration File", True, f"{config_file} valid")
            return True
        else:
            print_status("Configuration File", False, "Missing required keys")
            return False
    except json.JSONDecodeError:
        print_status("Configuration File", False, f"{config_file} invalid JSON")
        return False
    except Exception as e:
        print_status("Configuration File", False, str(e))
        return False

def check_directories():
    """Check required directories"""
    directories = [
        ('models', 'Model Directory'),
        ('data', 'Data Directory'),
        ('data/archive', 'Archive Directory')
    ]
    
    all_exist = True
    for dir_path, desc in directories:
        exists = check_directory(dir_path, desc)
        all_exist = all_exist and exists
    
    return all_exist

def check_requirements_file():
    """Check requirements file exists and is valid"""
    req_file = "requirements-dashboard.txt"
    if not os.path.exists(req_file):
        print_status("Requirements File", False, f"{req_file} not found")
        return False
    
    try:
        with open(req_file, 'r') as f:
            lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        if len(lines) > 0:
            print_status("Requirements File", True, f"{len(lines)} packages")
            return True
        else:
            print_status("Requirements File", False, "Empty")
            return False
    except Exception as e:
        print_status("Requirements File", False, str(e))
        return False

def check_disk_space():
    """Check available disk space"""
    try:
        import shutil
        disk_usage = shutil.disk_usage('.')
        available_gb = disk_usage.free / (1024**3)
        required_gb = 2  # Minimum 2GB
        
        check_pass = available_gb >= required_gb
        print_status(
            "Disk Space",
            check_pass,
            f"{available_gb:.1f} GB available (need {required_gb} GB)"
        )
        return check_pass
    except Exception as e:
        print_status("Disk Space", False, str(e))
        return False

def check_streamlit_config():
    """Check if .streamlit config directory exists"""
    streamlit_dir = Path.home() / '.streamlit'
    exists = streamlit_dir.exists()
    print_status(
        "Streamlit Config",
        exists,
        str(streamlit_dir)
    )
    return True  # Not critical if missing

def main():
    """Run all checks"""
    print_header("FloodML Dashboard - Setup Verification")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python Executable: {sys.executable}")
    print(f"Working Directory: {os.getcwd()}")
    
    checks_passed = 0
    checks_total = 0
    
    # System checks
    print_header("System Requirements")
    
    if check_python():
        checks_passed += 1
    checks_total += 1
    
    if check_disk_space():
        checks_passed += 1
    checks_total += 1
    
    # Python packages
    print_header("Python Dependencies")
    
    packages = [
        ('streamlit', 'streamlit'),
        ('plotly', 'plotly'),
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('joblib', 'joblib'),
        ('scikit-learn', 'sklearn'),
        ('scipy', 'scipy'),
        ('Pillow', 'PIL'),
        ('matplotlib', 'matplotlib'),
    ]
    
    for pkg_name, import_name in packages:
        if check_package(pkg_name, import_name):
            checks_passed += 1
        checks_total += 1
    
    # Configuration files
    print_header("Configuration & Files")
    
    if check_file("app.py", "Dashboard Application"):
        checks_passed += 1
    checks_total += 1
    
    if check_file("dashboard_config.json", "Dashboard Config"):
        checks_passed += 1
    checks_total += 1
    
    if check_requirements_file():
        checks_passed += 1
    checks_total += 1
    
    if check_config_json():
        checks_passed += 1
    checks_total += 1
    
    # Directories
    print_header("Required Directories")
    
    if check_directories():
        checks_passed += 1
    checks_total += 1
    
    # Optional checks
    print_header("Optional Checks")
    check_streamlit_config()
    
    check_file("DASHBOARD_README.md", "Documentation (README)")
    check_file("QUICKSTART.md", "Quick Start Guide")
    check_file("run_dashboard.bat", "Windows Launcher")
    check_file("run_dashboard.sh", "Linux/Mac Launcher")
    
    # Summary
    print_header("Verification Summary")
    
    percentage = (checks_passed / checks_total * 100) if checks_total > 0 else 0
    print(f"Checks Passed: {checks_passed}/{checks_total} ({percentage:.0f}%)")
    
    if checks_passed == checks_total:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYou can now run the dashboard with:")
        
        if platform.system() == "Windows":
            print("  → run_dashboard.bat")
            print("  → python -m streamlit run app.py")
        else:
            print("  → ./run_dashboard.sh")
            print("  → python3 -m streamlit run app.py")
        
        print("\nThe dashboard will open at: http://localhost:8501")
        return 0
    
    else:
        missing_count = checks_total - checks_passed
        print(f"\n⚠️  {missing_count} check(s) failed")
        print("\nTo install missing dependencies, run:")
        print("  → pip install -r requirements-dashboard.txt")
        
        print("\nTo fix common issues:")
        print("  1. Ensure Python 3.8+ is installed")
        print("  2. Install all dependencies: pip install -r requirements-dashboard.txt")
        print("  3. Create required directories: models/, data/, data/archive/")
        print("  4. Ensure app.py exists in current directory")
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    print()
    sys.exit(exit_code)
