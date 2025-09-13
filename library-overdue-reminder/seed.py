from app import create_app
from app.database import db
from app.models import User, Book, Borrow
from datetime import date, timedelta

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    # 添加测试数据
    u1 = User(name="张三", email="zhangsan@example.com", phone="13800000000")
    u2 = User(name="李四", email="lisi@example.com")
    b1 = Book(title="数据库系统概论", author="王珊")
    b2 = Book(title="计算机网络", author="谢希仁")
    db.session.add_all([u1, u2, b1, b2])
    db.session.commit()

    br1 = Borrow(user_id=u1.id, book_id=b1.id,
                 borrow_date=date.today()-timedelta(days=20),
                 due_date=date.today()-timedelta(days=5))
    br2 = Borrow(user_id=u2.id, book_id=b2.id,
                 borrow_date=date.today()-timedelta(days=10),
                 due_date=date.today()+timedelta(days=3))
    db.session.add_all([br1, br2])
    db.session.commit()
    print("Seed done.")
