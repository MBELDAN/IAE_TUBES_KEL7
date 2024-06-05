class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/rumorPlayerDb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLAYER_SERVICE_URL = 'http://localhost:5001'
    TEAM_RANK_SERVICE_URL = 'http://localhost:5002'
    PORT = 5005
