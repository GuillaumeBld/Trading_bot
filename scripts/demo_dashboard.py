#!/usr/bin/env python3
"""
Dashboard Demo Script

This script demonstrates the advanced dashboard features and creates sample data
for testing purposes. It's useful for:
- Testing dashboard functionality
- Demonstrating features to new users
- Development and debugging
- Creating sample portfolios
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os
import random
from pathlib import Path

def create_sample_portfolio_data():
    """Create sample portfolio data for demonstration"""
    print("📊 Creating sample portfolio data...")
    
    # Ensure data directory exists
    data_dir = Path("Scripts and CSV Files")
    data_dir.mkdir(exist_ok=True)
    
    # Sample stock data
    stocks = [
        {"ticker": "ABEO", "name": "Abeona Therapeutics", "sector": "Healthcare"},
        {"ticker": "CADL", "name": "Candel Therapeutics", "sector": "Healthcare"}, 
        {"ticker": "CSAI", "name": "C3.ai Inc", "sector": "Technology"},
        {"ticker": "MNMD", "name": "Mind Medicine", "sector": "Healthcare"},
        {"ticker": "SAVA", "name": "Cassava Sciences", "sector": "Healthcare"}
    ]
    
    # Generate 60 days of sample data
    start_date = datetime.now() - timedelta(days=60)
    dates = [start_date + timedelta(days=i) for i in range(61)]
    
    # Initial portfolio setup
    initial_cash = 1000.0
    current_cash = 150.0
    
    # Sample positions
    positions = [
        {"ticker": "ABEO", "shares": 50, "cost_basis": 4.20, "stop_loss": 3.57},
        {"ticker": "CADL", "shares": 40, "cost_basis": 5.80, "stop_loss": 4.93},
        {"ticker": "CSAI", "shares": 25, "cost_basis": 12.40, "stop_loss": 10.54},
    ]
    
    portfolio_data = []
    trade_data = []
    
    # Generate daily portfolio snapshots
    for i, date in enumerate(dates):
        # Simulate price movements
        total_value = current_cash
        
        for pos in positions:
            # Random walk with slight upward bias for demo
            if i == 0:
                current_price = pos["cost_basis"]
            else:
                prev_price = portfolio_data[-1][f"{pos['ticker']}_price"] if portfolio_data else pos["cost_basis"]
                change = np.random.normal(0.01, 0.05)  # Small upward bias
                current_price = max(0.1, prev_price * (1 + change))
            
            position_value = pos["shares"] * current_price
            total_value += position_value
            
            # Add position data
            portfolio_data.append({
                "Date": date.strftime("%Y-%m-%d"),
                "Ticker": pos["ticker"],
                "Shares": pos["shares"],
                "Cost Basis": pos["cost_basis"],
                "Stop Loss": pos["stop_loss"],
                "Current Price": round(current_price, 2),
                "Total Value": round(position_value, 2),
                "PnL": round((current_price - pos["cost_basis"]) * pos["shares"], 2),
                "Action": "HOLD",
                "Cash Balance": current_cash,
                "Total Equity": round(total_value, 2)
            })
            
            # Store price for next iteration
            if f"{pos['ticker']}_price" not in locals():
                locals()[f"{pos['ticker']}_price"] = current_price
        
        # Add benchmark data (S&P 500 simulation)
        if i == 0:
            benchmark_value = initial_cash
        else:
            benchmark_change = np.random.normal(0.0003, 0.015)  # Typical S&P 500 daily return
            benchmark_value = benchmark_value * (1 + benchmark_change)
        
        # Update last row with benchmark
        if portfolio_data:
            portfolio_data[-1]["Benchmark"] = round(benchmark_value, 2)
    
    # Create portfolio DataFrame
    portfolio_df = pd.DataFrame(portfolio_data)
    
    # Generate some sample trades
    trade_dates = [
        start_date + timedelta(days=0),   # Initial buys
        start_date + timedelta(days=15),  # Additional buy
        start_date + timedelta(days=30),  # Sell some position
        start_date + timedelta(days=45),  # Another buy
    ]
    
    sample_trades = [
        {
            "Date": trade_dates[0].strftime("%Y-%m-%d"),
            "Ticker": "ABEO",
            "Shares Bought": 30,
            "Buy Price": 4.20,
            "Cost Basis": 126.0,
            "PnL": 0.0,
            "Reason": "Initial position - AI recommendation with high confidence (0.85)",
            "Shares Sold": 0,
            "Sell Price": 0.0
        },
        {
            "Date": trade_dates[0].strftime("%Y-%m-%d"),
            "Ticker": "CADL",
            "Shares Bought": 40,
            "Buy Price": 5.80,
            "Cost Basis": 232.0,
            "PnL": 0.0,
            "Reason": "Biotech catalyst play - Phase 2 results expected",
            "Shares Sold": 0,
            "Sell Price": 0.0
        },
        {
            "Date": trade_dates[1].strftime("%Y-%m-%d"),
            "Ticker": "ABEO",
            "Shares Bought": 20,
            "Buy Price": 3.95,
            "Cost Basis": 79.0,
            "PnL": 0.0,
            "Reason": "Adding to winning position on dip",
            "Shares Sold": 0,
            "Sell Price": 0.0
        },
        {
            "Date": trade_dates[2].strftime("%Y-%m-%d"),
            "Ticker": "CSAI",
            "Shares Bought": 25,
            "Buy Price": 12.40,
            "Cost Basis": 310.0,
            "PnL": 0.0,
            "Reason": "AI sector momentum - diversification play",
            "Shares Sold": 0,
            "Sell Price": 0.0
        },
        {
            "Date": trade_dates[3].strftime("%Y-%m-%d"),
            "Ticker": "CADL",
            "Shares Bought": 0,
            "Buy Price": 0.0,
            "Cost Basis": 0.0,
            "PnL": 45.0,
            "Reason": "Partial profit taking - 25% of position",
            "Shares Sold": 10,
            "Sell Price": 6.30
        }
    ]
    
    trades_df = pd.DataFrame(sample_trades)
    
    # Save to CSV files
    portfolio_file = data_dir / "chatgpt_portfolio_update.csv"
    trades_file = data_dir / "chatgpt_trade_log.csv"
    
    portfolio_df.to_csv(portfolio_file, index=False)
    trades_df.to_csv(trades_file, index=False)
    
    print(f"✅ Created {len(portfolio_df)} portfolio records")
    print(f"✅ Created {len(trades_df)} trade records")
    print(f"📁 Files saved to: {data_dir}")
    
    return portfolio_df, trades_df

def create_sample_configuration():
    """Create sample configuration files"""
    print("⚙️ Creating sample configuration...")
    
    # Create sample .env file (without real API keys)
    env_content = """# ChatGPT Micro-Cap Trading Bot Configuration
