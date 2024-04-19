from dataclasses import dataclass
import os
from dotenv import load_dotenv


@dataclass(frozen=False)
class Config:
    load_dotenv()
    openai_api_type: str = os.environ.get("OPENAI_API_TYPE")
    openai_api_version: str = os.environ.get("OPENAI_API_VERSION")
    openai_api_base_url: str = os.environ.get("OPENAI_API_BASE_URL")
    openai_api_key: str = os.environ.get("OPENAI_API_KEY")