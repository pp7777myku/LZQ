from .database import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(160), nullable=False, unique=True)
    phone = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(120), nullable=True)
    isbn = db.Column(db.String(40), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Borrow(db.Model):
    __tablename__ = "borrows"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    borrow_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    returned = db.Column(db.Boolean, default=False)
    return_date = db.Column(db.Date, nullable=True)

    user = db.relationship("User", backref=db.backref("borrows", lazy=True))
    book = db.relationship("Book", backref=db.backref("borrows", lazy=True))

class MailLog(db.Model):
    __tablename__ = "mail_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_email = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    body = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(40), nullable=False)  # SENT / DISABLED / ERROR
    error = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
