import json
import re

def extract_tweet_ids(js_file_path: str) -> None:
    """
    Extracts tweet IDs from a given tweets.js file and saves them to a text file.

    Parameters:
    - js_file_path (str): The file path to the tweets.js file.

    Returns:
    - None: Outputs a file named 'tweet_ids.txt' with one tweet ID per line.
    """
    try:
        # Read the contents of the tweets.js file
        with open(js_file_path, 'r') as f:
            content = f.read()

        # Remove the JavaScript variable assignment to isolate the JSON part
        json_str = re.sub(r'window\.YTD\.tweets\.part\d+\s*=\s*', '', content)

        # Load the JSON content
        tweets_data = json.loads(json_str)

        # Extract the tweet IDs
        tweet_ids = [tweet['tweet']['id'] for tweet in tweets_data]

        # Save the tweet IDs to a text file
        output_file_name = 'tweet_ids.csv'
        with open(output_file_name, 'w') as f:
            f.write("tweet_id,status\n")
            for tweet_id in tweet_ids:
                f.write(f"{tweet_id},pending\n")

        print(f"Tweet IDs have been extracted to '{output_file_name}'.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    js_file_path = './twitter-archive/data/tweets.js'  # Replace with the path to your tweets.js file
    extract_tweet_ids(js_file_path)
