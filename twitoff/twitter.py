"""
Retreive Tweets, embeddings, and persist in the database

"""
import basilica
import tweepy
from decouple import config
from .models import DB, Tweet, Company
import re
from textblob import TextBlob


# configure API keys
TWITTER_AUTH = tweepy.OAuthHandler(config('TWITTER_CONSUMER_KEY'),
                                   config('TWITTER_CONSUMER_SECRET'))
TWITTER_AUTH.set_access_token(config('TWITTER_ACCESS_TOKEN'),
                              config('TWITTER_ACCESS_TOKEN_SECRET'))
TWITTER = tweepy.API(TWITTER_AUTH)

BASILICA = basilica.Connection(config('BASCILICA_KEY'))


def add_tweets(tweets):
    """
    Adds a list of tweet objects to our database

    tweets : list
        List of Tweet objects to be added

    return: None
        Commits changes to the database
    """
    for tweet in tweets:
        if not DB.session.query(Tweet).filter(Tweet.id==tweet.id).first():
            DB.session.add(tweet)
    DB.session.commit()


def search_competitor(competitor, company_id, count=5000):
    """
    competitor : str
        Name of cometitive entity for which to search mentions
    company : str
        Name of company gatherering BI

    return : list
        List of negative tweets mentioning the company
    """
    # search competitors name and return list of tweets
    since_id = DB.session.query(DB.func.max(Tweet.id))\
        .filter(Tweet.company_id == company_id).first()[0]
    # import pdb; pdb.set_trace()
    search = TWITTER.search(q=competitor,
                            lang='en',
                            since_id=since_id,
                            count=100)

    # filter out retweets
    tweets = [parse_search(tweet) for tweet in search if tweet.text[:2] != 'RT']
    # filter for negative tweets only
    if len(tweets) != 0:
        tweets = [tweet for tweet in tweets if get_tweet_sentiment(tweet['text']) < 0.0]
    else:
        return []

    # get tweet embeddings from basilica
    competitor_tweets = []
    for tweet in tweets:
        sentiment = get_tweet_sentiment(tweet['text'])
        embedding = BASILICA.embed_sentence(tweet['text'], model='twitter')
        competitor_tweets.append(Tweet(id=tweet['id'],
                                       text=tweet['text'],
                                       user=tweet['user'],
                                       embedding=embedding,
                                       sentiment=round(sentiment,2),
                                       company_id=company_id,
                                       link='https://twitter.com/i/web/status/' +
                                            str(tweet['id'])))

    # return the tweets
    return competitor_tweets

def parse_search(result):
    """
    Parses through search result for relevant fields

    result : SearchResult object

    return : dictionary
        Dictionary containing id, user_id, username, and text
    """
    parse = {}
    parse['id'] = result.id
    parse['user_id'] = result.user.id
    parse['user'] = result.user.screen_name
    parse['text'] = result.text
    return parse

def clean_tweet(tweet):
    """
    Utility function to clean tweet text by removing links, special characters
    using simple regex statements.
    """
    return ''.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\ / \ / \S+)","", tweet))


def get_tweet_sentiment(tweet):
    """
    Utility function to classify sentiment of passed tweet
    using textblob's sentiment method
    """
    # create TextBlob object of passed tweet text
    return TextBlob(clean_tweet(tweet)).sentiment.polarity


def add_or_update_company(name, competitor):
    """
    Add or update a company

    name : str
        name of company

    return : None
        Updates are made directly to the database
    """
    try:
        # add company if it doesn't exist
        if not DB.session.query(Company).filter(Company.name==name).first():
            db_company = Company(name=name, competitor=competitor)
            DB.session.add(db_company)
            DB.session.commit()
    except:
        pass
    # get latest tweets about competitors
    db_company_id = DB.session.query(Company).filter(Company.name == name).first().id
    add_tweets(search_competitor(competitor, company_id=db_company_id))
    DB.session.commit()

def update_conversion(tweet_id, status):
    """
    Updates conversion status of tweet

    tweet_id: int
        Unique key of tweet
    status: int
        1 for converted, 0 for not

    return: None
        Updates database
    """
    DB.session.query(Tweet).\
            filter(Tweet.id == tweet_id).\
            update({'converted' : status})
    DB.session.commit()
