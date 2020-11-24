import tweepy

BEARER_TOKEN = "YOUR_BEARER_TOKEN"

CONSUMER_KEY = "YOUR_CONSUMER_KEY"

CONSUMER_SECRET = "YOUR_CONSUMER_SECRET"

ACCESS_TOKEN = "YOUR ACCESS TOKEN"

ACCESS_TOKEN_SECRET = "YOUR ACCESS TOKEN SECRET"

def get_api_tweepy():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(auth)
    return api


def load_resource(resource):
    d = []
    with open(resource) as f:
        for line in f:
            d.append(line.replace('\n', ''))

    return d


def update_resource(col, file):
    f = open(file, 'w')
    for ele in col:
        f.write(ele + '\n')

    f.close()
