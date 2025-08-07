#!/usr/bin/env python3
"""
Pydantic Models for Trading Bot API

Defines all request/response models for the FastAPI wrapper
used in n8n integration.
"""

from pydantic import BaseModel, Field, validator
from typing import List, Dict, Any, Optional, Union
from datetime import datetime
from enum import Enum

class TradeAction(str, Enum):
    """Trade action types"""
    BUY = "buy"
    SELL = "sell"
    HOLD = "hold"

class NotificationChannel(str, Enum):
    """Notification channel types"""
    SLACK = "slack"
    DISCORD = "discord"
    EMAIL = "email"
    TELEGRAM = "telegram"
    SMS = "sms"

class EventType(str, Enum):
    """Webhook event types"""
    TRADE_SIGNAL = "trade_signal"
    PORTFOLIO_ALERT = "portfolio_alert"
    MARKET_UPDATE = "market_update"
    NEWS_UPDATE = "news_update"
    RISK_ALERT = "risk_alert"

# Request Models
class TradeRequest(BaseModel):
    """Request model for trade operations"""
    symbol: str = Field(..., description="Stock ticker symbol", min_length=1, max_length=10)
    shares: float = Field(..., description="Number of shares to trade", gt=0)
    price: Optional[float] = Field(None, description="Target price per share", gt=0)
    stop_loss: Optional[float] = Field(None, description="Stop loss price", gt=0)
    action: TradeAction = Field(..., description="Trade action to perform")
    
    @validator('symbol')
    def symbol_must_be_uppercase(cls, v):
        return v.upper().strip()
    
    @validator('stop_loss')
    def stop_loss_must_be_reasonable(cls, v, values):
        if v is not None and 'price' in values and values['price'] is not None:
            if values['action'] == TradeAction.BUY and v >= values['price']:
                raise ValueError('Stop loss must be below buy price')
            elif values['action'] == TradeAction.SELL and v <= values['price']:
                raise ValueError('Stop loss must be above sell price')
        return v

class AIAnalysisRequest(BaseModel):
    """Request model for AI analysis"""
    symbols: Optional[List[str]] = Field(None, description="Specific symbols to analyze")
    provider: Optional[str] = Field(None, description="AI provider to use")
    prompt: Optional[str] = Field(None, description="Custom analysis prompt")
    include_market_data: bool = Field(True, description="Include current market data")
    include_news: bool = Field(True, description="Include recent news")
    
    @validator('symbols')
    def symbols_must_be_valid(cls, v):
        if v:
            return [symbol.upper().strip() for symbol in v]
        return v

class NotificationRequest(BaseModel):
    """Request model for sending notifications"""
    message: str = Field(..., description="Notification message", min_length=1)
    title: Optional[str] = Field(None, description="Notification title")
    channels: List[NotificationChannel] = Field(..., description="Target channels")
    priority: int = Field(1, description="Priority level (1-5)", ge=1, le=5)
    data: Optional[Dict[str, Any]] = Field(None, description="Additional notification data")

class WebhookRequest(BaseModel):
    """Request model for webhook events"""
    event_type: EventType = Field(..., description="Type of webhook event")
    data: Dict[str, Any] = Field(..., description="Event data payload")
    source: Optional[str] = Field(None, description="Source system identifier")
    timestamp: Optional[datetime] = Field(None, description="Event timestamp")
    
    @validator('timestamp', pre=True, always=True)
    def set_timestamp(cls, v):
        return v or datetime.now()

# Response Models
class TradeResponse(BaseModel):
    """Response model for trade operations"""
    trade_id: str = Field(..., description="Unique trade identifier")
    symbol: str = Field(..., description="Stock ticker symbol")
    action: TradeAction = Field(..., description="Trade action performed")
    shares: float = Field(..., description="Number of shares traded")
    price: Optional[float] = Field(None, description="Execution price per share")
    status: str = Field(..., description="Trade status")
    timestamp: datetime = Field(..., description="Trade execution timestamp")
    message: str = Field(..., description="Status message")
    fees: Optional[float] = Field(None, description="Trading fees")

class PortfolioPosition(BaseModel):
    """Model for individual portfolio position"""
    symbol: str = Field(..., description="Stock ticker symbol")
    shares: float = Field(..., description="Number of shares held")
    avg_cost: float = Field(..., description="Average cost per share")
    current_price: float = Field(..., description="Current market price")
    current_value: float = Field(..., description="Current position value")
    unrealized_pnl: float = Field(..., description="Unrealized profit/loss")
    unrealized_pnl_percent: float = Field(..., description="Unrealized P&L percentage")
    stop_loss: Optional[float] = Field(None, description="Stop loss price")

class PerformanceMetrics(BaseModel):
    """Model for portfolio performance metrics"""
    total_return: float = Field(..., description="Total return percentage")
    sharpe_ratio: float = Field(..., description="Sharpe ratio")
    sortino_ratio: Optional[float] = Field(None, description="Sortino ratio")
    max_drawdown: float = Field(..., description="Maximum drawdown percentage")
    volatility: float = Field(..., description="Annualized volatility")
    win_rate: float = Field(..., description="Win rate percentage")
    profit_factor: Optional[float] = Field(None, description="Profit factor")
    total_trades: int = Field(..., description="Total number of trades")

class PortfolioResponse(BaseModel):
    """Response model for portfolio information"""
    total_value: float = Field(..., description="Total portfolio value")
    cash: float = Field(0, description="Available cash")
    positions: List[PortfolioPosition] = Field(..., description="Current positions")
    performance_metrics: PerformanceMetrics = Field(..., description="Performance metrics")
    last_updated: datetime = Field(..., description="Last update timestamp")

class MarketDataPoint(BaseModel):
    """Model for individual market data point"""
    symbol: str = Field(..., description="Stock ticker symbol")
    price: float = Field(..., description="Current price")
    change: float = Field(..., description="Price change")
    change_percent: float = Field(..., description="Price change percentage")
    volume: int = Field(..., description="Trading volume")
    timestamp: datetime = Field(..., description="Data timestamp")

class MarketDataResponse(BaseModel):
    """Response model for market data"""
    data: Dict[str, MarketDataPoint] = Field(..., description="Market data by symbol")
    timestamp: datetime = Field(..., description="Data timestamp")
    symbols: List[str] = Field(..., description="Requested symbols")

class AIRecommendation(BaseModel):
    """Model for AI trading recommendation"""
    action: TradeAction = Field(..., description="Recommended action")
    symbol: str = Field(..., description="Stock ticker symbol")
    confidence: float = Field(..., description="Confidence score (0-1)", ge=0, le=1)
    reasoning: str = Field(..., description="Reasoning for recommendation")
    target_price: Optional[float] = Field(None, description="Target price")
    stop_loss: Optional[float] = Field(None, description="Recommended stop loss")
    position_size: Optional[float] = Field(None, description="Recommended position size")

class AIAnalysisResponse(BaseModel):
    """Response model for AI analysis"""
    recommendations: List[AIRecommendation] = Field(..., description="AI recommendations")
    provider: str = Field(..., description="AI provider used")
    timestamp: datetime = Field(..., description="Analysis timestamp")
    confidence_score: float = Field(..., description="Overall confidence", ge=0, le=1)
    market_context: Optional[Dict[str, Any]] = Field(None, description="Market context data")

class NewsItem(BaseModel):
    """Model for news item"""
    title: str = Field(..., description="News headline")
    summary: Optional[str] = Field(None, description="News summary")
    url: Optional[str] = Field(None, description="News article URL")
    source: str = Field(..., description="News source")
    timestamp: datetime = Field(..., description="Publication timestamp")
    sentiment: Optional[str] = Field(None, description="Sentiment analysis")
    relevance_score: Optional[float] = Field(None, description="Relevance score", ge=0, le=1)

class NotificationResponse(BaseModel):
    """Response model for notifications"""
    notification_id: str = Field(..., description="Unique notification identifier")
    message: str = Field(..., description="Notification message")
    channels: List[NotificationChannel] = Field(..., description="Target channels")
    status: str = Field(..., description="Delivery status")
    timestamp: datetime = Field(..., description="Notification timestamp")
    delivered_to: List[str] = Field(..., description="Successfully delivered channels")
    failed_channels: List[str] = Field(default_factory=list, description="Failed delivery channels")

class HealthResponse(BaseModel):
    """Response model for health checks"""
    status: str = Field(..., description="Overall health status")
    timestamp: datetime = Field(..., description="Health check timestamp")
    services: Dict[str, bool] = Field(..., description="Individual service health")
    uptime: Optional[float] = Field(None, description="Uptime in seconds")
    version: Optional[str] = Field(None, description="API version")

class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error message")
    error_code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(..., description="Error timestamp")
    path: Optional[str] = Field(None, description="Request path")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")

# Webhook-specific models
class TradingSignal(BaseModel):
    """Model for trading signals from n8n"""
    symbol: str = Field(..., description="Stock ticker symbol")
    action: TradeAction = Field(..., description="Recommended action")
    confidence: float = Field(..., description="Signal confidence", ge=0, le=1)
    source: str = Field(..., description="Signal source")
    reasoning: Optional[str] = Field(None, description="Signal reasoning")
    target_price: Optional[float] = Field(None, description="Target price")
    stop_loss: Optional[float] = Field(None, description="Stop loss price")
    
    @validator('symbol')
    def symbol_must_be_uppercase(cls, v):
        return v.upper().strip()

class PortfolioAlert(BaseModel):
    """Model for portfolio alerts"""
    alert_type: str = Field(..., description="Type of alert")
    message: str = Field(..., description="Alert message")
    severity: int = Field(..., description="Alert severity (1-5)", ge=1, le=5)
    affected_positions: Optional[List[str]] = Field(None, description="Affected stock symbols")
    threshold_value: Optional[float] = Field(None, description="Threshold that triggered alert")
    current_value: Optional[float] = Field(None, description="Current value")

class MarketUpdate(BaseModel):
    """Model for market updates"""
    update_type: str = Field(..., description="Type of market update")
    symbols: List[str] = Field(..., description="Affected symbols")
    data: Dict[str, Any] = Field(..., description="Update data")
    impact_level: int = Field(..., description="Impact level (1-5)", ge=1, le=5)
    
    @validator('symbols')
    def symbols_must_be_uppercase(cls, v):
        return [symbol.upper().strip() for symbol in v]

# Configuration models
class APIConfiguration(BaseModel):
    """Model for API configuration"""
    rate_limit: int = Field(100, description="Requests per minute")
    timeout: int = Field(30, description="Request timeout in seconds")
    max_workers: int = Field(4, description="Maximum worker processes")
    debug: bool = Field(False, description="Debug mode enabled")
    log_level: str = Field("INFO", description="Logging level")

class WebhookConfiguration(BaseModel):
    """Model for webhook configuration"""
    url: str = Field(..., description="Webhook URL")
    events: List[EventType] = Field(..., description="Subscribed events")
    secret: Optional[str] = Field(None, description="Webhook secret")
    enabled: bool = Field(True, description="Webhook enabled")
    retry_count: int = Field(3, description="Retry attempts on failure")
    timeout: int = Field(10, description="Webhook timeout in seconds")

# Batch operation models
class BatchTradeRequest(BaseModel):
    """Model for batch trade operations"""
    trades: List[TradeRequest] = Field(..., description="List of trade requests")
    execute_all_or_none: bool = Field(False, description="Execute all trades or none")
    dry_run: bool = Field(False, description="Perform dry run without execution")

class BatchTradeResponse(BaseModel):
    """Response model for batch trade operations"""
    batch_id: str = Field(..., description="Batch operation identifier")
    total_trades: int = Field(..., description="Total number of trades")
    successful_trades: int = Field(..., description="Successfully executed trades")
    failed_trades: int = Field(..., description="Failed trade executions")
    results: List[TradeResponse] = Field(..., description="Individual trade results")
    timestamp: datetime = Field(..., description="Batch execution timestamp")

# Statistics and analytics models
class TradingStatistics(BaseModel):
    """Model for trading statistics"""
    total_trades: int = Field(..., description="Total number of trades")
    winning_trades: int = Field(..., description="Number of winning trades")
    losing_trades: int = Field(..., description="Number of losing trades")
    average_win: float = Field(..., description="Average winning trade amount")
    average_loss: float = Field(..., description="Average losing trade amount")
    largest_win: float = Field(..., description="Largest winning trade")
    largest_loss: float = Field(..., description="Largest losing trade")
    win_rate: float = Field(..., description="Win rate percentage")
    profit_factor: float = Field(..., description="Profit factor")

class RiskMetrics(BaseModel):
    """Model for risk metrics"""
    portfolio_beta: float = Field(..., description="Portfolio beta")
    value_at_risk: float = Field(..., description="Value at Risk (VaR)")
    expected_shortfall: float = Field(..., description="Expected Shortfall")
    maximum_drawdown: float = Field(..., description="Maximum drawdown")
    sharpe_ratio: float = Field(..., description="Sharpe ratio")
    sortino_ratio: float = Field(..., description="Sortino ratio")
    correlation_matrix: Optional[Dict[str, Dict[str, float]]] = Field(None, description="Asset correlation matrix")