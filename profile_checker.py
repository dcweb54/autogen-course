import os
from pathlib import Path
import platform

def check_chrome_profile(profile_name="Default"):
    """Check if a specific Chrome profile exists"""
    system = platform.system()
    
    if system == "Windows":
        base_path = Path(os.environ['LOCALAPPDATA']) / "Google" / "Chrome" / "User Data"
    elif system == "Darwin":
        base_path = Path.home() / "Library" / "Application Support" / "Google" / "Chrome"
    else:
        base_path = Path.home() / ".config" / "google-chrome"
    
    profile_path = base_path / profile_name
    
    if not base_path.exists():
        return False, "Chrome user data directory not found"
    
    if not profile_path.exists():
        return False, f"Profile '{profile_name}' does not exist"
    
    # Check if it's a valid Chrome profile
    required_files = ["Preferences", "Cookies"]
    for file in required_files:
        if not (profile_path / file).exists():
            return False, f"Profile '{profile_name}' is missing essential file: {file}"
    
    return True, f"Profile '{profile_name}' exists and appears valid"

# Usage
profiles_to_check = ["Default", "Profile 1", "Profile 2", "Work", "Personal"]

for profile in profiles_to_check:
    exists, message = check_chrome_profile(profile)
    print(f"{profile}: {message}")