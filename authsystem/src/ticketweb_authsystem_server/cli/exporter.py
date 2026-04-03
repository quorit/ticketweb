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




def export_schema():
    parser = argparse.ArgumentParser(description="Export the session storage schema SQL file.")
    parser.add_argument(
        "target", 
        help="The destination directory or exact file path (e.g., /tmp/ or /tmp/my_schema.sql)"
    )
    args = parser.parse_args()
    
    package = 'ticketweb_authsystem_server'
    filename = 'session_storage_schema.sql'
    
    try:
        # Locate the specific SQL file within the installed package
        source_file = resources.files(package).joinpath(filename)
        
        # Verify it actually exists in the built package
        if not source_file.is_file():
            print(f"Error: '{filename}' not found inside the '{package}' package.")
            print("Did you forget 'include_package_data = True' in setup.cfg?")
            sys.exit(1)
            
        # Determine the final destination path
        if os.path.isdir(args.target) or args.target.endswith(os.sep):
            # Target is a directory, keep the original filename
            os.makedirs(args.target, exist_ok=True)
            dest_path = os.path.join(args.target, filename)
        else:
            # Target is a full file path, ensure parent directories exist
            target_dir = os.path.dirname(os.path.abspath(args.target))
            if target_dir:
                os.makedirs(target_dir, exist_ok=True)
            dest_path = args.target
            
        # Copy the file out of the package to the target
        with source_file.open('rb') as f_src:
            with open(dest_path, 'wb') as f_dst:
                shutil.copyfileobj(f_src, f_dst)
                
        print(f"Success! Exported schema to: {dest_path}")
        
    except ModuleNotFoundError:
        print(f"Error: Package '{package}' is not installed in the current environment.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied writing to '{args.target}'. Try using sudo.")
        sys.exit(1)




