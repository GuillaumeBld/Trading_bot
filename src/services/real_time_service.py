#!/usr/bin/env python3
"""
Real-Time Data Service

Provides real-time data feeds for the dynamic dashboard:
- WebSocket connections for live updates
- Background data processing
- Event-driven notifications
- Data streaming capabilities
- Cache management with TTL
"""

import asyncio
import websockets
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
import logging
from dataclasses import dataclass, asdict
from enum import Enum
import queue
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor
import pandas as pd

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EventType(Enum):
    """Types of real-time events"""
    PORTFOLIO_UPDATE = "portfolio_update"
    MARKET_DATA = "market_data"
    TRADE_EXECUTED = "trade_executed"
    PRICE_ALERT = "price_alert"
    NEWS_UPDATE = "news_update"
    SYSTEM_STATUS = "system_status"
    ERROR = "error"

@dataclass
class RealTimeEvent:
    """Real-time event data structure"""
    event_type: EventType
    timestamp: datetime
    data: Dict[str, Any]
    source: str = "system"
    priority: int = 1  # 1=low, 2=medium, 3=high

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        result['event_type'] = self.event_type.value
        return result

class RealTimeDataService:
    """Main real-time data service"""
    
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
        self.event_queue = queue.Queue()
        self.running = False
        self.websocket_server = None
        self.connected_clients = set()
        self.data_cache: Dict[str, Any] = {}
        self.cache_ttl: Dict[str, datetime] = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.background_tasks = []
        
    async def start_websocket_server(self, host: str = "localhost", port: int = 8765):
        """Start WebSocket server for real-time communication"""
        try:
            self.websocket_server = await websockets.serve(
                self.handle_websocket_connection,
                host,
                port
            )
            logger.info(f"WebSocket server started on ws://{host}:{port}")
        except Exception as e:
            logger.error(f"Failed to start WebSocket server: {e}")
    
    async def handle_websocket_connection(self, websocket, path):
        """Handle new WebSocket connections"""
        self.connected_clients.add(websocket)
        logger.info(f"New WebSocket client connected: {websocket.remote_address}")
        
        try:
            # Send initial data
            await self.send_initial_data(websocket)
            
            # Keep connection alive and handle messages
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_client_message(websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({
                        "error": "Invalid JSON format"
                    }))
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"WebSocket client disconnected: {websocket.remote_address}")
        finally:
            self.connected_clients.discard(websocket)
    
    async def send_initial_data(self, websocket):
        """Send initial data to newly connected client"""
        initial_data = {
            "type": "initial_data",
            "timestamp": datetime.now().isoformat(),
            "data": {
                "portfolio": self.get_cached_data("portfolio"),
                "market_data": self.get_cached_data("market_data"),
                "system_status": "online"
            }
        }
        await websocket.send(json.dumps(initial_data))
    
    async def handle_client_message(self, websocket, data: Dict[str, Any]):
        """Handle messages from WebSocket clients"""
        message_type = data.get("type")
        
        if message_type == "subscribe":
            # Handle subscription requests
            events = data.get("events", [])
            client_id = data.get("client_id", str(websocket.remote_address))
            
            for event in events:
                self.subscribe(event, lambda event_data: 
                              asyncio.create_task(websocket.send(json.dumps(event_data))))
            
            await websocket.send(json.dumps({
                "type": "subscription_confirmed",
                "events": events
            }))
        
        elif message_type == "request_data":
            # Handle data requests
            data_type = data.get("data_type")
            cached_data = self.get_cached_data(data_type)
            
            await websocket.send(json.dumps({
                "type": "data_response",
                "data_type": data_type,
                "data": cached_data,
                "timestamp": datetime.now().isoformat()
            }))
    
    def subscribe(self, event_type: str, callback: Callable):
        """Subscribe to real-time events"""
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Unsubscribe from real-time events"""
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(callback)
    
    def emit_event(self, event: RealTimeEvent):
        """Emit event to all subscribers"""
        self.event_queue.put(event)
        
        # Notify WebSocket clients
        if self.connected_clients:
            event_data = event.to_dict()
            asyncio.create_task(self.broadcast_to_websockets(event_data))
        
        # Notify local subscribers
        event_type_str = event.event_type.value
        if event_type_str in self.subscribers:
            for callback in self.subscribers[event_type_str]:
                try:
                    callback(event.to_dict())
                except Exception as e:
                    logger.error(f"Error in event callback: {e}")
    
    async def broadcast_to_websockets(self, data: Dict[str, Any]):
        """Broadcast data to all connected WebSocket clients"""
        if self.connected_clients:
            message = json.dumps(data)
            disconnected = []
            
            for client in self.connected_clients:
                try:
                    await client.send(message)
                except websockets.exceptions.ConnectionClosed:
                    disconnected.append(client)
                except Exception as e:
                    logger.error(f"Error broadcasting to client: {e}")
                    disconnected.append(client)
            
            # Remove disconnected clients
            for client in disconnected:
                self.connected_clients.discard(client)
    
    def set_cached_data(self, key: str, data: Any, ttl_seconds: int = 30):
        """Set cached data with TTL"""
        self.data_cache[key] = data
        self.cache_ttl[key] = datetime.now() + timedelta(seconds=ttl_seconds)
    
    def get_cached_data(self, key: str) -> Optional[Any]:
        """Get cached data if not expired"""
        if key in self.data_cache and key in self.cache_ttl:
            if datetime.now() < self.cache_ttl[key]:
                return self.data_cache[key]
            else:
                # Expired, remove from cache
                del self.data_cache[key]
                del self.cache_ttl[key]
        return None
    
    def start_background_tasks(self):
        """Start background data collection tasks"""
        self.running = True
        
        # Start market data collection
        market_task = threading.Thread(target=self._market_data_collector, daemon=True)
        market_task.start()
        self.background_tasks.append(market_task)
        
        # Start portfolio monitoring
        portfolio_task = threading.Thread(target=self._portfolio_monitor, daemon=True)
        portfolio_task.start()
        self.background_tasks.append(portfolio_task)
        
        # Start event processor
        event_task = threading.Thread(target=self._event_processor, daemon=True)
        event_task.start()
        self.background_tasks.append(event_task)
        
        logger.info("Background tasks started")
    
    def stop_background_tasks(self):
        """Stop all background tasks"""
        self.running = False
        logger.info("Background tasks stopped")
    
    def _market_data_collector(self):
        """Background task to collect market data"""
        symbols = ['SPY', 'QQQ', 'IWM', 'VIX', 'AAPL', 'MSFT', 'GOOGL']
        
        while self.running:
            try:
                market_data = {}
                
                # Use ThreadPoolExecutor for parallel data fetching
                future_to_symbol = {
                    self.executor.submit(self._fetch_symbol_data, symbol): symbol 
                    for symbol in symbols
                }
                
                for future in future_to_symbol:
                    symbol = future_to_symbol[future]
                    try:
                        data = future.result(timeout=10)
                        if data:
                            market_data[symbol] = data
                    except Exception as e:
                        logger.error(f"Error fetching data for {symbol}: {e}")
                
                if market_data:
                    self.set_cached_data("market_data", market_data, ttl_seconds=60)
                    
                    # Emit market data event
                    event = RealTimeEvent(
                        event_type=EventType.MARKET_DATA,
                        timestamp=datetime.now(),
                        data=market_data,
                        source="market_collector"
                    )
                    self.emit_event(event)
                
                time.sleep(30)  # Update every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in market data collector: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _fetch_symbol_data(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch data for a single symbol"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d", interval="1m")
            
            if not hist.empty:
                current_price = hist['Close'].iloc[-1]
                prev_close = info.get('previousClose', current_price)
                change = current_price - prev_close
                change_percent = (change / prev_close) * 100 if prev_close != 0 else 0
                
                return {
                    'symbol': symbol,
                    'price': float(current_price),
                    'change': float(change),
                    'change_percent': float(change_percent),
                    'volume': int(hist['Volume'].iloc[-1]) if 'Volume' in hist.columns else 0,
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {e}")
        
        return None
    
    def _portfolio_monitor(self):
        """Background task to monitor portfolio changes"""
        last_portfolio_hash = None
        
        while self.running:
            try:
                # Load current portfolio data
                from core.trading_script import load_portfolio_data
                portfolio_data = load_portfolio_data()
                
                if portfolio_data is not None:
                    # Create hash to detect changes
                    portfolio_hash = hash(str(portfolio_data.to_dict()))
                    
                    if portfolio_hash != last_portfolio_hash:
                        self.set_cached_data("portfolio", portfolio_data.to_dict(), ttl_seconds=120)
                        
                        # Emit portfolio update event
                        event = RealTimeEvent(
                            event_type=EventType.PORTFOLIO_UPDATE,
                            timestamp=datetime.now(),
                            data={
                                'portfolio': portfolio_data.to_dict(),
                                'total_value': float(portfolio_data['current_value'].sum()) if 'current_value' in portfolio_data.columns else 0
                            },
                            source="portfolio_monitor"
                        )
                        self.emit_event(event)
                        
                        last_portfolio_hash = portfolio_hash
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logger.error(f"Error in portfolio monitor: {e}")
                time.sleep(30)  # Wait longer on error
    
    def _event_processor(self):
        """Background task to process events"""
        while self.running:
            try:
                # Process events from queue
                while not self.event_queue.empty():
                    event = self.event_queue.get_nowait()
                    
                    # Log high priority events
                    if event.priority >= 2:
                        logger.info(f"High priority event: {event.event_type.value}")
                    
                    # Additional event processing can be added here
                    # (e.g., persistence, alerts, notifications)
                
                time.sleep(1)  # Process events every second
                
            except Exception as e:
                logger.error(f"Error in event processor: {e}")
                time.sleep(5)
    
    def trigger_price_alert(self, symbol: str, current_price: float, alert_price: float, condition: str):
        """Trigger a price alert event"""
        event = RealTimeEvent(
            event_type=EventType.PRICE_ALERT,
            timestamp=datetime.now(),
            data={
                'symbol': symbol,
                'current_price': current_price,
                'alert_price': alert_price,
                'condition': condition,
                'message': f"{symbol} price {condition} ${alert_price:.2f} (Current: ${current_price:.2f})"
            },
            source="price_monitor",
            priority=3  # High priority
        )
        self.emit_event(event)
    
    def trigger_trade_event(self, trade_data: Dict[str, Any]):
        """Trigger a trade execution event"""
        event = RealTimeEvent(
            event_type=EventType.TRADE_EXECUTED,
            timestamp=datetime.now(),
            data=trade_data,
            source="trading_engine",
            priority=2  # Medium priority
        )
        self.emit_event(event)

# Global service instance
_real_time_service: Optional[RealTimeDataService] = None

def get_real_time_service() -> RealTimeDataService:
    """Get or create the global real-time service instance"""
    global _real_time_service
    if _real_time_service is None:
        _real_time_service = RealTimeDataService()
    return _real_time_service

def start_real_time_service():
    """Start the real-time service with all background tasks"""
    service = get_real_time_service()
    service.start_background_tasks()
    return service

def stop_real_time_service():
    """Stop the real-time service"""
    global _real_time_service
    if _real_time_service:
        _real_time_service.stop_background_tasks()

# Context manager for easy service management
class RealTimeServiceContext:
    """Context manager for real-time service"""
    
    def __enter__(self):
        return start_real_time_service()
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        stop_real_time_service()

if __name__ == "__main__":
    # Example usage
    async def main():
        service = start_real_time_service()
        
        # Start WebSocket server
        await service.start_websocket_server()
        
        # Subscribe to events
        def handle_market_data(event_data):
            print(f"Market update: {event_data}")
        
        service.subscribe("market_data", handle_market_data)
        
        # Keep running
        try:
            await asyncio.Future()  # Run forever
        except KeyboardInterrupt:
            print("Shutting down...")
        finally:
            service.stop_background_tasks()
    
    asyncio.run(main())