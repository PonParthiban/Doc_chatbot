"""
Configuration module for RAG API
Loads and validates environment variables
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Configuration settings for the RAG application"""

    # HuggingFace API
    HF_TOKEN = os.getenv("HF_TOKEN")
    if not HF_TOKEN:
        raise ValueError("HF_TOKEN environment variable not set. Please check your .env file.")

    MODEL_ID = os.getenv("MODEL_ID", "meta-llama/Llama-3.1-8B-Instruct")

    # Embedding Model (runs locally)
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

    # LLM Parameters
    LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "512"))
    LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))

    # Index Configuration
    SIMILARITY_TOP_K = int(os.getenv("SIMILARITY_TOP_K", "3"))
    BREAKPOINT_PERCENTILE_THRESHOLD = int(
        os.getenv("BREAKPOINT_PERCENTILE_THRESHOLD", "95")
    )

    # Paths
    DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
    STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "./storage"))

    # Server
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    API_RELOAD = os.getenv("API_RELOAD", "False").lower() == "true"

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

    # Create storage directory if it doesn't exist
    STORAGE_DIR.mkdir(exist_ok=True)

    # Offline mode flag
    OFFLINE_MODE = os.getenv("OFFLINE_MODE", "False").lower() == "true"

    @staticmethod
    def validate():
        """Validate that required directories exist"""
        if not Config.DATA_DIR.exists():
            raise ValueError(f"Data directory not found: {Config.DATA_DIR}")
        mode = "OFFLINE" if Config.OFFLINE_MODE else "ONLINE"
        print(f"✓ Config loaded: Data dir={Config.DATA_DIR}, Storage dir={Config.STORAGE_DIR}, Mode={mode}")


# Validate on import
Config.validate()
