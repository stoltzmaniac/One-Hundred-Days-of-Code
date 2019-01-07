import re

from textblob import TextBlob


def clean_tweet(raw_tweet_text):
    ''' Utility function to clean tweet text by removing links, special characters using simple regex statements.'''
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ /  \ /  \S+)", " ", raw_tweet_text).split())


def analyze_tweet_sentiment(raw_tweet_text):
    analysis = TextBlob(clean_tweet(raw_tweet_text))
    if analysis.sentiment.polarity > 0:
        return 'positive'
    elif analysis.sentiment.polarity == 0:
        return 'neutral'
    else:
        return 'negative'
