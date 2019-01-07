import re

from textblob import TextBlob


def clean_tweet(raw_tweet_text: str):
    """ Utility function to clean tweet text by removing links, special characters using simple regex statements."""
    return " ".join(
        re.sub(
            "(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])| (\w+:\ /  \ /  \S+)",
            " ",
            raw_tweet_text,
        ).split()
    )


def analyze_tweet_sentiment(tweet_list: list) -> dict:
    positive = neutral = negative = 0
    for tweet in tweet_list:
        analysis = TextBlob(clean_tweet(tweet["text"]))
        if analysis.sentiment.polarity > 0:
            positive += 1
        elif analysis.sentiment.polarity == 0:
            neutral += 1
        else:
            negative += 1
    sentiment = {"positive": positive, "neutral": neutral, "negative": negative}
    return sentiment
