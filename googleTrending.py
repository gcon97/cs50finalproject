from bs4 import BeautifulSoup
import requests
import re


def googleuk7():
    page = requests.get(
        'https://trends.google.com/trends/trendingsearches/daily/rss?geo=GB')
    soup = BeautifulSoup(page.text, 'html.parser')

    recordstitle = soup.find_all('title')
    recordssub = soup.find_all('ht:news_item_title')

    googletrends = []

    for x in range(1, 8):
        name = re.sub('<title>', '', str(recordstitle[x]))
        name = re.sub('</title>', '', name)
        sub = re.sub('<ht:news_item_title>', '', str(recordssub[x]))
        sub = re.sub('</ht:news_item_title>', '', sub)
        dictentry = {'name': name, 'sub': sub}
        googletrends.append(dictentry)

    return googletrends
