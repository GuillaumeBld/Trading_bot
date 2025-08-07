# 📁 Repository Structure Guide

This document explains the clean, organized structure of the ChatGPT Micro-Cap Trading Bot repository.

## 🎯 Organization Principles

The repository follows modern Python project standards with clear separation of concerns:

- **📦 Source Code** (`src/`) - All Python modules organized by functionality
- **📊 Data** (`data/`) - Portfolio data, trades, and backups
- **🛠️ Scripts** (`scripts/`) - Utility scripts and tools
- **📚 Documentation** (`docs/`) - Comprehensive user and developer guides
- **🗃️ Archive** (`archive/`) - Historical files and original structure
- **🎨 Assets** (`assets/`) - Images, reports, and static files

## 📂 Directory Structure

```
chatgpt-microcap-experiment/
├── 📄 README.md                    # Main project overview
├── 📄 CONTRIBUTING.md              # Contribution guidelines
├── 📄 requirements.txt             # Python dependencies
├── 📄 setup.py                     # Package installation
├── 📄 .gitignore                   # Git ignore rules
├── 🚀 run_dashboard.py             # Quick dashboard launcher
├── 🚀 run_trading.py               # Quick CLI launcher
│
├── 📦 src/                         # Source Code
│   ├── 🧠 core/                    # Core Business Logic
│   │   ├── trading_script.py       # Main trading engine
│   │   ├── llm_interface.py        # AI integration
│   │   └── __init__.py
│   ├── 🖥️ interfaces/              # User Interfaces
│   │   ├── advanced_dashboard.py   # Full-featured dashboard
│   │   ├── dashboard_app.py        # Alternative dashboard
│   │   ├── streamlit_app.py        # Basic web interface
│   │   ├── trading_bot.py          # Command-line interface
│   │   └── __init__.py
│   ├── 🔧 services/                # External Services
│   │   ├── market_data_service.py  # Market data & news
│   │   └── __init__.py
│   ├── ⚙️ config/                  # Configuration
│   │   ├── dashboard_config.py     # Settings management
│   │   └── __init__.py
│   └── __init__.py
│
├── 📊 data/                        # Data Storage
│   ├── portfolio/                  # Portfolio snapshots
│   │   └── .gitkeep
│   ├── trades/                     # Trade history
│   │   └── .gitkeep
│   └── backups/                    # Data backups
│       └── .gitkeep
│
├── 🛠️ scripts/                     # Utility Scripts
│   ├── setup/                      # Installation & Setup
│   │   └── setup_llm.py           # AI provider setup
│   ├── utils/                      # Helper Utilities
│   │   └── launch_dashboard.py    # Dashboard launcher
│   └── demos/                      # Demonstrations
│       ├── demo_dashboard.py      # Dashboard demo
│       └── demo_llm_features.py   # AI features demo
│
├── 🎨 assets/                      # Static Assets
│   ├── images/                     # Screenshots & charts
│   │   └── (6-30 - 7-25) Results.png
│   └── reports/                    # Generated reports
│       ├── Starting Research.pdf
│       ├── Week 1.pdf
│       ├── Week 2.pdf
│       ├── Week 3.pdf
│       ├── Week 4.pdf
│       ├── Week 5.pdf
│       └── Week 6.pdf
│
├── 📚 docs/                        # Documentation
│   ├── README.md                   # Documentation index
│   ├── getting-started/            # New user guides
│   ├── installation/               # Setup instructions
│   ├── configuration/              # Settings guides
│   ├── usage/                      # Interface guides
│   ├── llm-providers/             # AI setup guides
│   ├── tutorials/                  # Step-by-step tutorials
│   ├── examples/                   # Real-world examples
│   ├── troubleshooting/           # Help & FAQ
│   └── api-reference/             # Technical docs
│
├── 🚀 future-enhancements/         # Development Planning
│   ├── README.md                   # Planning overview
│   ├── roadmap/                    # Development timeline
│   ├── feature-requests/           # Community requests
│   ├── research/                   # AI & trading research
│   ├── architecture/               # System design
│   ├── integrations/               # Third-party connections
│   └── DEVELOPMENT_PRIORITIES.md   # Strategic priorities
│
├── 🗃️ archive/                     # Historical Files
│   └── original-structure/         # Original file organization
│       ├── Experiment Details/
│       ├── Scripts and CSV Files/
│       ├── Start Your Own/
│       ├── Weekly Deep Research (MD)/
│       └── Weekly Deep Research (PDF)/
│
├── 🧪 tests/                       # Test Suites
│   ├── unit/                       # Unit tests
│   │   └── .gitkeep
│   └── integration/                # Integration tests
│       └── .gitkeep
│
└── 📁 Other/                       # Miscellaneous
    ├── License.txt                 # MIT License
    └── ignore_list.gitignore       # Additional ignore rules
```

## 🚀 Quick Start Commands

