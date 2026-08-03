from datetime import datetime, timedelta

from extensions import db

LOAN_PERIOD_DAYS = 14


class Loan(db.Model):
    __tablename__ = "loans"

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)

    status = db.Column(db.String(20), nullable=False, default="borrowed")  # "borrowed" or "returned"

    book = db.relationship("Book", backref="loans")
    user = db.relationship("User", backref="loans")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.due_date:
            self.due_date = datetime.utcnow() + timedelta(days=LOAN_PERIOD_DAYS)

    @property
    def is_overdue(self):
        return self.status == "borrowed" and datetime.utcnow() > self.due_date

    def to_dict(self):
        return {
            "id": self.id,
            "book_id": self.book_id,
            "book_title": self.book.title if self.book else None,
            "user_id": self.user_id,
            "username": self.user.username if self.user else None,
            "borrowed_at": self.borrowed_at.isoformat() if self.borrowed_at else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "returned_at": self.returned_at.isoformat() if self.returned_at else None,
            "status": self.status,
            "is_overdue": self.is_overdue,
        }
