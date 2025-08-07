# Project Structure Documentation

## Overview

This unified trading bot project consolidates all the best features from multiple development iterations into a single, well-organized codebase. The project follows a modular architecture with clear separation of concerns.

## Directory Structure

```
unified-trading-bot/
  src/                          # Core source code
     core/                     # Core trading logic
       trading_engine.py        # Main trading engine (783 lines)
       trading_script.py        # Trading script implementation (575 lines)
       llm_interface.py         # AI integration (485 lines)
     interfaces/               # User interfaces and dashboards
       advanced_dashboard.py    # Full-featured dashboard (1095 lines)
       dashboard_app.py         # Dashboard application (834 lines)
       dynamic_dashboard.py     # Dynamic dashboard (549 lines)
       trading_bot.py           # CLI interface (178 lines)
       streamlit_app.py         # Basic web UI (145 lines)
       real_time_service.py     # Real-time services (447 lines)
     services/                 # External services
       market_data_service.py   # Market data & news (558 lines)
       real_time_service.py     # Real-time monitoring (duplicate)
     config/                   # Configuration management
        dashboard_config.py      # Dashboard settings (430 lines)
        dynamic_config.py        # Dynamic configuration
  scripts/                      # Utility and setup scripts
    run_dashboard.py             # Dashboard launcher (28 lines)
    run_trading.py               # Trading bot launcher (33 lines)
    run_dynamic_dashboard.py     # Dynamic dashboard launcher (54 lines)
    demo_dashboard.py            # Demo dashboard (363 lines)
    demo_llm_features.py         # LLM features demo (198 lines)
    setup_llm.py                 # LLM setup wizard (262 lines)
    launch_dashboard.py          # Dashboard launcher (255 lines)
    utils/                       # Utility scripts
        launch_dynamic_dashboard.py
  data/                         # Data storage
    portfolio/                   # Portfolio snapshots
    trades/                      # Trade history
    backups/                     # Data backups
  assets/                       # Static assets
    images/                      # Screenshots & charts
    reports/                     # Generated reports
  docs/                         # Comprehensive documentation
    getting-started/             # Quick start guides
    configuration/               # Configuration guides
    usage/                       # Usage documentation
    tutorials/                   # Tutorial guides
    troubleshooting/             # FAQ and troubleshooting
    examples/                    # Code examples
    llm-providers/               # LLM provider guides
    installation/                # Installation guides
  deployment/                   # Deployment guides and scripts
    hostinger-deployment-guide.md
    hostinger-quick-deploy.sh
  n8n-integration/              # n8n workflow automation
    workflows/                   # Pre-built n8n workflows
    docker/                      # Docker deployment files
    api-wrapper/                 # FastAPI integration layer
    docs/                        # n8n setup guides
  future-enhancements/          # Development roadmap
    architecture/                # System evolution plans
    feature-requests/            # Feature request templates
    integrations/                # Broker integration plans
    research/                    # AI trading research
    roadmap/                     # Development roadmap
  Experiment Details/           # Original experiment data
  Scripts and CSV Files/        # Original trading scripts
  Start Your Own/               # Starter templates
  Weekly Deep Research (MD)/    # Research summaries
  Weekly Deep Research (PDF)/   # Research PDFs
  Other/                        # Miscellaneous files
```

## Key Components

### Core Trading Engine (`src/core/`)

- **`trading_engine.py`**: The main trading engine that orchestrates all trading operations
- **`trading_script.py`**: Implementation of trading strategies and algorithms
- **`llm_interface.py`**: Integration layer for all AI/LLM providers (OpenAI, Anthropic, Ollama, Hugging Face)

### User Interfaces (`src/interfaces/`)

- **`advanced_dashboard.py`**: Full-featured web dashboard with real-time monitoring
- **`dashboard_app.py`**: Streamlit-based dashboard application
- **`dynamic_dashboard.py`**: Dynamic dashboard with live updates
- **`trading_bot.py`**: Command-line interface for trading operations
- **`streamlit_app.py`**: Simple web interface for beginners
- **`real_time_service.py`**: Real-time data processing and monitoring

### Services (`src/services/`)

- **`market_data_service.py`**: Market data fetching and processing
- **`real_time_service.py`**: Real-time monitoring and alerting

### Configuration (`src/config/`)

- **`dashboard_config.py`**: Dashboard configuration settings
- **`dynamic_config.py`**: Dynamic configuration management

### Scripts (`scripts/`)

- **`run_dashboard.py`**: Launcher for the main dashboard
- **`run_trading.py`**: Launcher for the trading bot
- **`run_dynamic_dashboard.py`**: Launcher for the dynamic dashboard
- **`demo_dashboard.py`**: Demo dashboard with sample data
- **`demo_llm_features.py`**: Demo of LLM features
- **`setup_llm.py`**: Interactive LLM setup wizard
- **`launch_dashboard.py`**: Alternative dashboard launcher

## Data Organization

### Data Storage (`data/`)
- **`portfolio/`**: Portfolio snapshots and performance data
- **`trades/`**: Trade history and execution logs
- **`backups/`**: Automated data backups

### Assets (`assets/`)
- **`images/`**: Screenshots, charts, and visual assets
- **`reports/`**: Generated performance reports and analytics

## Documentation Structure

### Getting Started (`docs/getting-started/`)
- Quick start guides for new users
- Basic setup instructions
- Requirements and dependencies

### Configuration (`docs/configuration/`)
- Detailed configuration guides
- Environment setup
- API key management

### Usage (`docs/usage/`)
- Dashboard usage guides
- Trading bot usage
- Command-line interface guides

### Tutorials (`docs/tutorials/`)
- Step-by-step tutorials
- Example trading sessions
- Best practices

### Troubleshooting (`docs/troubleshooting/`)
- FAQ and common issues
- Error resolution guides
- Support resources

## Integration Features

### n8n Workflows (`n8n-integration/`)
- Pre-built automation workflows
- Docker deployment configuration
- API wrapper for external integrations

### Deployment (`deployment/`)
- Hostinger deployment guides
- Quick deployment scripts
- Cloud deployment instructions

## Development Roadmap

### Future Enhancements (`future-enhancements/`)
- Architecture evolution plans
- Feature request tracking
- Research and development notes
- Quarterly roadmaps

## File Size and Complexity

The project contains:
- **Total Python files**: 25+ core files
- **Total lines of code**: 10,000+ lines
- **Documentation**: Comprehensive guides and tutorials
- **Dependencies**: 51 packages in requirements.txt

## Migration Notes

This unified project consolidates the best features from:
1. **Original ChatGPT-Micro-Cap-Experiment**: Most complete implementation
2. **ChatGPT-Micro-Cap-Experiment-Rebuilt**: Better structure but incomplete
3. **Trading_bot_clean_new**: Minimal implementation (discarded)

## Key Improvements Made

1. **Organized Structure**: All files moved to appropriate directories
2. **Unified Codebase**: Single source of truth for all features
3. **Updated Documentation**: Corrected paths and instructions
4. **Clean Architecture**: Clear separation of concerns
5. **Comprehensive Features**: All original functionality preserved

## Usage Instructions

### Quick Start
```bash
cd unified-trading-bot
pip install -r requirements.txt
python setup.py
python scripts/run_dashboard.py
```

### Development
```bash
python scripts/run_trading.py
python scripts/run_dynamic_dashboard.py
```

### Documentation
- Start with `docs/getting-started/overview.md`
- Configuration: `docs/configuration/overview.md`
- Usage: `docs/usage/dashboard-guide.md` 