import requests
from bs4 import BeautifulSoup
import TwitterAPI
import GPTAPI
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


if __name__ == "__main__":
    Database.setup_db()
    news = get_mortgage_news()
    reaction = GPTAPI.get_gpt_reaction(news)
    TwitterAPI.post_tweet(reaction)
