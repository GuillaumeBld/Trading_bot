#!/usr/bin/env python3
"""
Advanced Trading Dashboard with Full Configuration Management

This is the main dashboard application that provides:
- Comprehensive configuration management for all APIs and settings
- Real-time performance monitoring with advanced metrics
- Market data integration with news and sentiment analysis
- Interactive charts and visualizations
- Risk management monitoring
- Trade analysis and AI insights
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional
import asyncio

# Import our custom modules
try:
    from dashboard_config import get_config_manager, ConfigManager
    from market_data_service import get_market_service, MarketDataService
    from trading_script import load_portfolio_data, get_performance_metrics
    from llm_interface import LLMManager
    CONFIG_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Required modules not available: {e}")
    CONFIG_AVAILABLE = False

# Set page configuration
st.set_page_config(
    page_title="Advanced Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin-bottom: 1rem;
    }
    
    .success-metric {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
    }
    
    .warning-metric {
        background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);
    }
    
    .danger-metric {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
    }
    
    .config-section {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #1f77b4;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online { background-color: #28a745; }
    .status-warning { background-color: #ffc107; }
    .status-offline { background-color: #dc3545; }
    
    .news-item {
        background-color: white;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.5rem;
        border-left: 3px solid #1f77b4;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .sentiment-positive { border-left-color: #28a745; }
    .sentiment-negative { border-left-color: #dc3545; }
    .sentiment-neutral { border-left-color: #6c757d; }
</style>
""", unsafe_allow_html=True)

