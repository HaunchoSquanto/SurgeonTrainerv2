"""
Configuration management for services
"""
from pydantic_settings import BaseSettings
from typing import Optional


class ServiceConfig(BaseSettings):
    """Shared configuration for all services"""
    
    # API Configuration
    api_base_url: str = "http://127.0.0.1:8000"
    api_timeout: int = 30
    
    # LLM Configuration (Studio LM)
    llm_base_url: str = "http://127.0.0.1:1234"
    llm_model: str = "lmstudio-community/qwen2.5-14b-instruct"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 2000
    
    # Database Agent Configuration  
    db_agent_enabled: bool = True
    db_agent_max_retries: int = 3
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    class Config:
        env_file = ".env"
        env_prefix = "SURGEON_"


_config: Optional[ServiceConfig] = None


def get_config() -> ServiceConfig:
    """Get or create singleton config instance"""
    global _config
    if _config is None:
        _config = ServiceConfig()
    return _config
