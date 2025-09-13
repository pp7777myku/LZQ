from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db():
    from .models import User, Book, Borrow, MailLog
    db.create_all()
