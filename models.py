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


@dataclass
class Rules(db.Model):
    id: str
    contest_id: str
    rules: dict

    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, nullable=False)
    rules = db.Column(db.JSON, nullable=False)

    def __repr__(self):
        return '<Rule {}>'.format(self.id)


class Submission(db.Model):
    id: str
    contest_id: str
    article_name: str
    submission_by: str
    submission_stats: dict
    submission_on: datetime
    assessment_by: str
    assessment_stats: dict
    assessment_on: datetime

    id = db.Column(db.Integer, primary_key=True)
    contest_id = db.Column(db.Integer, nullable=False)
    article_name = db.Column(db.String(255), nullable=False)
    submission_by = db.Column(db.String(75), nullable=False)
    submission_stats = db.Column(db.JSON, nullable=False)
    submission_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    assessment_by = db.Column(db.String(75))
    assessment_stats = db.Column(db.JSON)
    assessment_on = db.Column(db.DateTime)

    def __repr__(self):
        return '<Submission {}>'.format(self.id)
