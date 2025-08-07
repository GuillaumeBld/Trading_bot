#!/usr/bin/env python3
"""
Dashboard Configuration Management

This module handles all configuration aspects for the trading dashboard:
- API key management
- Broker connections
- Trading parameters
- Data source settings
- User preferences
"""

import os
import json
import yaml
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from cryptography.fernet import Fernet
import streamlit as st
from pathlib import Path

@dataclass
class BrokerConfig:
    """Broker configuration settings"""
    name: str
    api_key: str = ""
    secret_key: str = ""
    base_url: str = ""
    paper_trading: bool = True
    enabled: bool = False
    
@dataclass
class LLMConfig:
    """LLM provider configuration"""
    name: str
    api_key: str = ""
    model_name: str = ""
    temperature: float = 0.1
    max_tokens: int = 2000
    enabled: bool = False

@dataclass
class TradingConfig:
    """Trading parameters configuration"""
    max_position_size_pct: float = 20.0
    default_stop_loss_pct: float = 15.0
    max_positions: int = 7
    cash_reserve_pct: float = 5.0
    risk_free_rate: float = 0.045
    
@dataclass
class DataSourceConfig:
    """Data source configuration"""
    primary_provider: str = "yfinance"
    backup_provider: str = "alpha_vantage"
    update_frequency: str = "5min"
    news_enabled: bool = False
    news_api_key: str = ""
    
@dataclass
class DashboardConfig:
    """Complete dashboard configuration"""
    brokers: Dict[str, BrokerConfig]
    llm_providers: Dict[str, LLMConfig]
    trading: TradingConfig
    data_sources: DataSourceConfig
    auto_refresh: bool = False
    refresh_interval: int = 30
    theme: str = "light"

