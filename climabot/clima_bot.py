#!/usr/bin/env python3.7
import tweepy
import sys
import os

# change `priv_access` to `access` with your API tokens
from climabot.access import *
import subprocess


# Setup API:
def twitter_setup():
    # Authenticate and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    auth.secure = True
    # Return API access:
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    return api


class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):

        if hasattr(status, "retweeted_status"):  # Check if Retweet
            try:
                print("rt", status["retweeted_status"]["extended_tweet"]["full_text"])
            except AttributeError:
                print(status["retweeted_status"]["text"])
        else:
            try:
                # catch nesting
                replied_to = status.in_reply_to_screen_name
                answer_user = status.user.screen_name
                answer_id = status.id
                #  ignore replies that by default contain mention
                # in_reply_to_status_id = status.in_reply_to_status_id
                in_reply_to_user_id = status.in_reply_to_user_id

                print(
                    replied_to,
                    "nesting",
                    in_reply_to_user_id,
                    "replied to",
                    replied_to,
                    "message",
                    status.full_text,
                )

            except AttributeError:

                replied_to = status.in_reply_to_screen_name
                answer_user = status.user.screen_name
                answer_id = status.id
                # in_reply_to_status_id = status.in_reply_to_status_id
                in_reply_to_user_id = status.in_reply_to_user_id

                print(
                    replied_to,
                    "after atrib error",
                    in_reply_to_user_id,
                    "replied to",
                    replied_to,
                    "message",
                    status.full_text,
                )

            status_var = f"{answer_user},{replied_to},{answer_id}"

            with open("hold_that_tweet.txt", "w") as tf:
                tf.write(status_var)
            with open("hold_that_tweet.txt", "r") as tf:
                contents = tf.read()

                queried_user = contents.split(",")[1]
                # added for Paul's tool
                cred_score = check_cred_score(queried_user, cred_tool_path)

            update_status = (
                f"Thanks for calling me,"
                f" according to our calculations @{queried_user} "
                f"has a credibility score of {cred_score}. "
                f"to learn more visit https://bit.ly/3jSUTyJ"
            )

            # set the scores here
            # if score <= 5:
            #     update_status=f"Thanks for calling me, soon you will know if @{contents.split(',')[1]} has a {score} in our database. to learn more visit https://bit.ly/3jSUTyJ"
            # elif score > 5:
            #     update_status=f"Thanks for calling me,soon you will know if @{contents.split(',')[1]} has a {score} in our database. to learn more visit https://bit.ly/3jSUTyJ"
            # else:
            #     update_status=f"Thanks for calling me,soon you will know if @{contents.split(',')[1]} has a {score} in our database. to learn more visit https://bit.ly/3jSUTyJ"

            # don't reply to yourself!!
            if status.in_reply_to_user_id != 1319577341056733184:

                api.update_status(
                    update_status,
                    in_reply_to_status_id=contents.split(",")[2],
                    auto_populate_reply_metadata=True,
                )

    def on_error(self, status):
        print(status)


def check_cred_score(query_user, cred_tool_path):

    """
    try to run the credibility score java tool for a user.
    If that user does not exist on the db,
    inserts it into the database by calling `db_query_api.py`
    and runs the tool again.

    :param query_user: user to be queried from the hackathon database
    :param cred_tool_path: path to Pauls credibility score tool
    :return: a credibility score for a given user
    """

    # added for Paul's tool
    cred_score_cmd = [
        "java",
        "-jar",
        f"{cred_tool_path}",
        "--calculate-score",
        f"{query_user}",
    ]
    proc = subprocess.Popen(cred_score_cmd, stdout=subprocess.PIPE)
    stdout = proc.stdout.read().decode("utf-8")
    print(stdout, type(stdout))

    try:
        cred_score = float(stdout.rstrip())
    except ValueError:
        # if does not exist, insert user in the database
        insert_unknown_user = [
            "db_query_api.py",
            "-d",
            "clima_botdb",
            "-u",
            f"{query_user}",
        ]
        subprocess.call(insert_unknown_user, stdout=subprocess.PIPE)
        proc = subprocess.Popen(cred_score_cmd, stdout=subprocess.PIPE)
        cred_score = float(proc.stdout.read().decode("utf-8").rstrip())
    print(cred_score)
    return cred_score


def display_help():
    """Show available commands."""
    print("Syntax: python {} [command path]".format(sys.argv[0]))
    print()
    print(" Arguments:")
    print("    start  Starts the climaBot")
    print("    path   Path to the java-credibility-tool")
    print("    help   Show this help screen")


if __name__ == "__main__":
    if len(sys.argv) > 2:
        if sys.argv[1].lower() == "start":

            if os.path.isfile(sys.argv[2]):
                cred_tool_path = sys.argv[2]
            else:
                raise IOError("Credibility score tool path not found")

            api = twitter_setup()
            myStreamListener = MyStreamListener()
            myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
            myStream.filter(track=["@isthisanexpert"], is_async=True)
    else:
        display_help()
