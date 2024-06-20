# %%
import tweepy
from dotenv import load_dotenv
import os
from pathlib import Path
# %%
load_dotenv()
API_KEY = os.getenv('API_KEY')
API_KEY_SECRET = os.getenv('API_KEY_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
FILE_PATH = Path(os.getenv('TRACKER_FILE_PATH'))
# %%
client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_KEY_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)
# %%
client.get_all_tweets_count(query='test')
# %%
client.get_tweet(869239907578990593)
# %%
message = "Hello Twitter"
client.create_tweet(text=message)
# 1802804055950901252
# %%
client.delete_tweet(1802804055950901252)
# %%
# get list of tweets from archive
import json
# %%
with open('./twitter-archive/data/tweets.js') as f:
    tweet_data = json.load(f)
# %%
with open(FILE_PATH, 'r') as file:
    lines = [line.strip().split(',') for line in file]

# %%
with open('./tweet_tracker_updated.csv', 'w') as f:
    for tweet_id, status in lines:
        f.write(f'{tweet_id},{status}\n')
# %%
