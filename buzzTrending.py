from bs4 import BeautifulSoup
import requests
import re


def buzzuk7():
    page = requests.get('https://www.buzzfeed.com/index.xml')
    soup = BeautifulSoup((page.text).encode('utf-8'), 'html.parser')
    recordstitle = soup.find_all('title')
    buzztrends = []
    for x in range(2, 9):
        name = re.sub('<title>', '', str(recordstitle[x]))
        name = re.sub('</title>', '', name)
        buzztrends.append(name)

    return buzztrends
