#!/usr/bin/env python3
"""
LLM Setup and Configuration Script for ChatGPT Micro-Cap Trading Experiment

This script helps users configure their LLM providers for AI-powered trading recommendations.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any

def create_env_template():
    """Create a .env template file for API keys."""
    env_content = """# LLM API Keys Configuration
# Uncomment and fill in the API keys for the providers you want to use

# OpenAI API Key (get from https://platform.openai.com/api-keys)
# OPENAI_API_KEY=your_openai_api_key_here

# Anthropic API Key (get from https://console.anthropic.com/)
# ANTHROPIC_API_KEY=your_anthropic_api_key_here

# For local models, no API keys needed
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    print(" Created .env template file")
    print(" Edit .env file to add your API keys")


def create_llm_config():
    """Create LLM configuration file."""
    config = {
        "openai": {
            "model_name": "gpt-4o-mini",
            "temperature": 0.1,
            "max_tokens": 2000,
            "system_prompt": "You are an expert micro-cap stock analyst focused on generating maximum risk-adjusted returns."
        },
        "anthropic": {
            "model_name": "claude-3-haiku-20240307",
            "temperature": 0.1,
            "max_tokens": 2000,
            "system_prompt": "You are an expert micro-cap stock analyst focused on generating maximum risk-adjusted returns."
        },
        "ollama": {
            "model_name": "llama3.1:8b",
            "base_url": "http://localhost:11434",
            "temperature": 0.1,
            "max_tokens": 2000,
            "system_prompt": "You are an expert micro-cap stock analyst focused on generating maximum risk-adjusted returns."
        },
        "huggingface": {
            "model_name": "microsoft/DialoGPT-medium",
            "temperature": 0.1,
            "max_tokens": 1000,
            "system_prompt": "You are an expert micro-cap stock analyst focused on generating maximum risk-adjusted returns."
        }
    }
    
    with open(".llm_config.json", "w") as f:
        json.dump(config, f, indent=2)
    print(" Created .llm_config.json with default settings")


def check_provider_availability():
    """Check which LLM providers are available."""
    print("\n Checking LLM provider availability...\n")
    
    available_providers = []
    
    # Check OpenAI
    try:
        import openai
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            try:
                client = openai.OpenAI(api_key=api_key)
                client.models.list()
                print(" OpenAI: Available and configured")
                available_providers.append("openai")
            except Exception as e:
                print(f" OpenAI: API key invalid - {e}")
        else:
            print("  OpenAI: API key not configured")
    except ImportError:
        print(" OpenAI: Library not installed (pip install openai)")
    
    # Check Anthropic
    try:
        import anthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if api_key and api_key != "your_anthropic_api_key_here":
            try:
                client = anthropic.Anthropic(api_key=api_key)
                # Try a minimal test
                print(" Anthropic: Available and configured")
                available_providers.append("anthropic")
            except Exception as e:
                print(f" Anthropic: API key invalid - {e}")
        else:
            print("  Anthropic: API key not configured")
    except ImportError:
        print(" Anthropic: Library not installed (pip install anthropic)")
    
    # Check Ollama
    try:
        import ollama
        try:
            client = ollama.Client(host='http://localhost:11434')
            models = client.list()
            if models and 'models' in models:
                print(f" Ollama: Available with {len(models['models'])} models")
                available_providers.append("ollama")
                for model in models['models'][:3]:  # Show first 3 models
                    print(f"    {model['name']}")
                if len(models['models']) > 3:
                    print(f"   ... and {len(models['models']) - 3} more")
            else:
                print(" Ollama: No models found")
        except Exception as e:
            print(f" Ollama: Not running or inaccessible - {e}")
    except ImportError:
        print(" Ollama: Library not installed (pip install ollama)")
    
    # Check Hugging Face
    try:
        import transformers
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f" Hugging Face: Available (device: {device})")
        available_providers.append("huggingface")
    except ImportError:
        print(" Hugging Face: Libraries not installed (pip install transformers torch)")
    
    print(f"\n Summary: {len(available_providers)} provider(s) available")
    return available_providers


def install_ollama_guide():
    """Show guide for installing Ollama."""
    print("""
 Ollama Installation Guide:

1. Install Ollama:
   Mac/Linux: curl -fsSL https://ollama.ai/install.sh | sh
   Windows: Download from https://ollama.ai/download
   
2. Start Ollama service:
   ollama serve
   
3. Pull a recommended model:
   ollama pull llama3.1:8b       # 8B parameter model (4.7GB)
   ollama pull phi3:mini         # Smaller model (2.3GB)
   ollama pull mistral:7b        # Alternative 7B model (4.1GB)
   
4. Test the installation:
   ollama list
   
For trading, we recommend llama3.1:8b as it provides good analysis capabilities.
""")


def show_provider_setup_guide():
    """Show setup guide for each provider."""
    print("""
  LLM Provider Setup Guide:

 API-Based Providers (Remote):
  
   OpenAI GPT-4 (Recommended for best results)
     • Get API key: https://platform.openai.com/api-keys
     • Cost: ~$0.15-0.60 per query
     • Models: gpt-4o-mini, gpt-4o, gpt-4-turbo
  
    Anthropic Claude (Good alternative)
     • Get API key: https://console.anthropic.com/
     • Cost: ~$0.25-0.80 per query  
     • Models: claude-3-haiku, claude-3-sonnet, claude-3-opus

 Local Providers (Free but requires computation):
  
   Ollama (Easiest local setup)
     • Free and runs locally
     • Supports many open models
     • Good for privacy and unlimited usage
     • Requires 4-16GB RAM depending on model
  
   Hugging Face Transformers (Most flexible)
     • Free and runs locally
     • Requires Python ML setup
     • Can use GPU acceleration
     • Best for advanced users

 Recommendations:
   • Beginners: Start with OpenAI GPT-4o-mini ($0.15/query)
   • Privacy-focused: Use Ollama with llama3.1:8b
   • Advanced users: Hugging Face with local GPU
   • Budget-conscious: Anthropic Claude-3-haiku

After setup, use 'python setup_llm.py --check' to verify configuration.
""")


def main():
    """Main setup function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LLM Setup for Trading Bot")
    parser.add_argument("--check", action="store_true", help="Check provider availability")
    parser.add_argument("--ollama-guide", action="store_true", help="Show Ollama installation guide")
    parser.add_argument("--setup-guide", action="store_true", help="Show provider setup guide")
    parser.add_argument("--create-config", action="store_true", help="Create configuration files")
    
    args = parser.parse_args()
    
    if args.check:
        from dotenv import load_dotenv
        load_dotenv()
        check_provider_availability()
        return
    
    if args.ollama_guide:
        install_ollama_guide()
        return
        
    if args.setup_guide:
        show_provider_setup_guide()
        return
        
    if args.create_config:
        create_env_template()
        create_llm_config()
        return
    
    # Default: Interactive setup
    print(" LLM Setup for ChatGPT Micro-Cap Trading Experiment")
    print("=" * 60)
    
    print("\n1. Creating configuration files...")
    create_env_template()
    create_llm_config()
    
    print("\n2. Checking current availability...")
    from dotenv import load_dotenv
    load_dotenv()
    available = check_provider_availability()
    
    if not available:
        print("\n3. Next steps:")
        print("    Edit .env file to add API keys for remote providers")
        print("    Or install Ollama for local AI: python setup_llm.py --ollama-guide")
        print("    For detailed setup: python setup_llm.py --setup-guide")
    else:
        print(f"\n Setup complete! {len(available)} provider(s) ready to use.")
        print(" You can now enable AI recommendations in the trading interface.")


if __name__ == "__main__":
    main()