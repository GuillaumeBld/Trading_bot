#!/usr/bin/env python3
"""
FastAPI Wrapper for Trading Bot n8n Integration

This API wrapper provides REST endpoints for n8n workflows to interact
with the trading bot, including portfolio management, trading operations,
market data, and notifications.
"""

from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse
import uvicorn
import os
import sys
from pathlib import Path
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import asyncio
import httpx
import hashlib
import hmac

# Add src to path for importing trading bot modules
sys.path.append(str(Path(__file__).parent / "src"))

# Import custom modules
from models import (
    TradeRequest, TradeResponse, PortfolioResponse, 
    MarketDataResponse, NotificationRequest, WebhookRequest,
    AIAnalysisRequest, AIAnalysisResponse, HealthResponse
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Trading Bot API",
    description="REST API for n8n integration with ChatGPT Micro-Cap Trading Bot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:5678,http://localhost:3000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer(auto_error=False)
API_KEY = os.getenv("API_KEY", "your-api-key")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "your-webhook-secret")

# Trading bot connection
TRADING_BOT_URL = os.getenv("TRADING_BOT_URL", "http://localhost:8501")

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify API key for authentication"""
    if not credentials or credentials.credentials != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return credentials.credentials

def verify_webhook_signature(request: Request, payload: bytes) -> bool:
    """Verify webhook signature for security"""
    signature = request.headers.get("X-Webhook-Signature")
    if not signature:
        return False
    
    expected_signature = hmac.new(
        WEBHOOK_SECRET.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)

# Health check endpoint
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        # Check trading bot connection
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{TRADING_BOT_URL}/_stcore/health", timeout=5.0)
            trading_bot_status = response.status_code == 200
    except:
        trading_bot_status = False
    
    return HealthResponse(
        status="healthy" if trading_bot_status else "degraded",
        timestamp=datetime.now(),
        services={
            "api": True,
            "trading_bot": trading_bot_status,
            "database": True,  # TODO: Add actual database health check
        }
    )

# Portfolio Management Endpoints
@app.get("/api/portfolio", response_model=PortfolioResponse)
async def get_portfolio(api_key: str = Depends(verify_api_key)):
    """Get current portfolio information"""
    try:
        # Import here to avoid circular imports
        from src.core.trading_script import load_portfolio_data, get_performance_metrics
        
        portfolio_data = load_portfolio_data()
        if portfolio_data is None:
            raise HTTPException(status_code=404, detail="Portfolio data not found")
        
        performance_metrics = get_performance_metrics(portfolio_data)
        
        return PortfolioResponse(
            total_value=float(portfolio_data['current_value'].sum()) if 'current_value' in portfolio_data.columns else 0,
            positions=portfolio_data.to_dict('records'),
            performance_metrics=performance_metrics,
            last_updated=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error getting portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/portfolio/performance")
async def get_portfolio_performance(api_key: str = Depends(verify_api_key)):
    """Get portfolio performance metrics"""
    try:
        from src.core.trading_script import load_portfolio_data, get_performance_metrics
        
        portfolio_data = load_portfolio_data()
        if portfolio_data is None:
            raise HTTPException(status_code=404, detail="Portfolio data not found")
        
        metrics = get_performance_metrics(portfolio_data)
        return {
            "performance_metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting performance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/portfolio/refresh")
async def refresh_portfolio(background_tasks: BackgroundTasks, api_key: str = Depends(verify_api_key)):
    """Refresh portfolio data"""
    try:
        # Add background task to refresh portfolio
        background_tasks.add_task(refresh_portfolio_data)
        return {"message": "Portfolio refresh initiated", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        logger.error(f"Error refreshing portfolio: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Trading Operations Endpoints
@app.post("/api/trade/buy", response_model=TradeResponse)
async def execute_buy_order(trade_request: TradeRequest, api_key: str = Depends(verify_api_key)):
    """Execute a buy order"""
    try:
        from src.core.trading_script import log_manual_buy
        
        result = log_manual_buy(
            symbol=trade_request.symbol,
            shares=trade_request.shares,
            price=trade_request.price,
            stop_loss=trade_request.stop_loss
        )
        
        return TradeResponse(
            trade_id=f"buy_{datetime.now().timestamp()}",
            symbol=trade_request.symbol,
            action="buy",
            shares=trade_request.shares,
            price=trade_request.price,
            status="executed",
            timestamp=datetime.now(),
            message=f"Successfully bought {trade_request.shares} shares of {trade_request.symbol}"
        )
    except Exception as e:
        logger.error(f"Error executing buy order: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/trade/sell", response_model=TradeResponse)
async def execute_sell_order(trade_request: TradeRequest, api_key: str = Depends(verify_api_key)):
    """Execute a sell order"""
    try:
        from src.core.trading_script import log_manual_sell
        
        result = log_manual_sell(
            symbol=trade_request.symbol,
            shares=trade_request.shares,
            price=trade_request.price
        )
        
        return TradeResponse(
            trade_id=f"sell_{datetime.now().timestamp()}",
            symbol=trade_request.symbol,
            action="sell",
            shares=trade_request.shares,
            price=trade_request.price,
            status="executed",
            timestamp=datetime.now(),
            message=f"Successfully sold {trade_request.shares} shares of {trade_request.symbol}"
        )
    except Exception as e:
        logger.error(f"Error executing sell order: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/trades/recent")
async def get_recent_trades(limit: int = 10, api_key: str = Depends(verify_api_key)):
    """Get recent trades"""
    try:
        from src.core.trading_script import load_portfolio_data
        
        portfolio_data = load_portfolio_data()
        if portfolio_data is None:
            return {"trades": [], "timestamp": datetime.now().isoformat()}
        
        # Get recent trades (simplified - you might want to implement proper trade logging)
        recent_trades = portfolio_data.tail(limit).to_dict('records')
        
        return {
            "trades": recent_trades,
            "count": len(recent_trades),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting recent trades: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Market Data Endpoints
@app.get("/api/market/data", response_model=MarketDataResponse)
async def get_market_data(symbols: Optional[str] = "SPY,QQQ,IWM,VIX", api_key: str = Depends(verify_api_key)):
    """Get current market data"""
    try:
        from src.services.market_data_service import get_market_service
        
        symbol_list = symbols.split(",") if symbols else ["SPY", "QQQ", "IWM", "VIX"]
        market_service = get_market_service()
        
        market_data = {}
        for symbol in symbol_list:
            data = market_service.get_stock_data(symbol.strip())
            if data:
                market_data[symbol.strip()] = data
        
        return MarketDataResponse(
            data=market_data,
            timestamp=datetime.now(),
            symbols=symbol_list
        )
    except Exception as e:
        logger.error(f"Error getting market data: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market/news")
async def get_market_news(limit: int = 10, api_key: str = Depends(verify_api_key)):
    """Get latest market news"""
    try:
        from src.services.market_data_service import get_market_service
        
        market_service = get_market_service()
        news = market_service.get_news(limit=limit)
        
        return {
            "news": news,
            "count": len(news) if news else 0,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting market news: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/market/sentiment")
async def get_market_sentiment(api_key: str = Depends(verify_api_key)):
    """Get market sentiment analysis"""
    try:
        from src.services.market_data_service import get_market_service
        
        market_service = get_market_service()
        sentiment = market_service.get_market_sentiment()
        
        return {
            "sentiment": sentiment,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting market sentiment: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# AI Analysis Endpoints
@app.post("/api/ai/analyze", response_model=AIAnalysisResponse)
async def get_ai_analysis(request: AIAnalysisRequest, api_key: str = Depends(verify_api_key)):
    """Get AI trading analysis and recommendations"""
    try:
        from src.core.llm_interface import LLMManager
        from src.core.trading_script import load_portfolio_data
        
        llm_manager = LLMManager()
        portfolio_data = load_portfolio_data()
        
        if portfolio_data is None:
            raise HTTPException(status_code=404, detail="Portfolio data not found")
        
        # Get AI recommendations
        recommendations = llm_manager.analyze_portfolio(
            portfolio_data=portfolio_data.to_dict(),
            market_data={},  # TODO: Add market data
            prompt=request.prompt or "Analyze current portfolio and provide trading recommendations"
        )
        
        return AIAnalysisResponse(
            recommendations=recommendations,
            provider=request.provider or llm_manager.active_provider,
            timestamp=datetime.now(),
            confidence_score=0.8  # TODO: Calculate actual confidence
        )
    except Exception as e:
        logger.error(f"Error getting AI analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/ai/providers")
async def get_ai_providers(api_key: str = Depends(verify_api_key)):
    """Get available AI providers"""
    try:
        from src.core.llm_interface import LLMManager
        
        llm_manager = LLMManager()
        providers = llm_manager.get_available_providers()
        
        return {
            "providers": providers,
            "active_provider": llm_manager.active_provider,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting AI providers: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Webhook Endpoints
@app.post("/api/webhooks/n8n")
async def handle_n8n_webhook(request: Request, webhook_data: WebhookRequest):
    """Handle incoming webhooks from n8n"""
    try:
        # Verify webhook signature
        body = await request.body()
        if not verify_webhook_signature(request, body):
            raise HTTPException(status_code=401, detail="Invalid webhook signature")
        
        # Process webhook based on event type
        if webhook_data.event_type == "trade_signal":
            # Handle trading signal from n8n
            result = await process_trade_signal(webhook_data.data)
        elif webhook_data.event_type == "portfolio_alert":
            # Handle portfolio alert
            result = await process_portfolio_alert(webhook_data.data)
        elif webhook_data.event_type == "market_update":
            # Handle market update
            result = await process_market_update(webhook_data.data)
        else:
            result = {"message": f"Received {webhook_data.event_type} event", "processed": True}
        
        return {
            "status": "success",
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error handling webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/webhooks/register")
async def register_webhook(webhook_url: str, events: List[str], api_key: str = Depends(verify_api_key)):
    """Register a webhook URL for specific events"""
    try:
        # TODO: Implement webhook registration logic
        return {
            "message": "Webhook registered successfully",
            "webhook_url": webhook_url,
            "events": events,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error registering webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Notification Endpoints
@app.post("/api/notifications/send")
async def send_notification(notification: NotificationRequest, api_key: str = Depends(verify_api_key)):
    """Send notification to configured channels"""
    try:
        # TODO: Implement notification sending logic
        return {
            "message": "Notification sent successfully",
            "channels": notification.channels,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error sending notification: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/notifications")
async def get_notifications(limit: int = 50, api_key: str = Depends(verify_api_key)):
    """Get recent notifications"""
    try:
        # TODO: Implement notification retrieval logic
        return {
            "notifications": [],
            "count": 0,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting notifications: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background Tasks
async def refresh_portfolio_data():
    """Background task to refresh portfolio data"""
    try:
        from src.core.trading_script import load_portfolio_data
        # TODO: Implement portfolio refresh logic
        logger.info("Portfolio data refreshed")
    except Exception as e:
        logger.error(f"Error refreshing portfolio data: {e}")

async def process_trade_signal(data: Dict[str, Any]):
    """Process trading signal from n8n"""
    # TODO: Implement trade signal processing
    logger.info(f"Processing trade signal: {data}")
    return {"message": "Trade signal processed", "data": data}

async def process_portfolio_alert(data: Dict[str, Any]):
    """Process portfolio alert from n8n"""
    # TODO: Implement portfolio alert processing
    logger.info(f"Processing portfolio alert: {data}")
    return {"message": "Portfolio alert processed", "data": data}

async def process_market_update(data: Dict[str, Any]):
    """Process market update from n8n"""
    # TODO: Implement market update processing
    logger.info(f"Processing market update: {data}")
    return {"message": "Market update processed", "data": data}

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("DEBUG", "false").lower() == "true",
        workers=int(os.getenv("API_WORKERS", 1))
    )