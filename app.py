#Dependencies
from flask import Flask,render_template,session,redirect,url_for,jsonify,send_from_directory,request
from random import randint,choice
from itsdangerous import json
import tweepy
import constants
import loguru
# from dbs_scripts.get_question import *
# from misc_scripts.parse_answer import *
# App stuff
app = Flask(__name__)

loguru.add(f"logs/{__name__}.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="1 day")
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
    scope=["tweet.read", "users.read", "bookmark.read"],
    client_secret=constants.CLIENT_SECRET)

twitter_authorize_url = (oauth2_user_handler.get_authorization_url())

@app.route("/")
def home():
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
        twitter_access_token = oauth2_user_handler.fetch_token(response_url_from_app)['access_token']
        client = tweepy.Client(twitter_access_token)
        user = client.get_me(user_auth=False, tweet_fields=['author_id'])
        loguru.info(f"user: {user}")
    except Exception as e:
        return e
    return user.data
    
    
    
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