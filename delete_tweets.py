import tweepy
import logging
from typing import List
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

def authenticate_to_twitter(api_key: str, api_key_secret: str, access_token: str, access_token_secret: str) -> tweepy.Client:
  """
  Authenticate to the Twitter API using the provided credentials.

  Args:
    api_key (str): API key associated with X developer project
    api_key_secret (str): API key secret associated with X developer project
    access_token (str): access token associated with X developer account
    access_token_secret (str): access token secret associated with X developer account

  Returns:
    tweepy.Client: an authenticated Tweepy Client object
  """

  client = tweepy.Client(
    consumer_key=api_key,
    consumer_secret=api_key_secret,
    access_token=access_token,
    access_token_secret=access_token_secret,
  )

  return client

def load_tweets(file_path: Path) -> List[str]:
  """
  Read file containing tweet IDs and load to list object.

  Args:
    file_path (Path): path object to file containing tweet IDs

  Returns:
    List[str]: list of tuples representing tweet IDs and deletion status
  """
  with open(file_path, 'r') as f:
    tweet_list = [line.strip().split(',') for line in f]

  return tweet_list

def save_tweet_statuses(file_path: Path, tweet_list: List[str]) -> None:
  """
  Write tweet IDs and deletion status to tracking file.

  Args:
    file_path (Path): path object to file containing tweet IDs
    tweet_list (List[str]): list of tweet IDs and statuses to write
  """
  with open(file_path, 'w') as f:
    for tweet_id, status in tweet_list:
      f.write(f'{tweet_id},{status}\n')

def delete_tweets(client: tweepy.Client, tweet_list: List[str]) -> None:
  """
  Delete up to 50 tweets based on pending status.

  Args:
    client (tweepy.Client): the authenticated Tweepy Client object.
    tweet_list (List[str]): a list of tweet IDs to be deleted.
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

if __name__ == '__main__':
  # read environment variables
  load_dotenv()
  API_KEY = os.getenv('API_KEY')
  API_KEY_SECRET = os.getenv('API_KEY_SECRET')
  ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
  ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
  TRACKER_FILE_PATH = Path(os.getenv('TRACKER_FILE_PATH'))

  # authenticate
  client = authenticate_to_twitter(API_KEY, API_KEY_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

  # delete tweets
  tweet_list = load_tweets(TRACKER_FILE_PATH)
  tweet_list = delete_tweets(client, tweet_list)
  save_tweet_statuses(TRACKER_FILE_PATH, tweet_list)

