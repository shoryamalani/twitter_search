from dbs_scripts import get_data_from_database,create_database,execute_db
import json
import psycopg2
def set_up_db():
    conn = make_connection('dbs_scripts/database_login.json')
    users_table =create_database.create_table_command('users',[('id','int PRIMARY KEY'),('username','varchar'),('oauth2_long_term','varchar'),('last_updated_likes','TIMESTAMP'),('followers','int'),('following',"int"),('posts','int')])
    tweets_table = create_database.create_table_command("tweets",[('id','int PRIMARY KEY'),('text','varchar'),('creator_id','int'),('created_at','TIMESTAMP'),('likes','int'),('retweets','int'),('replies','int')])
    execute_db.execute_database_command(conn,users_table)
    execute_db.execute_database_command(conn,tweets_table)
    conn.commit()
    conn.close()
def delete_db():
    pass

def make_connection(filename):
    settings = json.load(open(filename))
    conn = get_data_from_database.connect_to_database(settings['database_location'],settings['database_user'],settings['database_name'])
    return conn

def add_tweets_to_db(tweets):
    final_tweets = []
    for tweet in tweets:
        final_tweets.append([tweet.id,tweet.text,tweet.creator_id,tweet.created_at,tweet.likes,tweet.retweets,tweet.replies])

def add_user_to_db():
    pass