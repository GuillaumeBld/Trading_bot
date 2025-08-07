# Basic Installation Guide

This guide will walk you through installing the ChatGPT Micro-Cap Trading Bot on your system. Choose the method that best suits your needs.

## 🎯 Installation Options

### Option 1: Quick Install (Recommended for Beginners)
- **Time**: 5-10 minutes
- **Complexity**: Low
- **Features**: Manual trading + basic AI

### Option 2: Full Install (Recommended for Most Users)
- **Time**: 15-20 minutes  
- **Complexity**: Medium
- **Features**: All AI providers + web interface

### Option 3: Development Install
- **Time**: 30+ minutes
- **Complexity**: High
- **Features**: Everything + development tools

## 🚀 Option 1: Quick Install

### Step 1: Download the Project
```bash
# Method A: Download ZIP file
# Go to GitHub, click "Code" → "Download ZIP"
# Extract to your desired location

# Method B: Git clone (if you have Git)
git clone https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment
```

### Step 2: Install Python Dependencies
```bash
# Install minimal dependencies for manual trading
pip install pandas numpy yfinance matplotlib

# Or install everything at once
pip install -r requirements.txt
```

### Step 3: Test Installation
```bash
# Test basic functionality
python trading_bot.py --help

# Run a quick demo
python demo_llm_features.py
```

### Step 4: Start Trading
```bash
# Manual trading mode
python trading_bot.py

# Follow the prompts to create your first portfolio
```

**✅ You're done!** Skip to [First Steps](#-first-steps) below.

## 🔧 Option 2: Full Install

### Step 1: Prepare Your Environment
```bash
# Create a virtual environment (recommended)
python -m venv trading_bot_env

# Activate the environment
# On Windows:
trading_bot_env\Scripts\activate
# On macOS/Linux:
source trading_bot_env/bin/activate
```

### Step 2: Get the Project
```bash
# Clone the repository
git clone https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment

# Or download and extract ZIP file, then navigate to folder
```

### Step 3: Install All Dependencies
```bash
# Install all packages including AI support
pip install -r requirements.txt

# Verify installation
pip list | grep -E "(pandas|yfinance|openai|anthropic|ollama)"
```

### Step 4: Configure AI Providers
```bash
# Run the setup wizard
python setup_llm.py

# This will:
# - Create .env file for API keys
# - Create .llm_config.json for settings
# - Check which providers are available
```

### Step 5: Add API Keys (Optional)
```bash
# Edit the .env file created by setup
# Add your API keys:
echo "OPENAI_API_KEY=your_key_here" >> .env
echo "ANTHROPIC_API_KEY=your_key_here" >> .env
```

### Step 6: Test Everything
```bash
# Check AI provider availability
python trading_bot.py --list-providers

# Test web interface
streamlit run streamlit_app.py
# Open browser to http://localhost:8501
```

**✅ Full installation complete!**

## 👨‍💻 Option 3: Development Install

### Step 1: Development Environment
```bash
# Install Git (if not already installed)
# Windows: Download from https://git-scm.com/
# macOS: Install Xcode command line tools
# Linux: sudo apt install git (Ubuntu) or yum install git (CentOS)

# Clone with development branch
git clone -b develop https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment
```

### Step 2: Python Environment Setup
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip setuptools wheel
```

### Step 3: Install Development Dependencies
```bash
# Install all dependencies including dev tools
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If available

# Or install manually
pip install pytest black flake8 mypy jupyter
```

### Step 4: Development Configuration
```bash
# Install in editable mode
pip install -e .

# Set up pre-commit hooks (optional)
pre-commit install

# Run tests to verify setup
python -m pytest tests/
```

### Step 5: IDE Setup (Optional)
```bash
# VS Code settings
mkdir .vscode
cat > .vscode/settings.json << EOF
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black"
}
EOF
```

## 🔧 Platform-Specific Instructions

### Windows Users
```powershell
# Use PowerShell or Command Prompt
# Make sure Python is in your PATH