# Replace with your actual API keys

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here

# Anthropic Configuration  
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# News API Configuration
NEWS_API_KEY=your-newsapi-key-here

# Alpaca Trading Configuration (Paper Trading)
ALPACA_API_KEY=your-alpaca-key-here
ALPACA_SECRET_KEY=your-alpaca-secret-here

# Optional: Custom API endpoints
# OPENAI_BASE_URL=https://api.openai.com/v1
# ANTHROPIC_BASE_URL=https://api.anthropic.com
"""
    
    # Create sample LLM config
    llm_config = {
        "openai": {
            "model_name": "gpt-4o-mini",
            "temperature": 0.1,
            "max_tokens": 2000,
            "enabled": False
        },
        "anthropic": {
            "model_name": "claude-3-haiku-20240307",
            "temperature": 0.1,
            "max_tokens": 2000,
            "enabled": False
        },
        "ollama": {
            "model_name": "llama3.1:8b",
            "temperature": 0.1,
            "max_tokens": 2000,
            "enabled": True
        }
    }
    
    # Save configuration files
    with open(".env.example", "w") as f:
        f.write(env_content)
    
    with open(".llm_config.json", "w") as f:
        json.dump(llm_config, f, indent=2)
    
    print("✅ Created .env.example (rename to .env and add your keys)")
    print("✅ Created .llm_config.json with default settings")

def create_sample_news_data():
    """Create sample news data for testing"""
    print("📰 Creating sample news data...")
    
    # This would normally be fetched from a news API
    sample_news = [
        {
            "title": "Small-Cap Biotech Stocks Rally on FDA Approval Hopes",
            "summary": "Several micro-cap biotechnology companies saw significant gains today as investors bet on upcoming FDA decisions for experimental treatments.",
            "source": "BioPharma Dive",
            "published_at": (datetime.now() - timedelta(hours=2)).isoformat(),
            "sentiment": "positive"
        },
        {
            "title": "Market Volatility Creates Opportunities in Micro-Cap Space",
            "summary": "Professional traders are finding new opportunities in the micro-cap market as increased volatility creates pricing inefficiencies.",
            "source": "MarketWatch",
            "published_at": (datetime.now() - timedelta(hours=4)).isoformat(),
            "sentiment": "neutral"
        },
        {
            "title": "AI Sector Continues Strong Performance Despite Market Concerns",
            "summary": "Artificial intelligence companies, including smaller players, continue to attract investor interest despite broader market uncertainties.",
            "source": "TechCrunch",
            "published_at": (datetime.now() - timedelta(hours=6)).isoformat(),
            "sentiment": "positive"
        }
    ]
    
    # Save sample news data
    with open("sample_news.json", "w") as f:
        json.dump(sample_news, f, indent=2)
    
    print("✅ Created sample_news.json for testing")

def display_demo_info():
    """Display information about the demo"""
    print("\n" + "="*60)
    print("🎯 DASHBOARD DEMO READY")
    print("="*60)
    
    print("\n📊 Sample Data Created:")
    print("   • 60 days of portfolio history")
    print("   • 3 active positions (ABEO, CADL, CSAI)")
    print("   • 5 historical trades")
    print("   • Performance metrics and benchmarks")
    print("   • Sample news and market data")
    
    print("\n🚀 Next Steps:")
    print("   1. Launch the dashboard:")
    print("      python launch_dashboard.py --advanced")
    print("   2. Open browser to: http://localhost:8502")
    print("   3. Explore all dashboard features")
    print("   4. Configure real API keys when ready")
    
    print("\n⚙️ Configuration:")
    print("   • Edit .env file with your API keys")
    print("   • Ollama is enabled by default (free)")
    print("   • All other providers need API keys")
    
    print("\n🔧 Demo Features:")
    print("   • Performance tracking with metrics")
    print("   • Position analysis and risk management")
    print("   • Market data and news integration")
    print("   • AI insights and configuration")
    print("   • Complete settings management")
    
    print("\n📚 Documentation:")
    print("   • Dashboard Guide: docs/usage/dashboard-guide.md")
    print("   • Configuration: docs/configuration/overview.md")
    print("   • Troubleshooting: docs/troubleshooting/faq.md")

def main():
    """Main demo setup function"""
    print("🎭 ChatGPT Micro-Cap Trading Bot - Dashboard Demo Setup")
    print("="*55)
    
    try:
        # Create all sample data
        create_sample_portfolio_data()
        create_sample_configuration()
        create_sample_news_data()
        
        # Display completion info
        display_demo_info()
        
        # Ask if user wants to launch dashboard
        print("\n" + "="*60)
        launch = input("🚀 Launch the advanced dashboard now? (y/N): ").strip().lower()
        
        if launch in ['y', 'yes']:
            print("\n🚀 Launching Advanced Dashboard...")
            import subprocess
            import sys
            
            try:
                subprocess.run([
                    sys.executable, "-m", "streamlit", "run", "advanced_dashboard.py",
                    "--server.headless", "true",
                    "--server.address", "0.0.0.0", 
                    "--server.port", "8502"
                ], check=True)
            except KeyboardInterrupt:
                print("\n👋 Dashboard stopped by user")
            except FileNotFoundError:
                print("❌ Streamlit not found. Install with: pip install streamlit")
            except Exception as e:
                print(f"❌ Error launching dashboard: {e}")
                print("💡 Try: python launch_dashboard.py --advanced")
        else:
            print("\n👍 Demo data ready! Launch when you're ready:")
            print("   python launch_dashboard.py --advanced")
    
    except Exception as e:
        print(f"❌ Error setting up demo: {e}")
        print("💡 Make sure you have write permissions in this directory")

if __name__ == "__main__":
    main()