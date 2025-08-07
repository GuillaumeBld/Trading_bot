# AI-Powered Trading Bot 🤖📈

A sophisticated trading bot powered by Large Language Models (LLMs) with comprehensive risk management, real-time monitoring, and multi-platform notifications.

## 🚀 Features

### Core Trading Capabilities
- **AI-Powered Decision Making**: Integration with OpenAI, Anthropic, and local LLMs (Ollama, Hugging Face)
- **Real-Time Market Analysis**: Live market data processing and sentiment analysis
- **Automated Trading**: Intelligent position management with stop-loss and take-profit automation
- **Risk Management**: Comprehensive portfolio monitoring and automated risk assessment

### Advanced Features
- **Multi-LLM Support**: Use different AI models for trading decisions
- **Dynamic Dashboard**: Real-time performance monitoring and configuration
- **n8n Workflow Integration**: Automated notifications and external system integration
- **Multi-Channel Notifications**: Slack, Discord, Email alerts
- **Backtesting**: Historical performance analysis
- **Docker Support**: Easy deployment and containerization

## 📊 System Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Trading Bot   │    │   Dashboard     │    │   n8n Workflows │
│                 │    │                 │    │                 │
│ • AI Analysis   │◄──►│ • Monitoring    │◄──►│ • Notifications │
│ • Risk Mgmt     │    │ • Configuration │    │ • Integrations  │
│ • Execution     │    │ • Visualization │    │ • Automation    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🛠️ Installation

### Quick Start
```bash
git clone https://github.com/GuillaumeBld/Trading_bot.git
cd Trading_bot
pip install -r requirements.txt
python setup.py
```

### Run the Dashboard
```bash
python scripts/run_dashboard.py
```

### Run the Trading Bot
```bash
python scripts/run_trading.py
```

### Run the Dynamic Dashboard
```bash
python scripts/run_dynamic_dashboard.py
```

## 📁 Project Structure

```
unified-trading-bot/
├── src/                    # Core source code
│   ├── core/              # Trading engine and LLM interface
│   │   ├── trading_engine.py    # Main trading engine
│   │   ├── trading_script.py    # Trading script implementation
│   │   └── llm_interface.py     # AI integration
│   ├── interfaces/        # User interfaces and dashboards
│   │   ├── advanced_dashboard.py    # Full-featured dashboard
│   │   ├── dashboard_app.py         # Dashboard application
│   │   ├── dynamic_dashboard.py     # Dynamic dashboard
│   │   ├── trading_bot.py           # CLI interface
│   │   ├── streamlit_app.py         # Basic web UI
│   │   └── real_time_service.py     # Real-time services
│   ├── services/          # Market data and real-time services
│   │   ├── market_data_service.py   # Market data service
│   │   └── real_time_service.py     # Real-time monitoring
│   └── config/            # Configuration management
│       ├── dashboard_config.py      # Dashboard settings
│       └── dynamic_config.py        # Dynamic configuration
├── scripts/               # Utility and setup scripts
│   ├── run_dashboard.py           # Dashboard launcher
│   ├── run_trading.py             # Trading bot launcher
│   ├── run_dynamic_dashboard.py   # Dynamic dashboard launcher
│   ├── demo_dashboard.py          # Demo dashboard
│   ├── demo_llm_features.py       # LLM features demo
│   ├── setup_llm.py               # LLM setup wizard
│   ├── launch_dashboard.py        # Dashboard launcher
│   └── utils/                     # Utility scripts
├── n8n-integration/       # n8n workflow automation
│   ├── workflows/         # Pre-built n8n workflows
│   ├── docker/           # Docker deployment files
│   └── api-wrapper/      # FastAPI integration layer
├── docs/                  # Comprehensive documentation
├── deployment/            # Deployment guides and scripts
├── data/                  # Data storage
│   ├── portfolio/         # Portfolio snapshots
│   ├── trades/           # Trade history
│   └── backups/          # Data backups
├── assets/               # Static assets
│   ├── images/           # Screenshots & charts
│   └── reports/          # Generated reports
└── future-enhancements/  # Development roadmap
```

