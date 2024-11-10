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