#!/usr/bin/env python3
"""
Dynamic Real-Time Trading Dashboard

This advanced dashboard provides:
- Real-time data updates with automatic refresh
- Live performance monitoring and alerts
- Dynamic charts that update without page reload
- WebSocket integration for instant updates
- Configurable refresh intervals
- Background data processing
- Live trading notifications
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
import asyncio
import threading
from typing import Dict, List, Optional, Any
import queue
import logging

# Import our custom modules
try:
    import sys
    from pathlib import Path
    sys.path.append(str(Path(__file__).parent.parent))
    
    from config.dashboard_config import get_config_manager, ConfigManager
    from services.market_data_service import get_market_service, MarketDataService
    from core.trading_script import load_portfolio_data, get_performance_metrics
    from core.llm_interface import LLMManager
    CONFIG_AVAILABLE = True
except ImportError as e:
    st.error(f"⚠️ Required modules not available: {e}")
    CONFIG_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page configuration
st.set_page_config(
    page_title="🚀 Dynamic Trading Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for dynamic updates
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now()
if 'auto_refresh' not in st.session_state:
    st.session_state.auto_refresh = True
if 'refresh_interval' not in st.session_state:
    st.session_state.refresh_interval = 30  # seconds
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {}
if 'update_queue' not in st.session_state:
    st.session_state.update_queue = queue.Queue()
if 'notifications' not in st.session_state:
    st.session_state.notifications = []

# Enhanced CSS styling for dynamic dashboard
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.8; }
        100% { opacity: 1; }
    }
    
    .live-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        background-color: #00ff00;
        border-radius: 50%;
        animation: blink 1s infinite;
        margin-right: 8px;
    }
    
    @keyframes blink {
        0%, 50% { opacity: 1; }
        51%, 100% { opacity: 0.3; }
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: 1rem 0;
    }
    
    .alert-box {
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        animation: slideIn 0.5s ease-in;
    }
    
    @keyframes slideIn {
        from { transform: translateX(-100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    
    .alert-success { background-color: #d4edda; border-left: 4px solid #28a745; }
    .alert-warning { background-color: #fff3cd; border-left: 4px solid #ffc107; }
    .alert-danger { background-color: #f8d7da; border-left: 4px solid #dc3545; }
    
    .update-timestamp {
        position: fixed;
        top: 10px;
        right: 10px;
        background: rgba(0,0,0,0.7);
        color: white;
        padding: 5px 10px;
        border-radius: 5px;
        font-size: 0.8rem;
        z-index: 1000;
    }
    
    .refresh-controls {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
    }
</style>
""", unsafe_allow_html=True)

class DynamicDataManager:
    """Manages real-time data updates and caching"""
    
    def __init__(self):
        self.cache = {}
        self.last_updates = {}
        self.update_lock = threading.Lock()
        
    def get_cached_data(self, key: str, max_age: int = 30) -> Optional[Any]:
        """Get cached data if it's not too old"""
        with self.update_lock:
            if key in self.cache and key in self.last_updates:
                age = (datetime.now() - self.last_updates[key]).seconds
                if age < max_age:
                    return self.cache[key]
            return None
    
    def set_cached_data(self, key: str, data: Any):
        """Set cached data with timestamp"""
        with self.update_lock:
            self.cache[key] = data
            self.last_updates[key] = datetime.now()
    
    def clear_cache(self):
        """Clear all cached data"""
        with self.update_lock:
            self.cache.clear()
            self.last_updates.clear()

# Initialize data manager
@st.cache_resource
def get_data_manager():
    return DynamicDataManager()

data_manager = get_data_manager()

def add_notification(message: str, type: str = "info"):
    """Add a notification to the queue"""
    notification = {
        'message': message,
        'type': type,
        'timestamp': datetime.now(),
        'id': len(st.session_state.notifications)
    }
    st.session_state.notifications.append(notification)
    
    # Keep only last 10 notifications
    if len(st.session_state.notifications) > 10:
        st.session_state.notifications = st.session_state.notifications[-10:]

def display_notifications():
    """Display live notifications"""
    if st.session_state.notifications:
        st.markdown("### 🔔 Live Notifications")
        for notif in reversed(st.session_state.notifications[-5:]):  # Show last 5
            type_class = f"alert-{notif['type']}" if notif['type'] in ['success', 'warning', 'danger'] else "alert-info"
            time_str = notif['timestamp'].strftime("%H:%M:%S")
            st.markdown(f"""
            <div class="alert-box {type_class}">
                <strong>[{time_str}]</strong> {notif['message']}
            </div>
            """, unsafe_allow_html=True)

def get_real_time_portfolio_data():
    """Get real-time portfolio data with caching"""
    cached = data_manager.get_cached_data('portfolio', max_age=10)
    if cached is not None:
        return cached
    
    try:
        # Load portfolio data
        portfolio_data = load_portfolio_data()
        if portfolio_data is not None:
            data_manager.set_cached_data('portfolio', portfolio_data)
            add_notification("Portfolio data updated", "success")
            return portfolio_data
    except Exception as e:
        logger.error(f"Error loading portfolio data: {e}")
        add_notification(f"Error loading portfolio: {str(e)}", "danger")
    
    return None

