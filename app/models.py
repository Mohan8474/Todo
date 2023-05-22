from datetime import datetime, timezone, date
from app import app, db


class Task(db.Model):

    id: int = db.Column(db.Integer, primary_key=True)
    task: str = db.Column(db.Text, nullable=False)
    create_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )
    modify_time: date = db.Column(
        db.DateTime(timezone.utc), nullable=False, default=datetime.utcnow
    )