#!/usr/bin/env python3
"""
Launch script for the AI Trading Bot CLI
"""

import sys
import argparse
from pathlib import Path

def main():
    """Launch the trading bot CLI"""
    parser = argparse.ArgumentParser(description="AI-Powered Trading Bot")
    parser.add_argument("--ai-enabled", action="store_true", help="Enable AI recommendations")
    parser.add_argument("--provider", default="openai", help="LLM provider (openai, anthropic, ollama)")
    parser.add_argument("--mode", default="paper", help="Trading mode (paper, live)")
    parser.add_argument("--symbols", help="Comma-separated list of symbols to analyze")
    parser.add_argument("--analyze-only", action="store_true", help="Only analyze, don't trade")
    
    args = parser.parse_args()
    
    # Add src to Python path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))
    
    try:
        from core.trading_script import main as trading_main
        trading_main(args)
    except ImportError:
        print("Trading core not found. Please ensure all files are properly installed.")
        print("Run: pip install -r requirements.txt")

if __name__ == "__main__":
    main()