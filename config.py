import os

class Config(object):
    SECRET_KEY = os.getenv("SECRET_KEY") or "token"
    DATABASE="Student.db"
    BABEL_DEFAULT_LOCALE = 'zh_cn'
    PAGESIZE = 10
    WTF_I18N_ENABLED = False