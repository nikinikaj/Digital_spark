import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DEPLOY_DIR = BASE_DIR / "deployed_sites"
GITHUB_PAGES_DIR = BASE_DIR / "gh_pages_site"
DOCS_DIR = BASE_DIR / "docs"


def load_env_file(env_path: Path) -> None:
    if not env_path.exists():
        return
    with env_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_env_file(BASE_DIR / ".env")

PAYPAL_BASE_URL = os.getenv("PAYPAL_BASE_URL", "https://www.paypal.com/paypalme/YourBusiness")
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "agency@example.com")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", EMAIL_FROM)

USE_SMTP = bool(SMTP_HOST and SMTP_USERNAME and SMTP_PASSWORD)
