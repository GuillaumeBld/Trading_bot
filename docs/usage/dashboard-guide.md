# Advanced Dashboard User Guide

## 🎯 Overview

The Advanced Trading Dashboard is a comprehensive web-based interface that provides complete control over your ChatGPT Micro-Cap Trading Bot. It features:

- **🔧 Complete Configuration Management** - Set up all APIs and trading parameters
- **📊 Real-time Performance Monitoring** - Track all key metrics and ratios
- **🌍 Market Data Integration** - Live market data, news, and sentiment analysis
- **🤖 AI Insights** - Manage AI providers and view recommendations
- **📈 Advanced Analytics** - Risk analysis, correlation matrices, and more

## 🚀 Quick Start

### Method 1: Using the Launcher (Recommended)
```bash
# Interactive launcher
python launch_dashboard.py

# Direct launch
python launch_dashboard.py --advanced
```

### Method 2: Direct Streamlit Launch
```bash
streamlit run advanced_dashboard.py --server.port 8502
```

### Method 3: First-time Setup
```bash
# Run setup wizard first
python launch_dashboard.py --setup

# Then launch dashboard
python launch_dashboard.py --advanced
```

## 📋 Dashboard Sections

### 1. 📊 Performance Tab

**Key Metrics Display:**
- **Total Return** - Overall portfolio performance vs initial investment
- **Portfolio Value** - Current total equity in dollars
- **Sharpe Ratio** - Risk-adjusted return measurement
- **Max Drawdown** - Largest peak-to-trough decline
- **Volatility** - Annualized portfolio volatility percentage

**Advanced Metrics** (when enabled):
- **Sortino Ratio** - Downside risk-adjusted returns
- **Win Rate** - Percentage of profitable trades
- **Days Active** - Number of trading days since inception

**Performance Charts:**
- **Portfolio Performance** - Equity curve vs benchmark
- **Daily Returns** - Daily percentage changes
- **Drawdown Chart** - Underwater equity curve
- **Rolling Sharpe** - 30-day rolling Sharpe ratio

### 2. 💼 Positions Tab

**Current Holdings Table:**
- Ticker symbols and share quantities
- Cost basis and current prices
- Total position values and P&L
- Stop-loss levels for risk management

**Position Analysis:**
- **Allocation Pie Chart** - Visual position sizing
- **P&L Bar Chart** - Profit/loss by position
- **Risk Metrics** - Position-level risk analysis

### 3. 🌍 Market Tab

**Market Indices:**
- S&P 500, NASDAQ, Dow Jones, Russell 2000
- VIX (volatility index) and 10-Year Treasury
- Real-time values with daily changes

**Market Sentiment Gauge:**
- Overall market sentiment score (0-100)
- Sentiment classification (Very Bearish to Very Bullish)
- Component analysis (VIX, indices, news sentiment)

**Economic Indicators:**
- Key economic data points
- Dollar index, gold, oil prices
- Interest rates and bond yields

### 4. 📰 News Tab

**Market News Feed:**
- Real-time financial news from major sources
- Sentiment analysis for each article
- Source attribution and publication timestamps
- Relevance scoring and symbol tagging

**News Sources:**
- Bloomberg, Reuters, CNBC, MarketWatch
- Yahoo Finance and other financial media
- Configurable news categories and keywords

### 5. 🤖 AI Insights Tab

**AI Provider Status:**
- Available and configured AI providers
- Connection status and model information
- Usage statistics and performance metrics

**AI Analysis Tools:**
- **Market Overview** - Comprehensive market analysis
- **Portfolio Review** - AI-driven portfolio assessment
- **Risk Assessment** - AI-powered risk evaluation
- **Trading Opportunities** - AI-identified opportunities

**Recent Recommendations:**
- Historical AI recommendations and outcomes
- Confidence scores and reasoning
- User decision tracking (accepted/rejected)

### 6. ⚙️ Configuration Tab

**AI Providers Configuration:**
- OpenAI API key and model settings
- Anthropic Claude configuration
- Ollama local model setup
- Hugging Face transformer settings

**Broker API Configuration:**
- Alpaca Markets API credentials
- TD Ameritrade OAuth setup
- Interactive Brokers connection
- Paper vs live trading toggle

**Trading Parameters:**
- Maximum position size percentage
- Default stop-loss percentage
- Maximum number of positions
- Cash reserve requirements

**Data Source Settings:**
- Primary market data provider
- News API configuration
- Update frequency settings
- Cache management options

## 🔧 Configuration Guide

### Setting Up AI Providers

#### OpenAI Configuration
1. Get API key from [OpenAI Platform](https://platform.openai.com/api-keys)
2. Go to Configuration → AI Providers → OpenAI
3. Enter your API key (stored securely)
4. Select model (gpt-4o-mini recommended)
5. Adjust temperature (0.1 for focused responses)
6. Enable the provider

#### Anthropic Configuration
1. Get API key from [Anthropic Console](https://console.anthropic.com)
2. Go to Configuration → AI Providers → Anthropic
3. Enter your API key
4. Select model (claude-3-haiku for cost-effectiveness)
5. Configure parameters and enable

#### Ollama (Free Local AI)
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Start service: `ollama serve`
3. Pull model: `ollama pull llama3.1:8b`
4. Enable in dashboard (no API key needed)

### Setting Up Broker Integration

#### Alpaca Markets (Recommended)
1. Create account at [Alpaca](https://alpaca.markets)
2. Generate API keys in your dashboard
3. Go to Configuration → Brokers → Alpaca
4. Enter API Key and Secret Key
5. Enable Paper Trading for testing
6. Test connection and save

#### TD Ameritrade
1. Create developer account
2. Register your application
3. Complete OAuth2 flow
4. Enter Client ID and Refresh Token
5. Test connection

### Trading Parameters Setup

**Risk Management Settings:**
- **Max Position Size**: 15-25% recommended for micro-caps
- **Default Stop Loss**: 15-20% for volatility protection
- **Max Positions**: 5-7 for proper diversification
- **Cash Reserve**: 5-10% for opportunities

**Performance Settings:**
- **Risk-Free Rate**: Current treasury rate (4-5%)
- **Benchmark**: S&P 500 for comparison
- **Rebalancing**: Quarterly or as needed

### Data Source Configuration

**Market Data:**
- **Primary Provider**: yFinance (free, reliable)
- **Update Frequency**: 5-minute intervals
- **Extended Hours**: Enable for pre/post market

**News Integration:**
- Get free API key from [NewsAPI](https://newsapi.org)
- Enter key in Data Sources configuration
- Enable news feeds and sentiment analysis

## 📱 Dashboard Features

### Auto-Refresh
- Enable automatic data refresh (10-300 seconds)
- Manual refresh button available
- Smart caching to minimize API calls

### Advanced Metrics Toggle
- Show/hide advanced performance metrics
- Detailed risk analysis and correlations
- Professional-grade analytics

### Timeframe Selection
- Chart timeframes: 1D, 1W, 1M, 3M, 6M, 1Y, 2Y
- Dynamic data loading based on selection
- Optimized for different analysis periods

### Configuration Validation
- Real-time configuration status checking
- Error and warning notifications
- Guided troubleshooting assistance

## 🛡️ Security Features

### API Key Protection
- All sensitive data encrypted at rest
- Secure key storage using Fernet encryption
- API keys never displayed in plain text
- Automatic key rotation support

### Data Privacy
- All data processed locally
- No external data sharing
- Configurable data retention
- Complete user control over information

### Access Control
- Local-only dashboard access
- Optional authentication (future feature)
- Session management
- Audit logging capabilities

## 🚨 Troubleshooting

### Common Issues

**Dashboard Won't Load:**
```bash
# Check requirements
python launch_dashboard.py --info

# Install missing packages
pip install -r requirements.txt

# Try different port
streamlit run advanced_dashboard.py --server.port 8503
```

**API Connection Errors:**
- Verify API keys are correct
- Check internet connectivity
- Confirm API quotas/limits
- Test with individual provider tools

**Performance Issues:**
- Reduce auto-refresh frequency
- Clear browser cache
- Restart dashboard application
- Check system resources

**Configuration Not Saving:**
- Check file permissions
- Verify disk space
- Look for error messages in console
- Try manual configuration backup

### Error Messages

**"Configuration manager not available":**
- Install missing dependencies: `pip install cryptography pyyaml`
- Check file permissions in project directory

**"Market data service not available":**
- Verify internet connection
- Check yFinance package installation
- Try manual market data test

**"No AI providers available":**
- Configure at least one AI provider
- Verify API keys are valid
- Check provider-specific setup guides

## 🎯 Best Practices

### Dashboard Usage
1. **Start with Configuration** - Set up all APIs before trading
2. **Monitor Regularly** - Check performance metrics daily
3. **Review AI Insights** - Use AI analysis for decision support
4. **Stay Informed** - Read news and market analysis
5. **Manage Risk** - Monitor drawdowns and position sizes

### Performance Optimization
1. **Use Auto-Refresh Wisely** - Balance updates with performance
2. **Enable Caching** - Reduce API calls and improve speed
3. **Monitor Resources** - Check CPU and memory usage
4. **Regular Cleanup** - Clear old cache and logs periodically

### Security Best Practices
1. **Protect API Keys** - Never share or commit to version control
2. **Use Paper Trading** - Test with fake money first
3. **Regular Backups** - Export configuration regularly
4. **Update Dependencies** - Keep packages up to date

## 📊 Advanced Usage

### Custom Analysis
- Export data for external analysis
- Create custom metrics and charts
- Integrate with other tools
- Build custom reporting

### Multi-Portfolio Management
- Use different data directories
- Separate configurations per strategy
- Compare performance across portfolios
- Risk management across accounts

### API Integration
- Access dashboard data programmatically
- Build custom extensions
- Integrate with other platforms
- Automated reporting and alerts

---

## 🆘 Getting Help

### Resources
- **[Complete Documentation](../README.md)** - Full system documentation
- **[FAQ](../troubleshooting/faq.md)** - Common questions and answers
- **[Configuration Guide](../configuration/overview.md)** - Detailed setup instructions
- **[Troubleshooting](../troubleshooting/common-issues.md)** - Problem-solving guide

### Support Channels
- **GitHub Issues** - Bug reports and feature requests
- **Discord Community** - Real-time help and discussion
- **Documentation** - Comprehensive guides and tutorials

**The Advanced Dashboard puts professional-grade trading tools at your fingertips. Take time to explore all features and configure them to match your trading style and risk tolerance.**