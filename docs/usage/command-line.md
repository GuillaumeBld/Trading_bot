# Command Line Interface Guide

Master the command-line interface for the ChatGPT Micro-Cap Trading Bot. This guide covers all commands, options, and advanced usage patterns.

##  Quick Reference

### Basic Commands
```bash
# Manual trading only
python trading_bot.py

# AI-powered trading
python trading_bot.py --ai

# Specific AI provider
python trading_bot.py --ai --provider openai

# Web interface
streamlit run streamlit_app.py
```

### Information Commands
```bash
# List available AI providers
python trading_bot.py --list-providers

# Run setup wizard
python trading_bot.py --setup

# Show help
python trading_bot.py --help
```

##  Complete Command Reference

### Main Trading Bot (`trading_bot.py`)

#### Basic Usage
```bash
python trading_bot.py [OPTIONS]
```

#### Available Options

| Option | Description | Example |
|--------|-------------|---------|
| `--ai` | Enable AI recommendations | `--ai` |
| `--provider PROVIDER` | Specific AI provider | `--provider openai` |
| `--data-dir PATH` | Data directory | `--data-dir "My Trading"` |
| `--portfolio-file FILE` | Portfolio CSV file | `--portfolio-file portfolio.csv` |
| `--list-providers` | Show available AI providers | `--list-providers` |
| `--setup` | Run setup wizard | `--setup` |
| `--help` | Show help message | `--help` |

#### Provider Options
- `openai` - OpenAI GPT models
- `anthropic` - Anthropic Claude models
- `ollama` - Local Ollama models
- `huggingface` - Local Hugging Face models

### Setup Script (`setup_llm.py`)

#### Usage
```bash
python setup_llm.py [OPTIONS]
```

#### Available Options

| Option | Description | Example |
|--------|-------------|---------|
| `--check` | Check provider availability | `--check` |
| `--create-config` | Create configuration files | `--create-config` |
| `--setup-guide` | Show setup guide | `--setup-guide` |
| `--ollama-guide` | Show Ollama installation guide | `--ollama-guide` |

### Core Trading Script (`trading_script.py`)

 **Note**: Typically called by `trading_bot.py`, but can be used directly:

```bash
python trading_script.py
```

### Web Interface (`streamlit_app.py`)

```bash
streamlit run streamlit_app.py [-- --OPTION VALUE]
```

##  Common Usage Patterns

### Daily Trading Workflow

#### Morning Setup
```bash
# Check AI provider status
python trading_bot.py --list-providers

# Start trading session
python trading_bot.py --ai --provider openai
```

#### Manual Trading Session
```bash
# Start manual trading
python trading_bot.py

# Follow prompts:
# - Enter starting cash (first time only)
# - Choose buy/sell/continue
# - Review portfolio and market data
```

#### AI-Powered Session
```bash
# Start with AI recommendations
python trading_bot.py --ai

# The system will:
# 1. Fetch current market data
# 2. Analyze your portfolio
# 3. Generate AI recommendations
# 4. Ask for your approval on each trade
# 5. Execute approved trades
# 6. Show updated portfolio and performance
```

### Advanced Usage

#### Custom Data Directory
```bash
# Use specific folder for data
python trading_bot.py --data-dir "/path/to/my/trading/data"

# This allows multiple portfolios:
python trading_bot.py --data-dir "Portfolio_A"
python trading_bot.py --data-dir "Portfolio_B"
```

#### Provider-Specific Trading
```bash
# Use OpenAI for high-value decisions
python trading_bot.py --ai --provider openai

# Use Ollama for frequent analysis  
python trading_bot.py --ai --provider ollama

# Use Anthropic for alternative perspective
python trading_bot.py --ai --provider anthropic
```

#### Batch Operations
```bash
# Process multiple portfolios
for dir in Portfolio_*; do
    echo "Processing $dir..."
    python trading_bot.py --ai --data-dir "$dir"
done
```

##  Interactive Mode Details

### Initial Setup (First Run)
```
$ python trading_bot.py
 Starting ChatGPT Micro-Cap Trading Bot
==================================================
 Data directory: Scripts and CSV Files
 Portfolio file: Scripts and CSV Files/chatgpt_portfolio_update.csv
 Mode: Manual trading only
==================================================

Portfolio CSV is empty. Returning set amount of cash for creating portfolio.
What would you like your starting cash amount to be? 100

 You have 100.0 in cash.
Would you like to log a manual trade? Enter 'b' for buy, 's' for sell, or press Enter to continue:
```

### Buying a Stock
```
Would you like to log a manual trade? Enter 'b' for buy, 's' for sell, or press Enter to continue: b
Enter ticker symbol: ABEO
Enter number of shares: 10
Enter buy price: 5.75
Enter stop loss: 4.89

You are currently trying to buy 10.0 shares of ABEO with a price of 5.75 and a stoploss of 4.89.
If this a mistake, type "1". 

Manual buy for ABEO complete!
```

