import tweepy
import configparser
import pandas as pd
#from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob
import numpy as np
import re
import matplotlib.pyplot as plt


#Read credentials from config file
config = configparser.ConfigParser()
config.read('config.ini')

api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']

access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

#Authenticate API to Twitter account

auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True)

#Extract tweets for the topic of interest and creates a dataframe with the information
max_tweets = 100
release_date = "2022-04-15"
topic = "#SecretsOfDumbledore"

tweets = tweepy.Cursor(api.search_tweets,q=topic,count=max_tweets,
                           lang="en", tweet_mode="extended").items(max_tweets)

for tweet in tweets:
    tweets_df = pd.DataFrame(data=[tweet.full_text for tweet in tweets],
                             columns=['Tweets'])
    #including tweet.created_at gives the date and time for the tweet


#Clean tweets text
def cleanText(text):
    text = re.sub(r'@[A-Za-z0-9]+', '', text) #cleans @ mentions
    text = re.sub(r'#', '', text) #removes # symbol but not the text
    text = re.sub(r'RT[\s]+', '', text) #Removes retweets
    text = re.sub(r'https?:\/\/\S+', '', text) #Removes hyperlinks
    return text

#This function eliminates retweets, so the number of analyzed tweets is going to be smaller than the max number
#of tweets
tweets_df['Tweets'] = tweets_df['Tweets'].apply(cleanText) #applies function above


#Get the subjectivity and polarity from the tweets
def getSubjectivity(text):
    return TextBlob(text).sentiment.subjectivity
def getPolarity(text):
    return TextBlob(text).sentiment.polarity

tweets_df['Subjectivity'] = tweets_df['Tweets'].apply(getSubjectivity)
tweets_df['Polarity'] = tweets_df['Tweets'].apply(getPolarity)

#WordCloud
    #Work on this later


#Positive, Neutral, Negative Analysis
def getAnalysis(score):
    if score < 0:
        return 'Negative'
    elif score == 0:
        return 'Neutral'
    elif score > 0:
        return 'Positive'

tweets_df['Sentiment'] = tweets_df['Polarity'].apply(getAnalysis)

#Plots
fig, (ax1, ax2) = plt.subplots(1,2)
fig.suptitle(topic + ' Sentiment Analysis', fontsize=16)
ax1.scatter(tweets_df['Polarity'], tweets_df['Subjectivity'], color='Purple')
ax1.set_title('Subjectivity and Polarity')
ax1.set(xlabel='Polarity', ylabel='Subjectivity')
ax1.set_xlim([-1, 1])
ax1.set_ylim([-0.1, 1.1])
#ax1.set_axhline(x=0, color='black', linestyle='-')
ax1.vlines(x=0.0, ymin=-1, ymax=2, linewidth=0.5, color='black')

ax2.set_title('Sentiment Frequency')
tweets_df['Sentiment'].value_counts().plot(kind='bar', color='Purple')
ax2.set(ylabel='Frequency')
plt.show()
