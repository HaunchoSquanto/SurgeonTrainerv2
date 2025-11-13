"""
Client for calling local Studio LM instance
"""
import requests
from typing import Optional
from .config import get_config
from .logging import get_logger

log = get_logger(__name__)


class LLMError(Exception):
    """Raised when LLM call fails"""
    pass


def call_studio_lm(
    user_prompt: str,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> str:
    """
    Call local Studio LM instance with a prompt.
    
    Args:
        user_prompt: The user message/prompt
        system_prompt: Optional system prompt for instruction
        temperature: Sampling temperature (0.0-1.0). Lower = more deterministic
        max_tokens: Maximum tokens in response
    
    Returns:
        LLM response text
    
    Raises:
        LLMError: If API call fails
    """
    config = get_config()
    
    # Build messages
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": user_prompt})
    
    # Build request payload
    payload = {
        "model": config.llm_model,
        "messages": messages,
        "temperature": temperature or config.llm_temperature,
        "max_tokens": max_tokens or config.llm_max_tokens,
        "stream": False
    }
    
    log.debug(f"Calling Studio LM: model={config.llm_model}, temp={payload['temperature']}")
    
    try:
        response = requests.post(
            f"{config.llm_base_url}/v1/chat/completions",
            json=payload,
            timeout=config.api_timeout
        )
        response.raise_for_status()
        
        data = response.json()
        content = data["choices"][0]["message"]["content"]
        
        log.debug(f"Studio LM response received: {len(content)} chars")
        return content
        
    except requests.RequestException as e:
        log.error(f"Studio LM API call failed: {e}")
        raise LLMError(f"Failed to call Studio LM: {e}") from e
    except (KeyError, IndexError) as e:
        log.error(f"Invalid Studio LM response format: {e}")
        raise LLMError(f"Invalid response from Studio LM: {e}") from e
