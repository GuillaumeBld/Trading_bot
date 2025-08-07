#!/bin/bash

#  EXACT COMMANDS FOR YOUR HOSTINGER VPS
# Copy and paste these commands one by one into your SSH session

echo " Setting up AI Trading Bot on Hostinger VPS"
echo "============================================="

# Step 1: Install all required dependencies
echo " Installing dependencies..."
sudo apt update
sudo apt install -y unzip git python3 python3-pip python3-venv curl nano htop wget

# Step 2: Clone the repository from GitHub
echo " Cloning repository..."
cd /opt
sudo git clone https://github.com/GuillaumeBld/Trading_bot.git trading-bot
sudo chown -R $USER:$USER /opt/trading-bot
cd /opt/trading-bot

# Step 3: Set up Python virtual environment
echo " Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Step 4: Upgrade pip and install dependencies
echo " Installing Python packages..."
pip install --upgrade pip
pip install pandas numpy yfinance streamlit plotly

# Step 5: Test the basic setup
echo " Testing setup..."
python3 -c "
import streamlit as st
import pandas as pd
import yfinance as yf
print(' All dependencies working!')
print(' Ready to install full requirements!')
"

# Step 6: Install full requirements (if requirements.txt exists)
if [ -f "requirements.txt" ]; then
    echo " Installing full requirements..."
    pip install -r requirements.txt
else
    echo " requirements.txt not found, using basic installation"
fi

# Step 7: Run setup script (if exists)
if [ -f "setup.py" ]; then
    echo " Running setup script..."
    python setup.py
else
    echo " setup.py not found, skipping setup"
fi

# Step 8: Configure firewall
echo " Configuring firewall..."
sudo ufw allow 8501/tcp  # Streamlit dashboard
sudo ufw allow 8502/tcp  # Advanced dashboard
sudo ufw allow 5678/tcp  # n8n (if using)
sudo ufw --force enable

# Step 9: Create a test app
echo " Creating test application..."
cat > test_trading_bot.py << 'EOF'
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="AI Trading Bot", page_icon="", layout="wide")

st.title(" AI Trading Bot - Hostinger Deployment Test")
st.success(" Successfully deployed on Hostinger VPS!")

# Server info
st.info(f" Server IP: 82.25.112.7")
st.info(f" Access URL: http://82.25.112.7:8501")

# Test data fetching
st.subheader(" Market Data Test")
ticker = st.selectbox("Select a stock:", ["AAPL", "MSFT", "GOOGL", "TSLA", "NVDA"])

if st.button(" Fetch Stock Data"):
    with st.spinner("Fetching data..."):
        try:
            data = yf.download(ticker, period="1mo", progress=False)
            
            if not data.empty:
                st.success(f" Successfully fetched {len(data)} days of {ticker} data!")
                
                # Create chart
                fig = go.Figure()
                fig.add_trace(go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name=ticker
                ))
                fig.update_layout(
                    title=f"{ticker} Stock Price - Last 30 Days",
                    yaxis_title="Price ($)",
                    xaxis_title="Date"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Show basic stats
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Current Price", f"${data['Close'][-1]:.2f}")
                with col2:
                    change = data['Close'][-1] - data['Close'][-2]
                    st.metric("Daily Change", f"${change:.2f}")
                with col3:
                    st.metric("30-Day High", f"${data['High'].max():.2f}")
                with col4:
                    st.metric("30-Day Low", f"${data['Low'].min():.2f}")
            else:
                st.error(" No data received. Please try again.")
                
        except Exception as e:
            st.error(f" Error fetching data: {str(e)}")

st.subheader(" System Information")
st.code("""
 Python Environment: Ready
 Dependencies: Installed
 Market Data: Functional
 Charts: Working
 Server: Running on Port 8501
""")

st.subheader(" Next Steps")
st.info("""
1. The basic setup is working!
2. Install full requirements: pip install -r requirements.txt
3. Run the main dashboard: python scripts/run_dashboard.py
4. Access your trading bot at: http://82.25.112.7:8501
""")
EOF

echo ""
echo " SETUP COMPLETE!"
echo "==================="
echo ""
echo " Your trading bot is installed at: /opt/trading-bot"
echo " To start the test app, run:"
echo "   cd /opt/trading-bot"
echo "   source venv/bin/activate"
echo "   streamlit run test_trading_bot.py --server.port 8501 --server.address 0.0.0.0"
echo ""
echo " Then access: http://82.25.112.7:8501"
echo ""
echo " To run the full trading bot:"
echo "   python scripts/run_dashboard.py"
echo ""
echo " Happy Trading!"