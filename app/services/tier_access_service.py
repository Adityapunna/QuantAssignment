from fastapi import HTTPException
from datetime import datetime, date

def check_access(user, indicator: str, start_date: str, end_date: str):
    allowed_indicators = {
        "Free": ["SMA", "EMA"],
        "Pro": ["SMA", "EMA", "RSI", "MACD"],
        "Premium": ["SMA", "EMA", "RSI", "MACD", "Bollinger"]
    }

    if user.last_request_date != date.today():
        user.requests_today = 0
        user.last_request_date = date.today()

    days_requested = (datetime.strptime(end_date, "%Y-%m-%d") - datetime.strptime(start_date, "%Y-%m-%d")).days

    if user.subscription_tier == "Free":
        if indicator not in allowed_indicators["Free"]:
            raise HTTPException(status_code=403, detail="Free tier: indicator not allowed")
        if days_requested > 90:
            raise HTTPException(status_code=403, detail="Free tier: max 90 days allowed")
        if user.requests_today >= 50:
            raise HTTPException(status_code=403, detail="Free tier: daily request limit exceeded")

    elif user.subscription_tier == "Pro":
        if indicator not in allowed_indicators["Pro"]:
            raise HTTPException(status_code=403, detail="Pro tier: indicator not allowed")
        if days_requested > 365:
            raise HTTPException(status_code=403, detail="Pro tier: max 1 year of data allowed")
        if user.requests_today >= 500:
            raise HTTPException(status_code=403, detail="Pro tier: daily request limit exceeded")

    elif user.subscription_tier == "Premium":
        if indicator not in allowed_indicators["Premium"]:
            raise HTTPException(status_code=403, detail="Premium tier: indicator not allowed")