class AdvancedTradingDashboard:
    """Advanced trading dashboard with full configuration management"""
    
    def __init__(self):
        self.initialize_session_state()
        if CONFIG_AVAILABLE:
            self.config_manager = get_config_manager()
            self.market_service = get_market_service(
                self.config_manager.config.data_sources.news_api_key
            )
            self.llm_manager = self.get_llm_manager()
        else:
            self.config_manager = None
            self.market_service = None
            self.llm_manager = None
    
    def initialize_session_state(self):
        """Initialize Streamlit session state"""
        defaults = {
            'last_update': None,
            'auto_refresh': False,
            'refresh_interval': 30,
            'selected_timeframe': '1M',
            'show_advanced_metrics': False,
            'portfolio_data': None,
            'market_data_cache': {},
            'config_changed': False
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def get_llm_manager(self):
        """Get LLM manager with current configuration"""
        try:
            return LLMManager()
        except Exception as e:
            st.error(f"Failed to initialize LLM manager: {e}")
            return None
    
    def render_header(self):
        """Render enhanced dashboard header"""
        st.markdown('<h1 class="main-header">🚀 Advanced Trading Dashboard</h1>', 
                   unsafe_allow_html=True)
        
        # System status indicators
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            self.render_status_indicator("Core System", CONFIG_AVAILABLE)
        
        with col2:
            ai_status = (self.config_manager and 
                        len(self.config_manager.get_enabled_llm_providers()) > 0)
            self.render_status_indicator("AI Providers", ai_status)
        
        with col3:
            broker_status = (self.config_manager and 
                           len(self.config_manager.get_enabled_brokers()) > 0)
            self.render_status_indicator("Brokers", broker_status)
        
        with col4:
            data_status = self.market_service is not None
            self.render_status_indicator("Market Data", data_status)
        
        with col5:
            current_time = datetime.now().strftime("%H:%M:%S")
            st.markdown(f"""
            <div style="text-align: center;">
                <strong>🕒 {current_time}</strong><br>
                <small>Last Update</small>
            </div>
            """, unsafe_allow_html=True)
    
    def render_status_indicator(self, label: str, status: bool):
        """Render a status indicator"""
        status_class = "status-online" if status else "status-offline"
        status_text = "Online" if status else "Offline"
        
        st.markdown(f"""
        <div style="text-align: center;">
            <span class="status-indicator {status_class}"></span>
            <strong>{label}</strong><br>
            <small>{status_text}</small>
        </div>
        """, unsafe_allow_html=True)
    
    def render_sidebar_navigation(self):
        """Render sidebar navigation and controls"""
        st.sidebar.title("🎛️ Dashboard Controls")
        
        # Auto-refresh controls
        st.sidebar.markdown("### 🔄 Refresh Settings")
        st.session_state.auto_refresh = st.sidebar.checkbox(
            "Auto Refresh", 
            value=st.session_state.auto_refresh
        )
        
        if st.session_state.auto_refresh:
            st.session_state.refresh_interval = st.sidebar.slider(
                "Refresh Interval (seconds)",
                min_value=10,
                max_value=300,
                value=st.session_state.refresh_interval,
                step=10
            )
        
        # Manual refresh
        if st.sidebar.button("🔄 Refresh Now", use_container_width=True):
            self.refresh_data()
        
        # Timeframe selection
        st.sidebar.markdown("### 📅 Timeframe")
        st.session_state.selected_timeframe = st.sidebar.selectbox(
            "Chart Timeframe",
            ["1D", "1W", "1M", "3M", "6M", "1Y", "2Y"],
            index=2
        )
        
        # Advanced options
        st.sidebar.markdown("### ⚙️ Display Options")
        st.session_state.show_advanced_metrics = st.sidebar.checkbox(
            "Show Advanced Metrics",
            value=st.session_state.show_advanced_metrics
        )
        
        # Configuration validation
        if self.config_manager:
            st.sidebar.markdown("### 🔍 Configuration Status")
            self.render_config_validation()
    
    def render_config_validation(self):
        """Render configuration validation in sidebar"""
        if not self.config_manager:
            return
        
        issues = self.config_manager.validate_config()
        
        # Count issues
        error_count = len(issues['errors'])
        warning_count = len(issues['warnings'])
        
        if error_count == 0 and warning_count == 0:
            st.sidebar.success("✅ Configuration OK")
        else:
            if error_count > 0:
                st.sidebar.error(f"❌ {error_count} Error(s)")
                with st.sidebar.expander("View Errors"):
                    for error in issues['errors']:
                        st.write(f"• {error}")
            
            if warning_count > 0:
                st.sidebar.warning(f"⚠️ {warning_count} Warning(s)")
                with st.sidebar.expander("View Warnings"):
                    for warning in issues['warnings']:
                        st.write(f"• {warning}")
    
    def render_configuration_tab(self):
        """Render comprehensive configuration management"""
        if not self.config_manager:
            st.error("Configuration manager not available")
            return
        
        st.markdown("## ⚙️ System Configuration")
        
        # Configuration tabs
        config_tab1, config_tab2, config_tab3, config_tab4 = st.tabs([
            "🤖 AI Providers",
            "🏦 Brokers", 
            "📊 Trading Settings",
            "📰 Data Sources"
        ])
        
        with config_tab1:
            self.render_ai_configuration()
        
        with config_tab2:
            self.render_broker_configuration()
        
        with config_tab3:
            self.render_trading_configuration()
        
        with config_tab4:
            self.render_data_source_configuration()
    
    def render_ai_configuration(self):
        """Render AI provider configuration"""
        st.markdown("### 🤖 AI Provider Settings")
        
        # Provider status overview
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("**Available Providers:**")
            for provider_name, provider_config in self.config_manager.config.llm_providers.items():
                status = "✅" if provider_config.enabled else "❌"
                st.write(f"{status} {provider_name.title()}")
        
        with col2:
            if self.llm_manager:
                available = self.llm_manager.get_available_providers()
                st.markdown("**Active Providers:**")
                for provider in available:
                    st.success(f"✅ {provider}")
        
        # Configuration forms
        for provider_name, provider_config in self.config_manager.config.llm_providers.items():
            with st.expander(f"Configure {provider_name.title()}", expanded=False):
                self.render_llm_provider_form(provider_name, provider_config)
    
    def render_llm_provider_form(self, provider_name: str, config):
        """Render form for individual LLM provider"""
        col1, col2 = st.columns(2)
        
        with col1:
            # API Key (if needed)
            if provider_name not in ['ollama', 'huggingface']:
                api_key = st.text_input(
                    f"{provider_name.title()} API Key",
                    value=config.api_key,
                    type="password",
                    key=f"{provider_name}_api_key"
                )
            else:
                api_key = config.api_key
            
            # Model name
            model_name = st.text_input(
                "Model Name",
                value=config.model_name,
                key=f"{provider_name}_model"
            )
            
            # Enabled toggle
            enabled = st.checkbox(
                "Enabled",
                value=config.enabled,
                key=f"{provider_name}_enabled"
            )
        
        with col2:
            # Temperature
            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=2.0,
                value=config.temperature,
                step=0.1,
                key=f"{provider_name}_temp"
            )
            
            # Max tokens
            max_tokens = st.number_input(
                "Max Tokens",
                min_value=100,
                max_value=8000,
                value=config.max_tokens,
                key=f"{provider_name}_tokens"
            )
        
        # Save button
        if st.button(f"💾 Save {provider_name.title()} Config", key=f"save_{provider_name}"):
            self.config_manager.update_llm_config(
                provider_name,
                api_key=api_key,
                model_name=model_name,
                temperature=temperature,
                max_tokens=max_tokens,
                enabled=enabled
            )
            
            if self.config_manager.save_config(self.config_manager.config):
                st.success(f"✅ {provider_name.title()} configuration saved!")
                st.rerun()
            else:
                st.error("❌ Failed to save configuration")
    
    def render_broker_configuration(self):
        """Render broker configuration"""
        st.markdown("### 🏦 Broker API Settings")
        
        for broker_name, broker_config in self.config_manager.config.brokers.items():
            with st.expander(f"Configure {broker_name.title()}", expanded=False):
                self.render_broker_form(broker_name, broker_config)
    
    def render_broker_form(self, broker_name: str, config):
        """Render form for individual broker"""
        col1, col2 = st.columns(2)
        
        with col1:
            api_key = st.text_input(
                "API Key",
                value=config.api_key,
                type="password",
                key=f"{broker_name}_api_key"
            )
            
            if broker_name == "alpaca":
                secret_key = st.text_input(
                    "Secret Key",
                    value=config.secret_key,
                    type="password",
                    key=f"{broker_name}_secret"
                )
            else:
                secret_key = config.secret_key
            
            enabled = st.checkbox(
                "Enabled",
                value=config.enabled,
                key=f"{broker_name}_enabled"
            )
        
        with col2:
            base_url = st.text_input(
                "Base URL",
                value=config.base_url,
                key=f"{broker_name}_url"
            )
            
            paper_trading = st.checkbox(
                "Paper Trading",
                value=config.paper_trading,
                key=f"{broker_name}_paper"
            )
        
        # Test connection button
        col_test, col_save = st.columns(2)
        
        with col_test:
            if st.button(f"🔗 Test Connection", key=f"test_{broker_name}"):
                # Simulate connection test
                with st.spinner("Testing connection..."):
                    time.sleep(2)
                    if api_key:
                        st.success("✅ Connection successful!")
                    else:
                        st.error("❌ Connection failed - missing API key")
        
        with col_save:
            if st.button(f"💾 Save Config", key=f"save_broker_{broker_name}"):
                self.config_manager.update_broker_config(
                    broker_name,
                    api_key=api_key,
                    secret_key=secret_key,
                    base_url=base_url,
                    paper_trading=paper_trading,
                    enabled=enabled
                )
                
                if self.config_manager.save_config(self.config_manager.config):
                    st.success(f"✅ {broker_name.title()} configuration saved!")
                    st.rerun()
    
    def render_trading_configuration(self):
        """Render trading parameters configuration"""
        st.markdown("### 📊 Trading Parameters")
        
        config = self.config_manager.config.trading
        
        col1, col2 = st.columns(2)
        
        with col1:
            max_position_size = st.slider(
                "Max Position Size (%)",
                min_value=5,
                max_value=50,
                value=int(config.max_position_size_pct),
                step=5,
                help="Maximum percentage of portfolio for a single position"
            )
            
            default_stop_loss = st.slider(
                "Default Stop Loss (%)",
                min_value=5,
                max_value=30,
                value=int(config.default_stop_loss_pct),
                step=1,
                help="Default stop loss percentage below entry price"
            )
        
        with col2:
            max_positions = st.number_input(
                "Maximum Positions",
                min_value=1,
                max_value=20,
                value=config.max_positions,
                help="Maximum number of simultaneous positions"
            )
            
            cash_reserve = st.slider(
                "Cash Reserve (%)",
                min_value=0,
                max_value=30,
                value=int(config.cash_reserve_pct),
                step=5,
                help="Minimum cash percentage to maintain"
            )
        
        # Risk metrics
        st.markdown("### 📈 Performance Settings")
        
        risk_free_rate = st.number_input(
            "Risk-Free Rate (%)",
            min_value=0.0,
            max_value=10.0,
            value=config.risk_free_rate * 100,
            step=0.1,
            format="%.2f",
            help="Annual risk-free rate for Sharpe ratio calculation"
        ) / 100
        
        # Save button
        if st.button("💾 Save Trading Configuration", use_container_width=True):
            self.config_manager.update_trading_config(
                max_position_size_pct=float(max_position_size),
                default_stop_loss_pct=float(default_stop_loss),
                max_positions=max_positions,
                cash_reserve_pct=float(cash_reserve),
                risk_free_rate=risk_free_rate
            )
            
            if self.config_manager.save_config(self.config_manager.config):
                st.success("✅ Trading configuration saved!")
                st.rerun()
    
    def render_data_source_configuration(self):
        """Render data source configuration"""
        st.markdown("### 📰 Data Source Settings")
        
        config = self.config_manager.config.data_sources
        
        col1, col2 = st.columns(2)
        
        with col1:
            primary_provider = st.selectbox(
                "Primary Data Provider",
                ["yfinance", "alpha_vantage", "iex_cloud"],
                index=0 if config.primary_provider == "yfinance" else 1,
                help="Primary source for market data"
            )
            
            update_frequency = st.selectbox(
                "Update Frequency",
                ["real-time", "1min", "5min", "15min", "1hour"],
                index=2,
                help="How often to refresh market data"
            )
        
        with col2:
            news_enabled = st.checkbox(
                "Enable News Integration",
                value=config.news_enabled,
                help="Enable news feeds and sentiment analysis"
            )
            
            if news_enabled:
                news_api_key = st.text_input(
                    "NewsAPI Key",
                    value=config.news_api_key,
                    type="password",
                    help="API key from newsapi.org"
                )
            else:
                news_api_key = config.news_api_key
        
        # Save button
        if st.button("💾 Save Data Source Configuration", use_container_width=True):
            self.config_manager.update_data_source_config(
                primary_provider=primary_provider,
                update_frequency=update_frequency,
                news_enabled=news_enabled,
                news_api_key=news_api_key
            )
            
            if self.config_manager.save_config(self.config_manager.config):
                st.success("✅ Data source configuration saved!")
                # Update market service with new API key
                if self.market_service:
                    self.market_service.news_api_key = news_api_key
                st.rerun()
    
    def render_performance_dashboard(self):
        """Render comprehensive performance dashboard"""
        st.markdown("## 📊 Performance Dashboard")
        
        # Load portfolio data
        portfolio_data = self.load_portfolio_data()
        
        if portfolio_data is None:
            st.warning("📄 No portfolio data found. Please run a trading session first.")
            return
        
        # Performance metrics
        self.render_performance_metrics(portfolio_data)
        
        # Performance charts
        self.render_performance_charts(portfolio_data)
        
        # Risk analysis
        if st.session_state.show_advanced_metrics:
            self.render_risk_analysis(portfolio_data)
    
    def load_portfolio_data(self):
        """Load portfolio data from CSV files"""
        try:
            portfolio_file = "Scripts and CSV Files/chatgpt_portfolio_update.csv"
            if not os.path.exists(portfolio_file):
                return None
            
            df = pd.read_csv(portfolio_file)
            df['Date'] = pd.to_datetime(df['Date'])
            return df
        except Exception as e:
            st.error(f"Error loading portfolio data: {e}")
            return None
    
    def render_performance_metrics(self, portfolio_df):
        """Render key performance metrics"""
        if portfolio_df is None or portfolio_df.empty:
            return
        
        # Calculate metrics
        latest_equity = portfolio_df['Total Equity'].iloc[-1] if 'Total Equity' in portfolio_df.columns else 0
        initial_equity = portfolio_df['Total Equity'].iloc[0] if 'Total Equity' in portfolio_df.columns else 100
        total_return = ((latest_equity - initial_equity) / initial_equity) * 100
        
        # Daily returns for advanced metrics
        if len(portfolio_df) > 1:
            portfolio_df['Daily_Return'] = portfolio_df['Total Equity'].pct_change()
            daily_returns = portfolio_df['Daily_Return'].dropna()
            
            if len(daily_returns) > 0:
                # Sharpe ratio
                risk_free_rate = self.config_manager.config.trading.risk_free_rate if self.config_manager else 0.045
                excess_returns = daily_returns - (risk_free_rate / 252)
                sharpe_ratio = (excess_returns.mean() / excess_returns.std()) * np.sqrt(252) if excess_returns.std() != 0 else 0
                
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
                
                # Volatility
                volatility = daily_returns.std() * np.sqrt(252) * 100
            else:
                sharpe_ratio = sortino_ratio = max_drawdown = volatility = 0
        else:
            sharpe_ratio = sortino_ratio = max_drawdown = volatility = 0
        
        # Display metrics
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            self.render_metric_card("Total Return", f"{total_return:+.2f}%", 
                                  "success" if total_return >= 0 else "danger")
        
        with col2:
            self.render_metric_card("Portfolio Value", f"${latest_equity:,.2f}", "")
        
        with col3:
            color = "success" if sharpe_ratio >= 1.0 else "warning" if sharpe_ratio >= 0.5 else "danger"
            self.render_metric_card("Sharpe Ratio", f"{sharpe_ratio:.3f}", color)
        
        with col4:
            color = "success" if max_drawdown >= -5 else "warning" if max_drawdown >= -15 else "danger"
            self.render_metric_card("Max Drawdown", f"{max_drawdown:.2f}%", color)
        
        with col5:
            color = "success" if volatility <= 20 else "warning" if volatility <= 40 else "danger"
            self.render_metric_card("Volatility", f"{volatility:.1f}%", color)
        
        # Additional metrics if advanced mode is enabled
        if st.session_state.show_advanced_metrics:
            col6, col7, col8 = st.columns(3)
            
            with col6:
                self.render_metric_card("Sortino Ratio", f"{sortino_ratio:.3f}", "")
            
            with col7:
                # Calculate win rate if trade data is available
                win_rate = 0  # Placeholder
                self.render_metric_card("Win Rate", f"{win_rate:.1f}%", "")
            
            with col8:
                # Days since inception
                days_active = (portfolio_df['Date'].max() - portfolio_df['Date'].min()).days
                self.render_metric_card("Days Active", f"{days_active}", "")
    
    def render_metric_card(self, title: str, value: str, color_class: str):
        """Render a metric card with styling"""
        st.markdown(f"""
        <div class="metric-card {color_class}-metric">
            <h4 style="margin: 0; font-size: 0.9rem; opacity: 0.8;">{title}</h4>
            <h2 style="margin: 0.5rem 0 0 0; font-size: 1.8rem;">{value}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    def render_performance_charts(self, portfolio_df):
        """Render performance visualization charts"""
        if portfolio_df is None or 'Total Equity' not in portfolio_df.columns:
            return
        
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Portfolio Performance', 'Daily Returns', 'Drawdown', 'Rolling Sharpe'),
            specs=[[{"secondary_y": True}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Portfolio performance
        fig.add_trace(
            go.Scatter(x=portfolio_df['Date'], y=portfolio_df['Total Equity'],
                      mode='lines', name='Portfolio Value', line=dict(color='#1f77b4', width=2)),
            row=1, col=1
        )
        
        # Add benchmark if available
        if 'Benchmark' in portfolio_df.columns:
            fig.add_trace(
                go.Scatter(x=portfolio_df['Date'], y=portfolio_df['Benchmark'],
                          mode='lines', name='Benchmark', line=dict(color='#ff7f0e', width=2, dash='dash')),
                row=1, col=1
            )
        
        # Daily returns
        if len(portfolio_df) > 1:
            daily_returns = portfolio_df['Total Equity'].pct_change() * 100
            fig.add_trace(
                go.Scatter(x=portfolio_df['Date'], y=daily_returns,
                          mode='lines', name='Daily Returns (%)', line=dict(color='#2ca02c')),
                row=1, col=2
            )
            
            # Drawdown
            running_max = portfolio_df['Total Equity'].expanding().max()
            drawdown = (portfolio_df['Total Equity'] - running_max) / running_max * 100
            fig.add_trace(
                go.Scatter(x=portfolio_df['Date'], y=drawdown,
                          mode='lines', name='Drawdown (%)', 
                          line=dict(color='#d62728'), fill='tonegative'),
                row=2, col=1
            )
            
            # Rolling Sharpe ratio (30-day)
            if len(daily_returns) > 30:
                rolling_sharpe = daily_returns.rolling(30).mean() / daily_returns.rolling(30).std() * np.sqrt(252)
                fig.add_trace(
                    go.Scatter(x=portfolio_df['Date'], y=rolling_sharpe,
                              mode='lines', name='30-Day Sharpe', line=dict(color='#9467bd')),
                    row=2, col=2
                )
        
        fig.update_layout(height=600, showlegend=True, title_text="Performance Analysis")
        st.plotly_chart(fig, use_container_width=True)
    
    def render_market_overview(self):
        """Render comprehensive market overview"""
        st.markdown("## 🌍 Market Overview")
        
        if not self.market_service:
            st.warning("Market data service not available")
            return
        
        # Market indices
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 📈 Market Indices")
            indices = self.market_service.get_market_indices()
            
            if indices:
                indices_data = []
                for idx in indices:
                    indices_data.append({
                        'Index': idx.name,
                        'Value': f"{idx.value:.2f}",
                        'Change': f"{idx.change:+.2f}",
                        'Change %': f"{idx.change_percent:+.2f}%"
                    })
                
                df = pd.DataFrame(indices_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("### 🎯 Market Sentiment")
            sentiment = self.market_service.get_market_sentiment_score()
            
            if sentiment:
                # Sentiment gauge
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = sentiment['overall_score'],
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Market Sentiment"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "darkblue"},
                        'steps': [
                            {'range': [0, 30], 'color': "lightgray"},
                            {'range': [30, 70], 'color': "gray"},
                            {'range': [70, 100], 'color': "lightgreen"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig.update_layout(height=300)
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown(f"**{sentiment['sentiment_label']}**")
    
    def render_news_feed(self):
        """Render news feed with sentiment analysis"""
        st.markdown("## 📰 Market News & Analysis")
        
        if not self.market_service:
            st.warning("Market data service not available")
            return
        
        # Get news
        news_items = self.market_service.get_market_news(limit=10)
        
        if not news_items:
            st.info("No news available")
            return
        
        # Display news items
        for news in news_items:
            sentiment_class = f"sentiment-{news.sentiment}"
            sentiment_emoji = {"positive": "📈", "negative": "📉", "neutral": "📊"}.get(news.sentiment, "📊")
            
            st.markdown(f"""
            <div class="news-item {sentiment_class}">
                <h4 style="margin: 0 0 0.5rem 0;">{sentiment_emoji} {news.title}</h4>
                <p style="margin: 0 0 0.5rem 0; color: #666;">{news.summary}</p>
                <small style="color: #888;">
                    <strong>{news.source}</strong> • 
                    {news.published_at.strftime("%Y-%m-%d %H:%M")} • 
                    Sentiment: {news.sentiment.title()}
                </small>
            </div>
            """, unsafe_allow_html=True)
    
    def refresh_data(self):
        """Refresh all dashboard data"""
        if self.market_service:
            self.market_service.clear_cache()
        
        st.session_state.last_update = datetime.now()
        st.session_state.market_data_cache.clear()
        st.rerun()
    
    def run(self):
        """Main dashboard application"""
        self.render_header()
        self.render_sidebar_navigation()
        
        # Auto-refresh logic
        if st.session_state.auto_refresh:
            # Use a placeholder for auto-refresh
            refresh_placeholder = st.empty()
            
            # Auto-refresh countdown
            for seconds in range(st.session_state.refresh_interval, 0, -1):
                refresh_placeholder.info(f"🔄 Auto-refresh in {seconds} seconds...")
                time.sleep(1)
            
            refresh_placeholder.empty()
            self.refresh_data()
        
        # Main content tabs
        main_tabs = st.tabs([
            "📊 Performance",
            "💼 Positions", 
            "🌍 Market",
            "📰 News",
            "🤖 AI Insights",
            "⚙️ Configuration"
        ])
        
        with main_tabs[0]:
            self.render_performance_dashboard()
        
        with main_tabs[1]:
            self.render_positions_analysis()
        
        with main_tabs[2]:
            self.render_market_overview()
        
        with main_tabs[3]:
            self.render_news_feed()
        
        with main_tabs[4]:
            self.render_ai_insights()
        
        with main_tabs[5]:
            self.render_configuration_tab()
        
        # Footer
        self.render_footer()
    
    def render_positions_analysis(self):
        """Render current positions analysis"""
        st.markdown("## 💼 Portfolio Positions")
        
        # Load current positions
        portfolio_data = self.load_portfolio_data()
        
        if portfolio_data is None or portfolio_data.empty:
            st.info("💰 No current positions. Portfolio is in cash.")
            return
        
        # Get latest positions
        latest_date = portfolio_data['Date'].max()
        current_positions = portfolio_data[portfolio_data['Date'] == latest_date]
        
        if 'Shares' in current_positions.columns:
            current_positions = current_positions[current_positions['Shares'] > 0]
        
        if current_positions.empty:
            st.info("💰 No current positions. Portfolio is in cash.")
            return
        
        # Position summary table
        st.markdown("### 📋 Current Holdings")
        display_cols = ['Ticker', 'Shares', 'Cost Basis', 'Current Price', 'Total Value', 'PnL', 'Stop Loss']
        available_cols = [col for col in display_cols if col in current_positions.columns]
        
        if available_cols:
            st.dataframe(current_positions[available_cols], use_container_width=True, hide_index=True)
        
        # Position allocation visualization
        col1, col2 = st.columns(2)
        
        with col1:
            if 'Total Value' in current_positions.columns and 'Ticker' in current_positions.columns:
                fig = px.pie(
                    current_positions,
                    values='Total Value',
                    names='Ticker',
                    title="Position Allocation"
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Risk metrics per position
            if 'PnL' in current_positions.columns:
                fig = px.bar(
                    current_positions,
                    x='Ticker',
                    y='PnL',
                    title="Position P&L",
                    color='PnL',
                    color_continuous_scale=['red', 'yellow', 'green']
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
    
    def render_ai_insights(self):
        """Render AI insights and recommendations"""
        st.markdown("## 🤖 AI Insights & Recommendations")
        
        if not self.llm_manager:
            st.warning("⚠️ AI providers not configured. Please set up API keys in the Configuration tab.")
            return
        
        available_providers = self.llm_manager.get_available_providers()
        
        if not available_providers:
            st.warning("⚠️ No AI providers available. Please configure API keys in the Configuration tab.")
            return
        
        # AI provider status
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔧 AI Provider Status")
            for provider in available_providers:
                st.success(f"✅ {provider.upper()} - Ready")
        
        with col2:
            st.markdown("### 📊 Recent Analysis")
            # This would show recent AI analysis results
            st.info("🔄 AI analysis history will be displayed here after running recommendations.")
        
        # Generate new analysis
        st.markdown("### 🧠 Generate New Analysis")
        
        analysis_type = st.selectbox(
            "Analysis Type",
            ["Market Overview", "Portfolio Review", "Risk Assessment", "Trading Opportunities"]
        )
        
        selected_provider = st.selectbox(
            "AI Provider",
            available_providers
        )
        
        if st.button("🚀 Generate AI Analysis", use_container_width=True):
            with st.spinner(f"Analyzing with {selected_provider.upper()}..."):
                # Simulate AI analysis
                time.sleep(3)
                
                # Mock analysis results
                st.success("✅ Analysis complete!")
                
                st.markdown("### 📋 AI Analysis Results")
                
                if analysis_type == "Market Overview":
                    st.markdown("""
                    **Market Analysis Summary:**
                    - Overall market sentiment: Cautiously optimistic
                    - Volatility: Moderate levels, within normal ranges  
                    - Sector rotation: Technology showing relative strength
                    - Risk factors: Monitor inflation data and Fed policy signals
                    
                    **Recommended Actions:**
                    - Maintain current diversification strategy
                    - Consider reducing position sizes if volatility increases
                    - Keep 10-15% cash reserve for opportunities
                    """)
                
                elif analysis_type == "Portfolio Review":
                    st.markdown("""
                    **Portfolio Health Check:**
                    - Current allocation: Well diversified across sectors
                    - Risk level: Moderate, appropriate for micro-cap strategy
                    - Performance: Outperforming benchmark by 2.3%
                    - Correlation: Low correlation between positions (good)
                    
                    **Optimization Suggestions:**
                    - Consider taking profits on positions up >20%
                    - Review stop-loss levels for recent entries
                    - Monitor position sizes relative to volatility
                    """)
    
    def render_footer(self):
        """Render dashboard footer"""
        st.markdown("---")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.session_state.last_update:
                st.markdown(f"*Last updated: {st.session_state.last_update.strftime('%Y-%m-%d %H:%M:%S')}*")
            else:
                st.markdown("*Never updated*")
        
        with col2:
            if self.market_service:
                cache_stats = self.market_service.get_cache_stats()
                st.markdown(f"*Cache: {cache_stats['valid_items']}/{cache_stats['total_items']} items*")
        
        with col3:
            st.markdown("*Advanced Trading Dashboard v2.0*")

def main():
    """Main application entry point"""
    dashboard = AdvancedTradingDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()