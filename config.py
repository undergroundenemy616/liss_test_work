import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('8x+^)*br(0!nkc&r^4t4o1d^zo((#+h(f_q87c93$0!^b!71^e')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///DataBase.db'


config = {
    'default': DevelopmentConfig
}
