import os
BASE_DIR = os.path.dirname(__file__)

SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS= False       # 이벤트를 처리하는 옵션, pybo.py 에는 안필요해서 False

SECRET_KEY = 'dev'
