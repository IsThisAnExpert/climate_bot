# :seedling: @IsThisAnExpert: The ClimateChange Hackathon bot!

It can be difficult for the average user of a social media platform to identify if a post on the climate crisis is based on a reliable source or misinformation. As a consequence, erroneous ‘news’ are reproduced or go viral. Some users even intentionally mislead the internet community. This behaviour can cause confusion in raising awareness and taking action on the climate crisis.
`@IsThisAnExpert` is a Twitter bot that helps users see the credibility of another user on the climate crisis. Reply to a post on climate change to `@IsThisAnExpert` and it will run an assessment on the credibility of the user and their expertise on climate change. Created for the [ClimateChange Hackaton](https://www.goethe.de/prj/one/en/gea/for/clc.html) in frame of the [GENERATION A ](https://www.goethe.de/prj/one/en/gea.html) — project.

## What it does

1. Parses a manually curated list of experts and assigns a credibility score following a *credibility score* equation (see below).
2. Populates a MariaDB database with relevant user information.
3. Opens a stream on Twitter to hear any post with an `@IsThisAnExpert` mention.
4. Calculates the credibility score for the user posting the message where the bot is called.*
5. Replies to the mention with a message with the credibility score of the person.

## Credibility score

A user’s credibility score is calculated by tweets and retweets of credible sources. A scientist affiliated with the IPCC, a reputable institution, many publications and citations (therefore a high h-index) will have a high credibility score. A random user that has frequently retweeted the IPCC report will be assigned with a higher credibility score than Donald Trump who does not make references to credible sources.


###### \*on development, currently calculates the *cred_score* for the users on the curated list


## Install

0. Install required tools (developed on Fedora 32 unix distribution)
    * `sudo yum install python3-devel mysql-devel gcc`
1. Create a Twitter application, and generate keys, tokens etc. 
2. Modify the variables in the access.py file and add keys, tokens etc. for connecting to your Twitter app.
3. Install the [`java-credibility-tool`](https://github.com/IsThisAnExpert/java-credibility-tool) 
4. Download or git clone the **clima_bot**:
    * `git clone https://github.com/franasa/clima_bot`
5. Install the **climabot**:
    * cd into `climabot` and run `pip install .`

## Requirements

* `~/.my.cnf` file with database connection parameters
* Python 3+
* Twitter developer account
* Java JRE 8
* MySQL/MariaDB

## Usage

### database 

Script to populate a MySQL/MariaDB with Twitter handles of a manually parsed list of experts.

usage: 
* `db_query_api.py [-h] [-p CSV_FILE] [-d MARIADB_GROUP] [-u USER_HANDLE]`

arguments:

* `-h, --help `          
show help message and exit

* `-d MARIADB_GROUP, --mariadb_group`     
name of the MariaDB group on the `.my.cnf` config file with connection parameters

* `-p CSV_FILE, --csv_file`
path to the csv file with the twitter handles

* `-u USER_HANDLE, --user_handle`
use to query/insert one user handle at a time

note : `-p` and `-u` are mutually exclusive arguments.


### running the bot

Main script of the **climabot** to automatically reply to mentions with the calculated credibility score

usage: 
* `clima_bot.py  [start] [path]`

positional arguments:

* `start`
   start the bot

* `path`
 path to the java-credibility-tool

to deploy the bot for automatically reply any mention run:

```bash
$ clima_bot.py  start <path>/credibility-0.0.7.jar
```

:tada:
