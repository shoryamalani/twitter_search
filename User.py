import database_worker
from flask_login import UserMixin
import twitter_worker
from datetime import datetime
class User(UserMixin):
    logged_in = False
    user_data = None
    access_token = None
    refresh_token = None
    expires_at = None
    def __init__(self, id,user_data):
        self.id = id
        self.user_data = user_data
        if self.user_data != None:
            self.logged_in = True
            self.access_token = self.user_data[9]
            self.refresh_token = self.user_data[10]
            self.expires_at = self.user_data[19]
            if int(float(self.expires_at)-1000) < int(datetime.timestamp(datetime.now())):
                self.refresh_token()
            print(self.user_data)
        else:
            return None

    def refresh_valid_token(self):
        if self.user_data != None:
            tokens = twitter_worker.refresh_token(self)
            print(tokens)
            if 'error' in tokens:
                return False
            tokens['expires_at'] = str(datetime.timestamp(datetime.now())+7200)
            database_worker.update_tokens_in_db(tokens,self.id)
            self.access_token = tokens['access_token']
            self.refresh_token = tokens['refresh_token']
            self.expires_at = tokens['expires_at']
            return True
        else:
            return False
    def is_authenticated(self):
        return self.logged_in # Later check if access token is still valid
    def is_active(self):
        return True # I wont do bans till I need to
    def is_anonymous(self):
        return False # no user can be anon
    def get_id(self):
        return self.id
    @staticmethod
    def get(id):
        user_data = database_worker.get_user_data(id)
        if user_data != None:
            return User(id,user_data)
        else:
            return None
    def download_all_tweets(self):
        if self.user_data != None:
            downloaded =  twitter_worker.download_all_liked_tweets_from_user(self)
        else:
            return False
    
    