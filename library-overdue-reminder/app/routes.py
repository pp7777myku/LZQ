from flask import Blueprint, jsonify, request, render_template, current_app
from datetime import date, datetime
from .database import db
from .models import User, Book, Borrow
from .utils import days_overdue
from .notifier import send_mail

bp = Blueprint("api", __name__)

@bp.get("/")
def index():
    return render_template("index.html")

# ---------- Users ----------
@bp.get("/api/users")
def list_users():
    users = User.query.order_by(User.id.desc()).all()
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "phone": u.phone} for u in users])

@bp.post("/api/users")
def create_user():
    data = request.json or {}
    u = User(name=data["name"], email=data["email"], phone=data.get("phone"))
    db.session.add(u)
    db.session.commit()
    return jsonify({"id": u.id}), 201

# ---------- Books ----------
@bp.get("/api/books")
def list_books():
    books = Book.query.order_by(Book.id.desc()).all()
    return jsonify([{"id": b.id, "title": b.title, "author": b.author, "isbn": b.isbn} for b in books])

@bp.post("/api/books")
def create_book():
    data = request.json or {}
    b = Book(title=data["title"], author=data.get("author"), isbn=data.get("isbn"))
    db.session.add(b)
    db.session.commit()
    return jsonify({"id": b.id}), 201

# ---------- Borrows ----------
@bp.get("/api/borrows")
def list_borrows():
    borrows = Borrow.query.order_by(Borrow.id.desc()).all()
    cfg = current_app.config
    out = []
    for br in borrows:
        d_over = days_overdue(date.today(), br.due_date, cfg["EXCLUDE_WEEKENDS"], cfg["HOLIDAYS"] if cfg["EXCLUDE_HOLIDAYS"] else [])
        out.append({
            "id": br.id,
            "user": {"id": br.user.id, "name": br.user.name, "email": br.user.email},
            "book": {"id": br.book.id, "title": br.book.title},
            "borrow_date": br.borrow_date.isoformat(),
            "due_date": br.due_date.isoformat(),
            "returned": br.returned,
            "return_date": br.return_date.isoformat() if br.return_date else None,
            "days_overdue": d_over
        })
    return jsonify(out)

@bp.post("/api/borrows")
def create_borrow():
    data = request.json or {}
    br = Borrow(
        user_id=data["user_id"],
        book_id=data["book_id"],
        borrow_date=datetime.fromisoformat(data["borrow_date"]).date(),
        due_date=datetime.fromisoformat(data["due_date"]).date(),
    )
    db.session.add(br)
    db.session.commit()
    return jsonify({"id": br.id}), 201

@bp.post("/api/borrows/return")
def return_borrow():
    data = request.json or {}
    br = Borrow.query.get_or_404(data["id"])
    br.returned = True
    br.return_date = date.today()
    db.session.commit()
    return jsonify({"ok": True})

# ---------- Overdue & Notify ----------
@bp.get("/api/overdue")
def get_overdue():
    cfg = current_app.config
    all_borrows = Borrow.query.filter_by(returned=False).all()
    result = []
    for br in all_borrows:
        d_over = days_overdue(date.today(), br.due_date, cfg["EXCLUDE_WEEKENDS"], cfg["HOLIDAYS"] if cfg["EXCLUDE_HOLIDAYS"] else [])
        if d_over > 0:
            result.append({
                "borrow_id": br.id,
                "user_name": br.user.name,
                "user_email": br.user.email,
                "book_title": br.book.title,
                "due_date": br.due_date.isoformat(),
                "days_overdue": d_over
            })
    return jsonify(result)

@bp.post("/api/notify/run")
def notify_run():
    return jsonify(run_overdue_notify())

def run_overdue_notify():
    cfg = current_app.config
    overdues = get_overdues_list()
    sent = 0
    for item in overdues:
        subject = f"逾期提醒：{item['book_title']} 已逾期 {item['days_overdue']} 天"
        body = (
            f"亲爱的 {item['user_name']}：\n\n"
            f"您借阅的《{item['book_title']}》已于 {item['due_date']} 到期，"
            f"目前逾期 {item['days_overdue']} 天。请尽快归还或联系馆员处理。\n\n"
            f"本邮件为系统自动发送。如已归还，请忽略。\n"
        )
        status = send_mail(item["user_email"], subject, body)
        if status == "SENT":
            sent += 1
    return {"total_overdues": len(overdues), "sent": sent, "mail_enabled": cfg["MAIL_ENABLED"]}

def get_overdues_list():
    cfg = current_app.config
    all_borrows = Borrow.query.filter_by(returned=False).all()
    result = []
    from datetime import date
    for br in all_borrows:
        d_over = days_overdue(date.today(), br.due_date, cfg["EXCLUDE_WEEKENDS"], cfg["HOLIDAYS"] if cfg["EXCLUDE_HOLIDAYS"] else [])
        if d_over > 0:
            result.append({
                "borrow_id": br.id,
                "user_name": br.user.name,
                "user_email": br.user.email,
                "book_title": br.book.title,
                "due_date": br.due_date.isoformat(),
                "days_overdue": d_over
            })
    return result
