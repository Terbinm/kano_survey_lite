# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class Survey(db.Model):
    """問卷填寫記錄"""
    __tablename__ = 'survey'  # 明確指定資料表名稱

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    responses = db.relationship('Response', backref='survey', lazy=True)


class Response(db.Model):
    """個別問題回應"""
    __tablename__ = 'response'  # 明確指定資料表名稱

    id = db.Column(db.Integer, primary_key=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('survey.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    positive_response = db.Column(db.Integer, nullable=False)
    negative_response = db.Column(db.Integer, nullable=False)
    kano_category = db.Column(db.String(1), nullable=False)

class Question(db.Model):
    """問卷問題"""
    __tablename__ = 'question'

    id = db.Column(db.Integer, primary_key=True)
    positive = db.Column(db.Text, nullable=False)  # 正向問題
    negative = db.Column(db.Text, nullable=False)  # 負向問題
    order = db.Column(db.Integer, default=0)       # 問題順序
    active = db.Column(db.Boolean, default=True)   # 是否啟用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'positive': self.positive,
            'negative': self.negative,
            'order': self.order,
            'active': self.active
        }