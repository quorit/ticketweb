import argparse
# Import the logic we wrote earlier
from .exporter import export_configs 


def export_configs_cli():
    parser = argparse.ArgumentParser(description="Export systemd files.")
    parser.add_argument("target", help="Target directory for export")
    args = parser.parse_args()
    
    # Call the actual logic
    export_configs(args.target)



    