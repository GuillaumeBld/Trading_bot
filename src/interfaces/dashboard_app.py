#!/usr/bin/env python3
"""
Advanced Trading Dashboard for ChatGPT Micro-Cap Trading Bot

This comprehensive dashboard provides:
- Configuration management (APIs, settings)
- Real-time performance monitoring
- Trade analysis and visualization
- News and market data integration
- Risk management overview
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import json
import os
from typing import Dict, List, Optional
import time

# Set page config
st.set_page_config(
    page_title="Trading Bot Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Import our modules
try:
    from trading_script import (
        load_portfolio_data, get_performance_metrics,
        get_market_data, calculate_sharpe_ratio
    )
    from llm_interface import LLMManager
    MODULES_AVAILABLE = True
except ImportError:
    MODULES_AVAILABLE = False
    st.error(" Core modules not available. Please ensure all dependencies are installed.")

class TradingDashboard:
    def __init__(self):
        self.initialize_session_state()
        self.llm_manager = self.get_llm_manager()
        
    def initialize_session_state(self):
        """Initialize session state variables"""
        if 'portfolio_data' not in st.session_state:
            st.session_state.portfolio_data = None
        if 'last_update' not in st.session_state:
            st.session_state.last_update = None
        if 'auto_refresh' not in st.session_state:
            st.session_state.auto_refresh = False
        if 'config_data' not in st.session_state:
            st.session_state.config_data = self.load_config()
    
    def get_llm_manager(self):
        """Get LLM manager instance"""
        if MODULES_AVAILABLE:
            try:
                from llm_interface import LLMManager
                return LLMManager()
            except Exception as e:
                st.error(f"Failed to initialize LLM manager: {e}")
        return None
    
    def load_config(self) -> Dict:
        """Load configuration from files"""
        config = {
            'brokers': {},
            'llm_providers': {},
            'trading_settings': {},
            'data_sources': {}
        }
        
        # Load .env file
        env_file = '.env'
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                for line in f:
                    if '=' in line and not line.startswith('#'):
                        key, value = line.strip().split('=', 1)
                        if 'API_KEY' in key:
                            config['llm_providers'][key] = value
        
        # Load LLM config
        llm_config_file = '.llm_config.json'
        if os.path.exists(llm_config_file):
            try:
                with open(llm_config_file, 'r') as f:
                    config['llm_providers'].update(json.load(f))
            except json.JSONDecodeError:
                pass
        
        return config
    
    def save_config(self, config: Dict):
        """Save configuration to files"""
        # Save API keys to .env
        env_content = []
        for key, value in config.get('llm_providers', {}).items():
            if 'API_KEY' in key and value:
                env_content.append(f"{key}={value}")
        
        if env_content:
            with open('.env', 'w') as f:
                f.write('\n'.join(env_content))
        
        # Save LLM config
        llm_config = {k: v for k, v in config.get('llm_providers', {}).items() 
                      if 'API_KEY' not in k}
        if llm_config:
            with open('.llm_config.json', 'w') as f:
                json.dump(llm_config, f, indent=2)
        
        st.session_state.config_data = config

    def render_header(self):
        """Render dashboard header"""
        st.markdown('<h1 class="main-header"> ChatGPT Micro-Cap Trading Dashboard</h1>', 
                   unsafe_allow_html=True)
        
        # Status indicators
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if MODULES_AVAILABLE:
                st.success(" Core System")
            else:
                st.error(" Core System")
        
        with col2:
            if self.llm_manager and self.llm_manager.get_available_providers():
                st.success(" AI Providers")
            else:
                st.warning(" AI Providers")
        
        with col3:
            if os.path.exists('Scripts and CSV Files/chatgpt_portfolio_update.csv'):
                st.success(" Portfolio Data")
            else:
                st.warning(" Portfolio Data")
        
        with col4:
            current_time = datetime.now().strftime("%H:%M:%S")
            st.info(f" {current_time}")

    def render_sidebar_config(self):
        """Render configuration sidebar"""
        st.sidebar.markdown("##  Configuration")
        
        # Auto-refresh toggle
        st.session_state.auto_refresh = st.sidebar.checkbox(
            " Auto Refresh (30s)", 
            value=st.session_state.auto_refresh
        )
        
        # Manual refresh button
        if st.sidebar.button(" Refresh Now", use_container_width=True):
            self.refresh_data()
        
        # Configuration sections
        with st.sidebar.expander(" AI Providers", expanded=False):
            self.render_llm_config()
        
        with st.sidebar.expander(" Broker APIs", expanded=False):
            self.render_broker_config()
        
        with st.sidebar.expander(" Trading Settings", expanded=False):
            self.render_trading_config()
        
        with st.sidebar.expander(" Data Sources", expanded=False):
            self.render_data_source_config()

    def render_llm_config(self):
        """Render LLM provider configuration"""
        st.markdown("**API Keys:**")
        
        # OpenAI
        openai_key = st.text_input(
            "OpenAI API Key",
            value=st.session_state.config_data.get('llm_providers', {}).get('OPENAI_API_KEY', ''),
            type="password",
            key="openai_key"
        )
        
        # Anthropic
        anthropic_key = st.text_input(
            "Anthropic API Key",
            value=st.session_state.config_data.get('llm_providers', {}).get('ANTHROPIC_API_KEY', ''),
            type="password",
            key="anthropic_key"
        )
        
        st.markdown("**Model Settings:**")
        
        # Default provider
        providers = ["openai", "anthropic", "ollama", "huggingface"]
        default_provider = st.selectbox(
            "Default Provider",
            providers,
            index=0,
            key="default_provider"
        )
        
        # Confidence threshold
        confidence_threshold = st.slider(
            "Confidence Threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            step=0.05,
            key="confidence_threshold"
        )
        
        # Save button
        if st.button(" Save AI Config", key="save_ai_config"):
            config = st.session_state.config_data.copy()
            config['llm_providers'].update({
                'OPENAI_API_KEY': openai_key,
                'ANTHROPIC_API_KEY': anthropic_key,
                'default_provider': default_provider,
                'confidence_threshold': confidence_threshold
            })
            self.save_config(config)
            st.success(" AI configuration saved!")

    def render_broker_config(self):
        """Render broker API configuration"""
        st.markdown("**Broker APIs:**")
        
        # Alpaca
        st.markdown("**Alpaca Markets:**")
        alpaca_key = st.text_input(
            "Alpaca API Key",
            type="password",
            key="alpaca_key"
        )
        alpaca_secret = st.text_input(
            "Alpaca Secret Key",
            type="password",
            key="alpaca_secret"
        )
        alpaca_paper = st.checkbox("Paper Trading", value=True, key="alpaca_paper")
        
        # TD Ameritrade
        st.markdown("**TD Ameritrade:**")
        td_client_id = st.text_input(
            "TD Client ID",
            key="td_client_id"
        )
        td_refresh_token = st.text_input(
            "TD Refresh Token",
            type="password",
            key="td_refresh_token"
        )
        
        # Save button
        if st.button(" Save Broker Config", key="save_broker_config"):
            config = st.session_state.config_data.copy()
            config['brokers'] = {
                'alpaca': {
                    'api_key': alpaca_key,
                    'secret_key': alpaca_secret,
                    'paper_trading': alpaca_paper
                },
                'td_ameritrade': {
                    'client_id': td_client_id,
                    'refresh_token': td_refresh_token
                }
            }
            self.save_config(config)
            st.success(" Broker configuration saved!")

    def render_trading_config(self):
        """Render trading settings configuration"""
        st.markdown("**Risk Management:**")
        
        max_position_size = st.slider(
            "Max Position Size (%)",
            min_value=5,
            max_value=50,
            value=20,
            step=5,
            key="max_position_size"
        )
        
        default_stop_loss = st.slider(
            "Default Stop Loss (%)",
            min_value=5,
            max_value=30,
            value=15,
            step=1,
            key="default_stop_loss"
        )
        
        max_positions = st.number_input(
            "Max Positions",
            min_value=1,
            max_value=20,
            value=7,
            key="max_positions"
        )
        
        cash_reserve = st.slider(
            "Cash Reserve (%)",
            min_value=0,
            max_value=20,
            value=5,
            step=1,
            key="cash_reserve"
        )
        
        if st.button(" Save Trading Config", key="save_trading_config"):
            config = st.session_state.config_data.copy()
            config['trading_settings'] = {
                'max_position_size': max_position_size,
                'default_stop_loss': default_stop_loss,
                'max_positions': max_positions,
                'cash_reserve': cash_reserve
            }
            self.save_config(config)
            st.success(" Trading configuration saved!")

    def render_data_source_config(self):
        """Render data source configuration"""
        st.markdown("**Market Data:**")
        
        data_provider = st.selectbox(
            "Primary Data Provider",
            ["yfinance", "alpha_vantage", "iex_cloud"],
            index=0,
            key="data_provider"
        )
        
        update_frequency = st.selectbox(
            "Update Frequency",
            ["real-time", "1min", "5min", "15min", "1hour"],
            index=2,
            key="update_frequency"
        )
        
        # News sources
        st.markdown("**News Sources:**")
        news_enabled = st.checkbox("Enable News Integration", key="news_enabled")
        
        if news_enabled:
            news_api_key = st.text_input(
                "NewsAPI Key",
                type="password",
                key="news_api_key"
            )
        
        if st.button(" Save Data Config", key="save_data_config"):
            config = st.session_state.config_data.copy()
            config['data_sources'] = {
                'data_provider': data_provider,
                'update_frequency': update_frequency,
                'news_enabled': news_enabled
            }
            if news_enabled:
                config['data_sources']['news_api_key'] = st.session_state.get('news_api_key', '')
            self.save_config(config)
            st.success(" Data source configuration saved!")

    def load_portfolio_data(self):
        """Load portfolio data from CSV files"""
        try:
            portfolio_file = "Scripts and CSV Files/chatgpt_portfolio_update.csv"
            trades_file = "Scripts and CSV Files/chatgpt_trade_log.csv"
            
            if os.path.exists(portfolio_file):
                portfolio_df = pd.read_csv(portfolio_file)
                portfolio_df['Date'] = pd.to_datetime(portfolio_df['Date'])
                
                trades_df = None
                if os.path.exists(trades_file):
                    trades_df = pd.read_csv(trades_file)
                    trades_df['Date'] = pd.to_datetime(trades_df['Date'])
                
                return portfolio_df, trades_df
            else:
                return None, None
        except Exception as e:
            st.error(f"Error loading portfolio data: {e}")
            return None, None

    def get_current_positions(self, portfolio_df):
        """Get current portfolio positions"""
        if portfolio_df is None or portfolio_df.empty:
            return pd.DataFrame()
        
        # Get the latest date
        latest_date = portfolio_df['Date'].max()
        current_positions = portfolio_df[portfolio_df['Date'] == latest_date].copy()
        
        # Filter out positions with 0 shares
        if 'Shares' in current_positions.columns:
            current_positions = current_positions[current_positions['Shares'] > 0]
        
        return current_positions

    def calculate_performance_metrics(self, portfolio_df):
        """Calculate comprehensive performance metrics"""
        if portfolio_df is None or portfolio_df.empty:
            return {}
        
        try:
            # Basic metrics
            latest_equity = portfolio_df['Total Equity'].iloc[-1] if 'Total Equity' in portfolio_df.columns else 0
            initial_equity = portfolio_df['Total Equity'].iloc[0] if 'Total Equity' in portfolio_df.columns else 100
            total_return = ((latest_equity - initial_equity) / initial_equity) * 100
            
            # Daily returns
            if 'Total Equity' in portfolio_df.columns and len(portfolio_df) > 1:
                portfolio_df['Daily_Return'] = portfolio_df['Total Equity'].pct_change()
                
                # Sharpe ratio (assuming 4.5% risk-free rate)
                daily_returns = portfolio_df['Daily_Return'].dropna()
                if len(daily_returns) > 0:
                    excess_returns = daily_returns - (0.045 / 252)  # Daily risk-free rate
                    sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() != 0 else 0
                else:
                    sharpe_ratio = 0
                
                # Sortino ratio
                negative_returns = daily_returns[daily_returns < 0]
                if len(negative_returns) > 0:
                    downside_deviation = negative_returns.std()
                    sortino_ratio = (daily_returns.mean() / downside_deviation) * np.sqrt(252) if downside_deviation != 0 else 0
                else:
                    sortino_ratio = sharpe_ratio
                
                # Maximum drawdown
                running_max = portfolio_df['Total Equity'].expanding().max()
                drawdown = (portfolio_df['Total Equity'] - running_max) / running_max
                max_drawdown = drawdown.min() * 100
            else:
                sharpe_ratio = 0
                sortino_ratio = 0
                max_drawdown = 0
            
            # Win rate (if trades data available)
            win_rate = 0  # Will be calculated from trades data if available
            
            return {
                'total_equity': latest_equity,
                'initial_equity': initial_equity,
                'total_return': total_return,
                'sharpe_ratio': sharpe_ratio,
                'sortino_ratio': sortino_ratio,
                'max_drawdown': max_drawdown,
                'win_rate': win_rate
            }
        except Exception as e:
            st.error(f"Error calculating performance metrics: {e}")
            return {}

    def render_performance_overview(self):
        """Render performance overview section"""
        st.markdown("##  Performance Overview")
        
        portfolio_df, trades_df = self.load_portfolio_data()
        
        if portfolio_df is None:
            st.warning(" No portfolio data found. Please run a trading session first.")
            return
        
        # Calculate metrics
        metrics = self.calculate_performance_metrics(portfolio_df)
        
        # Display key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_return = metrics.get('total_return', 0)
            color = "success" if total_return >= 0 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h4>Total Return</h4>
                <h2>{total_return:+.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            sharpe = metrics.get('sharpe_ratio', 0)
            color = "success" if sharpe >= 1.0 else "warning" if sharpe >= 0.5 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h4>Sharpe Ratio</h4>
                <h2>{sharpe:.3f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            max_dd = metrics.get('max_drawdown', 0)
            color = "success" if max_dd >= -5 else "warning" if max_dd >= -15 else "danger"
            st.markdown(f"""
            <div class="metric-card {color}-metric">
                <h4>Max Drawdown</h4>
                <h2>{max_dd:.2f}%</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            equity = metrics.get('total_equity', 0)
            st.markdown(f"""
            <div class="metric-card">
                <h4>Total Equity</h4>
                <h2>${equity:,.2f}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # Performance chart
        if 'Total Equity' in portfolio_df.columns:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=portfolio_df['Date'],
                y=portfolio_df['Total Equity'],
                mode='lines',
                name='Portfolio Value',
                line=dict(color='#1f77b4', width=2)
            ))
            
            # Add benchmark if available
            if 'Benchmark' in portfolio_df.columns:
                fig.add_trace(go.Scatter(
                    x=portfolio_df['Date'],
                    y=portfolio_df['Benchmark'],
                    mode='lines',
                    name='S&P 500 Benchmark',
                    line=dict(color='#ff7f0e', width=2, dash='dash')
                ))
            
            fig.update_layout(
                title="Portfolio Performance Over Time",
                xaxis_title="Date",
                yaxis_title="Portfolio Value ($)",
                hovermode='x unified',
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)

    def render_current_positions(self):
        """Render current positions section"""
        st.markdown("##  Current Positions")
        
        portfolio_df, _ = self.load_portfolio_data()
        current_positions = self.get_current_positions(portfolio_df)
        
        if current_positions.empty:
            st.info(" No current positions. Portfolio is in cash.")
            return
        
        # Position summary
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Positions table
            display_cols = ['Ticker', 'Shares', 'Cost Basis', 'Current Price', 'Total Value', 'PnL', 'Stop Loss']
            available_cols = [col for col in display_cols if col in current_positions.columns]
            
            if available_cols:
                st.dataframe(
                    current_positions[available_cols],
                    use_container_width=True,
                    hide_index=True
                )
        
        with col2:
            # Position allocation pie chart
            if 'Total Value' in current_positions.columns:
                fig = px.pie(
                    current_positions,
                    values='Total Value',
                    names='Ticker',
                    title="Position Allocation"
                )
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)

    def render_trade_analysis(self):
        """Render trade analysis section"""
        st.markdown("##  Trade Analysis")
        
        _, trades_df = self.load_portfolio_data()
        
        if trades_df is None or trades_df.empty:
            st.info(" No trade history available.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Recent trades
            st.markdown("### Recent Trades")
            recent_trades = trades_df.tail(10)
            display_cols = ['Date', 'Ticker', 'Shares Bought', 'Buy Price', 'Reason']
            available_cols = [col for col in display_cols if col in recent_trades.columns]
            
            if available_cols:
                st.dataframe(
                    recent_trades[available_cols],
                    use_container_width=True,
                    hide_index=True
                )
        
        with col2:
            # Trade statistics
            st.markdown("### Trade Statistics")
            
            if 'PnL' in trades_df.columns:
                profitable_trades = trades_df[trades_df['PnL'] > 0]
                total_trades = len(trades_df)
                win_rate = len(profitable_trades) / total_trades * 100 if total_trades > 0 else 0
                
                avg_profit = profitable_trades['PnL'].mean() if len(profitable_trades) > 0 else 0
                avg_loss = trades_df[trades_df['PnL'] < 0]['PnL'].mean() if len(trades_df[trades_df['PnL'] < 0]) > 0 else 0
                
                st.metric("Win Rate", f"{win_rate:.1f}%")
                st.metric("Average Profit", f"${avg_profit:.2f}")
                st.metric("Average Loss", f"${avg_loss:.2f}")
                st.metric("Total Trades", total_trades)

    def render_ai_insights(self):
        """Render AI insights section"""
        st.markdown("##  AI Insights")
        
        if not self.llm_manager:
            st.warning(" AI providers not configured. Please set up API keys in the sidebar.")
            return
        
        available_providers = self.llm_manager.get_available_providers()
        
        if not available_providers:
            st.warning(" No AI providers available. Please configure API keys.")
            return
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### AI Provider Status")
            for provider in available_providers:
                st.success(f" {provider.upper()}")
        
        with col2:
            st.markdown("### Recent Recommendations")
            # This would show recent AI recommendations
            st.info(" AI recommendation history will be displayed here.")
        
        # AI analysis button
        if st.button(" Get AI Market Analysis", use_container_width=True):
            with st.spinner("Analyzing market conditions..."):
                # Simulate AI analysis
                time.sleep(2)
                st.success(" AI analysis complete!")
                
                # Display mock analysis
                st.markdown("**Market Analysis:**")
                st.write("- Market sentiment: Neutral to bullish")
                st.write("- Volatility: Moderate")
                st.write("- Recommended action: Continue current strategy")

    def render_market_overview(self):
        """Render market overview section"""
        st.markdown("##  Market Overview")
        
        # Market indices
        indices = {
            "S&P 500": "^GSPC",
            "Russell 2000": "^RUT",
            "NASDAQ": "^IXIC",
            "VIX": "^VIX"
        }
        
        col1, col2, col3, col4 = st.columns(4)
        cols = [col1, col2, col3, col4]
        
        for i, (name, symbol) in enumerate(indices.items()):
            with cols[i]:
                try:
                    ticker = yf.Ticker(symbol)
                    data = ticker.history(period="2d")
                    if not data.empty:
                        current_price = data['Close'].iloc[-1]
                        prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
                        change = ((current_price - prev_price) / prev_price) * 100
                        
                        color = "🟢" if change >= 0 else ""
                        st.metric(
                            label=name,
                            value=f"{current_price:.2f}",
                            delta=f"{change:+.2f}%"
                        )
                except Exception:
                    st.metric(label=name, value="N/A")

    def render_news_feed(self):
        """Render news feed section"""
        st.markdown("##  Market News")
        
        # Mock news data (in real implementation, would fetch from news API)
        news_items = [
            {
                "title": "Market Update: Small-cap stocks show resilience",
                "source": "MarketWatch",
                "time": "2 hours ago",
                "sentiment": "Positive"
            },
            {
                "title": "Fed signals potential rate cuts in Q4",
                "source": "Reuters",
                "time": "4 hours ago",
                "sentiment": "Neutral"
            },
            {
                "title": "Tech earnings season approaches with mixed expectations",
                "source": "CNBC",
                "time": "6 hours ago",
                "sentiment": "Neutral"
            }
        ]
        
        for news in news_items:
            sentiment_color = {
                "Positive": "🟢",
                "Negative": "",
                "Neutral": "🟡"
            }.get(news["sentiment"], "")
            
            st.markdown(f"""
            **{news['title']}**  
            {sentiment_color} {news['source']} • {news['time']}
            """)
            st.markdown("---")

    def refresh_data(self):
        """Refresh all dashboard data"""
        st.session_state.last_update = datetime.now()
        st.rerun()

    def run(self):
        """Run the main dashboard"""
        self.render_header()
        self.render_sidebar_config()
        
        # Auto-refresh logic
        if st.session_state.auto_refresh:
            time.sleep(30)
            self.refresh_data()
        
        # Main content tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            " Performance", 
            " Positions", 
            " Trades", 
            " AI Insights", 
            " Market"
        ])
        
        with tab1:
            self.render_performance_overview()
        
        with tab2:
            self.render_current_positions()
        
        with tab3:
            self.render_trade_analysis()
        
        with tab4:
            self.render_ai_insights()
        
        with tab5:
            col1, col2 = st.columns([1, 1])
            with col1:
                self.render_market_overview()
            with col2:
                self.render_news_feed()
        
        # Footer
        st.markdown("---")
        st.markdown("*Dashboard last updated: {}*".format(
            st.session_state.last_update.strftime("%Y-%m-%d %H:%M:%S") 
            if st.session_state.last_update else "Never"
        ))

def main():
    """Main function"""
    dashboard = TradingDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()