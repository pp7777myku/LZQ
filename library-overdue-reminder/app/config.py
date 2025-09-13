import os
from dotenv import load_dotenv

def str2bool(v: str) -> bool:
    return str(v).lower() in ("1", "true", "yes", "on")

def load_config(app):
    load_dotenv()
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///library.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["MAIL_ENABLED"] = str2bool(os.getenv("MAIL_ENABLED", "false"))
    app.config["MAIL_SMTP_HOST"] = os.getenv("MAIL_SMTP_HOST", "")
    app.config["MAIL_SMTP_PORT"] = int(os.getenv("MAIL_SMTP_PORT", "465"))
    app.config["MAIL_USE_SSL"] = str2bool(os.getenv("MAIL_USE_SSL", "true"))
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME", "")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD", "")
    app.config["MAIL_FROM"] = os.getenv("MAIL_FROM", os.getenv("MAIL_USERNAME", ""))

    app.config["NOTIFY_SEND_HOUR"] = int(os.getenv("NOTIFY_SEND_HOUR", "9"))
    app.config["TIMEZONE"] = os.getenv("TIMEZONE", "Asia/Shanghai")

    app.config["EXCLUDE_WEEKENDS"] = str2bool(os.getenv("EXCLUDE_WEEKENDS", "true"))
    app.config["EXCLUDE_HOLIDAYS"] = str2bool(os.getenv("EXCLUDE_HOLIDAYS", "true"))
    holidays_str = os.getenv("HOLIDAYS", "")
    app.config["HOLIDAYS"] = [h.strip() for h in holidays_str.split(",") if h.strip()]
