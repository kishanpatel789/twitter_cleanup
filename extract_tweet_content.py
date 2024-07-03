import json
import re
import argparse
import csv

def extract_tweet_content(js_file_path: str) -> None:
  """
  Extracts tweet IDs and text from a given tweets.js file and saves them to a text file.

  Parameters:
  - js_file_path (str): The file path to the tweets.js file.

  Returns:
  - None: Outputs a file named 'tweet_content.csv' with one tweet per line.
  """
  try:
    # read tweets.js file
    with open(js_file_path, 'r') as f:
      content = f.read()

    # isolate JSON objects and load content
    json_str = re.sub(r'window\.YTD\.tweets\.part\d+\s*=\s*', '', content)
    tweets_data = json.loads(json_str)

    # extract tweet ID and content
    tweet_info = [(tweet['tweet']['id'], tweet['tweet']['full_text']) for tweet in tweets_data]

    # save the tweet ids to file
    output_file_name = 'tweet_content.csv'
    with open(output_file_name, 'w', newline='', encoding='utf-8') as f:
      writer = csv.writer(f, quoting=csv.QUOTE_ALL)
      for tweet_id, tweet_text in tweet_info:
        writer.writerow([tweet_id, tweet_text])

    print(f"Tweet IDs and text have been extracted to '{output_file_name}'.")

  except Exception as e:
    print(f"An error occurred: {e}")


if __name__ == "__main__":
  js_file_path_default = './twitter-archive/data/tweets.js'

  parser = argparse.ArgumentParser(
    description='Extracts tweet IDs and content from Twitter archive',
  )  
  parser.add_argument(
    '--file_name',
    default=js_file_path_default,
    help="path to file 'tweets.js', which contains tweet objects for archive",
    required=False,
  )
  args = parser.parse_args()

  extract_tweet_content(args.file_name)