### AI Recommendations
```
 Getting AI recommendations...
Using LLM provider: openai

 LLM provided 2 recommendations:

--- Recommendation 1 ---
Action: BUY
Ticker: CADL
Shares: 8.0
Price: $5.04
Stop Loss: $4.03
Confidence: 0.85
Reasoning: Strong technical breakout above resistance with volume confirmation...

Execute this recommendation? (y/n/skip): y
 BUY executed

--- Recommendation 2 ---
Action: SELL
Ticker: ABEO
Shares: 5.0
Price: $5.68
Stop Loss: N/A
Confidence: 0.72
Reasoning: Position has reached profit target and showing signs of distribution...

Execute this recommendation? (y/n/skip): n
 Recommendation skipped by user
```

### Portfolio Summary
```
prices and updates for 2024-08-06
ABEO closing price: 5.68
ABEO volume for today: $45,000
percent change from the day before: -1.56%

CADL closing price: 5.06
CADL volume for today: $32,000
percent change from the day before: 0.40%

Total Sharpe Ratio over 15 days: 1.2450
Total Sortino Ratio over 15 days: 1.8900
Latest ChatGPT Equity: $105.23
$100 Invested in the S&P 500: $101.50

today's portfolio:
   ticker  shares  stop_loss  buy_price  cost_basis
0    ABEO     6.0       4.90       5.77       34.62
1    CADL     5.0       4.03       5.04       25.20

cash balance: 25.5
```

##  Advanced Features

### Environment Variable Overrides
```bash
# Override data directory
export TRADING_DATA_DIR="/custom/path"
python trading_bot.py

# Override log level
export LOG_LEVEL=DEBUG
python trading_bot.py

# Use custom API endpoint
export OPENAI_BASE_URL="https://custom-api.com/v1"
python trading_bot.py --ai --provider openai
```

### Configuration File Usage
```bash
# Use custom configuration
python trading_bot.py --config custom_config.json

# Override specific settings
python trading_bot.py --ai --provider openai --data-dir "Test Portfolio"
```

### Debugging and Logging
```bash
# Enable debug mode
export DEBUG=true
python trading_bot.py --ai

# Save conversation logs
export SAVE_AI_CONVERSATIONS=true
python trading_bot.py --ai

# Verbose output
python -v trading_bot.py --ai
```

##  Security Considerations

### API Key Management
```bash
# Set API keys securely
export OPENAI_API_KEY="sk-your-key-here"
python trading_bot.py --ai --provider openai

# Use .env file (recommended)
echo "OPENAI_API_KEY=sk-your-key-here" > .env
python trading_bot.py --ai --provider openai
```

### Data Protection
```bash
# Use dedicated data directory
mkdir -p ~/trading_data
python trading_bot.py --data-dir ~/trading_data

# Set proper permissions
chmod 700 ~/trading_data
chmod 600 ~/trading_data/*.csv
```

##  Troubleshooting Commands

### Diagnostic Commands
```bash
# Check system compatibility
python -c "import pandas, numpy, yfinance; print(' Core dependencies OK')"

# Test AI provider availability
python setup_llm.py --check

# Validate configuration
python -c "from llm_interface import LLMManager; LLMManager()"

# Test market data access
python -c "import yfinance as yf; print(yf.download('AAPL', period='1d'))"
```

### Error Recovery
```bash
# Reset configuration
rm .env .llm_config.json
python setup_llm.py

# Clear cache
rm -rf __pycache__ .streamlit

# Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### Performance Monitoring
```bash
# Time execution
time python trading_bot.py --ai

# Monitor memory usage
python -c "
import psutil
print(f'Memory usage: {psutil.Process().memory_info().rss / 1024**2:.1f}MB')
"

# Profile execution
python -m cProfile trading_bot.py --ai > profile.txt
```

##  Output Formats

### CSV Data Files
```bash
# View portfolio history
cat chatgpt_portfolio_update.csv

# View trade log
cat chatgpt_trade_log.csv

# Export to Excel
python -c "
import pandas as pd
pd.read_csv('chatgpt_portfolio_update.csv').to_excel('portfolio.xlsx')
"
```

### JSON Output (Advanced)
```bash
# Get JSON output (if implemented)
python trading_bot.py --output json --ai

# Parse with jq (Linux/Mac)
python trading_bot.py --output json --ai | jq '.recommendations'
```

##  Best Practices

### Daily Usage
1. **Check provider status** before trading
2. **Review overnight news** that might affect positions
3. **Monitor stop-loss levels** during volatile periods
4. **Save important decisions** and reasoning

### Performance Optimization
1. **Use local AI** for frequent analysis
2. **Cache market data** when possible
3. **Batch operations** when updating multiple portfolios
4. **Monitor API usage** to avoid rate limits

### Error Prevention
1. **Validate ticker symbols** before trading
2. **Check available cash** before buy orders
3. **Verify stop-loss levels** are reasonable
4. **Backup data** regularly

---

**Next Steps:**
- **[Web Interface Guide](web-interface.md)** - Learn the Streamlit interface
- **[AI Trading Guide](ai-trading.md)** - Master AI-powered recommendations
- **[Portfolio Management](portfolio-management.md)** - Advanced portfolio strategies