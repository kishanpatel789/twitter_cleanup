import tweepy
import logging
from typing import List, NoReturn
from dotenv import load_dotenv
import time
import os
from pathlib import Path


# configure logging
logger = logging.getLogger('tweet_deletion')
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler('deletion_log.txt')
console_handler = logging.StreamHandler()

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

def authenticate_to_twitter(api_key: str, api_secret: str, access_token: str, access_token_secret: str) -> tweepy.Client:
    """
    Authenticate to the Twitter API using the provided credentials.

    Parameters:
    - api_key (str): The API key obtained from the Twitter developer account.
    - api_secret (str): The API secret obtained from the Twitter developer account.
    - access_token (str): The access token obtained from the Twitter developer account.
    - access_token_secret (str): The access token secret obtained from the Twitter developer account.

    Returns:
    - tweepy.Client: An authenticated Tweepy Client object.
    """

    client = tweepy.Client(
        consumer_key=API_KEY,
        consumer_secret=API_KEY_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET,
    )

    return client

def load_tweets(file_path):
    with open(file_path, 'r') as f:
        tweet_list = [line.strip().split(',') for line in f]

    return tweet_list

def save_tweet_statuses(file_path, tweet_list):
    with open(file_path, 'w') as f:
        for tweet_id, status in tweet_list:
            f.write(f'{tweet_id},{status}\n')

def delete_tweets(client: tweepy.Client, tweet_list: List[str]) -> NoReturn:
    """
    Delete tweets based on a list of tweet IDs.

    Parameters:
    - client (tweepy.Client): The authenticated Tweepy Client object.
    - tweet_ids (List[str]): A list of tweet IDs to be deleted.

    Returns:
    - NoReturn
    """
    deleted_count = 0
    for tweet in tweet_list:
        tweet_id, status = tweet
        if status == 'pending' and deleted_count < 50:
            try:
                client.delete_tweet(tweet_id)
                logger.info(f"Deleted tweet {tweet_id}")
                tweet[1] = 'deleted'
                deleted_count += 1
            except tweepy.TooManyRequests:
                logger.error(f"Failed to delete tweet {tweet_id} due to too many requests")
                return tweet_list
            except tweepy.TweepyException as e:
                logger.error(f"Failed to delete tweet {tweet_id}: {e}")
            time.sleep(1)  # sleep to avoid hitting API rate limits

    return tweet_list

if __name__ == "__main__":
    # read environment variables
    load_dotenv()
    API_KEY = os.getenv('API_KEY')
    API_KEY_SECRET = os.getenv('API_KEY_SECRET')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
    FILE_PATH = Path(os.getenv('TRACKER_FILE_PATH'))

    # authenticate
    client = authenticate_to_twitter(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    # delete tweets
    tweet_list = load_tweets(FILE_PATH)
    tweet_list = delete_tweets(client, tweet_list)
    save_tweet_statuses(FILE_PATH, tweet_list)

