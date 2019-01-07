import re

from textblob import TextBlob
import pandas as pd
import altair as alt


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


def analyze_csv() -> pd.DataFrame:
    url = "http://samplecsvs.s3.amazonaws.com/SacramentocrimeJanuary2006.csv"
    data = pd.read_csv(url)
    return data


def altair_plot():
    data = analyze_csv()[0:1000]
    base = alt.Chart(data)

    bar = base.mark_bar().encode(
        x=alt.X('latitude', bin=True, axis=None),
        y='count()'
    )

    return bar
