# Frequently Asked Questions (FAQ)

Find quick answers to common questions about the ChatGPT Micro-Cap Trading Bot.

##  Getting Started

### Q: Do I need a brokerage account to use this?
**A:** No! This is a portfolio tracking and analysis tool. It doesn't execute real trades with any broker. You manually track your trades and the system helps with analysis and recommendations.

### Q: Can I start with less than $100?
**A:** Absolutely! You can start with any amount. The $100 is just from the original experiment. Some users start with $50 or even $25 to learn the system.

### Q: Is this suitable for beginners?
**A:** Yes, but with caveats:
-  Great for learning portfolio management
-  Excellent for understanding AI in trading  
-  Micro-cap stocks are very risky
-  Only invest what you can afford to lose

### Q: Do I need coding experience?
**A:** Not for basic usage! The system has:
- Simple command-line interface
- User-friendly web interface
- Step-by-step setup guides

##  AI Features

### Q: Which AI provider should I choose?
**A:** It depends on your needs:
- **OpenAI GPT-4o-mini**: Best overall (costs ~$10-30/month)
- **Ollama**: Best free option (requires good computer)
- **Anthropic Claude**: Good OpenAI alternative
- **Hugging Face**: For advanced users only

### Q: How much do AI recommendations cost?
**A:** Typical monthly costs for daily trading:
- **OpenAI GPT-4o-mini**: $10-30
- **Anthropic Claude-3-haiku**: $15-40
- **Ollama**: $0 (free, uses your computer)
- **Hugging Face**: $0 (free, uses your computer)

### Q: Can I use the bot without AI?
**A:** Yes! The bot works perfectly for manual trading without any AI features. You get:
- Portfolio tracking
- Performance metrics
- Automatic stop-loss monitoring
- Data visualization

### Q: How accurate are AI recommendations?
**A:** AI recommendations are tools, not guarantees:
- They provide sophisticated analysis you might miss
- They consider multiple factors simultaneously
- **You** make the final decision on all trades
- Past performance doesn't predict future results

### Q: Can the AI execute trades automatically?
**A:** No, and this is intentional for safety:
- AI makes recommendations only
- You approve or reject each suggestion
- All trades are logged for transparency
- You maintain full control

##  Technical Issues

### Q: "No LLM providers available" error
**A:** This means no AI providers are configured:
1. Run `python setup_llm.py --check`
2. Install missing dependencies: `pip install -r requirements.txt`
3. Add API keys to `.env` file, or
4. Install Ollama for free local AI

### Q: OpenAI API key not working
**A:** Check these common issues:
- Key starts with "sk-" and is complete
- Account has billing set up
- Key has correct permissions
- No typos in `.env` file
- Account isn't suspended/rate limited

### Q: Ollama models not downloading
**A:** Try these solutions:
1. Check internet connection
2. Restart Ollama service: `ollama serve`
3. Try smaller model: `ollama pull phi3:mini`
4. Check disk space (models are 2-8GB)
5. Update Ollama: `ollama --version`

### Q: Web interface not loading
**A:** Common fixes:
1. Install Streamlit: `pip install streamlit`
2. Check port isn't blocked: try http://localhost:8501
3. Try different port: `streamlit run streamlit_app.py --server.port 8502`
4. Check firewall settings

### Q: Market data not updating
**A:** This is usually a network issue:
1. Check internet connection
2. Try: `python -c "import yfinance as yf; print(yf.download('AAPL', period='1d'))"`
3. Restart your router if needed
4. Some corporate networks block financial APIs

##  Trading Questions

### Q: What are micro-cap stocks?
**A:** Micro-cap stocks are companies with market capitalization under $300 million:
- Often undervalued and overlooked
- Higher growth potential than large caps
- **Much higher risk and volatility**
- Less liquid (harder to buy/sell)
- Limited analyst coverage

### Q: How do stop-losses work?
**A:** Stop-losses protect you from large losses:
- Set when you buy a stock (e.g., 15% below purchase price)
- Automatically trigger sale if price drops to that level
- Help limit emotional trading decisions
- Essential for risk management

### Q: Why focus on micro-caps instead of large stocks?
**A:** Several reasons:
- **Inefficiency**: Less analyst coverage = more opportunities
- **Growth potential**: Small companies can grow faster
- **AI advantage**: Pattern recognition in under-analyzed stocks
- **Experiment focus**: Testing AI in challenging market segment

### Q: How is performance calculated?
**A:** The system calculates multiple metrics:
- **Total return**: Absolute gains/losses
- **Sharpe ratio**: Risk-adjusted returns
- **Sortino ratio**: Downside risk-adjusted returns
- **Benchmark comparison**: vs S&P 500, Russell 2000

### Q: Can I track multiple portfolios?
**A:** Yes! Use different data directories:
```bash
python trading_bot.py --data-dir "Portfolio_A"
python trading_bot.py --data-dir "Portfolio_B"
```

##  Cost and Pricing

