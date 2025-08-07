#!/usr/bin/env python3
"""
Dynamic Dashboard Launcher

Launches the dynamic trading dashboard with real-time capabilities:
- Starts background data services
- Configures WebSocket server
- Sets up auto-refresh mechanisms
- Provides health monitoring
"""

import sys
import os
import argparse
import subprocess
import time
import threading
import signal
from pathlib import Path
from typing import Optional
import logging

# Add src to path
src_path = Path(__file__).parent.parent.parent / "src"
sys.path.insert(0, str(src_path))

try:
    from services.real_time_service import start_real_time_service, stop_real_time_service
    from services.real_time_service import RealTimeServiceContext
    REAL_TIME_AVAILABLE = True
except ImportError:
    REAL_TIME_AVAILABLE = False
    print("⚠️ Real-time service not available. Running in basic mode.")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DynamicDashboardLauncher:
    """Manages the dynamic dashboard launch process"""
    
    def __init__(self):
        self.streamlit_process: Optional[subprocess.Popen] = None
        self.real_time_service = None
        self.websocket_server = None
        self.running = False
        
    def setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def start_real_time_services(self):
        """Start real-time data services"""
        if REAL_TIME_AVAILABLE:
            try:
                logger.info("Starting real-time data services...")
                self.real_time_service = start_real_time_service()
                logger.info("✅ Real-time services started successfully")
                return True
            except Exception as e:
                logger.error(f"❌ Failed to start real-time services: {e}")
                return False
        else:
            logger.warning("⚠️ Real-time services not available")
            return False
    
    def start_streamlit_app(self, port: int = 8502, host: str = "localhost"):
        """Start the Streamlit dashboard application"""
        try:
            dashboard_path = src_path / "interfaces" / "dynamic_dashboard.py"
            
            if not dashboard_path.exists():
                logger.error(f"❌ Dashboard file not found: {dashboard_path}")
                return False
            
            logger.info(f"Starting Streamlit dashboard on {host}:{port}...")
            
            # Streamlit command
            cmd = [
                sys.executable, "-m", "streamlit", "run",
                str(dashboard_path),
                "--server.port", str(port),
                "--server.address", host,
                "--server.headless", "true",
                "--server.runOnSave", "true",
                "--browser.gatherUsageStats", "false"
            ]
            
            # Start Streamlit process
            self.streamlit_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitor Streamlit output in a separate thread
            threading.Thread(
                target=self._monitor_streamlit_output,
                daemon=True
            ).start()
            
            # Wait a moment to check if it started successfully
            time.sleep(2)
            
            if self.streamlit_process.poll() is None:
                logger.info(f"✅ Streamlit dashboard started successfully")
                logger.info(f"🌐 Access dashboard at: http://{host}:{port}")
                return True
            else:
                logger.error("❌ Streamlit failed to start")
                return False
                
        except Exception as e:
            logger.error(f"❌ Error starting Streamlit: {e}")
            return False
    
    def _monitor_streamlit_output(self):
        """Monitor Streamlit process output"""
        if not self.streamlit_process:
            return
        
        try:
            # Read stdout
            for line in iter(self.streamlit_process.stdout.readline, ''):
                if line.strip():
                    if "You can now view your Streamlit app" in line:
                        logger.info("🎉 Dashboard is ready!")
                    elif "ERROR" in line.upper() or "EXCEPTION" in line.upper():
                        logger.error(f"Streamlit error: {line.strip()}")
                    else:
                        logger.debug(f"Streamlit: {line.strip()}")
        except Exception as e:
            logger.error(f"Error monitoring Streamlit output: {e}")
    
    def check_health(self) -> dict:
        """Check health of all services"""
        health = {
            'streamlit': False,
            'real_time_service': False,
            'overall': False
        }
        
        # Check Streamlit
        if self.streamlit_process and self.streamlit_process.poll() is None:
            health['streamlit'] = True
        
        # Check real-time service
        if self.real_time_service and REAL_TIME_AVAILABLE:
            health['real_time_service'] = True
        
        # Overall health
        health['overall'] = health['streamlit']
        
        return health
    
    def display_status(self):
        """Display current status"""
        health = self.check_health()
        
        print("\n" + "="*50)
        print("🚀 DYNAMIC DASHBOARD STATUS")
        print("="*50)
        print(f"📊 Streamlit Dashboard: {'✅ Running' if health['streamlit'] else '❌ Stopped'}")
        print(f"⚡ Real-time Services: {'✅ Running' if health['real_time_service'] else '❌ Not Available'}")
        print(f"🌐 Overall Status: {'✅ Healthy' if health['overall'] else '❌ Issues Detected'}")
        
        if health['streamlit']:
            print(f"🔗 Dashboard URL: http://localhost:8502")
        
        print("="*50)
    
    def launch(self, port: int = 8502, host: str = "localhost", 
               enable_real_time: bool = True):
        """Launch the complete dynamic dashboard system"""
        logger.info("🚀 Starting Dynamic Trading Dashboard...")
        
        self.running = True
        success = True
        
        # Setup signal handlers
        self.setup_signal_handlers()
        
        # Start real-time services if enabled
        if enable_real_time:
            if not self.start_real_time_services():
                logger.warning("⚠️ Continuing without real-time services")
        
        # Start Streamlit dashboard
        if not self.start_streamlit_app(port, host):
            logger.error("❌ Failed to start dashboard")
            self.shutdown()
            return False
        
        # Display status
        time.sleep(3)  # Give services time to fully start
        self.display_status()
        
        return True
    
    def run_forever(self):
        """Run the dashboard system until interrupted"""
        try:
            logger.info("🔄 Dashboard system running. Press Ctrl+C to stop.")
            
            while self.running:
                # Periodic health check
                health = self.check_health()
                
                if not health['overall']:
                    logger.warning("⚠️ Health check failed, attempting restart...")
                    # Could implement auto-restart logic here
                
                time.sleep(30)  # Health check every 30 seconds
                
        except KeyboardInterrupt:
            logger.info("👋 Shutdown requested by user")
        finally:
            self.shutdown()
    
    def shutdown(self):
        """Gracefully shutdown all services"""
        logger.info("🛑 Shutting down dashboard system...")
        
        self.running = False
        
        # Stop Streamlit
        if self.streamlit_process:
            logger.info("Stopping Streamlit dashboard...")
            self.streamlit_process.terminate()
            try:
                self.streamlit_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning("Force killing Streamlit process...")
                self.streamlit_process.kill()
        
        # Stop real-time services
        if REAL_TIME_AVAILABLE:
            logger.info("Stopping real-time services...")
            stop_real_time_service()
        
        logger.info("✅ Shutdown complete")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description="Launch Dynamic Trading Dashboard",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_dynamic_dashboard.py                    # Start with defaults
  python launch_dynamic_dashboard.py --port 8503       # Custom port
  python launch_dynamic_dashboard.py --no-real-time    # Disable real-time features
  python launch_dynamic_dashboard.py --host 0.0.0.0    # Allow external access
        """
    )
    
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8502,
        help="Port for the dashboard (default: 8502)"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="localhost",
        help="Host address (default: localhost)"
    )
    
    parser.add_argument(
        "--no-real-time",
        action="store_true",
        help="Disable real-time data services"
    )
    
    parser.add_argument(
        "--status-only",
        action="store_true",
        help="Show status and exit"
    )
    
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Create launcher
    launcher = DynamicDashboardLauncher()
    
    if args.status_only:
        launcher.display_status()
        return
    
    # Launch dashboard
    enable_real_time = not args.no_real_time
    
    print(f"""
🚀 Dynamic Trading Dashboard Launcher
=====================================
📊 Dashboard Port: {args.port}
🌐 Host: {args.host}
⚡ Real-time Services: {'Enabled' if enable_real_time else 'Disabled'}
🔧 Verbose Logging: {'Enabled' if args.verbose else 'Disabled'}
=====================================
    """)
    
    if launcher.launch(args.port, args.host, enable_real_time):
        launcher.run_forever()
    else:
        logger.error("❌ Failed to launch dashboard system")
        sys.exit(1)

if __name__ == "__main__":
    main()