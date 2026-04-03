import argparse
# Import the logic we wrote earlier
from .exporter import export_configs 
from .exporter import export_schema

def export_configs_cli():
    parser = argparse.ArgumentParser(description="Export systemd files.")
    parser.add_argument("target", help="Target directory for export")
    args = parser.parse_args()
    
    # Call the actual logic
    export_configs(args.target)

def export_session_schema_cli():
    parser = argparse.ArgumentParser(description="Export the session storage schema SQL file.")
    parser.add_argument("target", help="Target directory or exact file path for export")
    args = parser.parse_args()
    
    # Call the actual logic
    export_schema(args.target)


    