import json
import re
import argparse

def extract_tweet_ids(js_file_path: str) -> None:
  """
  Extracts tweet IDs from a given tweets.js file and saves them to a text file.

  Parameters:
  - js_file_path (str): The file path to the tweets.js file.

  Returns:
  - None: Outputs a file named 'tweet_ids.txt' with one tweet ID per line.
  """
  try:
    # read tweets.js file
    with open(js_file_path, 'r') as f:
      content = f.read()

    # isolate JSON objects and load content
    json_str = re.sub(r'window\.YTD\.tweets\.part\d+\s*=\s*', '', content)
    tweets_data = json.loads(json_str)

    # extract the tweet IDs
    tweet_ids = [tweet['tweet']['id'] for tweet in tweets_data]

    # save the tweet ids to file
    output_file_name = 'tweet_ids.csv'
    with open(output_file_name, 'w') as f:
      for tweet_id in tweet_ids:
        f.write(f"{tweet_id},pending\n")

    print(f"Tweet IDs have been extracted to '{output_file_name}'.")

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  js_file_path_default = './twitter-archive/data/tweets.js'

  parser = argparse.ArgumentParser(
    description='Extracts tweet IDs from Twitter archive',
  )  
  parser.add_argument(
    '--file_name',
    default=js_file_path_default,
    help="path to file 'tweets.js', which contains tweet objects for archive",
    required=False,
  )
  args = parser.parse_args()

  extract_tweet_ids(args.file_name)
