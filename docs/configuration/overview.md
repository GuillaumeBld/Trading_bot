# Configuration Overview

The ChatGPT Micro-Cap Trading Bot offers extensive configuration options to customize your trading experience. This guide covers all available settings and how to modify them.

##  Configuration Files

### Core Configuration Files
- **`.env`** - Environment variables and API keys
- **`.llm_config.json`** - LLM provider settings and models
- **`config.json`** - Trading parameters and portfolio settings (optional)

### Data Files
- **`chatgpt_portfolio_update.csv`** - Portfolio history and tracking
- **`chatgpt_trade_log.csv`** - Complete trade transaction log

### Generated Files
- **`__pycache__/`** - Python bytecode cache (auto-generated)
- **`.streamlit/`** - Streamlit app settings (auto-generated)

##  Configuration Hierarchy

Settings are loaded in the following priority order (highest to lowest):

1. **Command-line arguments** - Override everything
2. **Environment variables** - API keys and system settings
3. **Configuration files** - Persistent user preferences
4. **Default values** - Built-in fallbacks

##  Core Settings Categories

### 1. Trading Parameters
```json
{
  "risk_management": {
    "default_stop_loss_pct": 0.15,
    "max_position_size_pct": 0.20,
    "max_portfolio_positions": 7,
    "min_cash_reserve_pct": 0.05
  },
  "market_data": {
    "data_provider": "yfinance",
    "update_frequency": "daily",
    "benchmark_symbols": ["^SPX", "^RUT", "IWO", "XBI"]
  }
}
```

### 2. AI Configuration
```json
{
  "llm_settings": {
    "default_provider": "openai",
    "confidence_threshold": 0.30,
    "max_recommendations": 5,
    "retry_attempts": 3
  },
  "provider_configs": {
    "openai": {
      "model_name": "gpt-4o-mini",
      "temperature": 0.1,
      "max_tokens": 2000
    }
  }
}
```

### 3. Interface Settings
```json
{
  "interface": {
    "default_mode": "interactive",
    "auto_approve_threshold": 0.85,
    "display_reasoning": true,
    "save_conversations": false
  },
  "web_interface": {
    "theme": "light",
    "auto_refresh": false,
    "chart_style": "professional"
  }
}
```

### 4. Data Management
```json
{
  "data_settings": {
    "backup_enabled": true,
    "backup_frequency": "daily",
    "retention_days": 365,
    "export_format": "csv"
  }
}
```

##  Environment Variables

### Required for AI Features
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-key-here
OPENAI_ORG_ID=org-your-org-id-here  # Optional

# Anthropic Configuration  
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Custom API Endpoints (Advanced)
OPENAI_BASE_URL=https://api.openai.com/v1  # Optional override
ANTHROPIC_BASE_URL=https://api.anthropic.com  # Optional override
```

### Optional System Settings
```bash
# Data Directory Override
TRADING_DATA_DIR=/custom/path/to/data

# Logging Configuration
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR
LOG_FILE=/path/to/trading.log

# Performance Settings
MAX_CONCURRENT_REQUESTS=3
REQUEST_TIMEOUT=30
CACHE_ENABLED=true
```

### Development Settings
```bash
# Development Mode
DEVELOPMENT_MODE=true
DEBUG_AI_RESPONSES=true
MOCK_MARKET_DATA=false

# Testing Configuration
TEST_MODE=true
USE_FAKE_API_KEYS=true
SIMULATION_SPEED=1.0
```

##  Quick Configuration

### Setup Wizard
```bash
# Run interactive configuration
python setup_llm.py

# Create configuration with defaults
python setup_llm.py --create-config

# Check current configuration
python setup_llm.py --check
```

### Manual Configuration
```bash
# Create .env file
cat > .env << EOF
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
LOG_LEVEL=INFO
EOF

