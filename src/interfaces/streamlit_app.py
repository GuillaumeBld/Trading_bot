from pathlib import Path
import io
from contextlib import redirect_stdout

import pandas as pd
import streamlit as st

from trading_script import (
    load_latest_portfolio_state,
    set_data_dir,
    log_manual_buy,
    log_manual_sell,
    process_portfolio,
    daily_results,
    get_llm_manager,
    LLM_AVAILABLE,
)


st.title("ChatGPT Micro-Cap Trading Interface")

# Sidebar Configuration
st.sidebar.header("Configuration")

DEFAULT_DIR = Path("Scripts and CSV Files")
data_dir = Path(st.sidebar.text_input("Data directory", str(DEFAULT_DIR)))
set_data_dir(data_dir)
portfolio_file = data_dir / "chatgpt_portfolio_update.csv"

# LLM Configuration
st.sidebar.header(" AI Assistant")

if LLM_AVAILABLE:
    llm_manager = get_llm_manager()
    available_providers = llm_manager.get_available_providers() if llm_manager else []
    
    use_llm = st.sidebar.checkbox("Enable AI Recommendations", value=False)
    
    if use_llm and available_providers:
        selected_provider = st.sidebar.selectbox(
            "LLM Provider",
            available_providers,
            help="Choose which AI model to use for trading recommendations"
        )
        
        if llm_manager:
            llm_manager.set_active_provider(selected_provider)
            st.sidebar.success(f" {selected_provider.upper()} ready")
    elif use_llm and not available_providers:
        st.sidebar.error("No LLM providers available. Check your configuration.")
        use_llm = False
    else:
        selected_provider = None
else:
    st.sidebar.warning("LLM interface not available")
    use_llm = False
    selected_provider = None

# Load state on first run
if "portfolio_df" not in st.session_state:
    portfolio, cash = load_latest_portfolio_state(str(portfolio_file))
    st.session_state.portfolio_df = pd.DataFrame(portfolio)
    st.session_state.cash = cash

st.subheader("Current Portfolio")
st.write(f"Cash: ${st.session_state.cash:.2f}")
st.dataframe(st.session_state.portfolio_df)

# Manual buy form
with st.expander("Log Manual Buy"):
    with st.form("buy_form"):
        ticker = st.text_input("Ticker").upper()
        shares = st.number_input("Shares", min_value=0.0, step=1.0)
        buy_price = st.number_input("Buy Price", min_value=0.0, step=0.01, format="%.2f")
        stop_loss = st.number_input("Stop Loss", min_value=0.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("Log Buy")
        if submitted and ticker:
            cash, df = log_manual_buy(
                buy_price,
                shares,
                ticker,
                stop_loss,
                st.session_state.cash,
                st.session_state.portfolio_df,
                interactive=False,
            )
            st.session_state.cash = cash
            st.session_state.portfolio_df = df
            st.success("Manual buy logged")

# Manual sell form
with st.expander("Log Manual Sell"):
    with st.form("sell_form"):
        ticker = st.text_input("Ticker", key="sell_ticker").upper()
        shares = st.number_input("Shares to sell", min_value=0.0, step=1.0, key="sell_shares")
        sell_price = st.number_input(
            "Sell Price", min_value=0.0, step=0.01, format="%.2f", key="sell_price"
        )
        reason = st.text_input("Reason", key="sell_reason")
        submitted = st.form_submit_button("Log Sell")
        if submitted and ticker:
            cash, df = log_manual_sell(
                sell_price,
                shares,
                ticker,
                st.session_state.cash,
                st.session_state.portfolio_df,
                reason=reason,
                interactive=False,
            )
            st.session_state.cash = cash
            st.session_state.portfolio_df = df
            st.success("Manual sell logged")

st.subheader("Updated Portfolio")
st.write(f"Cash: ${st.session_state.cash:.2f}")
st.dataframe(st.session_state.portfolio_df)

# Process Portfolio Section
col1, col2 = st.columns(2)

with col1:
    if st.button(" Process Portfolio (Manual)", use_container_width=True):
        buf = io.StringIO()
        with redirect_stdout(buf):
            st.session_state.portfolio_df, st.session_state.cash = process_portfolio(
                st.session_state.portfolio_df, st.session_state.cash, 
                interactive=False, use_llm=False
            )
            daily_results(st.session_state.portfolio_df, st.session_state.cash)
        st.text(buf.getvalue())

with col2:
    if st.button(" Process with AI", use_container_width=True, disabled=not use_llm):
        if use_llm:
            buf = io.StringIO()
            with redirect_stdout(buf):
                st.session_state.portfolio_df, st.session_state.cash = process_portfolio(
                    st.session_state.portfolio_df, st.session_state.cash,
                    interactive=False, use_llm=True, llm_provider=selected_provider
                )
                daily_results(st.session_state.portfolio_df, st.session_state.cash)
            st.text(buf.getvalue())
        else:
            st.error("Enable AI recommendations first!")