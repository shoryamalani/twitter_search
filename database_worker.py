from dbs_scripts import get_data_from_database,create_database,execute_db,write_and_read_to_database
import json
import psycopg2

def set_up_db():
    conn = make_connection('dbs_scripts/database_login.json')
    users_table =create_database.create_table_command('users',[('id','int PRIMARY KEY'),('username','varchar'),('oauth2_long_term','varchar'),('last_updated_likes','TIMESTAMP'),('followers','int'),('following',"int"),('posts','int'),('likes','int'),('active','int'),('access_token','varchar'),('refresh_token','varchar'),('verified','BOOLEAN'),('bio','varchar'),('url','varchar'),('profile_image','varchar'),('created_at','TIMESTAMP'),('updated_at','TIMESTAMP'),('protected',"BOOLEAN")])
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
    final = cur.get_result()
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

def add_user_to_db(id,username,oauth2_long_term,last_updated_likes,followers,following,posts,likes,active,access_token,refresh_token,verified,bio,url,profile_image,created_at,updated_at,protected):
    user_values = ('id','username','oauth2_long_term','last_updated_likes','followers','following','posts','likes','active','access_token','refresh_token','verified','bio','url','profile_image','created_at','updated_at','protected')
    user_data = (id,username,oauth2_long_term,last_updated_likes,followers,following,posts,likes,active,access_token,refresh_token,verified,bio,url,profile_image,created_at,updated_at,protected)
    write_user = write_and_read_to_database.make_write_to_db(user_values,'users',user_data)
    conn = make_connection('dbs_scripts/database_login.json')
    [conn,cur] = execute_db.execute_database_command(conn,write_user[0],write_user[1])
    final = cur.get_result()
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
    

    