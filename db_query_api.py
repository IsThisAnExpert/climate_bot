import MySQLdb.cursors
import pandas as pd

twitter_handles=pd.read_csv('TwitterHandles.csv')
display(twitter_handles.head())
## database connection
db = MySQLdb.connect(host='',
                               user='hackathon',
                               port=(3306),
                               password='',
                               database='')

c = db.cursor()

def fill_database(user):

    # IPCC_CH
    # GretaThunberg

    tables_list=['new_retweet', 'new_tweet', 'new_user']



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
    print(created_at)
    user_id=user_data['id']


    tables_dic={}
#     dictionary for the columns insert statement 
    for table in tables_list:
        sql = f"DESCRIBE {table};"
        c.execute(sql)
        fetch_cols = c.fetchall()
        ## keep columns that are in the MySQL table
        column_names = [x[0] for x in fetch_cols]

        cols = ",".join([str(i) for i in column_names])
        tables_dic[table]=cols

    insert_vals=(user_id, user,'',created_at)
    sql = f'INSERT IGNORE INTO new_user ({tables_dic["new_user"]}) VALUES (%s,%s,"%s",%s);'
    # print((sql%insert_vals))
#     c.execute(sql,insert_vals)

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
#         print(created_at)
        insert_vals_sql_tweet=(tweet_id,tweet_text,user_id,created_at,tweet_url,is_rt,user)
        sql_tweet = f'INSERT IGNORE INTO new_tweet ({tables_dic["new_tweet"]}) VALUES (%s,"%s",%s,"%s","%s",%s,%s);'

#         print(sql_tweet% insert_vals_sql_tweet)
        c.execute(sql_tweet,insert_vals_sql_tweet)

#         if is_rt == 1:

        if 'retweeted_status' in tweet:

            original_author=tweet['retweeted_status']['user']['id_str']
            retweeted__id=tweet['retweeted_status']['id_str']
#         else:
#             original_author=user_id
#             retweeted__id='?'

            insert_vals_rt=(tweet_id, 0, user_id, original_author)
            sql_retweet = f'INSERT IGNORE INTO new_retweet ({tables_dic["new_retweet"]}) VALUES (%s, %s,%s,%s);'
    #         print(sql% insert_vals_rt)
#             c.execute(sql_retweet,insert_vals_rt)



    db.commit()
