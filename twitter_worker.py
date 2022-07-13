import tweepy
import constants
import requests
import json
oauth2_user_handler = tweepy.OAuth2UserHandler(
    client_id=constants.CLIENT_ID,
    redirect_uri=constants.CALLBACK_URL,
    scope=["tweet.read", "users.read", "like.read",'offline.access'],
    client_secret=constants.CLIENT_SECRET)

def download_all_liked_tweets_from_user(user):
    user_data = user.user_data
    client = tweepy.Client(user.access_token)
    # liked_tweets = client.get_liked_tweets()
    return []
def refresh_token(user):
    # client = tweepy.Client(user.access_token)
    # user_tokens = oauth2_user_handler.refresh_token(user.refresh_token)
    user_tokens = make_refresh_token_request(user.refresh_token)
    print(user_tokens)
    print(type(user_tokens))
    return user_tokens

def make_refresh_token_request(refresh_token):
    url = f"https://api.twitter.com/2/oauth2/token?refresh_token={refresh_token}&grant_type=refresh_token&client_id={constants.CLIENT_ID}"

    payload={}
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    }

    response = requests.request("POST", url, headers=headers, data=payload,auth=requests.auth.HTTPBasicAuth(constants.CLIENT_ID, constants.CLIENT_SECRET))

    return json.loads(response.text)