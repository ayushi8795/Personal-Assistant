import os 
from dataclasses import dataclass
from dotenv import load_dotenv
load_dotenv(override=True)

@dataclass(frozen=True)
class Config:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    RESEND_API_KEY: str = os.getenv("RESEND_API_KEY")
    RESEND_EMAIL_DEFAULT_SENDER: str = os.getenv("RESEND_EMAIL_DEFAULT_SENDER")
    RECEIVER_EMAIL: str = os.getenv("RECEIVER_EMAIL")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-5-nano")
    openai_embed_model: str = os.getenv("OPENAI_EMBED_MODEL", "text-embedding-ada-002")

personalConfig = Config()

if not personalConfig.OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not set")