class ConfigManager:
    """Manages all configuration for the dashboard"""
    
    def __init__(self, config_dir: str = "."):
        self.config_dir = Path(config_dir)
        self.config_file = self.config_dir / "dashboard_config.json"
        self.env_file = self.config_dir / ".env"
        self.secrets_file = self.config_dir / ".secrets.key"
        
        # Initialize encryption
        self.cipher_suite = self._get_or_create_cipher()
        
        # Load configuration
        self.config = self.load_config()
    
    def _get_or_create_cipher(self) -> Fernet:
        """Get or create encryption cipher for sensitive data"""
        if self.secrets_file.exists():
            with open(self.secrets_file, 'rb') as f:
                key = f.read()
        else:
            key = Fernet.generate_key()
            with open(self.secrets_file, 'wb') as f:
                f.write(key)
            # Make file readable only by owner
            os.chmod(self.secrets_file, 0o600)
        
        return Fernet(key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """Encrypt sensitive data like API keys"""
        if not data:
            return ""
        return self.cipher_suite.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """Decrypt sensitive data"""
        if not encrypted_data:
            return ""
        try:
            return self.cipher_suite.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return ""  # Return empty string if decryption fails
    
    def load_config(self) -> DashboardConfig:
        """Load configuration from files"""
        # Default configuration
        config = DashboardConfig(
            brokers={
                "alpaca": BrokerConfig(
                    name="alpaca",
                    base_url="https://paper-api.alpaca.markets",
                    paper_trading=True
                ),
                "td_ameritrade": BrokerConfig(
                    name="td_ameritrade",
                    base_url="https://api.tdameritrade.com"
                ),
                "interactive_brokers": BrokerConfig(
                    name="interactive_brokers",
                    enabled=False
                )
            },
            llm_providers={
                "openai": LLMConfig(
                    name="openai",
                    model_name="gpt-4o-mini",
                    temperature=0.1
                ),
                "anthropic": LLMConfig(
                    name="anthropic",
                    model_name="claude-3-haiku-20240307",
                    temperature=0.1
                ),
                "ollama": LLMConfig(
                    name="ollama",
                    model_name="llama3.1:8b",
                    enabled=True  # Local, no API key needed
                ),
                "huggingface": LLMConfig(
                    name="huggingface",
                    model_name="microsoft/DialoGPT-medium",
                    enabled=False
                )
            },
            trading=TradingConfig(),
            data_sources=DataSourceConfig()
        )
        
        # Load from JSON file if exists
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved_config = json.load(f)
                    config = self._merge_config(config, saved_config)
            except Exception as e:
                st.error(f"Error loading config file: {e}")
        
        # Load environment variables
        self._load_env_variables(config)
        
        return config
    
    def _merge_config(self, default_config: DashboardConfig, saved_config: Dict) -> DashboardConfig:
        """Merge saved configuration with defaults"""
        # This is a simplified merge - in production, you'd want more sophisticated merging
        try:
            # Update broker configs
            if 'brokers' in saved_config:
                for broker_name, broker_data in saved_config['brokers'].items():
                    if broker_name in default_config.brokers:
                        for key, value in broker_data.items():
                            if key in ['api_key', 'secret_key'] and value:
                                # Decrypt sensitive data
                                value = self.decrypt_sensitive_data(value)
                            setattr(default_config.brokers[broker_name], key, value)
            
            # Update LLM configs
            if 'llm_providers' in saved_config:
                for provider_name, provider_data in saved_config['llm_providers'].items():
                    if provider_name in default_config.llm_providers:
                        for key, value in provider_data.items():
                            if key == 'api_key' and value:
                                # Decrypt sensitive data
                                value = self.decrypt_sensitive_data(value)
                            setattr(default_config.llm_providers[provider_name], key, value)
            
            # Update other configs
            if 'trading' in saved_config:
                for key, value in saved_config['trading'].items():
                    if hasattr(default_config.trading, key):
                        setattr(default_config.trading, key, value)
            
            if 'data_sources' in saved_config:
                for key, value in saved_config['data_sources'].items():
                    if key == 'news_api_key' and value:
                        value = self.decrypt_sensitive_data(value)
                    if hasattr(default_config.data_sources, key):
                        setattr(default_config.data_sources, key, value)
            
        except Exception as e:
            st.error(f"Error merging configuration: {e}")
        
        return default_config
    
    def _load_env_variables(self, config: DashboardConfig):
        """Load configuration from environment variables"""
        # Load from .env file
        if self.env_file.exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key] = value
        
        # Update config with environment variables
        openai_key = os.getenv('OPENAI_API_KEY', '')
        if openai_key:
            config.llm_providers['openai'].api_key = openai_key
            config.llm_providers['openai'].enabled = True
        
        anthropic_key = os.getenv('ANTHROPIC_API_KEY', '')
        if anthropic_key:
            config.llm_providers['anthropic'].api_key = anthropic_key
            config.llm_providers['anthropic'].enabled = True
        
        alpaca_key = os.getenv('ALPACA_API_KEY', '')
        alpaca_secret = os.getenv('ALPACA_SECRET_KEY', '')
        if alpaca_key and alpaca_secret:
            config.brokers['alpaca'].api_key = alpaca_key
            config.brokers['alpaca'].secret_key = alpaca_secret
            config.brokers['alpaca'].enabled = True
        
        news_api_key = os.getenv('NEWS_API_KEY', '')
        if news_api_key:
            config.data_sources.news_api_key = news_api_key
            config.data_sources.news_enabled = True
    
    def save_config(self, config: DashboardConfig):
        """Save configuration to file"""
        try:
            # Prepare config for saving (encrypt sensitive data)
            config_dict = asdict(config)
            
            # Encrypt sensitive broker data
            for broker_name, broker_data in config_dict['brokers'].items():
                if broker_data.get('api_key'):
                    broker_data['api_key'] = self.encrypt_sensitive_data(broker_data['api_key'])
                if broker_data.get('secret_key'):
                    broker_data['secret_key'] = self.encrypt_sensitive_data(broker_data['secret_key'])
            
            # Encrypt sensitive LLM data
            for provider_name, provider_data in config_dict['llm_providers'].items():
                if provider_data.get('api_key'):
                    provider_data['api_key'] = self.encrypt_sensitive_data(provider_data['api_key'])
            
            # Encrypt news API key
            if config_dict['data_sources'].get('news_api_key'):
                config_dict['data_sources']['news_api_key'] = self.encrypt_sensitive_data(
                    config_dict['data_sources']['news_api_key']
                )
            
            # Save to file
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            # Update instance config
            self.config = config
            
            return True
            
        except Exception as e:
            st.error(f"Error saving configuration: {e}")
            return False
    
    def export_config(self, file_path: str, include_secrets: bool = False) -> bool:
        """Export configuration to file"""
        try:
            config_dict = asdict(self.config)
            
            if not include_secrets:
                # Remove sensitive data
                for broker_data in config_dict['brokers'].values():
                    broker_data['api_key'] = ""
                    broker_data['secret_key'] = ""
                
                for provider_data in config_dict['llm_providers'].values():
                    provider_data['api_key'] = ""
                
                config_dict['data_sources']['news_api_key'] = ""
            
            # Export as YAML for readability
            with open(file_path, 'w') as f:
                yaml.dump(config_dict, f, default_flow_style=False, indent=2)
            
            return True
            
        except Exception as e:
            st.error(f"Error exporting configuration: {e}")
            return False
    
    def import_config(self, file_path: str) -> bool:
        """Import configuration from file"""
        try:
            with open(file_path, 'r') as f:
                if file_path.endswith('.json'):
                    imported_config = json.load(f)
                elif file_path.endswith('.yaml') or file_path.endswith('.yml'):
                    imported_config = yaml.safe_load(f)
                else:
                    raise ValueError("Unsupported file format. Use JSON or YAML.")
            
            # Merge with current config
            self.config = self._merge_config(self.config, imported_config)
            
            # Save the merged config
            return self.save_config(self.config)
            
        except Exception as e:
            st.error(f"Error importing configuration: {e}")
            return False
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Validate configuration and return any issues"""
        issues = {
            'errors': [],
            'warnings': [],
            'info': []
        }
        
        # Validate broker configurations
        enabled_brokers = [name for name, broker in self.config.brokers.items() if broker.enabled]
        if not enabled_brokers:
            issues['warnings'].append("No brokers are enabled. You won't be able to execute real trades.")
        
        for name, broker in self.config.brokers.items():
            if broker.enabled:
                if not broker.api_key:
                    issues['errors'].append(f"Broker {name} is enabled but missing API key.")
                if name == 'alpaca' and not broker.secret_key:
                    issues['errors'].append(f"Alpaca broker is enabled but missing secret key.")
        
        # Validate LLM configurations
        enabled_llms = [name for name, llm in self.config.llm_providers.items() if llm.enabled]
        if not enabled_llms:
            issues['warnings'].append("No LLM providers are enabled. AI recommendations will not be available.")
        
        for name, llm in self.config.llm_providers.items():
            if llm.enabled and name not in ['ollama', 'huggingface']:  # These don't need API keys
                if not llm.api_key:
                    issues['errors'].append(f"LLM provider {name} is enabled but missing API key.")
        
        # Validate trading configuration
        if self.config.trading.max_position_size_pct > 50:
            issues['warnings'].append("Maximum position size is very high (>50%). Consider reducing for better risk management.")
        
        if self.config.trading.default_stop_loss_pct < 5:
            issues['warnings'].append("Default stop loss is very tight (<5%). May result in frequent stop-outs.")
        
        if self.config.trading.max_positions > 15:
            issues['warnings'].append("Maximum positions is very high (>15). May be difficult to manage effectively.")
        
        # Validate data sources
        if self.config.data_sources.news_enabled and not self.config.data_sources.news_api_key:
            issues['errors'].append("News integration is enabled but no API key is provided.")
        
        return issues
    
    def get_broker_config(self, broker_name: str) -> Optional[BrokerConfig]:
        """Get configuration for a specific broker"""
        return self.config.brokers.get(broker_name)
    
    def get_llm_config(self, provider_name: str) -> Optional[LLMConfig]:
        """Get configuration for a specific LLM provider"""
        return self.config.llm_providers.get(provider_name)
    
    def get_enabled_brokers(self) -> List[str]:
        """Get list of enabled brokers"""
        return [name for name, broker in self.config.brokers.items() if broker.enabled]
    
    def get_enabled_llm_providers(self) -> List[str]:
        """Get list of enabled LLM providers"""
        return [name for name, llm in self.config.llm_providers.items() if llm.enabled]
    
    def update_broker_config(self, broker_name: str, **kwargs):
        """Update broker configuration"""
        if broker_name in self.config.brokers:
            for key, value in kwargs.items():
                if hasattr(self.config.brokers[broker_name], key):
                    setattr(self.config.brokers[broker_name], key, value)
    
    def update_llm_config(self, provider_name: str, **kwargs):
        """Update LLM provider configuration"""
        if provider_name in self.config.llm_providers:
            for key, value in kwargs.items():
                if hasattr(self.config.llm_providers[provider_name], key):
                    setattr(self.config.llm_providers[provider_name], key, value)
    
    def update_trading_config(self, **kwargs):
        """Update trading configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config.trading, key):
                setattr(self.config.trading, key, value)
    
    def update_data_source_config(self, **kwargs):
        """Update data source configuration"""
        for key, value in kwargs.items():
            if hasattr(self.config.data_sources, key):
                setattr(self.config.data_sources, key, value)

# Global configuration manager instance
_config_manager = None

def get_config_manager() -> ConfigManager:
    """Get global configuration manager instance"""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager