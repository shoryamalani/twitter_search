#Dependencies
from datetime import datetime,timedelta
from site import USER_BASE
from flask import Flask,render_template,session,redirect,url_for,jsonify,send_from_directory,request
from random import randint,choice
from itsdangerous import json
import tweepy
import constants
import loguru
from database_worker import get_user_data
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
import database_worker
from User import User
from dateutil import parser
import json
# from flask_session import Session
import os

# from dbs_scripts.get_question import *
# from misc_scripts.parse_answer import *
# App stuff
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or os.urandom(24)
# Session(app)
loguru.logger.add(f"logs/{__name__}.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="1 day")
#Routers
# @app.route("/",methods=["GET"])
# def home():
#     return render_template("index.html")

# @app.route("/echo/<text>")
# def repeat(text):
#     return render_template("text.html",txt=text)

oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=constants.CLIENT_ID,
    redirect_uri=constants.CALLBACK_URL,
    scope=["tweet.read", "users.read", "like.read",'offline.access'],
    client_secret=constants.CLIENT_SECRET)

twitter_authorize_url = (oauth2_user_handler.get_authorization_url())
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return render_template("error.html",error_message="You must be logged in to access this content.")

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def home():
    loguru.logger.debug("Home page")
    return render_template("index.html", authorize_url=twitter_authorize_url)

# Handle Twitter Callback
@app.route('/callback')
def callback():
    state = request.args.get('state')
    code = request.args.get('code')
    access_denied = request.args.get('error')
    try:
        if access_denied:
            return render_template('error.html', error_message="the OAuth request was denied by this user")
        twitter_redirect_uri = constants.CALLBACK_URL
        response_url_from_app = '{}?state={}&code={}'.format(twitter_redirect_uri, state,code)
        loguru.logger.info(code)
        user_tokens = oauth2_user_handler.fetch_token(response_url_from_app)
        twitter_access_token = user_tokens['access_token']
        twitter_refresh_token = user_tokens['refresh_token']
        client = tweepy.Client(twitter_access_token)
        user = client.get_me(user_auth=False, user_fields=[
'created_at', 'description', 'id', 'name', 'public_metrics', 'url', 'verified', 'protected','profile_image_url'],tweet_fields=['public_metrics','author_id','non_public_metrics'])
        loguru.logger.info(user)
        loguru.logger.info(user[0].data)
        user_from_db = User.get(str(user.data["id"]))
        loguru.logger.debug(user_from_db)
        if user_from_db == None:
            # database_worker.add_user(user.id,user.screen_name)
            created_at = database_worker.convert_to_utc(user.data["created_at"])
            loguru.logger.info("User not found in database")
            d = user.data
            database_worker.add_user_to_db(id=str(d["id"]),oauth2_long_term=code,access_token=twitter_access_token,username=d["username"],profile_image=d["profile_image_url"],bio=d["description"],created_at=d["created_at"],url=d["url"],verified=d["verified"],protected=d["protected"],updated_at=database_worker.convert_to_utc(datetime.now()),followers=d["public_metrics"]["followers_count"],following=d["public_metrics"]["following_count"],posts=d["public_metrics"]["tweet_count"],likes=0,active=1,refresh_token=twitter_refresh_token,last_updated_likes=database_worker.convert_to_utc(datetime.now()-timedelta(days=4)),relevant_tweets=json.dumps({"tweets_posted":[],"tweets_liked":[]}),expires_at=user_tokens["expires_at"])
            user = User.get(str(d["id"]))
            login_user(user)
            return redirect(url_for("search_tweets"))
        else:
            loguru.logger.info("User found in database user_data:".format(user_from_db.user_data))
            
            login_user(user_from_db)
            return redirect(url_for("search_tweets"))
        # tweets = client.get_liked_tweets(id=user.data["id"],user_auth=False, tweet_fields=['id','created_at',"public_metrics"],user_fields=['id','username'])
        
        # final_tweet_data = []
        # loguru.logger.info(f"user: {tweets}")

    except Exception as e:
        loguru.logger.error(e)
        return "Error:"+str(e)
    return jsonify({"user":[str(user)]})
    # return render_template("search_tweets.html")
    
    
    
    id = user.data['id']
    name = user.data['name']
    return user.data
    return render_template('callback.html', name=name, tweet_count=tweet_count, authorize_url=authorize_url)


@app.route("/search_tweets")
@login_required
def search_tweets():
    loguru.logger.debug("Search tweets page")
    return render_template("search_tweets.html")

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500
#Run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)