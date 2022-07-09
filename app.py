#Dependencies
from flask import Flask,render_template,session,redirect,url_for,jsonify,send_from_directory,request
from random import randint,choice
import tweepy
import constants
# from dbs_scripts.get_question import *
# from misc_scripts.parse_answer import *
# App stuff
app = Flask(__name__)


#Routers
# @app.route("/",methods=["GET"])
# def home():
#     return render_template("index.html")

# @app.route("/echo/<text>")
# def repeat(text):
#     return render_template("text.html",txt=text)
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=constants.APP_ID,
    redirect_uri=constants.CALLBACK_URL,
    scope=["tweet.read", "users.read", "bookmark.read"],
    client_secret=constants.CLIENT_SECRET)

twitter_authorize_url = (oauth2_user_handler.get_authorization_url())

@app.route("/")
def home():
    return render_template("index.html", authorize_url=twitter_authorize_url)


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('error.html', error_message='uncaught exception'), 500
#Run
if __name__ == "__main__":
    app.run(host="0.0.0.0",port=5000)