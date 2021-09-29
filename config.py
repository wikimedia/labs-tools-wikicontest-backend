import os


class config(object):
    DEBUG = False
    TESTING = False


class production(config):
    DEBUG = False
    CONSUMER_KEY = ""
    CONSUMER_SECRET = ""
    SESSION_COOKIE_SECURE = True
    SESSION_REFRESH_EACH_REQUEST = False
    PREFERRED_URL_SCHEME = 'https'
    OAUTH_MWURI = "https://meta.wikimedia.org/w/"
    APP_REDIRECT_URI = "https://wikicontest.toolforge.org"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://username:password@host/wikicontests"


class local(config):
    DEVELOPMENT = True
    DEBUG = True
    CONSUMER_KEY = "42e2993ea0d859abc856179387a0b652"
    CONSUMER_SECRET = "eef670ed1e6b3be313c05f957c626fc49dad078c"
    OAUTH_MWURI = "http://localhost/mw135/"
    APP_REDIRECT_URI = "http://127.0.0.1:3000"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://jay:iampassword@localhost/wikicontests"
