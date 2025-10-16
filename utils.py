"""
utils.py
Small helpers for date parsing and natural-language duration guesses.
"""
import re, datetime

def parse_date(text: str):
    # try ISO
    try:
        return datetime.date.fromisoformat(text.strip())
    except Exception:
        pass
    # basic 'today', 'tomorrow'
    t = text.lower().strip()
    if t in ("today",):
        return datetime.date.today()
    if t in ("tomorrow",):
        return datetime.date.today() + datetime.timedelta(days=1)
    # try numeric like 'in 5 days'
    m = re.search(r"in (\d+)\s*days?", t)
    if m:
        return datetime.date.today() + datetime.timedelta(days=int(m.group(1)))
    return None
