#!/usr/bin/env python3
"""
Launch script for the AI Trading Bot Dashboard
"""

import sys
import subprocess
import os
from pathlib import Path

def main():
    """Launch the trading dashboard"""
    # Add src to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    # Launch Streamlit dashboard
    dashboard_path = src_path / "interfaces" / "streamlit_app.py"
    
    if dashboard_path.exists():
        cmd = [sys.executable, "-m", "streamlit", "run", str(dashboard_path), "--server.port=8502"]
        subprocess.run(cmd)
    else:
        print("Dashboard not found. Please ensure all files are properly installed.")
        print("Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()