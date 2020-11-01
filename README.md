# :robot: Bot, what a concept! 

Built on top of @peterdalle's [Twitterbot](https://github.com/peterdalle/twitterbot), uses `tweepy` instead of `twython` and adds further functionality: 

* reads and parses a list of RSS feeds. Posts its title and links to a Twitter account.
* retweets previous post after a determined time. 
* searches tweets for keywords or hashtags and retweet those tweets.
* retweets the most up-voted and retweeted posts from a given distribution list.
* schedule jobs for any of the above 

All functions can be used independently.

## Install

1. Download or git clone Twitterbot:
   - `git clone https://github.com/franasa/bot_what_a_concept`
2. Install dependencies:
   - `pip install feedparser`
   - `pip install tweepy`
   - `pip install schedule`
3. Create a [Twitter application](https://apps.twitter.com/), and generate keys, tokens etc.
4. Modifiy the settings in the source code.
   - Modify `feed_urls` to add the RSS feeds you want to read.
   - Modify the variables in the `access.py` file and add keys, tokens etc. for connecting to your Twitter app.
   - Modify `retweet_include_words` for keywords you want to search and retweet, and `retweet_exclude_words` for keywords you would like to exclude from retweeting. For example `retweet_include_words = ["foo"]` and `retweet_exclude_words = ["bar"]` will include any tweet with the word "foo", as long as the word "bar" is absent. This list can also be left empty, i.e. `retweet_exclude_words = []`.
   - Modify OR add jobs to the `scheduled_job()` function.
## Requirements

* Python 3+
* Twitter account

## Usage

Read the RSS feeds and post to Twitter account:

```bash
$ python d_what_a_c.py rss   
```

Search globally for tweets and retweet them:

```bash
$ python d_what_a_c.py rtg
```
Search for tweets within a Twitter list and retweet them:

```bash
$ python d_what_a_c.py rtl
```
Retweet last own tweet:

```bash
$ python d_what_a_c.py rto 
```
## :tada: Run scheduled jobs on infinite loop:

[Here](https://schedule.readthedocs.io/en/stable/) you can learn how set up tasks for the the `scheduled_job()` function

There are some nice free cloud solutions such as [pythonanywhere](https://www.pythonanywhere.com/), where you can start a console and leave the script running:

```bash
$ python d_what_a_c.py  sch
```

Take a look at a slightly controversial [example bot](https://twitter.com/drug_papers).

:green_heart:

