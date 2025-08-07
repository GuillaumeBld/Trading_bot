#!/usr/bin/env python3
"""
Webhook Integration Examples for n8n

This file contains examples of how to integrate the trading bot
with n8n workflows using webhooks and HTTP requests.
"""

import requests
import json
import hmac
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import aiohttp

# Configuration
N8N_WEBHOOK_BASE = "http://localhost:5678/webhook"
API_BASE = "http://localhost:8000/api"
WEBHOOK_SECRET = "your-webhook-secret"
API_KEY = "your-api-key"

class TradingBotWebhookClient:
    """Client for sending webhooks to n8n from the trading bot"""
    
    def __init__(self, webhook_base: str, secret: str):
        self.webhook_base = webhook_base
        self.secret = secret
    
    def _create_signature(self, payload: str) -> str:
        """Create webhook signature for security"""
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def send_trade_executed(self, trade_data: Dict[str, Any]) -> requests.Response:
        """Send trade execution notification to n8n"""
        webhook_url = f"{self.webhook_base}/trading-bot-alerts"
        
        payload = {
            "event_type": "trade_executed",
            "timestamp": datetime.now().isoformat(),
            "source": "trading_bot",
            "data": trade_data
        }
        
        payload_json = json.dumps(payload)
        signature = self._create_signature(payload_json)
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": f"sha256={signature}",
            "User-Agent": "TradingBot/1.0"
        }
        
        return requests.post(webhook_url, data=payload_json, headers=headers)
    
    def send_portfolio_alert(self, alert_data: Dict[str, Any]) -> requests.Response:
        """Send portfolio alert to n8n"""
        webhook_url = f"{self.webhook_base}/trading-bot-alerts"
        
        payload = {
            "event_type": "portfolio_alert",
            "timestamp": datetime.now().isoformat(),
            "source": "trading_bot",
            "data": alert_data
        }
        
        payload_json = json.dumps(payload)
        signature = self._create_signature(payload_json)
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": f"sha256={signature}"
        }
        
        return requests.post(webhook_url, data=payload_json, headers=headers)
    
    def send_market_update(self, market_data: Dict[str, Any]) -> requests.Response:
        """Send market update to n8n"""
        webhook_url = f"{self.webhook_base}/market-updates"
        
        payload = {
            "event_type": "market_update",
            "timestamp": datetime.now().isoformat(),
            "source": "market_service",
            "data": market_data
        }
        
        payload_json = json.dumps(payload)
        signature = self._create_signature(payload_json)
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": f"sha256={signature}"
        }
        
        return requests.post(webhook_url, data=payload_json, headers=headers)

