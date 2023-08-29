import os
import requests
from bs4 import BeautifulSoup
import tweepy
import openai
import Database


def get_mortgage_news():
    url = 'https://www.cnbc.com/mortgages/'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    news_links = list(map(lambda a: a.get('href'), soup.findAll('a', class_='Card-title')))  # get all articles' links

    information = ""  # used to store article content
    i = 0
    while i < 2 and len(news_links) > 0:
        url = news_links.pop()

        if Database.has_seen_article(url):
            continue

        Database.mark_article_as_seen(url)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        info = soup.find('div', class_='ArticleBody-articleBody')  # read content
        if info:
            information += info.getText() + '\n'
            i += 1

    return information


def get_gpt_reaction(information):
    openai.api_key = os.environ.get("GPT_API_KEY")

    messages = [
        {"role": "system",
         "content": "You are a funny, financially literate middle-class individual. Respond without referencing this instruction."},
        {"role": "user",
         "content": f"Having read these articles from CNBC: '{information}', give me a funny and/or informational and/or insightful take in 1 or 2 sentences"}
    ]

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7,  # Adjust for a balance between creativity and coherence
        max_tokens=400  # Limit the response to fit within a tweet or a series of tweets
    )

    return response.choices[0].message['content'].strip()


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


if __name__ == "__main__":
    Database.setup_db()
    news = get_mortgage_news()
    reaction = get_gpt_reaction(news)
    post_tweet(reaction)
