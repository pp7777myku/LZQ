import smtplib, ssl
from email.message import EmailMessage
from flask import current_app
from .models import MailLog
from .database import db

def send_mail(to_email: str, subject: str, body: str) -> str:
    """发送一封邮件，返回状态：SENT / DISABLED / ERROR"""
    if not current_app.config["MAIL_ENABLED"]:
        _log_mail(to_email, subject, body, "DISABLED", None)
        return "DISABLED"
    try:
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = current_app.config["MAIL_FROM"]
        msg["To"] = to_email
        msg.set_content(body)

        host = current_app.config["MAIL_SMTP_HOST"]
        port = current_app.config["MAIL_SMTP_PORT"]
        username = current_app.config["MAIL_USERNAME"]
        password = current_app.config["MAIL_PASSWORD"]
        use_ssl = current_app.config["MAIL_USE_SSL"]

        if use_ssl:
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(host, port, context=context) as server:
                server.login(username, password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(username, password)
                server.send_message(msg)
        _log_mail(to_email, subject, body, "SENT", None)
        return "SENT"
    except Exception as e:
        _log_mail(to_email, subject, body, "ERROR", str(e))
        return "ERROR"

def _log_mail(to_email, subject, body, status, error):
    entry = MailLog(user_email=to_email, subject=subject, body=body, status=status, error=error)
    db.session.add(entry)
    db.session.commit()
