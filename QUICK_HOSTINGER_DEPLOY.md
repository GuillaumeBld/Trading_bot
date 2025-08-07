#  Quick Hostinger Deployment - Working Solution

## Current Situation
You're connected to your Hostinger VPS (Ubuntu 24.04.2 LTS) but the original deployment guide references a non-existent GitHub repository.

##  Step-by-Step Solution (Copy & Paste These Commands)

### Step 1: Install Required Dependencies
```bash
# Install all required packages (copy and paste this entire block)
sudo apt update
sudo apt install -y unzip git python3 python3-pip python3-venv curl nano htop wget
```

### Step 2: Install Docker (Required for the full system)
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Step 3: Create Project Directory
```bash
# Create and set up project directory
sudo mkdir -p /opt/trading-bot
sudo chown $USER:$USER /opt/trading-bot
cd /opt/trading-bot
```

### Step 4: Upload Your Code (Choose One Method)

#### Method A: Manual File Creation (Quick Test)
```bash
# Create a basic Python environment for testing
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy yfinance streamlit plotly

# Create a simple test file
cat > test_app.py << 'EOF'
import streamlit as st
import pandas as pd
import yfinance as yf

st.title(" Trading Bot - Test Deployment")
st.write("If you can see this, your server is working!")

# Test data fetching
ticker = st.selectbox("Select a stock:", ["AAPL", "MSFT", "GOOGL"])
if st.button("Get Stock Data"):
    data = yf.download(ticker, period="1mo")
    st.line_chart(data['Close'])
EOF

# Run the test app
streamlit run test_app.py --server.port 8501 --server.address 0.0.0.0
```

#### Method B: Clone from GitHub (Easiest)
```bash
# Clone the repository directly
cd /opt/trading-bot
git clone https://github.com/GuillaumeBld/Trading_bot.git
cd Trading_bot
```

#### Method C: Upload via SCP (From Your Local Machine)
On your local machine, open a new terminal and run:
```bash
# Replace YOUR_SERVER_IP with your actual server IP (82.25.112.7)
scp -r /path/to/your/unified-trading-bot root@82.25.112.7:/opt/trading-bot/

# Then SSH back to continue
ssh root@82.25.112.7
cd /opt/trading-bot/unified-trading-bot
```

#### Method C: Upload via Hostinger File Manager
1. Open your Hostinger control panel
2. Go to "File Manager"
3. Navigate to `/opt/trading-bot/`
4. Upload your `unified-trading-bot` folder
5. Extract if needed

### Step 5: Set Up the Full Application (After Upload)
```bash
cd /opt/trading-bot/unified-trading-bot

# Create Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run setup
python setup.py

# Start the dashboard
python scripts/run_dashboard.py
```

### Step 6: Configure Firewall and Access
```bash
# Open the required ports
sudo ufw allow 8501/tcp  # Streamlit dashboard
sudo ufw allow 8502/tcp  # Advanced dashboard
sudo ufw allow 5678/tcp  # n8n (if using)
sudo ufw enable
```

### Step 7: Access Your Application
- **Basic Dashboard**: `http://82.25.112.7:8501`
- **Advanced Dashboard**: `http://82.25.112.7:8502`

##  Troubleshooting

### If you get "Command not found" errors:
```bash
# Reload your shell environment
source ~/.bashrc
newgrp docker  # For Docker group permissions
```

### If Python modules are missing:
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### If ports are blocked:
```bash
# Check if the application is running
netstat -tlnp | grep :8501

# Check firewall status
sudo ufw status

# Restart the application
pkill -f streamlit
python scripts/run_dashboard.py
```

##  Quick Commands for Right Now

**Copy and paste these commands one by one in your current SSH session:**

```bash
# 1. Install basics
sudo apt update && sudo apt install -y python3 python3-pip python3-venv git curl

# 2. Create working directory
mkdir -p ~/trading-bot && cd ~/trading-bot

# 3. Create a quick test
python3 -m venv venv && source venv/bin/activate && pip install streamlit yfinance pandas

# 4. Create test file
echo 'import streamlit as st
st.title(" Trading Bot Test")
st.write("Server is working! IP: 82.25.112.7")
st.balloons()' > test.py

# 5. Run test (this will start the server)
streamlit run test.py --server.port 8501 --server.address 0.0.0.0
```

**Then visit**: `http://82.25.112.7:8501` in your browser

If you see the test page, your server is ready for the full deployment! 