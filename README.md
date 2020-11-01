# :seedling: @IsThisAnExpert: The ClimateChange Hackathon bot!

It can be difficult for the average user of a social media platform to identify if a post on the climate crisis is based on a reliable source or misinformation. As a consequence, erroneous ‘news’ are reproduced or go viral. Some users even intentionally mislead the internet community. This behaviour can cause confusion in raising awareness and taking action on climate crisis.
`@IsThisAnExpert` is a Twitter bot that helps users see the credibility of another user on the climate crisis. Retweet a post on climate change to @IsThisAnExpert and it will run an assessment on the credibility of the user and their expertise on climate change. Created for the [ClimateChange Hackaton](https://www.goethe.de/prj/one/en/gea/for/clc/ag.html) in frame of the [GENERATION A ](https://www.goethe.de/prj/one/en/gea.html) — project.

## What it does 

1. Parses a manully curated list of experts an assigns a credibility score following this equation {see *credibility score* below}.
2. Populates a MariaDB database with relevant tweet information {description}
3. Hears a twitter stream for any tweet with the `@IsThisAnExpert` mention. 
4. Calclulates the credibility score for the tweet of the user calling the bot.
5. Replies to the mention* with a message with the credibility score of the person. 

## Credibility score

A user’s credibility score is calculated by tweets and retweets of credible sources. A scientist affiliated with the IPCC, a reputable institution, many publications and citations (therefore a high h-index) will have a high credibility score. A random user that has frequently retweeted the IPCC report will be assigned with a higher credibility score than Donald Trump who does not make references to credible sources.
 

###### * right now only can answer to retweets with a quouted reply calling it (further dev: answer to tweet replies)

## Install

tbd, but similar as https://github.com/franasa/bot_what_a_concept

## Requirements

* Python 3+
* Twitter account

## Usage

Enter the infinite loop:tada: :

```bash
$ python d_what_a_c.py  start
```


There are some nice free cloud solutions such as [pythonanywhere](https://www.pythonanywhere.com/), where you can start a console and leave the script running:



:green_heart:

