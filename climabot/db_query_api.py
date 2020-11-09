#!/usr/bin/env python3
import MySQLdb.cursors
import pandas as pd
import argparse
from argparse import RawTextHelpFormatter
from os.path import expanduser
from configobj import ConfigObj
import tweepy, time
from datetime import datetime
from climabot.access import *  ## change `priv_access` to `access` with your API tokens


#  define args
parser = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=RawTextHelpFormatter)
group = parser.add_mutually_exclusive_group(required=True) ## add mutually exclusive required args
parser.add_argument("-d", "--mariadb_group", help="name of the MariaDB group on the `.my.cnf` config file with connection parameters",required=True)
group.add_argument("-u", "--user_handle", help="user handle to query")
group.add_argument("-f", "--csv_file", help="path to the csv file with the twitter handles to parse in the first (0) column")

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
    ## convert to datetime
    created_at = datetime.strftime(datetime.strptime(user_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y'), '%Y-%m-%d %H:%M:%S')
    user_id=user_data['id']

    # dictionary for the columns insert statement
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
        tweet_text=tweet['full_text']  ## message of the tweet
        ## check if is rt
        if 'retweeted_status' in tweet:
            is_rt=True
        else: is_rt=False

        ## table tweet#############################
        insert_vals_sql_tweet=(tweet_id,tweet_text,user_id,created_at,is_rt,user)
        sql_tweet = f'INSERT IGNORE INTO tweet ({tables_dic["tweet"]}) VALUES (%s,"%s",%s,%s,%s,%s);'
        # print(sql_tweet% insert_vals_sql_tweet)
        c.execute(sql_tweet,insert_vals_sql_tweet)

        ## if is a retweet insert all data from the original tweet(user and tweet info)
        if is_rt:
            ## retweeted user
            original_author_id=tweet['retweeted_status']['user']['id_str']
            original_author_screen = tweet['retweeted_status']['user']['screen_name']
            original_author_created = tweet['retweeted_status']['user']['created_at']
            # retweeted_id=tweet['retweeted_status']['id_str']
            insert_vals = (original_author_id, original_author_screen, '', original_author_created)
            sql = f'INSERT IGNORE INTO user ({tables_dic["user"]}) VALUES (%s,%s,"%s",%s);'
            # print((sql%insert_vals))
            c.execute(sql, insert_vals)

            ## retweeted tweet info
            original_created_at=tweet['retweeted_status']['created_at']
            original_tweet_id = tweet['retweeted_status']['id']
            original_tweet_text = tweet['retweeted_status']['full_text']
            ## insert in table tweet #############################
            insert_vals_sql_tweet = (original_tweet_id, original_tweet_text, original_author_id, original_created_at, False, original_author_screen)
            sql_tweet = f'INSERT IGNORE INTO tweet ({tables_dic["tweet"]}) VALUES (%s,"%s",%s,"%s",%s,%s);'
            # print(sql_tweet% insert_vals_sql_tweet)
            c.execute(sql_tweet, insert_vals_sql_tweet)

            ## insert in table retweet
            ## insert who retweeted @greta; their id, greta_id; and the original tweet_id, original_tweet_id
            insert_vals_rt=(tweet_id, user_id, original_tweet_id)
            sql_retweet = f'INSERT IGNORE INTO retweet ({tables_dic["retweet"]}) VALUES (%s,%s,%s);'
            # print(sql_retweet% insert_vals_rt)
            c.execute(sql_retweet,insert_vals_rt)

    db.commit()

if args.user_handle:
    ## to insert just one user in the db
    fill_database(args.user_handle)

elif args.csv_file:
    ## to insert all users from a csv
    files_path = args.csv_file
    twitter_handles = pd.read_csv(files_path)

    count = 0
    # feed that db!!
    for i, row in twitter_handles.iterrows():
        count += 1
        import_user = (row[0][1:])
        print(import_user)
        fill_database(import_user)



