# INSERT INTO users (username, hashed_password, subscription_tier, requests_today, created_at, last_request_at)
# VALUES
# ('alice', 'hashed_pass_123', 'Free', 12, NOW(), NULL),
# ('bob', 'hashed_pass_456', 'Pro', 85, NOW(), NOW()),
# ('charlie', 'hashed_pass_789', 'Premium', 0, NOW(), NOW());

from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models import User
from datetime import datetime

# Dummy users
users = [
    User(
        username='alice',
        hashed_password='hashed_pass_123',
        subscription_tier='Free',
        requests_today=12,
        created_at=datetime.utcnow(),
        last_request_at=None
    ),
    User(
        username='bob',
        hashed_password='hashed_pass_456',
        subscription_tier='Pro',
        requests_today=85,
        created_at=datetime.utcnow(),
        last_request_at=datetime.utcnow()
    ),
    User(
        username='charlie',
        hashed_password='hashed_pass_789',
        subscription_tier='Premium',
        requests_today=0,
        created_at=datetime.utcnow(),
        last_request_at=datetime.utcnow()
    )
]

# Insert users
def insert_dummy_users():
    db: Session = SessionLocal()
    try:
        for user in users:
            existing = db.query(User).filter(User.username == user.username).first()
            if not existing:
                db.add(user)
        db.commit()
        print("✅ Dummy users inserted!")
    except Exception as e:
        db.rollback()
        print("❌ Error inserting users:", e)
    finally:
        db.close()

if __name__ == "__main__":
    insert_dummy_users()