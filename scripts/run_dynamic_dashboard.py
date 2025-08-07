#!/usr/bin/env python3
"""
Quick launcher for the Dynamic Trading Dashboard

This script provides easy access to the dynamic dashboard
with real-time updates and live data feeds.
"""

import sys
import os
from pathlib import Path

# Add src to path so we can import modules
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def main():
    """Launch the dynamic dashboard"""
    try:
        # Try to use the full launcher first
        launcher_path = Path(__file__).parent / "scripts" / "utils" / "launch_dynamic_dashboard.py"
        
        if launcher_path.exists():
            print("🚀 Starting Dynamic Trading Dashboard...")
            print("📊 Features: Real-time updates, Live charts, Auto-refresh")
            print("🌐 Dashboard will open at: http://localhost:8502")
            print("⚡ Press Ctrl+C to stop")
            print("-" * 50)
            
            os.system(f"python {launcher_path}")
        else:
            # Fallback to direct Streamlit launch
            print("📊 Starting Dynamic Dashboard (Basic Mode)...")
            import streamlit.cli
            sys.argv = [
                "streamlit",
                "run", 
                str(Path(__file__).parent / "src" / "interfaces" / "dynamic_dashboard.py"),
                "--server.port", "8502",
                "--server.headless", "true"
            ]
            streamlit.cli.main()
            
    except ImportError:
        print("❌ Streamlit not found. Install with: pip install streamlit")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Dynamic dashboard stopped by user")
    except Exception as e:
        print(f"❌ Error launching dynamic dashboard: {e}")
        print("💡 Try: python scripts/utils/launch_dynamic_dashboard.py")

if __name__ == "__main__":
    main()