# Create LLM config
cat > .llm_config.json << EOF
{
  "openai": {
    "model_name": "gpt-4o-mini",
    "temperature": 0.1
  }
}
EOF
```

##  Trading Configuration

### Risk Management Settings
```python
# In trading_script.py or config file
RISK_SETTINGS = {
    "default_stop_loss_percentage": 15,  # 15% below entry
    "maximum_position_size": 20,         # 20% of portfolio
    "maximum_positions": 7,              # Max 7 stocks
    "minimum_cash_reserve": 5,           # Keep 5% cash
    "volatility_adjustment": True,       # Adjust size by volatility
    "correlation_check": True            # Avoid correlated positions
}
```

### Market Data Configuration
```python
MARKET_SETTINGS = {
    "data_source": "yfinance",
    "update_frequency": "daily",
    "premarket_data": False,
    "extended_hours": False,
    "benchmark_indices": ["^SPX", "^RUT", "IWO"],
    "currency": "USD",
    "market": "US"
}
```

### Performance Tracking
```python
PERFORMANCE_SETTINGS = {
    "calculate_sharpe": True,
    "calculate_sortino": True,
    "risk_free_rate": 0.045,  # 4.5% annual
    "benchmark_comparison": True,
    "save_daily_snapshots": True,
    "generate_reports": "weekly"
}
```

##  AI Provider Configuration

### OpenAI Settings
```json
{
  "openai": {
    "model_name": "gpt-4o-mini",        // or "gpt-4o", "gpt-4-turbo"
    "temperature": 0.1,                  // 0.0-2.0, lower = more focused
    "max_tokens": 2000,                  // Response length limit
    "frequency_penalty": 0.0,            // Reduce repetition
    "presence_penalty": 0.0,             // Encourage new topics
    "top_p": 1.0,                        // Nucleus sampling
    "system_prompt": "Custom prompt..."  // Override default prompt
  }
}
```

### Anthropic Settings
```json
{
  "anthropic": {
    "model_name": "claude-3-haiku-20240307",  // or "claude-3-sonnet", "claude-3-opus"
    "temperature": 0.1,
    "max_tokens": 2000,
    "top_p": 1.0,
    "system_prompt": "Custom prompt..."
  }
}
```

### Ollama Settings
```json
{
  "ollama": {
    "model_name": "llama3.1:8b",        // or "mistral:7b", "phi3:mini"
    "base_url": "http://localhost:11434",
    "temperature": 0.1,
    "max_tokens": 2000,
    "num_predict": 2000,                 // Ollama-specific
    "repeat_penalty": 1.1,               // Reduce repetition
    "top_k": 40,                         // Top-K sampling
    "top_p": 0.9                         // Nucleus sampling
  }
}
```

### Hugging Face Settings
```json
{
  "huggingface": {
    "model_name": "microsoft/DialoGPT-medium",
    "device": "auto",                    // "cpu", "cuda", "auto"
    "torch_dtype": "float16",            // "float32", "float16", "bfloat16"
    "max_memory": "8GB",                 // GPU memory limit
    "cache_dir": "./models",             // Model cache location
    "trust_remote_code": false           // Security setting
  }
}
```

##  Configuration Updates

### Dynamic Configuration
```python
# Update settings during runtime
from trading_script import get_llm_manager

llm_manager = get_llm_manager()
llm_manager.config.temperature = 0.2
llm_manager.set_active_provider("anthropic")
```

### Configuration Validation
```bash
# Validate current configuration
python -c "
from llm_interface import LLMManager
manager = LLMManager()
print(' Configuration valid')
print(f'Available providers: {manager.get_available_providers()}')
"
```

### Backup and Restore
```bash
# Backup configuration
cp .env .env.backup
cp .llm_config.json .llm_config.json.backup

# Restore configuration
cp .env.backup .env
cp .llm_config.json.backup .llm_config.json
```

##  Configuration Best Practices

### Security
- **Never commit API keys** to version control
- **Use environment variables** for sensitive data
- **Rotate keys regularly** for production use
- **Limit API key permissions** where possible

### Performance
- **Use local models** for frequent queries
- **Cache responses** when appropriate
- **Set reasonable timeouts** for API calls
- **Monitor usage costs** for paid APIs

### Reliability
- **Configure multiple providers** for redundancy
- **Set conservative confidence thresholds**
- **Enable automatic fallbacks**
- **Log all configuration changes**

### Testing
- **Use separate configs** for development/production
- **Test configuration changes** in safe environment
- **Validate settings** before trading sessions
- **Keep configuration simple** and well-documented

##  Configuration File Locations

### Default Locations
```
Project Root/
 .env                    # Environment variables
 .llm_config.json       # LLM provider settings  
 config.json            # Optional extended config
 .streamlit/            # Streamlit app settings
 data/                  # Data directory
     chatgpt_portfolio_update.csv
     chatgpt_trade_log.csv
```

### Custom Locations
```bash
# Override data directory
export TRADING_DATA_DIR="/custom/path"
python trading_bot.py --data-dir "/custom/path"

# Override config file
python trading_bot.py --config "/path/to/config.json"
```

---

**Next Steps:**
- [Environment Variables Guide](environment-variables.md)
- [LLM Configuration Details](llm-config.md)
- [Trading Parameters Guide](trading-parameters.md)