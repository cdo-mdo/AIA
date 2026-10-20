"""Minimal Django settings for the terminal chatbot assignment."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = "development-only-key-not-for-deployment"
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = ["chat.apps.ChatConfig"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "django.sqlite3",
    }
}
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
