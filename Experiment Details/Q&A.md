# Q&A

## How does this experiment work?
Starting with $100, ChatGPT manages a portfolio of micro-cap stocks (market cap under $300M). Every trading day, I provide it with current price data and it can make buy/sell decisions with strict stop-loss rules applied.

## Why micro-cap stocks?
Micro-cap stocks are typically more volatile and less efficiently priced, potentially offering opportunities for alpha generation that large-cap stocks might not provide.

## How are trades executed?
All trades are manually executed based on ChatGPT's decisions. The AI provides specific buy/sell recommendations with price targets and stop-loss levels.

## What are the constraints?
- Only full-share positions
- U.S.-listed stocks only
- Market cap under $300M
- Strict stop-loss rules
- 6-month time horizon (June 2025 - December 2025)

## How is performance measured?
Performance is tracked against major indices like the S&P 500 and Russell 2000, with daily portfolio updates recorded in CSV files.

## Can I replicate this experiment?
Yes! The "Start Your Own" folder contains scripts and instructions to run your own version of this experiment.

## What happens if ChatGPT makes a bad recommendation?
Stop-loss rules are automatically enforced to limit downside risk. All decisions are logged for transparency.

## Is this financial advice?
No. This is purely an educational experiment to test AI capabilities. See the disclaimer for full details.