# If you get execution policy errors:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install using pip
pip install -r requirements.txt

# For Ollama (optional):
# Download from https://ollama.ai/download
```

### macOS Users
```bash
# Install Python via Homebrew (recommended)
brew install python

# Or use the official installer from python.org

# For Apple Silicon Macs, you might need:
export GRPC_PYTHON_BUILD_SYSTEM_OPENSSL=1
export GRPC_PYTHON_BUILD_SYSTEM_ZLIB=1

# Install dependencies
pip install -r requirements.txt

# For Ollama:
brew install ollama
```

### Linux Users
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv git

# CentOS/RHEL/Fedora
sudo yum install python3 python3-pip git
# or
sudo dnf install python3 python3-pip git

# Install dependencies
pip3 install -r requirements.txt

# For Ollama:
curl -fsSL https://ollama.ai/install.sh | sh
```

## 🐳 Docker Installation (Alternative)

### Using Docker Compose
```bash
# Download docker-compose.yml
curl -O https://raw.githubusercontent.com/your-repo/chatgpt-microcap-experiment/main/docker-compose.yml

# Start the application
docker-compose up -d

# Access web interface at http://localhost:8501
```

### Manual Docker Build
```bash
# Clone repository
git clone https://github.com/your-repo/chatgpt-microcap-experiment.git
cd chatgpt-microcap-experiment

# Build image
docker build -t trading-bot .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data trading-bot
```

## ✅ Verification Steps

### Test Core Functionality
```bash
# Test Python imports
python -c "import pandas, numpy, yfinance, matplotlib; print('✅ Core imports successful')"

# Test market data access
python -c "import yfinance as yf; data = yf.download('AAPL', period='1d'); print('✅ Market data access working')"

# Test trading script
python trading_script.py --help
```

### Test AI Integration
```bash
# Check provider availability
python setup_llm.py --check

# Test AI functionality (if configured)
python trading_bot.py --list-providers
```

### Test Web Interface
```bash
# Start Streamlit app
streamlit run streamlit_app.py

# Should open browser to http://localhost:8501
# You should see the trading interface
```

## 🆘 Common Installation Issues

### Python Version Issues
```bash
# Check Python version
python --version

# If version < 3.9, update Python:
# Windows: Download from python.org
# macOS: brew install python@3.11
# Linux: Use package manager or pyenv
```

### Package Installation Failures
```bash
# Update pip first
pip install --upgrade pip

# Install with verbose output to see errors
pip install -v package_name

# Use conda as alternative
conda install package_name
```

### Permission Issues
```bash
# Use virtual environment (recommended)
python -m venv venv
source venv/bin/activate

# Or install for user only
pip install --user -r requirements.txt
```

### Network/Firewall Issues
```bash
# Test internet connectivity
ping pypi.org

# Use different index if blocked
pip install -i https://pypi.python.org/simple/ package_name

# Download packages offline
pip download -r requirements.txt
pip install --find-links . --no-index -r requirements.txt
```

## 🎯 First Steps

Once installation is complete:

1. **Manual Trading**: Run `python trading_bot.py` and follow prompts
2. **AI Setup**: Run `python setup_llm.py` to configure AI providers
3. **Web Interface**: Run `streamlit run streamlit_app.py` for GUI
4. **Read Documentation**: Check [Usage Guides](../usage/command-line.md)

## 📚 Next Steps

- **[Quick Start Guide](../getting-started/quick-start.md)** - Start trading immediately
- **[Configuration Guide](../configuration/overview.md)** - Customize your setup
- **[AI Provider Setup](../llm-providers/comparison.md)** - Configure AI assistance
- **[Usage Tutorials](../tutorials/basic-tutorial.md)** - Learn the interface

---

**Need help?** Check our [Troubleshooting Guide](../troubleshooting/common-issues.md) or [FAQ](../troubleshooting/faq.md).