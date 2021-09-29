from flask import Flask, render_template, jsonify, request, redirect, session
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import mwoauth
import os

from utils import _str


app = Flask(__name__)
cors = CORS(
    app,
    supports_credentials=True,
    resources={
        r"/api/*": {
            "origins": [
                "https://wikicontest.toolforge.org",
                "http://127.0.0.1:3000"
            ]
        }
    }
)


# ----------- Basic configuration -------------
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'None'
app.config.from_object(os.environ['APP_SETTINGS'])
app.secret_key = os.urandom(50)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ---------- Database configuration -----------
db = SQLAlchemy(app)
from models import Contests
migrate = Migrate(app, db)

# ----------- OAuth configuration -------------
consumer_token = mwoauth.ConsumerToken(
    app.config["CONSUMER_KEY"],
    app.config["CONSUMER_SECRET"]
)
handshaker = mwoauth.Handshaker(app.config["OAUTH_MWURI"], consumer_token)
API_URL = app.config["OAUTH_MWURI"] + "api.php"


# ------- Index route -------
@app.route('/')
def index():
    return redirect(app.config["APP_REDIRECT_URI"])


#############################
# ----------- API -----------
#############################


@app.route('/api/contests', methods=['GET'])
def contests():
    constests = Contests.query.all()
    return jsonify({
        "status": "success",
        "contests": constests
    }), 200


@app.route('/api/contest/<int:id>', methods=['GET'])
def contest(id):
    pass


@app.route('/api/contest/create', methods=['POST'])
def createContest():
    pass


@app.route('/api/contest/<int:id>/edit', methods=['POST'])
def editContest(id):
    pass


@app.route('/api/addjury', methods=['POST'])
def addJury():
    pass


@app.route('/api/profile')
def api_profile():
    return jsonify({
        "logged": get_current_user() is not None,
        "username": get_current_user()
    })


#############################
# ---------- Login ----------
#############################


@app.route('/login')
def login():
    redirect_to, request_token = handshaker.initiate()
    keyed_token_name = _str(request_token.key) + '_request_token'
    keyed_next_name = _str(request_token.key) + '_next'
    session[keyed_token_name] = \
        dict(zip(request_token._fields, request_token))
    if 'next' in request.args:
        session[keyed_next_name] = request.args.get('next')
    else:
        session[keyed_next_name] = 'index'
    return redirect(redirect_to)


@app.route('/logout')
def logout():
    session['mwoauth_access_token'] = None
    session['mwoauth_username'] = None
    if 'next' in request.args:
        return redirect(request.args['next'])
    return redirect(app.config["APP_REDIRECT_URI"])


@app.route('/oauth-callback')
def oauth_callback():
    request_token_key = request.args.get('oauth_token', 'None')
    keyed_token_name = _str(request_token_key) + '_request_token'
    keyed_next_name = _str(request_token_key) + '_next'
    if keyed_token_name not in session:
        err_msg = "OAuth callback failed. Can't find keyed token. Are cookies disabled?"
        err_msg = err_msg + '\n Go <a href="https://wikicontest.toolforge.org">Wikicontest</a>'
        return err_msg
    access_token = handshaker.complete(
        mwoauth.RequestToken(**session[keyed_token_name]),
        request.query_string)
    session['mwoauth_access_token'] = \
        dict(zip(access_token._fields, access_token))
    del session[keyed_next_name]
    del session[keyed_token_name]
    get_current_user(False)
    return redirect(app.config["APP_REDIRECT_URI"])


def get_current_user(cached=True):
    if cached:
        return session.get('mwoauth_username')
    # Get user info
    identity = handshaker.identify(
        mwoauth.AccessToken(**session['mwoauth_access_token'])
    )
    # Store user info in session
    session['mwoauth_username'] = identity['username']
    return session['mwoauth_username']


if __name__ == "__main__":
    app.run()
