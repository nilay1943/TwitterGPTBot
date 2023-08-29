import os
import tweepy

def split_into_tweets(content, max_length=270):
    tweets = []

    while len(content) > 0:
        if len(content) > max_length:
            split_index = content[:max_length].rfind(' ')
            if split_index == -1:
                split_index = max_length
            tweet = content[:split_index]
            content = content[split_index:].strip()
        else:
            tweet = content
            content = ''

        tweets.append(tweet)

    return tweets


def post_tweet(tweet_content):
    tweets = split_into_tweets(tweet_content)

    client = tweepy.Client(consumer_key=os.environ.get('T_CONSUMER_KEY'),
                           consumer_secret=os.environ.get('T_CONSUMER_SECRET'),
                           access_token=os.environ.get('T_ACCESS_KEY'),
                           access_token_secret=os.environ.get('T_ACCESS_SECRET'))

    previous_tweet_id = None
    for index, tweet in enumerate(tweets, start=1):

        if len(tweets) > 1:
            tweet = f"({index}/{len(tweets)}) {tweet}"
        print(tweet)
        response = client.create_tweet(text=tweet, in_reply_to_tweet_id=previous_tweet_id)
        previous_tweet_id = response[0]['id']
