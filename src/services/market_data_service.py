#!/usr/bin/env python3
"""
Market Data Service

Provides comprehensive market data including:
- Real-time stock prices
- Historical data
- Market indices
- News feeds
- Economic indicators
- Sentiment analysis
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import requests
import json
import streamlit as st
from dataclasses import dataclass
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

@dataclass
class StockData:
    """Stock data container"""
    symbol: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    market_cap: Optional[float] = None
    pe_ratio: Optional[float] = None
    day_high: Optional[float] = None
    day_low: Optional[float] = None
    fifty_two_week_high: Optional[float] = None
    fifty_two_week_low: Optional[float] = None

@dataclass
class NewsItem:
    """News item container"""
    title: str
    summary: str
    source: str
    published_at: datetime
    url: str
    sentiment: str = "neutral"
    relevance_score: float = 0.5
    symbols: List[str] = None

@dataclass
class MarketIndex:
    """Market index data"""
    name: str
    symbol: str
    value: float
    change: float
    change_percent: float

class MarketDataService:
    """Comprehensive market data service"""
    
    def __init__(self, news_api_key: Optional[str] = None):
        self.news_api_key = news_api_key
        self.cache = {}
        self.cache_expiry = {}
        self.cache_duration = 300  # 5 minutes default
        
        # Market indices to track
        self.indices = {
            "S&P 500": "^GSPC",
            "NASDAQ": "^IXIC", 
            "Dow Jones": "^DJI",
            "Russell 2000": "^RUT",
            "VIX": "^VIX",
            "10-Year Treasury": "^TNX"
        }
    
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cached data is still valid"""
        if key not in self.cache:
            return False
        if key not in self.cache_expiry:
            return False
        return datetime.now() < self.cache_expiry[key]
    
    def _set_cache(self, key: str, data: Any, duration: int = None):
        """Set cache with expiry"""
        duration = duration or self.cache_duration
        self.cache[key] = data
        self.cache_expiry[key] = datetime.now() + timedelta(seconds=duration)
    
    def _get_cache(self, key: str) -> Optional[Any]:
        """Get cached data if valid"""
        if self._is_cache_valid(key):
            return self.cache[key]
        return None
    
    def get_stock_data(self, symbol: str) -> Optional[StockData]:
        """Get comprehensive stock data"""
        cache_key = f"stock_{symbol}"
        cached_data = self._get_cache(cache_key)
        if cached_data:
            return cached_data
        
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if hist.empty:
                return None
            
            current_price = hist['Close'].iloc[-1]
            prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
            change = current_price - prev_price
            change_percent = (change / prev_price) * 100 if prev_price != 0 else 0
            
            stock_data = StockData(
                symbol=symbol,
                current_price=current_price,
                change=change,
                change_percent=change_percent,
                volume=int(hist['Volume'].iloc[-1]) if not pd.isna(hist['Volume'].iloc[-1]) else 0,
                market_cap=info.get('marketCap'),
                pe_ratio=info.get('trailingPE'),
                day_high=hist['High'].iloc[-1],
                day_low=hist['Low'].iloc[-1],
                fifty_two_week_high=info.get('fiftyTwoWeekHigh'),
                fifty_two_week_low=info.get('fiftyTwoWeekLow')
            )
            
            self._set_cache(cache_key, stock_data)
            return stock_data
            
        except Exception as e:
            st.error(f"Error fetching data for {symbol}: {e}")
            return None
    
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, StockData]:
        """Get data for multiple stocks efficiently"""
        result = {}
        
        # Check cache first
        uncached_symbols = []
        for symbol in symbols:
            cached_data = self._get_cache(f"stock_{symbol}")
            if cached_data:
                result[symbol] = cached_data
            else:
                uncached_symbols.append(symbol)
        
        if not uncached_symbols:
            return result
        
        # Fetch uncached symbols in parallel
        with ThreadPoolExecutor(max_workers=5) as executor:
            future_to_symbol = {
                executor.submit(self.get_stock_data, symbol): symbol 
                for symbol in uncached_symbols
            }
            
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    stock_data = future.result()
                    if stock_data:
                        result[symbol] = stock_data
                except Exception as e:
                    st.error(f"Error fetching {symbol}: {e}")
        
        return result
    
    def get_market_indices(self) -> List[MarketIndex]:
        """Get current market indices"""
        cache_key = "market_indices"
        cached_data = self._get_cache(cache_key)
        if cached_data:
            return cached_data
        
        indices_data = []
        
        for name, symbol in self.indices.items():
            try:
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current_value = hist['Close'].iloc[-1]
                    prev_value = hist['Close'].iloc[-2] if len(hist) > 1 else current_value
                    change = current_value - prev_value
                    change_percent = (change / prev_value) * 100 if prev_value != 0 else 0
                    
                    indices_data.append(MarketIndex(
                        name=name,
                        symbol=symbol,
                        value=current_value,
                        change=change,
                        change_percent=change_percent
                    ))
            except Exception as e:
                st.error(f"Error fetching {name}: {e}")
        
        self._set_cache(cache_key, indices_data)
        return indices_data
    
    def get_historical_data(self, symbol: str, period: str = "1y") -> pd.DataFrame:
        """Get historical price data"""
        cache_key = f"hist_{symbol}_{period}"
        cached_data = self._get_cache(cache_key)
        if cached_data is not None:
            return cached_data
        
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            # Cache for longer period for historical data
            self._set_cache(cache_key, hist, duration=3600)  # 1 hour
            return hist
            
        except Exception as e:
            st.error(f"Error fetching historical data for {symbol}: {e}")
            return pd.DataFrame()
    
    def get_portfolio_correlation(self, symbols: List[str], period: str = "6mo") -> pd.DataFrame:
        """Calculate correlation matrix for portfolio stocks"""
        try:
            # Get historical data for all symbols
            price_data = {}
            for symbol in symbols:
                hist = self.get_historical_data(symbol, period)
                if not hist.empty:
                    price_data[symbol] = hist['Close']
            
            if not price_data:
                return pd.DataFrame()
            
            # Create DataFrame with all price series
            df = pd.DataFrame(price_data)
            
            # Calculate daily returns
            returns = df.pct_change().dropna()
            
            # Calculate correlation matrix
            correlation_matrix = returns.corr()
            
            return correlation_matrix
            
        except Exception as e:
            st.error(f"Error calculating portfolio correlation: {e}")
            return pd.DataFrame()
    
    def get_sector_performance(self) -> Dict[str, float]:
        """Get sector ETF performance"""
        sector_etfs = {
            "Technology": "XLK",
            "Healthcare": "XLV", 
            "Financials": "XLF",
            "Consumer Discretionary": "XLY",
            "Communication": "XLC",
            "Industrials": "XLI",
            "Consumer Staples": "XLP",
            "Energy": "XLE",
            "Utilities": "XLU",
            "Real Estate": "XLRE",
            "Materials": "XLB"
        }
        
        cache_key = "sector_performance"
        cached_data = self._get_cache(cache_key)
        if cached_data:
            return cached_data
        
        sector_performance = {}
        
        for sector, etf in sector_etfs.items():
            try:
                ticker = yf.Ticker(etf)
                hist = ticker.history(period="2d")
                
                if not hist.empty:
                    current = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
                    change_pct = ((current - prev) / prev) * 100 if prev != 0 else 0
                    sector_performance[sector] = change_pct
                    
            except Exception as e:
                st.error(f"Error fetching {sector} performance: {e}")
        
        self._set_cache(cache_key, sector_performance)
        return sector_performance
    
    def get_market_news(self, query: str = "stock market", limit: int = 10) -> List[NewsItem]:
        """Get market news from various sources"""
        if not self.news_api_key:
            return self._get_mock_news()
        
        cache_key = f"news_{query}_{limit}"
        cached_data = self._get_cache(cache_key)
        if cached_data:
            return cached_data
        
        try:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": query,
                "apiKey": self.news_api_key,
                "language": "en",
                "sortBy": "publishedAt",
                "pageSize": limit,
                "sources": "bloomberg,reuters,cnbc,marketwatch,yahoo-finance"
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            news_items = []
            
            for article in data.get("articles", []):
                if article.get("title") and article.get("publishedAt"):
                    news_items.append(NewsItem(
                        title=article["title"],
                        summary=article.get("description", "")[:200] + "...",
                        source=article.get("source", {}).get("name", "Unknown"),
                        published_at=datetime.fromisoformat(
                            article["publishedAt"].replace("Z", "+00:00")
                        ),
                        url=article.get("url", ""),
                        sentiment=self._analyze_sentiment(article["title"])
                    ))
            
            self._set_cache(cache_key, news_items, duration=1800)  # 30 minutes
            return news_items
            
        except Exception as e:
            st.error(f"Error fetching news: {e}")
            return self._get_mock_news()
    
    def _analyze_sentiment(self, text: str) -> str:
        """Simple sentiment analysis based on keywords"""
        positive_words = [
            "gain", "rise", "up", "bull", "growth", "profit", "strong", 
            "beat", "exceed", "positive", "rally", "surge", "boost"
        ]
        negative_words = [
            "fall", "drop", "down", "bear", "loss", "weak", "miss", 
            "decline", "negative", "crash", "plunge", "concern", "risk"
        ]
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            return "positive"
        elif negative_count > positive_count:
            return "negative"
        else:
            return "neutral"
    
    def _get_mock_news(self) -> List[NewsItem]:
        """Get mock news data when API is not available"""
        return [
            NewsItem(
                title="Small-cap stocks show resilience amid market volatility",
                summary="Small-capitalization stocks have demonstrated surprising strength in recent trading sessions, outperforming larger peers despite broader market concerns.",
                source="MarketWatch",
                published_at=datetime.now() - timedelta(hours=2),
                url="https://example.com/news1",
                sentiment="positive"
            ),
            NewsItem(
                title="Fed signals potential policy changes in upcoming meeting",
                summary="Federal Reserve officials hint at possible adjustments to monetary policy as economic indicators show mixed signals across different sectors.",
                source="Reuters",
                published_at=datetime.now() - timedelta(hours=4),
                url="https://example.com/news2",
                sentiment="neutral"
            ),
            NewsItem(
                title="Tech earnings season approaches with cautious optimism",
                summary="Analysts express measured optimism ahead of the technology sector's earnings reports, citing both opportunities and challenges in the current environment.",
                source="CNBC",
                published_at=datetime.now() - timedelta(hours=6),
                url="https://example.com/news3",
                sentiment="neutral"
            ),
            NewsItem(
                title="Micro-cap biotech companies see increased investor interest",
                summary="Smaller biotechnology companies are attracting renewed attention from investors seeking growth opportunities in the healthcare sector.",
                source="Bloomberg",
                published_at=datetime.now() - timedelta(hours=8),
                url="https://example.com/news4",
                sentiment="positive"
            ),
            NewsItem(
                title="Market volatility creates opportunities for active traders",
                summary="Recent market fluctuations have created new opportunities for traders willing to navigate the increased volatility in micro-cap stocks.",
                source="Yahoo Finance",
                published_at=datetime.now() - timedelta(hours=12),
                url="https://example.com/news5",
                sentiment="neutral"
            )
        ]
    
    def get_economic_indicators(self) -> Dict[str, Any]:
        """Get key economic indicators"""
        cache_key = "economic_indicators"
        cached_data = self._get_cache(cache_key)
        if cached_data:
            return cached_data
        
        indicators = {}
        
        try:
            # Get key economic data
            economic_symbols = {
                "10_year_yield": "^TNX",
                "dollar_index": "DX-Y.NYB",
                "gold": "GC=F",
                "oil": "CL=F",
                "vix": "^VIX"
            }
            
            for name, symbol in economic_symbols.items():
                try:
                    ticker = yf.Ticker(symbol)
                    hist = ticker.history(period="2d")
                    
                    if not hist.empty:
                        current = hist['Close'].iloc[-1]
                        prev = hist['Close'].iloc[-2] if len(hist) > 1 else current
                        change_pct = ((current - prev) / prev) * 100 if prev != 0 else 0
                        
                        indicators[name] = {
                            "value": current,
                            "change_percent": change_pct
                        }
                except Exception:
                    continue
            
            self._set_cache(cache_key, indicators, duration=1800)  # 30 minutes
            return indicators
            
        except Exception as e:
            st.error(f"Error fetching economic indicators: {e}")
            return {}
    
    def get_market_sentiment_score(self) -> Dict[str, Any]:
        """Calculate overall market sentiment score"""
        try:
            # Get VIX (fear index)
            vix_data = self.get_stock_data("^VIX")
            vix_score = 0
            
            if vix_data:
                # VIX interpretation: <20=low fear, 20-30=moderate, >30=high fear
                if vix_data.current_price < 20:
                    vix_score = 80  # Low fear = positive sentiment
                elif vix_data.current_price < 30:
                    vix_score = 50  # Moderate fear = neutral sentiment
                else:
                    vix_score = 20  # High fear = negative sentiment
            
            # Get market indices performance
            indices = self.get_market_indices()
            indices_score = 50  # Default neutral
            
            if indices:
                avg_change = np.mean([idx.change_percent for idx in indices[:4]])  # Major indices only
                if avg_change > 1:
                    indices_score = 75
                elif avg_change > 0:
                    indices_score = 60
                elif avg_change > -1:
                    indices_score = 40
                else:
                    indices_score = 25
            
            # Get news sentiment
            news_items = self.get_market_news(limit=20)
            news_score = 50
            
            if news_items:
                sentiment_scores = {
                    "positive": 75,
                    "neutral": 50,
                    "negative": 25
                }
                avg_news_score = np.mean([
                    sentiment_scores.get(item.sentiment, 50) 
                    for item in news_items
                ])
                news_score = avg_news_score
            
            # Combine scores
            overall_score = (vix_score * 0.4 + indices_score * 0.4 + news_score * 0.2)
            
            # Determine sentiment label
            if overall_score >= 70:
                sentiment_label = "Very Bullish"
            elif overall_score >= 60:
                sentiment_label = "Bullish"
            elif overall_score >= 40:
                sentiment_label = "Neutral"
            elif overall_score >= 30:
                sentiment_label = "Bearish"
            else:
                sentiment_label = "Very Bearish"
            
            return {
                "overall_score": overall_score,
                "sentiment_label": sentiment_label,
                "components": {
                    "vix_score": vix_score,
                    "indices_score": indices_score,
                    "news_score": news_score
                },
                "last_updated": datetime.now()
            }
            
        except Exception as e:
            st.error(f"Error calculating market sentiment: {e}")
            return {
                "overall_score": 50,
                "sentiment_label": "Neutral",
                "components": {},
                "last_updated": datetime.now()
            }
    
    def clear_cache(self):
        """Clear all cached data"""
        self.cache.clear()
        self.cache_expiry.clear()
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        valid_items = sum(1 for key in self.cache.keys() if self._is_cache_valid(key))
        return {
            "total_items": len(self.cache),
            "valid_items": valid_items,
            "expired_items": len(self.cache) - valid_items,
            "cache_keys": list(self.cache.keys())
        }

# Global market data service instance
_market_service = None

def get_market_service(news_api_key: Optional[str] = None) -> MarketDataService:
    """Get global market data service instance"""
    global _market_service
    if _market_service is None:
        _market_service = MarketDataService(news_api_key)
    return _market_service