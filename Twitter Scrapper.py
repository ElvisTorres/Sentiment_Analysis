from twitterscraper import query_tweets
import datetime as dt
import pandas as pd

#parameters for query tweets
begin_date = dt.date(2022,4,5)
end_date = dt.date(2022,4,16)
limit = 100
lang = 'english'
#user =

tweets = query_tweets('the batman', limit = limit)

df = pd.DataFrame(t.__dict__ for t in tweets)

print (df)