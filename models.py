from app import db
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Contests(db.Model):
    id: str
    name: str
    description: str
    language: str
    project: str
    start_date: datetime
    end_date: datetime
    created_by: str
    created_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(4), nullable=False)
    project = db.Column(db.String(15), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    created_by = db.Column(db.String(75), nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    def __repr__(self):
        return '<Contest {}>'.format(self.id)


@dataclass
class Juries(db.Model):
    id: str
    contest_id: str
    username: str
    added_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(75), nullable=False)
    added_at = db.Column(db.DateTime,
        nullable=False,
        default=datetime.utcnow()
    )

    def __repr__(self):
        return '<Jury {}>'.format(self.id)