## 🔧 Configuration

### LLM Configuration
Create a `.env` file:
```env
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
HUGGINGFACE_API_KEY=your_hf_key
TRADING_BOT_API_KEY=your_broker_api
```

### Dashboard Configuration
```python
# Edit src/config/dashboard_config.py
DASHBOARD_CONFIG = {
    "port": 8501,
    "theme": "dark",
    "update_interval": 30  # seconds
}
```

## 🤖 n8n Workflows

The system includes 5 pre-built n8n workflows:

1. **🤖 AI Trading Signal Processor** - Processes trading signals with AI analysis
2. **📊 Portfolio Monitor & Risk Management** - Continuous portfolio monitoring
3. **🔔 Multi-Channel Notification Hub** - Smart notification routing
4. **🧠 AI Market Analysis & News Monitor** - News-based market analysis
5. **⚠️ Risk Management & Stop Loss Automation** - Automated risk controls

### Deploy n8n Workflows
```bash
cd n8n-integration
docker-compose up -d
```

## 📈 Usage Examples

### Basic Trading
```python
from src.core.trading_script import TradingBot

bot = TradingBot()
bot.configure_llm("openai", model="gpt-4")
bot.start_trading()
```

### Advanced Configuration
```python
bot.set_risk_parameters({
    "max_position_size": 0.1,  # 10% of portfolio
    "stop_loss": 0.05,         # 5% stop loss
    "confidence_threshold": 0.7 # 70% AI confidence minimum
})
```

## 🛡️ Security Features

- **API Key Encryption**: Secure credential storage
- **Rate Limiting**: Protection against API abuse
- **Input Validation**: Comprehensive data sanitization
- **Error Handling**: Graceful failure management

## 📊 Performance Monitoring

Access the real-time dashboard at `http://localhost:8501`:

- Portfolio performance metrics
- Trade execution logs
- AI decision analysis
- Risk assessment dashboard
- Real-time market data

## 🔗 Integrations

### Supported Brokers
- **Paper Trading**: Built-in simulation mode
- **Interactive Brokers**: Professional trading platform
- **Alpaca**: Commission-free trading API
- **Custom Broker APIs**: Extensible integration framework

### AI Providers
- **OpenAI**: GPT-3.5, GPT-4, GPT-4-turbo
- **Anthropic**: Claude-3 Sonnet, Claude-3 Opus
- **Local Models**: Ollama, Hugging Face Transformers
- **Custom Providers**: Extensible LLM framework

## 🚀 Deployment

### Local Development
```bash
python scripts/run_dashboard.py
```

### Docker Deployment
```bash
docker-compose up -d
```

### Cloud Deployment (Hostinger/VPS)
```bash
./deployment/hostinger-quick-deploy.sh
```

## 📚 Documentation

- **[Getting Started Guide](docs/getting-started/overview.md)**
- **[Configuration Manual](docs/configuration/overview.md)**
- **[n8n Integration Guide](n8n-integration/docs/setup-guide.md)**
- **[API Reference](docs/api-reference/)**
- **[Troubleshooting](docs/troubleshooting/faq.md)**

## 🤝 Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## 📄 License

This project is licensed under the MIT License - see the [License.txt](Other/License.txt) file for details.

## ⚠️ Disclaimer

This software is for educational and research purposes. Trading involves substantial risk of loss. The authors are not responsible for any financial losses incurred through the use of this software.

## 🌟 Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/GuillaumeBld/Trading_bot/issues)
- **Documentation**: [Comprehensive guides and tutorials](docs/)
- **Community**: [Join our discussions](https://github.com/GuillaumeBld/Trading_bot/discussions)

---

**Built with ❤️ by [Guillaume](https://github.com/GuillaumeBld)**

*Empowering traders with AI-driven insights and automated decision-making.*