class N8NTradingClient:
    """Client for n8n to interact with trading bot API"""
    
    def __init__(self, api_base: str, api_key: str):
        self.api_base = api_base
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_portfolio(self) -> Dict[str, Any]:
        """Get current portfolio information"""
        response = requests.get(f"{self.api_base}/portfolio", headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def execute_trade(self, symbol: str, action: str, shares: float, price: Optional[float] = None) -> Dict[str, Any]:
        """Execute a trade"""
        endpoint = f"{self.api_base}/trade/{action}"
        
        payload = {
            "symbol": symbol,
            "shares": shares,
            "action": action
        }
        
        if price:
            payload["price"] = price
        
        response = requests.post(endpoint, json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_ai_analysis(self, symbols: Optional[list] = None, provider: str = "openai") -> Dict[str, Any]:
        """Get AI trading analysis"""
        payload = {
            "provider": provider,
            "include_market_data": True,
            "include_news": True
        }
        
        if symbols:
            payload["symbols"] = symbols
        
        response = requests.post(f"{self.api_base}/ai/analyze", json=payload, headers=self.headers)
        response.raise_for_status()
        return response.json()
    
    def get_market_data(self, symbols: str = "SPY,QQQ,IWM") -> Dict[str, Any]:
        """Get current market data"""
        params = {"symbols": symbols}
        response = requests.get(f"{self.api_base}/market/data", params=params, headers=self.headers)
        response.raise_for_status()
        return response.json()

# Example Usage Functions

def example_trade_notification():
    """Example: Send trade execution notification to n8n"""
    webhook_client = TradingBotWebhookClient(N8N_WEBHOOK_BASE, WEBHOOK_SECRET)
    
    trade_data = {
        "symbol": "AAPL",
        "action": "buy",
        "shares": 10,
        "price": 150.25,
        "total_cost": 1502.50,
        "reasoning": "AI analysis suggests strong upward momentum",
        "confidence": 0.85,
        "trade_id": "trade_123456"
    }
    
    try:
        response = webhook_client.send_trade_executed(trade_data)
        print(f"Trade notification sent: {response.status_code}")
        if response.status_code != 200:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Failed to send trade notification: {e}")

def example_portfolio_alert():
    """Example: Send portfolio alert to n8n"""
    webhook_client = TradingBotWebhookClient(N8N_WEBHOOK_BASE, WEBHOOK_SECRET)
    
    alert_data = {
        "alert_type": "drawdown_warning",
        "message": "Portfolio drawdown exceeds 10% threshold",
        "severity": 3,
        "current_drawdown": 12.5,
        "threshold": 10.0,
        "affected_positions": ["AAPL", "GOOGL", "TSLA"],
        "recommended_action": "Consider reducing position sizes"
    }
    
    try:
        response = webhook_client.send_portfolio_alert(alert_data)
        print(f"Portfolio alert sent: {response.status_code}")
    except Exception as e:
        print(f"Failed to send portfolio alert: {e}")

def example_market_update():
    """Example: Send market update to n8n"""
    webhook_client = TradingBotWebhookClient(N8N_WEBHOOK_BASE, WEBHOOK_SECRET)
    
    market_data = {
        "update_type": "volatility_spike",
        "symbols": ["SPY", "QQQ", "VIX"],
        "data": {
            "SPY": {"price": 420.50, "change_percent": -2.5},
            "QQQ": {"price": 350.25, "change_percent": -3.1},
            "VIX": {"price": 25.80, "change_percent": 15.2}
        },
        "impact_level": 4,
        "message": "High volatility detected across major indices"
    }
    
    try:
        response = webhook_client.send_market_update(market_data)
        print(f"Market update sent: {response.status_code}")
    except Exception as e:
        print(f"Failed to send market update: {e}")

def example_n8n_trade_execution():
    """Example: n8n executes a trade via API"""
    trading_client = N8NTradingClient(API_BASE, API_KEY)
    
    try:
        # Get AI analysis first
        analysis = trading_client.get_ai_analysis(symbols=["AAPL", "GOOGL"])
        print(f"AI Analysis: {analysis}")
        
        # Execute trade based on analysis
        if analysis.get("recommendations"):
            recommendation = analysis["recommendations"][0]
            if recommendation["confidence"] > 0.7:
                trade_result = trading_client.execute_trade(
                    symbol=recommendation["symbol"],
                    action=recommendation["action"],
                    shares=10,
                    price=recommendation.get("target_price")
                )
                print(f"Trade executed: {trade_result}")
        
    except Exception as e:
        print(f"Failed to execute trade: {e}")

def example_portfolio_monitoring():
    """Example: n8n monitors portfolio and triggers alerts"""
    trading_client = N8NTradingClient(API_BASE, API_KEY)
    webhook_client = TradingBotWebhookClient(N8N_WEBHOOK_BASE, WEBHOOK_SECRET)
    
    try:
        # Get current portfolio
        portfolio = trading_client.get_portfolio()
        
        # Check for alert conditions
        total_value = portfolio.get("total_value", 0)
        performance_metrics = portfolio.get("performance_metrics", {})
        max_drawdown = performance_metrics.get("max_drawdown", 0)
        
        # Trigger alert if drawdown exceeds threshold
        if abs(max_drawdown) > 0.15:  # 15% drawdown threshold
            alert_data = {
                "alert_type": "excessive_drawdown",
                "message": f"Portfolio drawdown of {abs(max_drawdown)*100:.1f}% exceeds 15% threshold",
                "severity": 4,
                "current_value": total_value,
                "max_drawdown": max_drawdown,
                "recommended_action": "Consider risk reduction measures"
            }
            
            response = webhook_client.send_portfolio_alert(alert_data)
            print(f"Alert triggered: {response.status_code}")
        
    except Exception as e:
        print(f"Portfolio monitoring failed: {e}")

# Async Examples for High-Performance Applications

async def async_webhook_example():
    """Example: Async webhook sending for high throughput"""
    async with aiohttp.ClientSession() as session:
        webhook_url = f"{N8N_WEBHOOK_BASE}/trading-bot-alerts"
        
        payload = {
            "event_type": "trade_executed",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "symbol": "MSFT",
                "action": "sell",
                "shares": 5,
                "price": 300.00
            }
        }
        
        payload_json = json.dumps(payload)
        signature = hmac.new(
            WEBHOOK_SECRET.encode(),
            payload_json.encode(),
            hashlib.sha256
        ).hexdigest()
        
        headers = {
            "Content-Type": "application/json",
            "X-Webhook-Signature": f"sha256={signature}"
        }
        
        try:
            async with session.post(webhook_url, data=payload_json, headers=headers) as response:
                print(f"Async webhook sent: {response.status}")
                result = await response.text()
                print(f"Response: {result}")
        except Exception as e:
            print(f"Async webhook failed: {e}")

async def async_api_example():
    """Example: Async API calls for better performance"""
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }
        
        try:
            # Get portfolio and market data concurrently
            portfolio_task = session.get(f"{API_BASE}/portfolio", headers=headers)
            market_task = session.get(f"{API_BASE}/market/data", headers=headers)
            
            portfolio_response, market_response = await asyncio.gather(
                portfolio_task, market_task, return_exceptions=True
            )
            
            if isinstance(portfolio_response, aiohttp.ClientResponse):
                portfolio_data = await portfolio_response.json()
                print(f"Portfolio: {portfolio_data}")
            
            if isinstance(market_response, aiohttp.ClientResponse):
                market_data = await market_response.json()
                print(f"Market: {market_data}")
                
        except Exception as e:
            print(f"Async API calls failed: {e}")

