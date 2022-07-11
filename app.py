#Dependencies
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
import User
# from dbs_scripts.get_question import *
# from misc_scripts.parse_answer import *
# App stuff
app = Flask(__name__)

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
    scope=["tweet.read", "users.read", "like.read"],
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
        twitter_access_token = oauth2_user_handler.fetch_token(response_url_from_app)['access_token']
        client = tweepy.Client(twitter_access_token)
        user = client.get_me(user_auth=False, user_fields=[
'created_at', 'description', 'id', 'name', 'public_metrics', 'url', 'verified', 'protected','profile_image_url'],tweet_fields=['public_metrics','author_id','non_public_metrics'])
        loguru.logger.info(user)
        loguru.logger.info(user[0].data)
        user_from_db = database_worker.get_user_data(user.data["id"])
        loguru.logger.debug(user_from_db)
        if user_from_db == None:
            # database_worker.add_user(user.id,user.screen_name)
            loguru.logger.info("User not found in database")
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




@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500
#Run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)