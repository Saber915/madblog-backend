import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'), encoding='utf-8')


class Config(object):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/madblog?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