### Easy Launchers (Root Directory)
```bash
# Launch advanced dashboard
python run_dashboard.py

# Launch CLI trading bot
python run_trading.py
```

### Full Commands
```bash
# Advanced dashboard
python scripts/utils/launch_dashboard.py --advanced

# CLI with AI
python src/interfaces/trading_bot.py --ai --provider openai

# Basic web interface
streamlit run src/interfaces/streamlit_app.py

# Setup wizard
python scripts/setup/setup_llm.py

# Demo with sample data
python scripts/demos/demo_dashboard.py
```

## 📦 Package Structure

The `src/` directory is organized as a proper Python package:

### Core Business Logic (`src/core/`)
- **`trading_script.py`** - Main trading engine with portfolio management
- **`llm_interface.py`** - AI provider integration and management

### User Interfaces (`src/interfaces/`)
- **`advanced_dashboard.py`** - Full-featured web dashboard with configuration
- **`trading_bot.py`** - Command-line interface for scripting
- **`streamlit_app.py`** - Basic web interface for beginners
- **`dashboard_app.py`** - Alternative dashboard implementation

### External Services (`src/services/`)
- **`market_data_service.py`** - Market data, news, and sentiment analysis

### Configuration (`src/config/`)
- **`dashboard_config.py`** - Comprehensive settings management with encryption

## 📊 Data Organization

### Portfolio Data (`data/portfolio/`)
- Daily portfolio snapshots
- Performance metrics
- Benchmark comparisons

### Trade Data (`data/trades/`)
- Complete trade history
- Transaction logs
- P&L tracking

### Backups (`data/backups/`)
- Automated data backups
- Configuration snapshots
- Recovery files

## 🛠️ Scripts Organization

### Setup Scripts (`scripts/setup/`)
- **`setup_llm.py`** - Interactive AI provider configuration

### Utilities (`scripts/utils/`)
- **`launch_dashboard.py`** - Multi-option dashboard launcher

### Demos (`scripts/demos/`)
- **`demo_dashboard.py`** - Creates sample data and launches demo
- **`demo_llm_features.py`** - Demonstrates AI integration features

## 📚 Documentation Structure

Comprehensive documentation organized by user type and use case:

- **Getting Started** - New user onboarding
- **Installation** - Setup guides for all platforms
- **Configuration** - Detailed settings documentation
- **Usage** - Interface guides and workflows
- **LLM Providers** - AI setup for each provider
- **Tutorials** - Step-by-step learning paths
- **Examples** - Real-world usage scenarios
- **Troubleshooting** - Problem-solving guides
- **API Reference** - Technical documentation

## 🔒 Security & Privacy

### Protected Files (.gitignore)
- API keys and secrets (`.env`, `*.key`)
- Personal trading data (`data/portfolio/*.csv`)
- Configuration with sensitive info
- Cache and temporary files

### Included Examples
- `.env.example` - Template for environment variables
- Sample configurations without sensitive data
- Demo data for testing

## 🧪 Testing Structure

### Unit Tests (`tests/unit/`)
- Core logic testing
- Individual component tests
- Mock external dependencies

### Integration Tests (`tests/integration/`)
- End-to-end workflows
- API integration testing
- User interface testing

## 🗃️ Archive Organization

Historical files preserved in `archive/original-structure/`:
- Original experiment documentation
- Legacy scripts and data
- Research reports and findings
- Maintains project history while keeping main structure clean

## ✨ Benefits of This Organization

### For Users
- **Easy Navigation** - Clear structure with logical grouping
- **Quick Access** - Root-level launchers for common tasks
- **Comprehensive Docs** - Everything needed to get started and succeed

### For Developers
- **Standard Structure** - Follows Python packaging conventions
- **Separation of Concerns** - Clear boundaries between components
- **Extensible** - Easy to add new features and interfaces
- **Testable** - Proper structure for unit and integration tests

### For Contributors
- **Clear Guidelines** - CONTRIBUTING.md with detailed instructions
- **Organized Codebase** - Easy to understand and modify
- **Documentation First** - Changes require documentation updates
- **Quality Standards** - Linting, testing, and review processes

## 🔄 Migration from Old Structure

If you have data from the old structure:

1. **Portfolio Data**: Move CSV files to `data/portfolio/`
2. **Configuration**: Run `python scripts/setup/setup_llm.py` to recreate
3. **Custom Scripts**: Place in appropriate `scripts/` subdirectory
4. **Documentation**: Check if covered in new docs, otherwise add to appropriate section

## 📞 Getting Help

- **Structure Questions**: Check this document first
- **Usage Help**: See `docs/README.md` for comprehensive guides
- **Technical Issues**: Use `docs/troubleshooting/faq.md`
- **Contributing**: Follow `CONTRIBUTING.md` guidelines

---

**This clean, organized structure makes the ChatGPT Micro-Cap Trading Bot professional, maintainable, and easy to navigate for users of all skill levels.**