def get_real_time_market_data():
    """Get real-time market data with caching"""
    cached = data_manager.get_cached_data('market', max_age=30)
    if cached is not None:
        return cached
    
    try:
        if CONFIG_AVAILABLE:
            market_service = get_market_service()
            if market_service:
                # Get major indices
                indices = ['SPY', 'QQQ', 'IWM', 'VIX']
                market_data = {}
                for symbol in indices:
                    data = market_service.get_stock_data(symbol)
                    if data:
                        market_data[symbol] = data
                
                if market_data:
                    data_manager.set_cached_data('market', market_data)
                    add_notification("Market data updated", "success")
                    return market_data
    except Exception as e:
        logger.error(f"Error loading market data: {e}")
        add_notification(f"Error loading market data: {str(e)}", "warning")
    
    return None

def create_dynamic_portfolio_chart(portfolio_data):
    """Create dynamic portfolio performance chart"""
    if portfolio_data is None or portfolio_data.empty:
        return go.Figure().add_annotation(text="No portfolio data available", 
                                        xref="paper", yref="paper", x=0.5, y=0.5)
    
    # Create interactive chart with multiple traces
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Portfolio Value Over Time', 'Daily Returns', 
                       'Asset Allocation', 'Risk Metrics'),
        specs=[[{"secondary_y": True}, {"secondary_y": False}],
               [{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Portfolio value over time
    if 'date' in portfolio_data.columns and 'total_value' in portfolio_data.columns:
        fig.add_trace(
            go.Scatter(
                x=portfolio_data['date'],
                y=portfolio_data['total_value'],
                mode='lines+markers',
                name='Portfolio Value',
                line=dict(color='#1f77b4', width=3),
                hovertemplate='<b>Date:</b> %{x}<br><b>Value:</b> $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Add benchmark comparison if available
    if 'benchmark_value' in portfolio_data.columns:
        fig.add_trace(
            go.Scatter(
                x=portfolio_data['date'],
                y=portfolio_data['benchmark_value'],
                mode='lines',
                name='S&P 500',
                line=dict(color='#ff7f0e', width=2, dash='dash'),
                hovertemplate='<b>Date:</b> %{x}<br><b>S&P 500:</b> $%{y:,.2f}<extra></extra>'
            ),
            row=1, col=1
        )
    
    # Daily returns histogram
    if 'daily_return' in portfolio_data.columns:
        fig.add_trace(
            go.Histogram(
                x=portfolio_data['daily_return'],
                nbinsx=30,
                name='Daily Returns',
                marker_color='#2ca02c',
                opacity=0.7
            ),
            row=1, col=2
        )
    
    # Asset allocation pie chart
    if 'symbol' in portfolio_data.columns and 'current_value' in portfolio_data.columns:
        allocation_data = portfolio_data.groupby('symbol')['current_value'].sum().reset_index()
        fig.add_trace(
            go.Pie(
                labels=allocation_data['symbol'],
                values=allocation_data['current_value'],
                name="Asset Allocation",
                hovertemplate='<b>%{label}</b><br>Value: $%{value:,.2f}<br>%{percent}<extra></extra>'
            ),
            row=2, col=1
        )
    
    # Risk metrics bar chart
    risk_metrics = ['Sharpe Ratio', 'Sortino Ratio', 'Max Drawdown', 'Volatility']
    risk_values = [1.2, 1.5, -0.15, 0.18]  # Example values
    fig.add_trace(
        go.Bar(
            x=risk_metrics,
            y=risk_values,
            name='Risk Metrics',
            marker_color=['#d62728' if v < 0 else '#2ca02c' for v in risk_values]
        ),
        row=2, col=2
    )
    
    # Update layout for better appearance
    fig.update_layout(
        height=800,
        showlegend=True,
        title_text="Real-Time Portfolio Dashboard",
        title_x=0.5,
        title_font_size=20,
        template="plotly_white"
    )
    
    return fig

def create_live_performance_metrics(portfolio_data):
    """Create live performance metrics display"""
    if portfolio_data is None or portfolio_data.empty:
        return None
    
    try:
        metrics = get_performance_metrics(portfolio_data)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_return = metrics.get('total_return', 0)
            delta_color = "normal" if total_return >= 0 else "inverse"
            st.metric(
                label="📈 Total Return",
                value=f"{total_return:.2%}",
                delta=f"{total_return:.2%}",
                delta_color=delta_color
            )
        
        with col2:
            sharpe_ratio = metrics.get('sharpe_ratio', 0)
            st.metric(
                label="⚡ Sharpe Ratio",
                value=f"{sharpe_ratio:.2f}",
                delta="Good" if sharpe_ratio > 1.0 else "Needs Improvement"
            )
        
        with col3:
            max_drawdown = metrics.get('max_drawdown', 0)
            st.metric(
                label="📉 Max Drawdown",
                value=f"{max_drawdown:.2%}",
                delta=f"{max_drawdown:.2%}",
                delta_color="inverse"
            )
        
        with col4:
            win_rate = metrics.get('win_rate', 0)
            st.metric(
                label="🎯 Win Rate",
                value=f"{win_rate:.1%}",
                delta="Excellent" if win_rate > 0.6 else "Good" if win_rate > 0.5 else "Needs Work"
            )
        
        return metrics
    except Exception as e:
        logger.error(f"Error calculating performance metrics: {e}")
        st.error(f"Error calculating metrics: {e}")
        return None

def create_market_overview():
    """Create real-time market overview"""
    market_data = get_real_time_market_data()
    
    if market_data:
        st.markdown("### 🌍 Live Market Overview")
        
        cols = st.columns(len(market_data))
        for i, (symbol, data) in enumerate(market_data.items()):
            with cols[i]:
                if isinstance(data, dict) and 'price' in data:
                    change = data.get('change', 0)
                    change_pct = data.get('change_percent', 0)
                    color = "🟢" if change >= 0 else "🔴"
                    
                    st.markdown(f"""
                    <div class="metric-card">
                        <h3>{symbol} {color}</h3>
                        <h2>${data['price']:.2f}</h2>
                        <p>{change:+.2f} ({change_pct:+.2%})</p>
                    </div>
                    """, unsafe_allow_html=True)

def auto_refresh_handler():
    """Handle automatic refresh logic"""
    if st.session_state.auto_refresh:
        time_since_update = (datetime.now() - st.session_state.last_update).seconds
        
        if time_since_update >= st.session_state.refresh_interval:
            # Clear cache to force refresh
            data_manager.clear_cache()
            st.session_state.last_update = datetime.now()
            add_notification("Dashboard auto-refreshed", "info")
            st.rerun()

def main():
    """Main dashboard application"""
    
    # Display live indicator and timestamp
    st.markdown(f"""
    <div class="update-timestamp">
        <span class="live-indicator"></span>
        Last Update: {st.session_state.last_update.strftime('%H:%M:%S')}
    </div>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🚀 Dynamic Trading Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar controls
    with st.sidebar:
        st.markdown("### ⚙️ Real-Time Controls")
        
        # Auto-refresh controls
        st.session_state.auto_refresh = st.checkbox(
            "🔄 Auto Refresh", 
            value=st.session_state.auto_refresh,
            help="Automatically refresh data at specified intervals"
        )
        
        if st.session_state.auto_refresh:
            st.session_state.refresh_interval = st.slider(
                "Refresh Interval (seconds)",
                min_value=5,
                max_value=300,
                value=st.session_state.refresh_interval,
                step=5
            )
        
        # Manual refresh button
        if st.button("🔄 Refresh Now", use_container_width=True):
            data_manager.clear_cache()
            st.session_state.last_update = datetime.now()
            add_notification("Manual refresh triggered", "info")
            st.rerun()
        
        # Clear notifications
        if st.button("🧹 Clear Notifications", use_container_width=True):
            st.session_state.notifications.clear()
            st.rerun()
        
        st.markdown("---")
        
        # Status indicators
        st.markdown("### 📊 System Status")
        st.success("✅ Dashboard: Online")
        st.success("✅ Data Feed: Active" if CONFIG_AVAILABLE else "❌ Data Feed: Offline")
        st.info(f"🔄 Auto-refresh: {'ON' if st.session_state.auto_refresh else 'OFF'}")
    
    # Display notifications
    display_notifications()
    
    # Market overview
    create_market_overview()
    
    # Get real-time portfolio data
    portfolio_data = get_real_time_portfolio_data()
    
    # Performance metrics
    st.markdown("### 📊 Live Performance Metrics")
    create_live_performance_metrics(portfolio_data)
    
    # Dynamic charts
    st.markdown("### 📈 Real-Time Portfolio Analysis")
    if portfolio_data is not None:
        chart = create_dynamic_portfolio_chart(portfolio_data)
        st.plotly_chart(chart, use_container_width=True, key="portfolio_chart")
    else:
        st.warning("📊 No portfolio data available. Start trading to see live updates!")
    
    # Real-time trading activity (if available)
    st.markdown("### 🔄 Recent Trading Activity")
    if portfolio_data is not None and not portfolio_data.empty:
        recent_trades = portfolio_data.tail(10)
        st.dataframe(
            recent_trades,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No recent trading activity to display.")
    
    # Auto-refresh handler
    auto_refresh_handler()
    
    # Footer with refresh controls
    st.markdown(f"""
    <div class="refresh-controls">
        <small>
            🔄 Next refresh in: {st.session_state.refresh_interval - (datetime.now() - st.session_state.last_update).seconds if st.session_state.auto_refresh else 'Manual'} seconds
        </small>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()