#!/usr/bin/env python3
"""
Dynamic Dashboard Configuration

Manages configuration for real-time dashboard features:
- Auto-refresh settings
- WebSocket configuration
- Data update intervals
- Performance optimization settings
- Notification preferences
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional, List
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

@dataclass
class RefreshSettings:
    """Auto-refresh configuration"""
    enabled: bool = True
    interval_seconds: int = 30
    portfolio_interval: int = 10
    market_data_interval: int = 30
    news_interval: int = 60
    charts_interval: int = 15

@dataclass
class WebSocketSettings:
    """WebSocket server configuration"""
    enabled: bool = True
    host: str = "localhost"
    port: int = 8765
    max_connections: int = 100
    heartbeat_interval: int = 30
    reconnect_attempts: int = 5

@dataclass
class DataCacheSettings:
    """Data caching configuration"""
    enabled: bool = True
    portfolio_ttl: int = 30
    market_data_ttl: int = 60
    news_ttl: int = 300
    max_cache_size_mb: int = 100

@dataclass
class NotificationSettings:
    """Notification preferences"""
    enabled: bool = True
    max_notifications: int = 10
    auto_clear_after_minutes: int = 30
    priority_filter: int = 1  # 1=all, 2=medium+high, 3=high only
    sound_enabled: bool = False
    desktop_notifications: bool = False

@dataclass
class PerformanceSettings:
    """Performance optimization settings"""
    max_data_points: int = 1000
    chart_animation: bool = True
    lazy_loading: bool = True
    compression_enabled: bool = True
    batch_updates: bool = True
    update_batch_size: int = 10

@dataclass
class UISettings:
    """User interface preferences"""
    theme: str = "light"  # light, dark, auto
    sidebar_collapsed: bool = False
    show_debug_info: bool = False
    chart_height: int = 400
    table_page_size: int = 50
    auto_scroll: bool = True

@dataclass
class DynamicDashboardConfig:
    """Complete dynamic dashboard configuration"""
    refresh: RefreshSettings
    websocket: WebSocketSettings
    cache: DataCacheSettings
    notifications: NotificationSettings
    performance: PerformanceSettings
    ui: UISettings
    
    def __init__(self):
        self.refresh = RefreshSettings()
        self.websocket = WebSocketSettings()
        self.cache = DataCacheSettings()
        self.notifications = NotificationSettings()
        self.performance = PerformanceSettings()
        self.ui = UISettings()

class DynamicConfigManager:
    """Manages dynamic dashboard configuration"""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file or self._get_default_config_path()
        self.config = DynamicDashboardConfig()
        self.load_config()
    
    def _get_default_config_path(self) -> str:
        """Get default configuration file path"""
        config_dir = Path.home() / ".trading_bot"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "dynamic_dashboard_config.json")
    
    def load_config(self) -> bool:
        """Load configuration from file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                
                # Load each section
                if 'refresh' in data:
                    self.config.refresh = RefreshSettings(**data['refresh'])
                if 'websocket' in data:
                    self.config.websocket = WebSocketSettings(**data['websocket'])
                if 'cache' in data:
                    self.config.cache = DataCacheSettings(**data['cache'])
                if 'notifications' in data:
                    self.config.notifications = NotificationSettings(**data['notifications'])
                if 'performance' in data:
                    self.config.performance = PerformanceSettings(**data['performance'])
                if 'ui' in data:
                    self.config.ui = UISettings(**data['ui'])
                
                logger.info(f"Configuration loaded from {self.config_file}")
                return True
            else:
                logger.info("No config file found, using defaults")
                self.save_config()  # Save defaults
                return False
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return False
    
    def save_config(self) -> bool:
        """Save configuration to file"""
        try:
            config_data = {
                'refresh': asdict(self.config.refresh),
                'websocket': asdict(self.config.websocket),
                'cache': asdict(self.config.cache),
                'notifications': asdict(self.config.notifications),
                'performance': asdict(self.config.performance),
                'ui': asdict(self.config.ui)
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_data, f, indent=2)
            
            logger.info(f"Configuration saved to {self.config_file}")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def update_refresh_settings(self, **kwargs) -> bool:
        """Update refresh settings"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.refresh, key):
                    setattr(self.config.refresh, key, value)
            return self.save_config()
        except Exception as e:
            logger.error(f"Error updating refresh settings: {e}")
            return False
    
    def update_websocket_settings(self, **kwargs) -> bool:
        """Update WebSocket settings"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.websocket, key):
                    setattr(self.config.websocket, key, value)
            return self.save_config()
        except Exception as e:
            logger.error(f"Error updating WebSocket settings: {e}")
            return False
    
    def update_notification_settings(self, **kwargs) -> bool:
        """Update notification settings"""
        try:
            for key, value in kwargs.items():
                if hasattr(self.config.notifications, key):
                    setattr(self.config.notifications, key, value)
            return self.save_config()
        except Exception as e:
            logger.error(f"Error updating notification settings: {e}")
            return False
    
    def get_refresh_interval(self, data_type: str) -> int:
        """Get refresh interval for specific data type"""
        intervals = {
            'portfolio': self.config.refresh.portfolio_interval,
            'market_data': self.config.refresh.market_data_interval,
            'news': self.config.refresh.news_interval,
            'charts': self.config.refresh.charts_interval
        }
        return intervals.get(data_type, self.config.refresh.interval_seconds)
    
    def get_cache_ttl(self, data_type: str) -> int:
        """Get cache TTL for specific data type"""
        ttls = {
            'portfolio': self.config.cache.portfolio_ttl,
            'market_data': self.config.cache.market_data_ttl,
            'news': self.config.cache.news_ttl
        }
        return ttls.get(data_type, 60)
    
    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled"""
        features = {
            'auto_refresh': self.config.refresh.enabled,
            'websocket': self.config.websocket.enabled,
            'cache': self.config.cache.enabled,
            'notifications': self.config.notifications.enabled,
            'chart_animation': self.config.performance.chart_animation,
            'lazy_loading': self.config.performance.lazy_loading,
            'batch_updates': self.config.performance.batch_updates
        }
        return features.get(feature, False)
    
    def get_ui_setting(self, setting: str) -> Any:
        """Get UI setting value"""
        return getattr(self.config.ui, setting, None)
    
    def export_config(self) -> Dict[str, Any]:
        """Export configuration as dictionary"""
        return {
            'refresh': asdict(self.config.refresh),
            'websocket': asdict(self.config.websocket),
            'cache': asdict(self.config.cache),
            'notifications': asdict(self.config.notifications),
            'performance': asdict(self.config.performance),
            'ui': asdict(self.config.ui)
        }
    
    def import_config(self, config_data: Dict[str, Any]) -> bool:
        """Import configuration from dictionary"""
        try:
            if 'refresh' in config_data:
                self.config.refresh = RefreshSettings(**config_data['refresh'])
            if 'websocket' in config_data:
                self.config.websocket = WebSocketSettings(**config_data['websocket'])
            if 'cache' in config_data:
                self.config.cache = DataCacheSettings(**config_data['cache'])
            if 'notifications' in config_data:
                self.config.notifications = NotificationSettings(**config_data['notifications'])
            if 'performance' in config_data:
                self.config.performance = PerformanceSettings(**config_data['performance'])
            if 'ui' in config_data:
                self.config.ui = UISettings(**config_data['ui'])
            
            return self.save_config()
        except Exception as e:
            logger.error(f"Error importing config: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        self.config = DynamicDashboardConfig()
        return self.save_config()
    
    def validate_config(self) -> List[str]:
        """Validate configuration and return any issues"""
        issues = []
        
        # Validate refresh intervals
        if self.config.refresh.interval_seconds < 5:
            issues.append("Refresh interval too low (minimum 5 seconds)")
        
        # Validate WebSocket settings
        if not (1024 <= self.config.websocket.port <= 65535):
            issues.append("WebSocket port must be between 1024 and 65535")
        
        # Validate cache settings
        if self.config.cache.max_cache_size_mb < 10:
            issues.append("Cache size too low (minimum 10MB)")
        
        # Validate performance settings
        if self.config.performance.max_data_points < 100:
            issues.append("Max data points too low (minimum 100)")
        
        return issues

# Global config manager instance
_config_manager: Optional[DynamicConfigManager] = None

def get_dynamic_config_manager() -> DynamicConfigManager:
    """Get or create the global dynamic config manager"""
    global _config_manager
    if _config_manager is None:
        _config_manager = DynamicConfigManager()
    return _config_manager

def get_dynamic_config() -> DynamicDashboardConfig:
    """Get the current dynamic configuration"""
    return get_dynamic_config_manager().config

# Convenience functions
def is_auto_refresh_enabled() -> bool:
    """Check if auto-refresh is enabled"""
    return get_dynamic_config().refresh.enabled

def get_refresh_interval() -> int:
    """Get the default refresh interval"""
    return get_dynamic_config().refresh.interval_seconds

def is_websocket_enabled() -> bool:
    """Check if WebSocket is enabled"""
    return get_dynamic_config().websocket.enabled

def get_websocket_config() -> WebSocketSettings:
    """Get WebSocket configuration"""
    return get_dynamic_config().websocket

def get_notification_config() -> NotificationSettings:
    """Get notification configuration"""
    return get_dynamic_config().notifications

if __name__ == "__main__":
    # Example usage and testing
    config_manager = DynamicConfigManager()
    
    print("Current configuration:")
    print(json.dumps(config_manager.export_config(), indent=2))
    
    # Test validation
    issues = config_manager.validate_config()
    if issues:
        print("\nConfiguration issues:")
        for issue in issues:
            print(f"- {issue}")
    else:
        print("\n✅ Configuration is valid")
    
    # Test feature checks
    print(f"\nAuto-refresh enabled: {is_auto_refresh_enabled()}")
    print(f"WebSocket enabled: {is_websocket_enabled()}")
    print(f"Default refresh interval: {get_refresh_interval()} seconds")