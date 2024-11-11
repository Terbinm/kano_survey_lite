# config.py
import os

class Config:
    # 取得目前檔案所在的目錄路徑
    basedir = os.path.abspath(os.path.dirname(__file__))
    # 設定 SQLite 資料庫檔案的完整路徑
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'instance', 'kano_survey.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'your-secret-key-here'  # 請更換為您的密鑰