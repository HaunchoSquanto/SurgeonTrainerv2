"""
Configuration for the AI agent.
"""
import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Load .env file from agent directory
env_path = Path(__file__).parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

# LM Studio Configuration
LM_STUDIO_URL = os.getenv("LM_STUDIO_URL", "http://localhost:1234/v1/chat/completions")
LM_STUDIO_MODEL = os.getenv("LM_STUDIO_MODEL", "qwen3-vl-30b-a3b-instruct")

# Backend API Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_PREFIX = "/api/v1"

# Agent Settings
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.3"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
TIMEOUT = int(os.getenv("TIMEOUT", "60"))

# Debug mode
DEBUG = os.getenv("DEBUG", "true").lower() == "true"  # Enable by default for troubleshooting


def get_full_url(endpoint: str) -> str:
    """Construct full URL for backend endpoint."""
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"
    return f"{BACKEND_URL}{API_PREFIX}{endpoint}"
