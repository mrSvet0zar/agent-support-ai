from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    ENV: str = os.getenv("ENV", "dev")
    LANGFLOW_URL: str = os.getenv("LANGFLOW_URL")
    LANGFLOW_FLOW_ID: str = os.getenv("LANGFLOW_FLOW_ID")
    LANGFLOW_API_KEY: str = os.getenv("LANGFLOW_API_KEY")

    class Config:
        env_file = ".env"

settings = Settings()
