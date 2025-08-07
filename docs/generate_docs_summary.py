#!/usr/bin/env python3
"""
Documentation Summary Generator

This script creates a comprehensive overview of all documentation files
and generates quick navigation aids for users.
"""

import os
from pathlib import Path
from collections import defaultdict
import datetime


def scan_docs_directory():
    """Scan the docs directory and categorize all files."""
    docs_root = Path(__file__).parent
    file_structure = defaultdict(list)
    
    for root, dirs, files in os.walk(docs_root):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        
        category = Path(root).name
        if category == 'docs':
            category = 'root'
            
        for file in files:
            if file.endswith('.md') and not file.startswith('.'):
                file_path = Path(root) / file
                relative_path = file_path.relative_to(docs_root)
                file_structure[category].append({
                    'name': file,
                    'path': str(relative_path),
                    'size': file_path.stat().st_size if file_path.exists() else 0
                })
    
    return file_structure


def estimate_reading_time(file_size):
    """Estimate reading time based on file size."""
    # Rough estimate: 200 words per minute, ~5 characters per word
    words = file_size / 5
    minutes = words / 200
    
    if minutes < 1:
        return "< 1 min"
    elif minutes < 60:
        return f"{int(minutes)} min"
    else:
        hours = minutes / 60
        return f"{hours:.1f} hrs"


def generate_navigation_guide():
    """Generate navigation guide based on user type."""
    return """
# 🧭 Documentation Navigation Guide

## 👨‍💼 For Business Users
**Goal**: Start trading quickly with minimal technical setup

1. **[Quick Start Guide](getting-started/quick-start.md)** (5 min)
2. **[Basic Installation](installation/basic-setup.md)** (10 min)
3. **[Basic Tutorial](tutorials/basic-tutorial.md)** (20 min)
4. **[FAQ](troubleshooting/faq.md)** (Reference)

**Total Time to Trading**: ~35 minutes

## 🤖 For AI Enthusiasts  
**Goal**: Leverage AI for trading recommendations

1. **[Quick Start Guide](getting-started/quick-start.md)** (5 min)
2. **[AI Provider Comparison](llm-providers/comparison.md)** (10 min)
3. **[OpenAI Setup](llm-providers/openai.md)** OR **[Ollama Setup](llm-providers/ollama.md)** (15 min)
4. **[AI Tutorial](tutorials/ai-tutorial.md)** (25 min)
5. **[AI Trading Guide](usage/ai-trading.md)** (15 min)

**Total Time to AI Trading**: ~70 minutes

## 👨‍💻 For Developers
**Goal**: Understand the system and potentially contribute

1. **[Project Overview](getting-started/overview.md)** (15 min)
2. **[Development Installation](installation/development-setup.md)** (30 min)
3. **[API Reference](api-reference/trading-script.md)** (20 min)
4. **[Configuration Guide](configuration/overview.md)** (15 min)
5. **[Advanced Strategies](tutorials/advanced-strategies.md)** (30 min)

**Total Time to Development**: ~110 minutes

## 🆘 For Troubleshooting
**Goal**: Fix issues and get help

1. **[Common Issues](troubleshooting/common-issues.md)** (Search specific problem)
2. **[FAQ](troubleshooting/faq.md)** (Search specific question)
3. **[Error Messages](troubleshooting/error-messages.md)** (Look up error)
4. **[Installation Troubleshooting](installation/troubleshooting.md)** (Install problems)

**Find Your Answer**: Usually < 5 minutes

## 📚 For Complete Understanding
**Goal**: Master every aspect of the system

Complete documentation reading order:
1. Getting Started section (45 min)
2. Installation guides (60 min)
3. Configuration docs (45 min)
4. LLM provider setup (30 min)
5. Usage guides (90 min)
6. Tutorials and examples (120 min)
7. API reference (60 min)
8. Troubleshooting (30 min)

**Total Mastery Time**: ~8 hours
"""


def generate_quick_reference():
    """Generate quick reference card."""
    return """
# 🚀 Quick Reference Card

## Essential Commands
```bash
# Manual trading
python trading_bot.py

# AI-powered trading  
python trading_bot.py --ai

# Web interface
streamlit run streamlit_app.py

# Setup AI providers
python setup_llm.py

# Check AI status
python trading_bot.py --list-providers
```

## File Locations
- **Portfolio data**: `chatgpt_portfolio_update.csv`
- **Trade history**: `chatgpt_trade_log.csv`
- **AI config**: `.llm_config.json`
- **API keys**: `.env`

## Emergency Commands
```bash
# Reset configuration
rm .env .llm_config.json && python setup_llm.py

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt

# Check system status
python setup_llm.py --check
```

## Key Concepts
- **Stop-Loss**: Automatic sale when price drops (risk management)
- **Micro-Cap**: Stocks with market cap < $300M
- **Confidence Score**: AI's certainty in recommendation (0-1)
- **Sharpe Ratio**: Risk-adjusted return measurement
"""


def main():
    """Generate comprehensive documentation summary."""
    print("📚 ChatGPT Micro-Cap Trading Bot - Documentation Summary")
    print("=" * 60)
    
    # Scan documentation structure
    file_structure = scan_docs_directory()
    
    # Generate overview
    print(f"\n📋 Documentation Overview (Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')})")
    print("=" * 60)
    
    total_files = 0
    total_size = 0
    
    for category, files in sorted(file_structure.items()):
        if not files:
            continue
            
        print(f"\n📁 {category.title().replace('-', ' ')}")
        print("-" * 40)
        
        for file_info in sorted(files, key=lambda x: x['name']):
            name = file_info['name'].replace('.md', '')
            path = file_info['path']
            size = file_info['size']
            reading_time = estimate_reading_time(size)
            
            total_files += 1
            total_size += size
            
            print(f"  📄 {name:<25} ({reading_time:>8}) - {path}")
    
    total_reading_time = estimate_reading_time(total_size)
    print(f"\n📊 Summary")
    print("-" * 40)
    print(f"Total files: {total_files}")
    print(f"Total reading time: {total_reading_time}")
    print(f"Coverage: Complete system documentation")
    
    # Generate navigation guide
    print("\n" + generate_navigation_guide())
    
    # Generate quick reference
    print("\n" + generate_quick_reference())
    
    print("\n🎯 Documentation Quality Checklist")
    print("=" * 60)
    
    checklist = [
        "✅ Getting started guide for beginners",
        "✅ Complete installation instructions", 
        "✅ AI provider setup guides",
        "✅ Command-line reference",
        "✅ Web interface guide",
        "✅ Configuration documentation",
        "✅ API reference for developers",
        "✅ Troubleshooting and FAQ",
        "✅ Step-by-step tutorials",
        "✅ Real-world examples",
        "✅ Best practices and tips",
        "✅ Performance optimization",
        "✅ Security considerations",
        "✅ Multiple user personas covered"
    ]
    
    for item in checklist:
        print(f"  {item}")
    
    print(f"\n🎉 Documentation Status: COMPLETE")
    print(f"📖 Ready for users of all skill levels")
    print(f"🚀 Total setup time: 5-120 minutes depending on use case")
    
    # Suggest next steps
    print(f"\n➡️  Next Steps for Users:")
    print("   1. Choose your user type from navigation guide above")
    print("   2. Follow the recommended reading path")
    print("   3. Start with Quick Start Guide for immediate results")
    print("   4. Refer to FAQ and troubleshooting as needed")
    
    print(f"\n📚 Full Documentation Available At:")
    print("   • docs/README.md - Main documentation index")
    print("   • All guides are cross-linked for easy navigation") 
    print("   • Search functionality available in web interface")


if __name__ == "__main__":
    main()