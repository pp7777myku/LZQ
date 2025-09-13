from datetime import date, timedelta, datetime
from typing import Iterable
import pytz

def daterange(d1: date, d2: date):
    for n in range((d2 - d1).days):
        yield d1 + timedelta(n)

def working_days_between(start: date, end: date, exclude_weekends: bool, holidays: Iterable[str]):
    """计算 start(含) 到 end(不含) 的工作日数量。"""
    hset = set(holidays or [])
    count = 0
    for d in daterange(start, end):
        if exclude_weekends and d.weekday() >= 5:
            continue
        if f"{d:%Y-%m-%d}" in hset:
            continue
        count += 1
    return count

def days_overdue(today: date, due_date: date, exclude_weekends: bool, holidays: Iterable[str]) -> int:
    """按配置计算逾期天数（可排除周末与节假日）"""
    if today <= due_date:
        return 0
    return working_days_between(due_date, today, exclude_weekends, holidays)

def now_in_tz(tz_name: str) -> datetime:
    tz = pytz.timezone(tz_name)
    return datetime.now(tz)
