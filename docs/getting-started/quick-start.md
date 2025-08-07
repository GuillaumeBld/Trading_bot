# Quick Start Guide

Get up and running with the ChatGPT Micro-Cap Trading Bot in under 5 minutes!

## 🚀 30-Second Overview

This trading bot helps you manage a micro-cap stock portfolio with optional AI assistance. You can trade manually or get AI-powered recommendations from OpenAI, Anthropic, Ollama, or Hugging Face models.

## ⚡ Quick Setup

### Option 1: Manual Trading Only (Fastest)
```bash
# 1. Clone or download the project
git clone https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment

# 2. Install dependencies
pip install pandas yfinance numpy matplotlib streamlit

# 3. Start trading
python trading_bot.py
```

### Option 2: AI-Enhanced Trading (Recommended)
```bash
# 1. Install all dependencies
pip install -r requirements.txt

# 2. Run setup wizard
python setup_llm.py

# 3. Start AI-powered trading
python trading_bot.py --ai
```

### Option 3: Web Interface (Easiest)
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start web interface
streamlit run streamlit_app.py

# 3. Open browser to http://localhost:8501
```

## 🎯 Your First Trade

### Manual Trading
1. Run `python trading_bot.py`
2. When prompted, enter your starting cash amount
3. Choose 'b' to buy a stock
4. Enter ticker, shares, price, and stop-loss
5. The system tracks everything automatically

### AI Trading
1. Run `python trading_bot.py --ai` 
2. The AI analyzes market data and suggests trades
3. Review each recommendation
4. Type 'y' to accept or 'n' to skip
5. Watch your portfolio grow with AI assistance!

## 📊 Understanding the Output

After each trading session, you'll see:
- **Portfolio Summary**: Your current holdings and cash
- **Performance Metrics**: Sharpe ratio, total return vs S&P 500
- **Market Data**: Price updates for your stocks and benchmarks
- **AI Recommendations**: Detailed reasoning for each suggestion (if using AI)

## 📁 Important Files

- **`chatgpt_portfolio_update.csv`** - Daily portfolio snapshots
- **`chatgpt_trade_log.csv`** - Complete trade history
- **`.env`** - API keys for AI providers (create this)
- **`.llm_config.json`** - AI model settings (auto-generated)

## 🔧 Quick Configuration

### Add AI Provider (Optional)
1. Get API key from [OpenAI](https://platform.openai.com/api-keys) or [Anthropic](https://console.anthropic.com/)
2. Create `.env` file with: `OPENAI_API_KEY=your_key_here`
3. Run `python trading_bot.py --ai --provider openai`

### Or Use Free Local AI
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Start service: `ollama serve`
3. Pull model: `ollama pull llama3.1:8b`
4. Run: `python trading_bot.py --ai --provider ollama`

## 🆘 Need Help?

- **Common Issues**: Check [troubleshooting guide](../troubleshooting/common-issues.md)
- **Detailed Setup**: See [installation guide](../installation/basic-setup.md)
- **AI Configuration**: Read [LLM provider guides](../llm-providers/comparison.md)
- **Usage Questions**: Browse [FAQ](../troubleshooting/faq.md)

## ➡️ Next Steps

Once you're up and running:

1. **Learn the Interface**: Try [Web Interface Guide](../usage/web-interface.md)
2. **Configure AI**: Set up your preferred [LLM Provider](../llm-providers/comparison.md)
3. **Understand Strategy**: Read [AI Trading Guide](../usage/ai-trading.md)
4. **Analyze Performance**: Follow [Data Analysis Tutorial](../tutorials/data-analysis.md)

---

**🎉 Congratulations!** You're now ready to start micro-cap trading with AI assistance. The system will handle all the tracking, risk management, and performance analysis automatically.

**⚠️ Important**: This is for educational/experimental purposes. Only invest money you can afford to lose, and always do your own research before making trading decisions.