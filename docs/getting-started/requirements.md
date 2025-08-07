# System Requirements

##  Hardware Requirements

### Minimum Requirements (Manual Trading)
- **CPU**: Any modern processor (Intel/AMD/ARM)
- **RAM**: 2GB available memory
- **Storage**: 100MB free disk space
- **Network**: Internet connection for market data

### Recommended Requirements (AI Trading)
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8GB total system memory (4GB+ available)
- **Storage**: 2GB free disk space
- **Network**: Stable broadband connection

### High-Performance Setup (Local AI)
- **CPU**: 8+ core processor with high single-thread performance
- **RAM**: 16GB+ (for large language models)
- **GPU**: NVIDIA GPU with 8GB+ VRAM (optional, for Hugging Face)
- **Storage**: SSD recommended for model loading

##  Operating System Support

### Officially Supported
- **macOS**: 10.15+ (Catalina and newer)
- **Windows**: Windows 10/11 (64-bit)
- **Linux**: Ubuntu 18.04+, CentOS 7+, Debian 10+

### Tested Configurations
- **macOS Big Sur/Monterey/Ventura** 
- **Windows 10 Pro/Enterprise** 
- **Windows 11** 
- **Ubuntu 20.04/22.04 LTS** 
- **Debian 11/12** 
- **CentOS Stream 8/9** 

### Other Platforms
- **Docker**: Works on any Docker-compatible system
- **WSL2**: Windows Subsystem for Linux (fully supported)
- **Cloud**: AWS, GCP, Azure virtual machines

##  Python Environment

### Python Version
- **Required**: Python 3.9 or higher
- **Recommended**: Python 3.10 or 3.11
- **Tested**: Python 3.9, 3.10, 3.11, 3.12

### Package Managers
- **pip**: Built-in Python package manager (required)
- **conda**: Anaconda/Miniconda (optional, supported)
- **poetry**: Modern dependency management (optional)

### Virtual Environments
- **venv**: Built-in virtual environment (recommended)
- **conda env**: Conda environments (supported)
- **virtualenv**: Third-party virtual environments (supported)

##  Core Dependencies

### Essential Packages (Always Required)
```
pandas>=2.0.0          # Data manipulation
numpy>=1.20.0           # Numerical computing
yfinance>=0.2.0         # Market data
matplotlib>=3.5.0       # Visualization
```

### Web Interface (Optional)
```
streamlit>=1.30.0       # Web application framework
```

### AI Integration (Optional)
```
openai>=1.0.0           # OpenAI API
anthropic>=0.8.0        # Anthropic API
ollama>=0.1.7           # Local Ollama models
transformers>=4.30.0    # Hugging Face models
torch>=2.0.0            # PyTorch (for local models)
python-dotenv>=1.0.0    # Environment variables
pydantic>=2.0.0         # Data validation
```

##  Network Requirements

### Internet Connectivity
- **Market Data**: Access to Yahoo Finance APIs
- **AI APIs**: HTTPS access to provider endpoints
- **Package Installation**: Access to PyPI and package repositories

### Firewall Considerations
- **Outbound HTTPS (443)**: Required for all external services
- **Outbound HTTP (80)**: May be needed for some package installations
- **Ollama Local (11434)**: Only if using local Ollama server

### Bandwidth Requirements
- **Market Data**: ~1MB per trading session
- **AI API Calls**: ~10-50KB per recommendation
- **Local AI**: No external bandwidth after initial setup

##  Account Requirements

### Trading (Required)
- **No brokerage account needed**: This is a tracking/analysis tool
- **Starting capital**: Any amount (can start with $100 or even less)

### AI Providers (Optional)
- **OpenAI**: Account at [platform.openai.com](https://platform.openai.com)
- **Anthropic**: Account at [console.anthropic.com](https://console.anthropic.com)
- **Ollama**: No account needed (fully local)
- **Hugging Face**: Optional account for model downloads

### Cost Estimates (AI Usage)
- **OpenAI GPT-4o-mini**: ~$0.15-0.60 per trading session
- **Anthropic Claude-3-haiku**: ~$0.25-0.80 per trading session
- **Ollama/Hugging Face**: $0 (free, uses local compute)

##  Development Requirements

### Additional Tools (For Contributors)
- **Git**: Version control system
- **Code Editor**: VS Code, PyCharm, or similar
- **pytest**: Testing framework
- **black**: Code formatting
- **flake8**: Code linting

### Optional Enhancements
- **Jupyter**: For data analysis notebooks
- **Docker**: For containerized deployment
- **PostgreSQL**: For advanced data storage (future feature)

##  Performance Considerations

### Manual Trading Performance
- **Startup Time**: < 5 seconds
- **Trade Processing**: < 1 second per trade
- **Memory Usage**: ~50-100MB
- **CPU Usage**: Minimal (< 5%)

### AI Trading Performance
- **API Response**: 2-10 seconds per recommendation
- **Local AI Response**: 5-30 seconds (depends on model size)
- **Memory Usage**: 100MB-4GB (depends on local model)
- **CPU Usage**: Variable (high during AI inference)

### Optimization Tips
- **Use SSD storage** for faster model loading
- **Close other applications** when using local AI
- **Use GPU acceleration** for Hugging Face models
- **Cache API responses** to reduce costs

##  Testing Your System

### Quick System Check
```bash
# Check Python version
python --version

# Check available memory
python -c "import psutil; print(f'Available RAM: {psutil.virtual_memory().available / 1024**3:.1f}GB')"

# Test core dependencies
python -c "import pandas, numpy, yfinance, matplotlib; print('Core dependencies OK')"
```

### Performance Benchmark
```bash
# Run the demo to test your system
python demo_llm_features.py

# Test market data access
python -c "import yfinance as yf; print(yf.download('AAPL', period='1d'))"
```

### AI System Check
```bash
# Test AI setup
python setup_llm.py --check

# List available providers
python trading_bot.py --list-providers
```

##  Known Limitations

### Platform-Specific Issues
- **Apple Silicon (M1/M2)**: Some AI packages need Rosetta for compatibility
- **Windows**: Long path support may need to be enabled
- **Linux**: Some distributions need additional development packages

### Memory Limitations
- **Local AI models**: Large models (>7B parameters) need 16GB+ RAM
- **Windows 32-bit**: Not supported (use 64-bit Python)
- **Low memory systems**: Stick to API-based AI providers

### Network Limitations
- **Corporate firewalls**: May block AI API access
- **Slow connections**: Local AI recommended for unreliable internet
- **Data caps**: AI APIs use minimal data, local models use none after setup

---

**Need help with installation?** Check our [Installation Guide](../installation/basic-setup.md) or [Troubleshooting](../troubleshooting/common-issues.md) section.