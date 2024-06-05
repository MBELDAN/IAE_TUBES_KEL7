class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:@localhost/matchscheduledb'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PLAYER_SERVICE_URL = 'http://localhost:5001'
    TEAM_SERVICE_URL = 'http://localhost:5002'
    STADIUM_SERVICE_URL = 'http://localhost:5003'
    PORT = 5004
