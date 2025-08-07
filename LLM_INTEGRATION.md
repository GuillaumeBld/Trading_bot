# LLM Integration Guide

The ChatGPT Micro-Cap Trading Experiment now supports **both local and API-based LLMs** for AI-powered trading decisions. This document explains how to set up and use these features.

## 🤖 Supported LLM Providers

### API-Based (Remote)
- **OpenAI GPT-4** - Best performance, requires API key (~$0.15-0.60 per query)
- **Anthropic Claude** - Good alternative, requires API key (~$0.25-0.80 per query)

### Local (Free)
- **Ollama** - Easy local setup with multiple models (free, requires 4-16GB RAM)
- **Hugging Face** - Most flexible, supports GPU acceleration (free)

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure LLM Providers
```bash
python setup_llm.py
```

This will:
- Create `.env` file for API keys
- Create `.llm_config.json` for model settings
- Check which providers are available

### 3. Choose Your Setup

#### Option A: OpenAI (Recommended for best results)
1. Get API key from https://platform.openai.com/api-keys
2. Add to `.env` file: `OPENAI_API_KEY=your_key_here`
3. Run: `python trading_bot.py --ai --provider openai`

#### Option B: Ollama (Free local AI)
1. Install Ollama: `curl -fsSL https://ollama.ai/install.sh | sh`
2. Start service: `ollama serve`
3. Pull model: `ollama pull llama3.1:8b`
4. Run: `python trading_bot.py --ai --provider ollama`

#### Option C: Anthropic Claude
1. Get API key from https://console.anthropic.com/
2. Add to `.env` file: `ANTHROPIC_API_KEY=your_key_here`
3. Run: `python trading_bot.py --ai --provider anthropic`

## 📊 Usage Examples

### Command Line Interface
```bash
# Manual trading only
python trading_bot.py

# AI-powered with best available provider
python trading_bot.py --ai

# Specific provider
python trading_bot.py --ai --provider openai

# List available providers
python trading_bot.py --list-providers

# Run setup wizard
python trading_bot.py --setup
```

### Streamlit Web Interface
```bash
streamlit run streamlit_app.py
```
- Enable "AI Recommendations" in sidebar
- Choose your preferred provider
- Use "Process with AI" button

### Python API
```python
from trading_script import process_portfolio, load_latest_portfolio_state

# Load portfolio
portfolio, cash = load_latest_portfolio_state("portfolio.csv")

# Process with AI
portfolio, cash = process_portfolio(
    portfolio, cash, 
    interactive=False, 
    use_llm=True, 
    llm_provider="openai"
)
```

## 🔧 Configuration

### LLM Settings (.llm_config.json)
```json
{
  "openai": {
    "model_name": "gpt-4o-mini",
    "temperature": 0.1,
    "max_tokens": 2000
  },
  "ollama": {
    "model_name": "llama3.1:8b",
    "base_url": "http://localhost:11434",
    "temperature": 0.1
  }
}
```

### Environment Variables (.env)
```bash
# API Keys
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
```

## 🎯 How AI Recommendations Work

### 1. Analysis Process
The AI analyzes:
- Current portfolio holdings and performance
- Real-time market data and price movements
- Stop-loss levels and risk metrics
- Micro-cap opportunities and catalysts

### 2. Decision Types
- **BUY**: New position recommendations with entry price and stop-loss
- **SELL**: Exit recommendations based on performance or risk
- **HOLD**: Maintain current positions
- **ADJUST_STOP_LOSS**: Update risk management levels

### 3. Safety Features
- **Confidence scoring**: Low confidence recommendations are filtered out
- **Validation checks**: Ensures sufficient cash and valid parameters
- **User approval**: Interactive mode asks for confirmation
- **Risk limits**: Respects stop-loss rules and position sizing

### 4. Decision Format
```python
TradingDecision(
    action="buy",
    ticker="ABEO", 
    shares=10,
    price=5.75,
    stop_loss=4.89,
    reasoning="Strong technical breakout with volume confirmation...",
    confidence=0.85
)
```

## 📋 Prompt Engineering

The system uses specialized prompts for trading analysis:

### System Prompt
```
You are an expert micro-cap stock analyst and portfolio manager. 
Your goal is to maximize risk-adjusted returns while maintaining strict risk management.

CONSTRAINTS:
- Only trade U.S.-listed micro-cap stocks (market cap < $300M)
- Always use stop-losses (typically 15-20% below entry)
- Consider position sizing based on volatility and conviction
- Maximum 5-7 positions for diversification
- Focus on stocks with clear catalysts and technical momentum
```

### Analysis Framework
1. **Fundamental Analysis**: Revenue growth, profitability, debt levels
2. **Technical Analysis**: Price trends, volume patterns, support/resistance
3. **Catalyst Analysis**: Upcoming events, news flow, insider activity
4. **Risk Assessment**: Volatility, liquidity, correlation analysis

## 🛡️ Safety and Risk Management

### Built-in Safeguards
- **Confidence filtering**: Recommendations below 30% confidence are rejected
- **Cash validation**: Prevents trades exceeding available capital
- **Price validation**: Ensures trade prices are within daily range
- **Position limits**: Respects portfolio diversification rules

### User Controls
- **Interactive approval**: Manual review of each recommendation
- **Provider selection**: Choose trusted AI models
- **Fallback modes**: System continues if AI fails

### Risk Monitoring
- **Stop-loss enforcement**: Automatic position liquidation
- **Portfolio limits**: Maximum position sizes and concentrations
- **Performance tracking**: Monitor AI decision outcomes

## 🔍 Troubleshooting

### Common Issues

#### "No LLM providers available"
1. Run `python setup_llm.py --check`
2. Install missing dependencies: `pip install openai anthropic ollama transformers`
3. Configure API keys in `.env` file
4. For Ollama: Check service is running with `ollama list`

#### API Key Errors
1. Verify API key is correct and active
2. Check account credits/billing status
3. Ensure key has proper permissions

#### Ollama Connection Issues
1. Start Ollama service: `ollama serve`
2. Check if model is pulled: `ollama list`
3. Pull recommended model: `ollama pull llama3.1:8b`

#### Poor AI Recommendations
1. Check confidence scores - low scores indicate uncertainty
2. Verify market data quality
3. Consider using different model (GPT-4 vs Llama vs Claude)
4. Review prompt engineering in `llm_interface.py`

### Getting Help
- Run diagnostic: `python setup_llm.py --check`
- View setup guide: `python setup_llm.py --setup-guide`
- Check logs for detailed error messages

## 💡 Best Practices

### Provider Selection
- **OpenAI GPT-4o-mini**: Best balance of cost and performance
- **Ollama llama3.1:8b**: Good free alternative, requires local resources
- **Anthropic Claude-3-haiku**: Fast and cost-effective API option

### Usage Patterns
- **Daily trading**: Use AI for position updates and new opportunities
- **Weekly reviews**: Deep analysis with higher-tier models (GPT-4, Claude-3-opus)
- **Risk management**: Regular stop-loss adjustments based on volatility

### Cost Management
- Start with cheaper models (GPT-4o-mini, Claude-3-haiku)
- Use local models for frequent queries
- Reserve premium models for complex decisions

## 📈 Performance Expectations

### AI Capabilities
- **Pattern recognition**: Identifies technical setups and breakouts
- **Risk assessment**: Evaluates portfolio concentration and correlation
- **Catalyst analysis**: Considers upcoming events and news flow
- **Market timing**: Helps with entry/exit decisions

### Limitations
- **Market unpredictability**: AI cannot predict black swan events
- **Data quality**: Recommendations depend on accurate market data
- **Model hallucinations**: May occasionally provide invalid suggestions
- **Bias effects**: Models trained on historical data may have biases

### Monitoring
- Track AI decision performance vs manual trades
- Monitor confidence scores and rejection rates
- Review reasoning quality for decision improvement

## 🔗 Integration with Existing Workflow

The LLM integration seamlessly works with existing features:

- **CSV logging**: All AI decisions are logged in trade history
- **Performance tracking**: AI trades included in Sharpe/Sortino calculations  
- **Visualization**: Charts show combined manual + AI performance
- **Stop-loss automation**: AI recommendations respect existing risk rules

This creates a hybrid approach where AI augments human decision-making while maintaining full transparency and control.