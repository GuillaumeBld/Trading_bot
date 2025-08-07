"""LLM interface for trading decisions with support for local and API-based models."""

import json
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

import pandas as pd
from pydantic import BaseModel


@dataclass
class TradingDecision:
    """Represents a trading decision from an LLM."""
    action: str  # "buy", "sell", "hold", "adjust_stop_loss"
    ticker: Optional[str] = None
    shares: Optional[float] = None
    price: Optional[float] = None
    stop_loss: Optional[float] = None
    reasoning: str = ""
    confidence: float = 0.0  # 0-1 scale


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: str  # "openai", "anthropic", "ollama", "huggingface"
    model_name: str
    temperature: float = 0.1
    max_tokens: int = 2000
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    system_prompt: Optional[str] = None


class LLMInterface(ABC):
    """Abstract base class for LLM integrations."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
        self.conversation_history: List[Dict[str, str]] = []
    
    @abstractmethod
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        """Generate a response from the LLM."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the LLM service is available."""
        pass
    
    def analyze_portfolio(self, portfolio_data: Dict, market_data: Dict) -> List[TradingDecision]:
        """Analyze portfolio and return trading decisions."""
        prompt = self._build_portfolio_analysis_prompt(portfolio_data, market_data)
        response = self.generate_response(prompt)
        return self._parse_trading_decisions(response)
    
    def _build_portfolio_analysis_prompt(self, portfolio_data: Dict, market_data: Dict) -> str:
        """Build a comprehensive prompt for portfolio analysis."""
        
        system_context = """You are a professional micro-cap portfolio analyst. Your objective is to maximize returns while managing risk. 
        
        RULES:
        1. Only trade micro-cap stocks (market cap < $300M)
        2. Always use stop-losses
        3. Consider both technical and fundamental factors
        4. Provide specific recommendations with reasoning
        5. Return decisions in JSON format
        
        RESPONSE FORMAT:
        {
            "decisions": [
                {
                    "action": "buy|sell|hold|adjust_stop_loss",
                    "ticker": "SYMBOL",
                    "shares": number,
                    "price": number,
                    "stop_loss": number,
                    "reasoning": "detailed explanation",
                    "confidence": 0.0-1.0
                }
            ],
            "market_outlook": "brief market analysis",
            "risk_assessment": "portfolio risk evaluation"
        }"""
        
        portfolio_summary = self._format_portfolio_data(portfolio_data)
        market_summary = self._format_market_data(market_data)
        
        prompt = f"""
{system_context}

CURRENT PORTFOLIO:
{portfolio_summary}

MARKET DATA:
{market_summary}

Analyze the portfolio and provide trading recommendations. Focus on:
1. Current position performance
2. Stop-loss adjustments needed
3. New opportunities in micro-cap space
4. Risk management improvements
5. Position sizing optimization

Provide your analysis and specific trading decisions:
"""
        return prompt
    
    def _format_portfolio_data(self, data: Dict) -> str:
        """Format portfolio data for prompt."""
        if 'holdings' in data:
            holdings_df = pd.DataFrame(data['holdings'])
            if not holdings_df.empty:
                return holdings_df.to_string(index=False)
        return f"Cash: ${data.get('cash', 0):.2f}\nNo current holdings"
    
    def _format_market_data(self, data: Dict) -> str:
        """Format market data for prompt."""
        formatted = []
        for ticker, info in data.items():
            if isinstance(info, dict):
                formatted.append(f"{ticker}: ${info.get('price', 0):.2f} ({info.get('change_pct', 0):+.2f}%)")
        return "\n".join(formatted) if formatted else "Market data unavailable"
    
    def _parse_trading_decisions(self, response: str) -> List[TradingDecision]:
        """Parse LLM response into trading decisions."""
        decisions = []
        
        try:
            # Try to extract JSON from response
            if "```json" in response:
                json_start = response.find("```json") + 7
                json_end = response.find("```", json_start)
                json_str = response[json_start:json_end].strip()
            elif "{" in response and "}" in response:
                json_start = response.find("{")
                json_end = response.rfind("}") + 1
                json_str = response[json_start:json_end]
            else:
                raise ValueError("No JSON found in response")
            
            parsed = json.loads(json_str)
            
            for decision_data in parsed.get("decisions", []):
                decision = TradingDecision(
                    action=decision_data.get("action", "hold"),
                    ticker=decision_data.get("ticker"),
                    shares=decision_data.get("shares"),
                    price=decision_data.get("price"),
                    stop_loss=decision_data.get("stop_loss"),
                    reasoning=decision_data.get("reasoning", ""),
                    confidence=decision_data.get("confidence", 0.5)
                )
                decisions.append(decision)
                
        except (json.JSONDecodeError, KeyError, ValueError) as e:
            print(f"Failed to parse LLM response: {e}")
            # Fallback: create a hold decision
            decisions.append(TradingDecision(
                action="hold",
                reasoning=f"Failed to parse LLM response: {response[:200]}...",
                confidence=0.0
            ))
        
        return decisions


class OpenAIProvider(LLMInterface):
    """OpenAI API provider."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            import openai
            self.client = openai.OpenAI(api_key=config.api_key)
        except ImportError:
            raise ImportError("OpenAI library not installed. Run: pip install openai")
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": self.config.system_prompt or "You are a helpful trading assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return "Error: Failed to get response from OpenAI"
    
    def is_available(self) -> bool:
        try:
            self.client.models.list()
            return True
        except:
            return False


class AnthropicProvider(LLMInterface):
    """Anthropic API provider."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            import anthropic
            self.client = anthropic.Anthropic(api_key=config.api_key)
        except ImportError:
            raise ImportError("Anthropic library not installed. Run: pip install anthropic")
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        try:
            response = self.client.messages.create(
                model=self.config.model_name,
                max_tokens=self.config.max_tokens,
                temperature=self.config.temperature,
                system=self.config.system_prompt or "You are a helpful trading assistant.",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            print(f"Anthropic API error: {e}")
            return "Error: Failed to get response from Anthropic"
    
    def is_available(self) -> bool:
        try:
            # Try a simple completion to check availability
            self.client.messages.create(
                model=self.config.model_name,
                max_tokens=10,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except:
            return False


class OllamaProvider(LLMInterface):
    """Ollama local LLM provider."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            import ollama
            self.client = ollama.Client(host=config.base_url or 'http://localhost:11434')
        except ImportError:
            raise ImportError("Ollama library not installed. Run: pip install ollama")
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        try:
            response = self.client.chat(
                model=self.config.model_name,
                messages=[
                    {"role": "system", "content": self.config.system_prompt or "You are a helpful trading assistant."},
                    {"role": "user", "content": prompt}
                ],
                options={
                    "temperature": self.config.temperature,
                    "num_predict": self.config.max_tokens
                }
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama API error: {e}")
            return "Error: Failed to get response from Ollama"
    
    def is_available(self) -> bool:
        try:
            models = self.client.list()
            return self.config.model_name in [model['name'] for model in models['models']]
        except:
            return False


class HuggingFaceProvider(LLMInterface):
    """Hugging Face local model provider."""
    
    def __init__(self, config: LLMConfig):
        super().__init__(config)
        try:
            from transformers import AutoTokenizer, AutoModelForCausalLM
            import torch
            
            self.device = "cuda" if torch.cuda.is_available() else "cpu"
            self.tokenizer = AutoTokenizer.from_pretrained(config.model_name)
            self.model = AutoModelForCausalLM.from_pretrained(
                config.model_name,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
                device_map="auto" if self.device == "cuda" else None
            )
            
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
        except ImportError:
            raise ImportError("Transformers library not installed. Run: pip install transformers torch")
    
    def generate_response(self, prompt: str, context: Optional[Dict] = None) -> str:
        try:
            full_prompt = f"{self.config.system_prompt or 'You are a helpful trading assistant.'}\n\nUser: {prompt}\n\nAssistant:"
            
            inputs = self.tokenizer(full_prompt, return_tensors="pt", padding=True, truncation=True)
            if self.device == "cuda":
                inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=self.config.max_tokens,
                    temperature=self.config.temperature,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            # Extract only the assistant's response
            if "Assistant:" in response:
                response = response.split("Assistant:")[-1].strip()
            
            return response
            
        except Exception as e:
            print(f"Hugging Face model error: {e}")
            return "Error: Failed to get response from local model"
    
    def is_available(self) -> bool:
        return hasattr(self, 'model') and self.model is not None


class LLMManager:
    """Manager for LLM providers with fallback support."""
    
    def __init__(self, config_path: Optional[str] = None):
        self.providers: Dict[str, LLMInterface] = {}
        self.active_provider: Optional[LLMInterface] = None
        self.config_path = config_path or ".llm_config.json"
        self._load_config()
    
    def _load_config(self):
        """Load LLM configuration from file or environment."""
        from dotenv import load_dotenv
        load_dotenv()
        
        # Default configurations
        default_configs = {
            "openai": LLMConfig(
                provider="openai",
                model_name="gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                temperature=0.1
            ),
            "anthropic": LLMConfig(
                provider="anthropic",
                model_name="claude-3-haiku-20240307",
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                temperature=0.1
            ),
            "ollama": LLMConfig(
                provider="ollama",
                model_name="llama3.1:8b",
                base_url="http://localhost:11434",
                temperature=0.1
            ),
            "huggingface": LLMConfig(
                provider="huggingface",
                model_name="microsoft/DialoGPT-medium",
                temperature=0.1
            )
        }
        
        # Try to load custom config
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    custom_config = json.load(f)
                    for provider, config_data in custom_config.items():
                        if provider in default_configs:
                            # Update default config with custom values
                            for key, value in config_data.items():
                                if hasattr(default_configs[provider], key):
                                    setattr(default_configs[provider], key, value)
            except Exception as e:
                print(f"Failed to load custom config: {e}")
        
        # Initialize providers
        for provider_name, config in default_configs.items():
            try:
                if provider_name == "openai" and config.api_key:
                    self.providers[provider_name] = OpenAIProvider(config)
                elif provider_name == "anthropic" and config.api_key:
                    self.providers[provider_name] = AnthropicProvider(config)
                elif provider_name == "ollama":
                    self.providers[provider_name] = OllamaProvider(config)
                elif provider_name == "huggingface":
                    self.providers[provider_name] = HuggingFaceProvider(config)
            except Exception as e:
                print(f"Failed to initialize {provider_name}: {e}")
    
    def get_available_providers(self) -> List[str]:
        """Get list of available LLM providers."""
        available = []
        for name, provider in self.providers.items():
            if provider.is_available():
                available.append(name)
        return available
    
    def set_active_provider(self, provider_name: str) -> bool:
        """Set the active LLM provider."""
        if provider_name in self.providers and self.providers[provider_name].is_available():
            self.active_provider = self.providers[provider_name]
            return True
        return False
    
    def analyze_portfolio(self, portfolio_data: Dict, market_data: Dict) -> List[TradingDecision]:
        """Analyze portfolio using the active LLM provider."""
        if not self.active_provider:
            # Try to find an available provider
            available = self.get_available_providers()
            if available:
                self.set_active_provider(available[0])
            else:
                print("No LLM providers available")
                return []
        
        return self.active_provider.analyze_portfolio(portfolio_data, market_data)
    
    def save_config_template(self):
        """Save a configuration template file."""
        template = {
            "openai": {
                "model_name": "gpt-4o-mini",
                "api_key": "your-openai-api-key-here",
                "temperature": 0.1
            },
            "anthropic": {
                "model_name": "claude-3-haiku-20240307",
                "api_key": "your-anthropic-api-key-here", 
                "temperature": 0.1
            },
            "ollama": {
                "model_name": "llama3.1:8b",
                "base_url": "http://localhost:11434",
                "temperature": 0.1
            },
            "huggingface": {
                "model_name": "microsoft/DialoGPT-medium",
                "temperature": 0.1
            }
        }
        
        with open(self.config_path, 'w') as f:
            json.dump(template, f, indent=2)
        print(f"Configuration template saved to {self.config_path}")


# Default system prompt for trading
DEFAULT_TRADING_PROMPT = """You are an expert micro-cap stock analyst and portfolio manager. Your goal is to maximize risk-adjusted returns while maintaining strict risk management.

CONSTRAINTS:
- Only trade U.S.-listed micro-cap stocks (market cap < $300M)
- Always use stop-losses (typically 15-20% below entry)
- Consider position sizing based on volatility and conviction
- Maximum 5-7 positions for diversification
- Focus on stocks with clear catalysts and technical momentum

ANALYSIS FRAMEWORK:
1. Fundamental Analysis: Revenue growth, profitability, debt levels, market opportunity
2. Technical Analysis: Price trends, volume patterns, support/resistance levels
3. Catalyst Analysis: Upcoming events, news flow, insider activity
4. Risk Assessment: Volatility, liquidity, correlation with existing positions

DECISION CRITERIA:
- Buy: Strong fundamentals + technical breakout + clear catalyst + reasonable valuation
- Sell: Stop-loss hit OR fundamental deterioration OR better opportunity identified
- Hold: Thesis intact, no immediate action needed
- Adjust Stop-Loss: Based on technical levels and volatility

Always provide specific reasoning for each recommendation and assign confidence levels."""