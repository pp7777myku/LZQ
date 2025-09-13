from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import current_app
from .routes import run_overdue_notify
from .utils import now_in_tz

scheduler = BackgroundScheduler()

def _job():
    # 直接调用内部逻辑；如需队列，可封装
    with current_app.app_context():
        run_overdue_notify()

def init_scheduler(app):
    # 每天在配置的小时运行一次（默认 9:00）
    hour = app.config["NOTIFY_SEND_HOUR"]
    tz = app.config["TIMEZONE"]
    trigger = CronTrigger(hour=hour, minute=0, timezone=tz)
    scheduler.add_job(_job, trigger, id="daily_notify", replace_existing=True)
    scheduler.start()
    app.logger.info(f"Scheduler started, next run around {now_in_tz(tz)}")
