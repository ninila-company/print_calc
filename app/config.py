import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """config."""

    SECRET_KEY = os.environ.get("SECRET_KEY") or "вам-нужно-будет-заменить-это"
    # Другие настройки конфигурации можно добавить здесь
