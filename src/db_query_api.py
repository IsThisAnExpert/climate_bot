import MySQLdb.cursors
import pandas as pd
import argparse
from argparse import RawTextHelpFormatter
from os.path import expanduser
from configobj import ConfigObj
import tweepy, time
from access import *  ## change `priv_access` to `access` with your API tokens


#  define args
parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=RawTextHelpFormatter)
parser.add_argument("-p", "--csv_file", help="path to the csv file with the twitter handles")
parser.add_argument("-d", "--mariadb_group", help="name of the MariaDB group on the `.my.cnf` config file with connection parameters")
parser.add_argument("-u", "--user_handle", help="user handle to query")

# get variables
args = parser.parse_args()
config_db = args.mariadb_group
user_handle = args.user_handle

## the config file for mariadb databases
config = (ConfigObj(expanduser('~/.my.cnf')))


# Setup API:
def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

    # Return API access:
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

    #     api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())
    return (api)

## main functions
## database connection
def connect(conf_db, database=""):
    """
    connect to db

    :param conf_db: the configuration name of the database in the config file
    :param database: database name
    :return: MySQLdb.connect object
    """

    return MySQLdb.connect(host=config[conf_db]['host'],
                           user=config[conf_db]['user'],
                           port=int(config[conf_db]['port']),
                           password=config[conf_db]['password'],
                           database=database)

db = connect(conf_db=config_db, database='hackathon')
c = db.cursor()

def fill_database(user):

    # IPCC_CH
    # GretaThunberg

    tables_list=['user', 'tweet', 'retweet']

    api=twitter_setup()
    tweets = api.user_timeline(screen_name=user,
                               # 200 is the maximum allowed count
                               count=200,
                               include_rts = True,
                               # Necessary to keep full_text
                               # otherwise only the first 140 words are extracted
                               tweet_mode = 'extended'
                               )
    user_data = api.get_user(user)
    created_at=user_data['created_at']
    user_id=user_data['id']

    #     dictionary for the columns insert statement
    tables_dic={}
    for table in tables_list:
        sql = f"DESCRIBE {table};"
        c.execute(sql)
        fetch_cols = c.fetchall()
        ## keep columns that are in the MySQL table
        column_names = [x[0] for x in fetch_cols]

        cols = ",".join([str(i) for i in column_names])
        tables_dic[table]=cols

    insert_vals=(user_id, user,'',created_at)
    sql = f'INSERT IGNORE INTO user ({tables_dic["user"]}) VALUES (%s,%s,"%s",%s);'
    # print((sql%insert_vals))
    c.execute(sql,insert_vals)

    for tweet in tweets:

        ## tweet variables
        created_at=tweet['created_at']
        tweet_id=tweet['id']  ## tweet_id
#         is_rt=tweet['retweeted'] ### does not work, gotta check why but
        if 'retweeted_status' in tweet:  ## but this works!
            is_rt=True
        else: is_rt=False

        tweet_text=tweet['full_text']  ## message of the tweet


        ## user variables
        user_id=tweet['user']['id']
#         created_at = user_id.created_at

        if 'media' in tweet['entities']:
            tweet_url=(tweet['entities']['media'][0]['url'])
        else:
            tweet_url=''


        ## table tweet#############################
        insert_vals_sql_tweet=(tweet_id,tweet_text,user_id,created_at,tweet_url,is_rt,user)
        sql_tweet = f'INSERT IGNORE INTO tweet ({tables_dic["tweet"]}) VALUES (%s,"%s",%s,"%s","%s",%s,%s);'
        # print(sql_tweet% insert_vals_sql_tweet)
        c.execute(sql_tweet,insert_vals_sql_tweet)

        if 'retweeted_status' in tweet:

            original_author=tweet['retweeted_status']['user']['id_str']
            retweeted_id=tweet['retweeted_status']['id_str']
#         else:
#             original_author=user_id
#             retweeted_id='?'

            insert_vals_rt=(tweet_id, 0, user_id, original_author)
            sql_retweet = f'INSERT IGNORE INTO retweet ({tables_dic["retweet"]}) VALUES (%s, %s,%s,%s);'
            print(sql_retweet% insert_vals_rt)
            c.execute(sql_retweet,insert_vals_rt)

    db.commit()

if args.user_handle:
    ## to insert just one user in the db
    fill_database(args.user_handle)

elif args.csv_file:
    files_path = args.csv_file
    twitter_handles = pd.read_csv(files_path)
    print(twitter_handles.head())

    count = 0
    # feed that db!!
    for i, row in twitter_handles.iterrows():
        count += 1
        import_user = (row[3][1:])
        fill_database(import_user)



