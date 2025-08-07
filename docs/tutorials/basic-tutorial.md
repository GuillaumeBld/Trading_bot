# Basic Tutorial: Your First Trading Session

This step-by-step tutorial will guide you through your first trading session with the ChatGPT Micro-Cap Trading Bot. No prior experience required!

## 🎯 What You'll Learn

By the end of this tutorial, you'll know how to:
- ✅ Set up your first portfolio
- ✅ Make your first trade
- ✅ Monitor performance
- ✅ Understand the output data

**Time Required**: 15-20 minutes  
**Prerequisites**: Python installed, basic command line knowledge

## 🚀 Before You Start

### Check Your Setup
```bash
# Verify Python installation
python --version
# Should show Python 3.9 or higher

# Check project files
ls -la
# Should show trading_bot.py, requirements.txt, etc.
```

### Install Dependencies (if not done already)
```bash
pip install pandas numpy yfinance matplotlib
```

## 📈 Step 1: Your First Portfolio

### Start the Trading Bot
```bash
python trading_bot.py
```

You should see output like this:
```
🚀 Starting ChatGPT Micro-Cap Trading Bot
==================================================
📁 Data directory: Scripts and CSV Files
📊 Portfolio file: Scripts and CSV Files/chatgpt_portfolio_update.csv
👤 Mode: Manual trading only
==================================================

Portfolio CSV is empty. Returning set amount of cash for creating portfolio.
What would you like your starting cash amount to be?
```

### Set Your Starting Cash
```
What would you like your starting cash amount to be? 100
```

**💡 Tip**: Start with $100 or any amount you're comfortable learning with. This is just tracking - no real money is at risk.

## 🛒 Step 2: Make Your First Trade

### The Trading Prompt
After setting your cash, you'll see:
```
 You have 100.0 in cash.
Would you like to log a manual trade? Enter 'b' for buy, 's' for sell, or press Enter to continue:
```

### Let's Buy a Stock
Type `b` and press Enter:
```
Would you like to log a manual trade? Enter 'b' for buy, 's' for sell, or press Enter to continue: b
```

### Enter Stock Details
The system will ask for trade details:

```
Enter ticker symbol: ABEO
Enter number of shares: 10
Enter buy price: 5.75
Enter stop loss: 4.89
```

**📝 Example Explanation**:
- **Ticker**: ABEO (a real micro-cap stock)
- **Shares**: 10 (invest $57.50 of your $100)
- **Price**: $5.75 (current market price)
- **Stop Loss**: $4.89 (15% below entry = risk management)

### Confirm Your Trade
```
You are currently trying to buy 10.0 shares of ABEO with a price of 5.75 and a stoploss of 4.89.
If this a mistake, type "1". 
```

Press Enter to confirm (or type "1" to cancel).

### Success!
```
Manual buy for ABEO complete!
```

## 📊 Step 3: Add Another Position

Let's diversify with a second stock:

```
 You have 42.5 in cash.
Would you like to log a manual trade? Enter 'b' for buy, 's' for sell, or press Enter to continue: b

Enter ticker symbol: CADL
Enter number of shares: 8
Enter buy price: 5.04
Enter stop loss: 4.03
```

Confirm the trade, and you should see:
```
Manual buy for CADL complete!
```

## 🎉 Step 4: Finish Setup

Press Enter to skip more trades:
```
 You have 2.18 in cash.
Would you like to log a manual trade? Enter 'b' for buy, 's' for sell, or press Enter to continue: 
```

Just press Enter to continue to the analysis phase.

## 📈 Step 5: Review Your Portfolio

The system will now:
1. Fetch current market data
2. Calculate your performance
3. Show portfolio summary

### Market Data Output
```
prices and updates for 2024-08-06
ABEO closing price: 5.68
ABEO volume for today: $45,000
percent change from the day before: -1.56%

CADL closing price: 5.06
CADL volume for today: $32,000
percent change from the day before: 0.40%

^RUT closing price: 2089.54
^RUT volume for today: $125,432,000
percent change from the day before: 0.15%
```

### Performance Metrics
```
Total Sharpe Ratio over 1 days: 0.0000
Total Sortino Ratio over 1 days: 0.0000
Latest ChatGPT Equity: $97.82
$100 Invested in the S&P 500: $100.15
```

### Portfolio Summary
```
today's portfolio:
   ticker  shares  stop_loss  buy_price  cost_basis
0    ABEO    10.0       4.89       5.75       57.50
1    CADL     8.0       4.03       5.04       40.32

cash balance: 2.18
```

## 📁 Step 6: Understanding Your Data

### Files Created
After your session, check these files:

```bash
ls -la "Scripts and CSV Files/"
```

You should see:
- `chatgpt_portfolio_update.csv` - Daily portfolio snapshots
- `chatgpt_trade_log.csv` - Complete trade history

### Portfolio File Structure
```bash
head "Scripts and CSV Files/chatgpt_portfolio_update.csv"
```

Shows columns:
- **Date**: Trading day
- **Ticker**: Stock symbol
- **Shares**: Number of shares owned
- **Cost Basis**: Price you paid
- **Stop Loss**: Risk management level
- **Current Price**: Latest market price
- **Total Value**: Shares × Current Price
- **PnL**: Profit/Loss vs purchase price
- **Action**: HOLD, SELL, etc.
- **Cash Balance**: Available cash
- **Total Equity**: Total portfolio value

### Trade Log Structure
```bash
head "Scripts and CSV Files/chatgpt_trade_log.csv"
```

Shows columns:
- **Date**: When trade occurred
- **Ticker**: Stock symbol
- **Shares Bought/Sold**: Transaction size
- **Buy/Sell Price**: Transaction price
- **Cost Basis**: Total cost
- **PnL**: Profit/Loss on sale
- **Reason**: Why trade was made

## 🔄 Step 7: Your Second Day

### Running the Bot Again
The next day (or anytime), run:
```bash
python trading_bot.py
```

Now it loads your existing portfolio:
```
🚀 Starting ChatGPT Micro-Cap Trading Bot
==================================================
📁 Data directory: Scripts and CSV Files
📊 Portfolio file: Scripts and CSV Files/chatgpt_portfolio_update.csv
👤 Mode: Manual trading only
==================================================

   ticker  shares  stop_loss  buy_price  cost_basis
0    ABEO    10.0       4.89       5.75       57.50
1    CADL     8.0       4.03       5.04       40.32
```

### Daily Updates
The system automatically:
- ✅ Fetches current prices for your stocks
- ✅ Checks if any stop-losses were triggered
- ✅ Updates your portfolio value
- ✅ Calculates performance metrics
- ✅ Saves everything to CSV files

### Stop-Loss Example
If a stock drops below your stop-loss:
```
ABEO closing price: 4.85  # Below your 4.89 stop-loss!
Action: SELL - Stop Loss Triggered
```

The system automatically:
- Sells the position at your stop-loss price
- Adds cash back to your account
- Logs the trade with loss/gain
- Removes the stock from your portfolio

## 🎯 Understanding Key Concepts

### Stop-Loss Protection
- **What**: Automatic sale when price drops to set level
- **Why**: Limits losses on bad trades
- **Example**: Buy at $5.75, stop-loss at $4.89 = max 15% loss

### Position Sizing
- **Small positions**: Less risk, less reward
- **Large positions**: More risk, more reward
- **Diversification**: Multiple positions reduce risk

### Performance Metrics
- **Total Return**: How much you've gained/lost
- **Sharpe Ratio**: Risk-adjusted performance
- **Benchmark Comparison**: How you're doing vs market

## 🛠️ Common Beginner Mistakes

### ❌ Avoid These
1. **No stop-losses**: Always set them!
2. **Position too large**: Don't risk >20% on one stock
3. **No diversification**: Don't put all money in one stock
4. **Emotional trading**: Stick to your plan
5. **Ignoring data**: Review your performance regularly

### ✅ Best Practices
1. **Start small**: Learn with amounts you can afford to lose
2. **Set stop-losses**: 15-20% below entry is common
3. **Diversify**: 3-7 positions maximum
4. **Keep records**: The system does this automatically
5. **Review regularly**: Learn from wins and losses

## 🎉 Congratulations!

You've completed your first trading session! You now know how to:
- ✅ Create and manage a portfolio
- ✅ Make buy and sell trades
- ✅ Set stop-loss protection
- ✅ Understand performance data
- ✅ Use the CSV tracking system

## 🚀 Next Steps

Ready to level up? Try these:

### 1. Add AI Recommendations
```bash
# Install AI dependencies
pip install -r requirements.txt

# Set up AI providers
python setup_llm.py

# Trade with AI assistance
python trading_bot.py --ai
```

### 2. Try the Web Interface
```bash
streamlit run streamlit_app.py
# Open browser to http://localhost:8501
```

### 3. Learn Advanced Features
- **[AI Tutorial](ai-tutorial.md)** - AI-powered trading
- **[Web Interface Guide](../usage/web-interface.md)** - Visual trading
- **[Performance Analysis](data-analysis.md)** - Deep dive into your results

### 4. Explore Real Strategies
- **[Advanced Strategies](advanced-strategies.md)** - Professional techniques
- **[Risk Management](../usage/portfolio-management.md)** - Protect your capital

## ⚠️ Important Reminders

- **This is for learning**: Start with small amounts
- **Not financial advice**: You make all trading decisions
- **High risk assets**: Micro-cap stocks are volatile
- **Backtest strategies**: Test before risking real money

---

**Questions?** Check our **[FAQ](../troubleshooting/faq.md)** or **[Getting Help](../troubleshooting/common-issues.md)** guides!