import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:@localhost/rankingdb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PORT = 5002  # Port untuk service ranking tim
    PLAYER_SERVICE_URL = 'http://localhost:5001'
