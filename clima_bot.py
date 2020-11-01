import csv, time
import tweepy
import json,ast
from priv_access import * ## change `priv_access` to `access` with your API tokens

IGNORE_ERRORS = [327]

# Setup API:
def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    # Return API access:
    api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())
    return (api)


class MyStreamListener(tweepy.StreamListener):
        
    def on_data(self, data):
        # Decode the JSON data
        tweet = json.load(data)
        # Print out the Tweet
        print((tweet['user']['screen_name'], tweet['text']))

        with open('hold_that_tweet.csv','a') as f:
                f.write(tweet['user']['screen_name'], tweet['text'])
#         except:
#             pass

    def on_error(self, status):
        print(status)

        
        
api=twitter_setup()
myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

# if __name__ == '__main__':
#     listener = PrintListener()

# Using readlines() 

# count = 0
# Strips the newline character 

def auto_replies(twit_log_file):
    file1 = open(twit_log_file, 'r') 
    Lines = file1.readlines() 

#     score=10
    for line in Lines: 
        tweet=(json.loads(line)) 
        replied_to=(tweet['quoted_status']['user']['screen_name'])
        answer_user=(tweet['user']['screen_name'])
        answer_id=tweet['id']

        ## set the scores here
        if score <= 5:
            pass
        elif score <= 5:
            pass
        else:
            pass

        update_status=f'@{answer_user} this is an expert you can trust!\n@{replied_to} has a score of {"$SCORE"}in our database\nto learn more visit bit.ly/test'
        try:

            api.update_status(update_status,answer_id)
            print(update_status)

        except tweepy.TweepError as e:
            continue

myStream.filter(track=['@IsThisAnExpert'], is_async=True)

while 1:
    try:
        time.sleep(3)
        auto_replies('hold_that_tweet.csv')
    except tweepy.TweepError as e:
        pass
    
# myStream.disconnect()
