#!/usr/bin/env python3
"""
Enhanced Trading Bot with LLM Integration

This script provides a command-line interface for running the trading bot
with various LLM providers for AI-powered trading decisions.
"""

import argparse
import sys
from pathlib import Path

# Import the trading script functions
from trading_script import main as trading_main, LLM_AVAILABLE, get_llm_manager


def list_available_providers():
    """List available LLM providers."""
    if not LLM_AVAILABLE:
        print("❌ LLM interface not available. Run: pip install -r requirements.txt")
        return []
    
    llm_manager = get_llm_manager()
    if llm_manager:
        available = llm_manager.get_available_providers()
        if available:
            print("✅ Available LLM providers:")
            for provider in available:
                print(f"   🤖 {provider}")
        else:
            print("⚠️  No LLM providers configured. Run: python setup_llm.py")
        return available
    else:
        print("❌ Failed to initialize LLM manager")
        return []


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="ChatGPT Micro-Cap Trading Bot with LLM Integration",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python trading_bot.py                                    # Manual trading only
  python trading_bot.py --ai                             # Use AI with best available provider
  python trading_bot.py --ai --provider openai           # Use specific provider
  python trading_bot.py --list-providers                 # Show available providers
  python trading_bot.py --data-dir "My Data"            # Use custom data directory

Supported LLM Providers:
  • openai     - OpenAI GPT models (requires API key)
  • anthropic  - Anthropic Claude models (requires API key) 
  • ollama     - Local Ollama models (free, requires ollama)
  • huggingface - Local Hugging Face models (free, requires transformers)

Setup:
  1. Run: python setup_llm.py
  2. Configure API keys in .env file or install Ollama
  3. Run with --ai flag for AI recommendations
        """
    )
    
    parser.add_argument(
        "--ai", 
        action="store_true", 
        help="Enable AI trading recommendations"
    )
    
    parser.add_argument(
        "--provider", 
        type=str, 
        choices=["openai", "anthropic", "ollama", "huggingface"],
        help="Specific LLM provider to use"
    )
    
    parser.add_argument(
        "--data-dir", 
        type=str, 
        default="Scripts and CSV Files",
        help="Directory for portfolio and trade data (default: 'Scripts and CSV Files')"
    )
    
    parser.add_argument(
        "--portfolio-file", 
        type=str, 
        help="Specific portfolio CSV file to use"
    )
    
    parser.add_argument(
        "--list-providers", 
        action="store_true",
        help="List available LLM providers and exit"
    )
    
    parser.add_argument(
        "--setup", 
        action="store_true",
        help="Run LLM setup wizard"
    )
    
    args = parser.parse_args()
    
    # Handle special commands
    if args.list_providers:
        list_available_providers()
        return
    
    if args.setup:
        import subprocess
        subprocess.run([sys.executable, "setup_llm.py"])
        return
    
    # Validate AI options
    if args.ai and not LLM_AVAILABLE:
        print("❌ LLM interface not available. Install dependencies:")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    if args.ai:
        available_providers = []
        llm_manager = get_llm_manager()
        if llm_manager:
            available_providers = llm_manager.get_available_providers()
        
        if not available_providers:
            print("❌ No LLM providers available. Run setup:")
            print("   python setup_llm.py")
            sys.exit(1)
        
        if args.provider and args.provider not in available_providers:
            print(f"❌ Provider '{args.provider}' not available.")
            print("Available providers:", ", ".join(available_providers))
            sys.exit(1)
        
        if not args.provider:
            # Use the first available provider
            args.provider = available_providers[0]
            print(f"🤖 Using AI provider: {args.provider}")
    
    # Set up file paths
    data_dir = Path(args.data_dir)
    if args.portfolio_file:
        portfolio_file = args.portfolio_file
    else:
        portfolio_file = str(data_dir / "chatgpt_portfolio_update.csv")
    
    # Display configuration
    print("🚀 Starting ChatGPT Micro-Cap Trading Bot")
    print("=" * 50)
    print(f"📁 Data directory: {data_dir}")
    print(f"📊 Portfolio file: {portfolio_file}")
    
    if args.ai:
        print(f"🤖 AI Provider: {args.provider}")
        print("✨ AI recommendations: ENABLED")
    else:
        print("👤 Mode: Manual trading only")
    
    print("=" * 50)
    
    # Run the trading script
    try:
        trading_main(
            file=portfolio_file,
            data_dir=data_dir,
            use_llm=args.ai,
            llm_provider=args.provider
        )
    except KeyboardInterrupt:
        print("\n⏹️  Trading session interrupted by user")
    except Exception as e:
        print(f"\n❌ Error during trading session: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()