import loguru
from dbs_scripts import get_data_from_database,create_database,execute_db,write_and_read_to_database
import json
import psycopg2
import datetime
import loguru
# loguru.logger.add(f"logs/{__name__}.log", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", rotation="1 day")

def set_up_db():
    conn = make_connection('dbs_scripts/database_login.json')
    users_table =create_database.create_table_command('users',[('id','varchar PRIMARY KEY'),('username','varchar'),('oauth2_long_term','varchar'),('last_updated_likes','TIMESTAMP'),('followers','int'),('following',"int"),('posts','int'),('likes','int'),('active','int'),('access_token','varchar'),('refresh_token','varchar'),('verified','BOOLEAN'),('bio','varchar'),('url','varchar'),('profile_image','varchar'),('created_at','TIMESTAMP'),('updated_at','TIMESTAMP'),('protected',"BOOLEAN"),("relevant_tweets",'json'),('access_token_expiry','varchar')])
    tweets_table = create_database.create_table_command("tweets",[('id','int PRIMARY KEY'),('text','varchar'),('creator_id','int'),('created_at','TIMESTAMP'),('likes','int'),('retweets','int'),('replies','int')])
    execute_db.execute_database_command(conn,users_table)
    execute_db.execute_database_command(conn,tweets_table)
    conn.commit()
    conn.close()
def delete_db():
    conn = make_connection('dbs_scripts/database_login.json')
    delete_db = create_database.delete_database()
    execute_db.execute_database_command(conn,delete_db)
    conn.commit()
    conn.close()

def make_connection(filename):
    settings = json.load(open(filename))
    conn = get_data_from_database.connect_to_database(settings['database_location'],settings['database_user'],settings['database_name'])
    return conn

def add_tweets_to_db(tweets):
    final_tweets = []
    for tweet in tweets:
        final_tweets.append([tweet.id,tweet.text,tweet.creator_id,tweet.created_at,tweet.likes,tweet.retweets,tweet.replies])
    conn = make_connection('dbs_scripts/database_login.json')
    write_tweets = write_and_read_to_database.make_write_to_db(['id','text','creator_id','created_at','likes','retweets','replies'],'tweets',final_tweets)
    [conn,cur] = execute_db.execute_database_command(conn,write_tweets[0],write_tweets[1])
    final = cur.rowcount
    conn.commit()
    conn.close()
    return final

def get_tweet_data(conn,tweet_id):
    find_tweet = write_and_read_to_database.get_from_where_db('tweets','id',tweet_id)
    [conn,tweet_data] = execute_db.execute_database_command(conn,find_tweet)
    try:
        tweet_data.fetchone()
        conn.close()
        return tweet_data
    except:
        conn.close()
        return None

def add_user_to_db(id,username,oauth2_long_term,last_updated_likes,followers,following,posts,likes,active,access_token,refresh_token,verified,bio,url,profile_image,created_at,updated_at,protected,relevant_tweets,expires_at):
    user_values = ('id','username','oauth2_long_term','last_updated_likes','followers','following','posts','likes','active','access_token','refresh_token','verified','bio','url','profile_image','created_at','updated_at','protected','relevant_tweets','access_token_expiry')
    user_data = (id,username,oauth2_long_term,last_updated_likes,followers,following,posts,likes,active,access_token,refresh_token,verified,bio,url,profile_image,created_at,updated_at,protected,relevant_tweets,str(expires_at))
    write_user = write_and_read_to_database.make_write_to_db(user_data,'users',user_values)
    conn = make_connection('dbs_scripts/database_login.json')
    [conn,cur] = execute_db.execute_with_data(conn,write_user[0],write_user[1])
    final = cur.rowcount
    conn.commit()
    conn.close()
    return final

def get_user_data(user_id):
    conn = make_connection('dbs_scripts/database_login.json')
    find_user = write_and_read_to_database.get_from_where_db('users','id',user_id)
    [conn,user_data] = execute_db.execute_database_command(conn,find_user)
    try:
        user_data = user_data.fetchone()
        conn.close()
        return user_data
    except:
        try:
            conn.close()
            return None
        except:
            return None
    
def update_tokens_in_db(tokens,id):
    useful_tokens = ['access_token','refresh_token','access_token_expiry']
    useful_tokens_values = [tokens['access_token'],tokens['refresh_token'],str(tokens['expires_at'])]
    conn = make_connection('dbs_scripts/database_login.json')
    update_tokens = write_and_read_to_database.make_update('users',useful_tokens,useful_tokens_values,'id',id)


def convert_to_utc(date):
    return datetime.datetime.strftime(date,'%Y-%m-%d %H:%M:%S')