# Project Overview

##  What is the ChatGPT Micro-Cap Trading Bot?

The ChatGPT Micro-Cap Trading Bot is an advanced portfolio management system designed to trade micro-cap stocks (market cap < $300M) with optional AI assistance. It combines traditional trading logic with cutting-edge language models to provide intelligent trading recommendations while maintaining strict risk management.

##  The Experiment

This project originated as a 6-month live trading experiment to answer a fundamental question:

> **Can large language models like ChatGPT actually generate alpha (excess returns) in micro-cap stock trading?**

Starting with just $100, the experiment tracks every trade, decision, and outcome to provide transparent insights into AI-powered trading performance.

##  System Architecture

### Core Components

```
ChatGPT Micro-Cap Trading Bot
 Trading Engine (trading_script.py)
 AI Integration (llm_interface.py)
 Web Interface (streamlit_app.py)
 CLI Interface (trading_bot.py)
 Configuration (setup_llm.py)
 Data Management (CSV files)
```

### Data Flow
1. **Market Data**: Real-time prices from Yahoo Finance
2. **AI Analysis**: LLM processes portfolio and market data
3. **Decision Making**: User approves/rejects AI recommendations
4. **Execution**: Trades logged and portfolio updated
5. **Performance Tracking**: Metrics calculated and stored

##  AI Integration

### Supported LLM Providers

| Provider | Type | Cost | Best For |
|----------|------|------|----------|
| **OpenAI GPT-4** | API | $0.15-0.60/query | Best analysis quality |
| **Anthropic Claude** | API | $0.25-0.80/query | Alternative high quality |
| **Ollama** | Local | Free | Privacy & unlimited usage |
| **Hugging Face** | Local | Free | Customization & GPU acceleration |

### AI Capabilities
- **Technical Analysis**: Pattern recognition, trend analysis
- **Fundamental Analysis**: Financial metrics evaluation
- **Risk Assessment**: Portfolio correlation and volatility analysis
- **Catalyst Identification**: News events and timing analysis
- **Position Sizing**: Optimal allocation recommendations

##  Trading Strategy

### Micro-Cap Focus
- **Market Cap < $300M**: Focus on undervalued small companies
- **High Growth Potential**: Target companies with significant upside
- **Catalyst-Driven**: Look for specific events that could drive prices
- **Limited Coverage**: Exploit information inefficiencies

### Risk Management
- **Stop-Loss Automation**: 15-20% downside protection
- **Position Limits**: Maximum 5-7 positions for diversification
- **Cash Management**: Maintain liquidity for opportunities
- **Volatility Adjustment**: Position sizing based on stock volatility

### Decision Framework
1. **Screening**: Identify micro-cap opportunities
2. **Analysis**: Fundamental + technical + catalyst review
3. **Entry**: Precise timing with stop-loss placement
4. **Monitoring**: Daily price tracking and alerts
5. **Exit**: Profit taking or loss cutting based on rules

##  Safety Features

### Financial Safeguards
- **Capital Protection**: Never risk more than available cash
- **Price Validation**: Ensure trades within daily price ranges
- **Position Limits**: Prevent over-concentration in single stocks
- **Stop-Loss Enforcement**: Automatic position liquidation

### AI Safety
- **Confidence Scoring**: Filter low-confidence recommendations
- **Human Oversight**: User approval required for all trades
- **Fallback Modes**: System continues if AI unavailable
- **Audit Trail**: Complete logging of all AI decisions

### Data Privacy
- **Local Options**: Use Ollama/HuggingFace for offline AI
- **Secure Storage**: API keys in environment variables
- **No External Sharing**: Portfolio data stays local

##  Performance Tracking

### Key Metrics
- **Total Return**: Absolute and percentage gains/losses
- **Sharpe Ratio**: Risk-adjusted return measurement
- **Sortino Ratio**: Downside risk-adjusted returns
- **Maximum Drawdown**: Largest peak-to-trough decline
- **Win Rate**: Percentage of profitable trades

### Benchmarking
- **S&P 500**: Large-cap market comparison
- **Russell 2000**: Small-cap market comparison
- **Micro-cap Indices**: IWO, XBI sector comparisons

### Data Export
- **CSV Format**: Daily portfolio snapshots
- **Trade Logs**: Complete transaction history
- **Performance Charts**: Visual portfolio tracking
- **Custom Analysis**: Pandas-compatible data format

##  Use Cases

### Individual Traders
- **Learning Tool**: Understand micro-cap market dynamics
- **AI Assistant**: Get sophisticated analysis without expensive tools
- **Risk Management**: Automated stop-losses and position tracking
- **Performance Analysis**: Professional-grade metrics and reporting

### Researchers
- **AI Efficacy**: Study LLM performance in financial markets
- **Strategy Testing**: Backtest different approaches and rules
- **Market Analysis**: Analyze micro-cap market inefficiencies
- **Academic Studies**: Transparent methodology and data

### Developers
- **API Integration**: Build custom trading interfaces
- **Model Comparison**: Test different AI providers
- **Strategy Development**: Implement new trading algorithms
- **Data Analysis**: Access rich trading datasets

##  Future Roadmap

### Planned Features
- **Multi-Asset Support**: Options, crypto, international stocks
- **Advanced AI**: Custom fine-tuned models for trading
- **Social Features**: Community sharing and discussion
- **Mobile App**: iOS/Android trading interface
- **Paper Trading**: Risk-free strategy testing

### Research Areas
- **Sentiment Analysis**: News and social media integration
- **Ensemble Models**: Combine multiple AI providers
- **Reinforcement Learning**: Adaptive trading strategies
- **Real-time Data**: Millisecond-level market feeds

##  Legal & Compliance

### Disclaimers
- **Educational Purpose**: This is for learning and research
- **Not Financial Advice**: Users make their own trading decisions
- **Risk Warning**: Micro-cap stocks are highly volatile
- **No Guarantees**: Past performance doesn't predict future results

### Open Source
- **MIT License**: Free to use, modify, and distribute
- **Community Driven**: Contributions welcome
- **Transparent**: All code and methodology public
- **No Vendor Lock-in**: Use any AI provider or none at all

---

**Ready to get started?** Check out our [Quick Start Guide](quick-start.md) or dive into [detailed installation](../installation/basic-setup.md).