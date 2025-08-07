#!/usr/bin/env python3
"""
Dashboard Launcher

This script provides multiple ways to launch the trading dashboard:
- Basic dashboard (original streamlit_app.py)
- Advanced dashboard with full configuration management
- Setup wizard for first-time users
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def check_requirements():
    """Check if all required packages are installed"""
    required_packages = [
        'streamlit', 'pandas', 'numpy', 'yfinance', 'plotly', 
        'requests', 'cryptography', 'pyyaml'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Please install missing packages:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def launch_basic_dashboard():
    """Launch the basic dashboard (original)"""
    print("🚀 Launching Basic Dashboard...")
    print("📍 URL: http://localhost:8501")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.headless", "true",
            "--server.address", "0.0.0.0",
            "--server.port", "8501"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch basic dashboard: {e}")
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")

def launch_advanced_dashboard():
    """Launch the advanced dashboard with full configuration"""
    print("🚀 Launching Advanced Dashboard...")
    print("📍 URL: http://localhost:8502")
    print("✨ Features: Full configuration management, market data, AI insights")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "advanced_dashboard.py",
            "--server.headless", "true", 
            "--server.address", "0.0.0.0",
            "--server.port", "8502"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch advanced dashboard: {e}")
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped by user")

def launch_setup_wizard():
    """Launch the setup wizard for first-time configuration"""
    print("🧙‍♂️ Launching Setup Wizard...")
    
    try:
        subprocess.run([sys.executable, "setup_llm.py"], check=True)
        print("✅ Setup completed!")
        
        # Ask user which dashboard to launch
        choice = input("\n🚀 Which dashboard would you like to launch?\n"
                      "1. Basic Dashboard\n"
                      "2. Advanced Dashboard\n"
                      "Choice (1-2): ").strip()
        
        if choice == "1":
            launch_basic_dashboard()
        elif choice == "2":
            launch_advanced_dashboard()
        else:
            print("Invalid choice. Exiting.")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Setup wizard failed: {e}")
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled by user")

def show_system_info():
    """Show system information and status"""
    print("📊 ChatGPT Micro-Cap Trading Bot - System Information")
    print("=" * 60)
    
    # Python version
    print(f"🐍 Python Version: {sys.version.split()[0]}")
    
    # Check if core files exist
    core_files = [
        "trading_script.py",
        "streamlit_app.py", 
        "advanced_dashboard.py",
        "llm_interface.py",
        "dashboard_config.py",
        "market_data_service.py"
    ]
    
    print("\n📁 Core Files Status:")
    for file in core_files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"   {status} {file}")
    
    # Check data files
    data_files = [
        "Scripts and CSV Files/chatgpt_portfolio_update.csv",
        "Scripts and CSV Files/chatgpt_trade_log.csv"
    ]
    
    print("\n📈 Data Files Status:")
    for file in data_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   ✅ {file} ({size} bytes)")
        else:
            print(f"   ❌ {file} (not found)")
    
    # Check configuration
    config_files = [".env", ".llm_config.json", "dashboard_config.json"]
    
    print("\n⚙️ Configuration Files:")
    for file in config_files:
        status = "✅" if os.path.exists(file) else "❌"
        print(f"   {status} {file}")
    
    # Check packages
    print("\n📦 Package Status:")
    check_requirements()
    
    print("\n🌐 Available Interfaces:")
    print("   • Command Line: python trading_bot.py")
    print("   • Basic Web UI: python launch_dashboard.py --basic")
    print("   • Advanced Dashboard: python launch_dashboard.py --advanced")
    print("   • Setup Wizard: python launch_dashboard.py --setup")

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        description="ChatGPT Micro-Cap Trading Dashboard Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_dashboard.py --basic          # Launch basic dashboard
  python launch_dashboard.py --advanced       # Launch advanced dashboard  
  python launch_dashboard.py --setup          # Run setup wizard
  python launch_dashboard.py --info           # Show system information
        """
    )
    
    parser.add_argument(
        '--basic', 
        action='store_true',
        help='Launch basic dashboard (streamlit_app.py)'
    )
    
    parser.add_argument(
        '--advanced',
        action='store_true', 
        help='Launch advanced dashboard with full configuration'
    )
    
    parser.add_argument(
        '--setup',
        action='store_true',
        help='Run setup wizard for first-time configuration'
    )
    
    parser.add_argument(
        '--info',
        action='store_true',
        help='Show system information and status'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=None,
        help='Custom port for dashboard (default: 8501 for basic, 8502 for advanced)'
    )
    
    args = parser.parse_args()
    
    # Show header
    print("🤖 ChatGPT Micro-Cap Trading Bot Dashboard Launcher")
    print("=" * 55)
    
    # Check requirements first (unless just showing info)
    if not args.info and not check_requirements():
        print("\n❌ Please install missing requirements first:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Handle arguments
    if args.info:
        show_system_info()
    elif args.setup:
        launch_setup_wizard()
    elif args.basic:
        launch_basic_dashboard()
    elif args.advanced:
        launch_advanced_dashboard()
    else:
        # Interactive mode
        print("\n🎯 Choose your dashboard:")
        print("1. 📊 Basic Dashboard - Simple portfolio tracking")
        print("2. 🚀 Advanced Dashboard - Full configuration & market data")
        print("3. 🧙‍♂️ Setup Wizard - First-time configuration")
        print("4. 📋 System Information - Check system status")
        print("5. ❌ Exit")
        
        try:
            choice = input("\nChoice (1-5): ").strip()
            
            if choice == "1":
                launch_basic_dashboard()
            elif choice == "2":
                launch_advanced_dashboard()
            elif choice == "3":
                launch_setup_wizard()
            elif choice == "4":
                show_system_info()
            elif choice == "5":
                print("👋 Goodbye!")
                sys.exit(0)
            else:
                print("❌ Invalid choice. Please select 1-5.")
                sys.exit(1)
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            sys.exit(0)

if __name__ == "__main__":
    main()