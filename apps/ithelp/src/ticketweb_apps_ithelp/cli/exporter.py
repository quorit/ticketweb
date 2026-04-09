import os
import shutil
import argparse
import sys
from importlib import resources

def export_configs(target_dir):
    package = 'ticketweb_authsystem_server'
    # The subdirectory within your package where systemd files live
    resource_path = 'systemd-unit-files'
    
    if not os.path.exists(target_dir):
        print(f"Creating target directory: {target_dir}")
        os.makedirs(target_dir, exist_ok=True)

    try:
        # Traverse the resources in the package
        # In modern Python (3.9+), files() is the preferred API
        traversable = resources.files(package).joinpath(resource_path)
        
        count = 0
        for item in traversable.rglob('*'):
            if item.is_file() and item.name.endswith(('.service', '.timer', '.conf')):
                # Create subdirectories if they exist (for the .service.d folders)
                relative_path = item.relative_to(traversable)
                dest_path = os.path.join(target_dir, relative_path)
                
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                
                with item.open('rb') as f_src:
                    with open(dest_path, 'wb') as f_dst:
                        shutil.copyfileobj(f_src, f_dst)
                
                print(f"Exported: {relative_path}")
                count += 1
        
        print(f"\nSuccess: {count} files exported to {target_dir}")

    except ModuleNotFoundError:
        print(f"Error: Package '{package}' not found. Is the venv active?")
        sys.exit(1)