### Q: Is the software free?
**A:** The software itself is completely free (MIT license):
-  Core trading bot: Free
-  Manual trading: Free
-  Local AI (Ollama/HuggingFace): Free
-  Cloud AI APIs: Paid (but cheap)

### Q: Are there hidden costs?
**A:** No hidden costs, but consider:
- **API usage**: $10-40/month for cloud AI (optional)
- **Electricity**: ~$1-5/month for local AI (minimal)
- **Internet**: Standard broadband sufficient

### Q: Can I try before paying?
**A:** Absolutely:
1. Start with manual trading (completely free)
2. Try Ollama for free local AI
3. Use free API credits from OpenAI/Anthropic
4. Switch to paid only if you like it

##  Privacy and Security

### Q: Is my trading data secure?
**A:** Your data security depends on your setup:
- **Local AI**: Data never leaves your computer
- **Cloud AI**: Portfolio data sent to AI provider
- **CSV files**: Stored locally on your computer
- **No external sharing**: We never see your data

### Q: What data do AI providers see?
**A:** When using cloud AI, providers see:
- Your current portfolio positions
- Recent market data for your stocks
- **They don't see**: Your personal info, account numbers, real money amounts

### Q: Can I use this without internet?
**A:** Partially:
-  Portfolio tracking: Works offline
-  Local AI: Works offline (after initial setup)
-  Market data: Requires internet
-  Cloud AI: Requires internet

##  Strategy and Performance

### Q: What trading strategy does the AI use?
**A:** The AI uses multiple approaches:
- **Technical analysis**: Chart patterns, momentum
- **Fundamental analysis**: Financial metrics, growth
- **Catalyst analysis**: News, events, timing
- **Risk management**: Position sizing, diversification

### Q: How often should I run the bot?
**A:** Most users run it:
- **Daily**: Check for stop-loss triggers and new opportunities
- **Weekly**: Deep analysis and strategy adjustment
- **As needed**: When market conditions change

### Q: Can I modify the AI prompts?
**A:** Yes! Advanced users can:
- Edit prompts in `llm_interface.py`
- Create custom `.llm_config.json` settings
- Adjust temperature and other parameters
- Add custom analysis criteria

### Q: What's a good starting strategy?
**A:** For beginners:
1. Start with small amount ($50-100)
2. Limit to 3-5 positions maximum
3. Set 15% stop-losses on all positions
4. Use AI for analysis, make your own decisions
5. Track everything and learn from results

##  Data and Backup

### Q: How do I backup my data?
**A:** Your trading data is in CSV files:
```bash
# Copy your data files
cp chatgpt_portfolio_update.csv backup_portfolio.csv
cp chatgpt_trade_log.csv backup_trades.csv

# Or backup entire data directory
cp -r "Scripts and CSV Files" "Backup_$(date +%Y%m%d)"
```

### Q: Can I export data to Excel?
**A:** Yes! The CSV files open directly in Excel, or use Python:
```python
import pandas as pd
df = pd.read_csv('chatgpt_portfolio_update.csv')
df.to_excel('portfolio.xlsx', index=False)
```

### Q: How do I import existing trades?
**A:** You can manually edit the CSV files or write a Python script:
- Follow the exact column format
- Use YYYY-MM-DD date format
- Add trades to `chatgpt_trade_log.csv`
- Update portfolio in `chatgpt_portfolio_update.csv`

##  Development and Customization

### Q: Can I contribute to the project?
**A:** Yes! The project welcomes contributions:
- Bug reports and feature requests
- Code improvements and new features
- Documentation improvements
- Example strategies and tutorials

### Q: How do I add a new AI provider?
**A:** For developers:
1. Create new class inheriting from `LLMInterface`
2. Implement required methods
3. Add to provider list in `LLMManager`
4. Update configuration options
5. Submit pull request!

### Q: Can I use this for other asset classes?
**A:** Currently focused on US stocks, but the framework could support:
- International stocks
- Cryptocurrencies
- Options and derivatives
- ETFs and mutual funds
- (Requires development work)

##  Getting Help

### Q: Where can I get help?
**A:** Multiple support options:
- **Documentation**: This comprehensive guide
- **GitHub Issues**: Report bugs and request features
- **Discord/Community**: Chat with other users
- **Email Support**: For serious issues

### Q: Something's not working, what should I do?
**A:** Follow this troubleshooting order:
1. Check [Common Issues](common-issues.md)
2. Run diagnostic: `python setup_llm.py --check`
3. Check your configuration files
4. Try with a fresh virtual environment
5. Search GitHub issues
6. Create new issue with details

### Q: Can I hire someone to set this up?
**A:** While not officially supported, you might find help through:
- Local Python developers
- Freelance platforms (Upwork, Fiverr)
- University computer science students
- Python user groups in your area

---

**Still have questions?** 
-  Check our [Complete Documentation](../README.md)
-  [Report Issues on GitHub](https://github.com/your-repo/issues)
-  [Join our Discord Community](https://discord.gg/your-invite)