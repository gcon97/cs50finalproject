from twitter import Twitter, OAuth
import oauth2
import json
import requests

consumer_key = "gGGonjRQkssNcDnQ4VpfOr4A7"
consumer_secret = "zbdHXOwSfUVhd7i5UPjk9OcRvHcMXFpPyBy01H5G6XOmDU4yRx"
access_token = "1297956746-hXfq6yaRpS8qtUR1zksSFsd6XI0ZnIlvgsAkfht"
access_token_secret = "2jN09aYfSugc1VVFHyETbTOBIG2L8I4q8tCcMG7vAKSgq"

consumer = oauth2.Consumer(key=consumer_key, secret=consumer_secret)
access = oauth2.Token(key=access_token, secret=access_token_secret)
client = oauth2.Client(consumer, access)


def twitteruk7():
    trendingreq = "https://api.twitter.com/1.1/trends/place.json?id=12723"
    data, data = client.request(trendingreq)
    records = json.loads(data)
    trending = []
    for record in records:
        for x in range(7):

            dictentry = {'trend': record['trends'][x]
                         ['name'], 'url': record['trends'][x]['url']}
            trending.append(dictentry)
    return trending
