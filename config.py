import os

DEBUG = True

SECRET_KEY = os.urandom(24)


DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '800819'
HOST = '127.0.0.1'
PORT = '3306'

DATABASE = 'arcqa'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

UPLOADED_PHOTOS_DEST = os.path.abspath(os.path.join(os.getcwd(), "/static/avatar"))

FLASKY_QUESTIONS_PER_PAGE = 2
