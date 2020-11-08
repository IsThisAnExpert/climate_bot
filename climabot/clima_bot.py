#!/usr/bin/env python3.7
import tweepy
import sys
from climabot.access import * ## change `priv_access` to `access` with your API tokens
import subprocess


# Setup API:
def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
#     auth.secure = True
    # Return API access:
    api = tweepy.API(auth,parser=tweepy.parsers.JSONParser())
    return api


class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):

        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                print('rt',status['retweeted_status']['extended_tweet']["full_text"])
            except AttributeError:
                print(status['retweeted_status']['text'])
        else:
            try:
                ## catch nesting
                replied_to=status.in_reply_to_screen_name
                answer_user=status.user.screen_name
                answer_id=status.id
                ## ignore replies that by default contain mention
                in_reply_to_status_id=status.in_reply_to_status_id
                in_reply_to_user_id=status.in_reply_to_user_id

                print(replied_to, in_reply_to_status_id,
in_reply_to_user_id)

            except AttributeError:

                replied_to=status.in_reply_to_screen_name
                answer_user=status.user.screen_name
                answer_id=status.id
                in_reply_to_status_id=status.in_reply_to_status_id
                in_reply_to_user_id=status.in_reply_to_user_id

            status_var=f"{answer_user},{replied_to},{answer_id}"

            with open('hold_that_tweet.txt', 'w') as tf:
                tf.write(status_var)
            with open('hold_that_tweet.txt', 'r') as tf:
                contents = tf.read()

            ## add for Paul's tool
                proc = subprocess.Popen(['echo', '0'], stdout=subprocess.PIPE)
                score = int(proc.stdout.read().decode("utf-8"))

            # set the scores here
            if score <= 5:
                update_status=f"Thanks for calling me, soon you will know if @{contents.split(',')[1]} has a {'-SCORE-'} in our database. to learn more visit https://bit.ly/3jSUTyJ"
            elif score > 5:
                update_status=f"Thanks for calling me,soon you will know if @{contents.split(',')[1]} has a {'-SCORE-'} in our database. to learn more visit https://bit.ly/3jSUTyJ"
            else:
                update_status=f"Thanks for calling me,soon you will know if @{contents.split(',')[1]} has a {'-SCORE-'} in our database. to learn more visit https://bit.ly/3jSUTyJ"

            # don't repty to yourself!!
            if status.in_reply_to_user_id != 1319577341056733184:

                api.update_status(update_status,in_reply_to_status_id=contents.split(',')[2],
                auto_populate_reply_metadata=True,)


    def on_error(self, status):
        print(status)

def display_help():
    """Show available commands."""
    print("Syntax: python {} [command]".format(sys.argv[0]))
    print()
    print(" Commands:")
    print("    start    Starts the ClimaBot")
    print("    help   Show this help screen")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1].lower() == "start":
            api=twitter_setup()
            myStreamListener = MyStreamListener()
            myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
            myStream.filter(track=['@isthisanexpert'], is_async=True)
        else:
            display_help()