# Batch Operations Example

def example_batch_operations():
    """Example: Batch multiple operations for efficiency"""
    trading_client = N8NTradingClient(API_BASE, API_KEY)
    webhook_client = TradingBotWebhookClient(N8N_WEBHOOK_BASE, WEBHOOK_SECRET)
    
    # Batch trade executions
    trades = [
        {"symbol": "AAPL", "action": "buy", "shares": 5},
        {"symbol": "GOOGL", "action": "buy", "shares": 2},
        {"symbol": "MSFT", "action": "sell", "shares": 3}
    ]
    
    trade_results = []
    for trade in trades:
        try:
            result = trading_client.execute_trade(**trade)
            trade_results.append(result)
            
            # Send notification for each trade
            webhook_client.send_trade_executed({
                "symbol": trade["symbol"],
                "action": trade["action"],
                "shares": trade["shares"],
                "status": "executed",
                "trade_id": result.get("trade_id")
            })
            
        except Exception as e:
            print(f"Trade failed: {trade}, Error: {e}")
    
    print(f"Batch trades completed: {len(trade_results)} successful")

# Error Handling and Retry Logic

def robust_webhook_send(webhook_client: TradingBotWebhookClient, data: Dict[str, Any], max_retries: int = 3):
    """Send webhook with retry logic"""
    for attempt in range(max_retries):
        try:
            response = webhook_client.send_trade_executed(data)
            if response.status_code == 200:
                return response
            else:
                print(f"Webhook attempt {attempt + 1} failed: {response.status_code}")
        except Exception as e:
            print(f"Webhook attempt {attempt + 1} error: {e}")
        
        if attempt < max_retries - 1:
            import time
            time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception(f"Failed to send webhook after {max_retries} attempts")

# Main execution examples
if __name__ == "__main__":
    print(" Trading Bot n8n Integration Examples")
    print("=" * 50)
    
    # Synchronous examples
    print("\n Sending trade notification...")
    example_trade_notification()
    
    print("\n Sending portfolio alert...")
    example_portfolio_alert()
    
    print("\n Sending market update...")
    example_market_update()
    
    print("\n n8n executing trade...")
    example_n8n_trade_execution()
    
    print("\n Portfolio monitoring...")
    example_portfolio_monitoring()
    
    print("\n Batch operations...")
    example_batch_operations()
    
    # Asynchronous examples
    print("\n Async webhook example...")
    asyncio.run(async_webhook_example())
    
    print("\n Async API example...")
    asyncio.run(async_api_example())
    
    print("\n All examples completed!")