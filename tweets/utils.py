import tweepy


def start():
    '''
        ToDo
        run: ./manage.py shell -c="from tweets.utils import start; start()"
    '''
    consumer_key = 'edGj6kTiDU1NOtdSyHHJ6yoD4'
    consumer_secret = 'sGZmEV7xq4yx2ixwbhuBq6v1aCgRwuBF3IqIqhfYNLhWMokOML'
    access_token = '1323543967-JcSeOiXMxND46nMj3mkx43J8SB4A3GBR24Pkfx2'
    access_token_secret = 'zr19f231ZuV8D8gpo8asjnfEXI4gX0xWQ6AXk0kyMvimu'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    '''
    '''

    user = api.get_user('vsdani')
    public_tweets = api.home_timeline()
    for tweet in public_tweets:
        print(tweet.text)
    print(user.screen_name)
    print(user.followers_count)