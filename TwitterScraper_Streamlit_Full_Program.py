import pandas as pd
import snscrape.modules.twitter as sntwitter
import json
from datetime import datetime
# import pymongo
# from pymongo import MongoClient
import streamlit as st

st.title("""
Scraping Data from Twitter Using Python
""")
st.write("""
This app scrapes the data from the Twitter
""")
st.write ("---")
st.write('**Description of Dataset**')
st.write("""
The dataset includes id, date, url, username, content, replycount, retweetcount,
likecount, language and source of the tweets
""")

#Inputs the number of tweets and username from the user
limit = st.number_input('Enter the limit:' )
username = st.text_input('Enter the username without @ symbol:')
start_date = st.date_input("Enter the start date YYYY/MM/DD: ")
end_date = st.date_input("Enter the end date YYYY/MM/DD: ")
lst1 = []
for tweet in sntwitter.TwitterSearchScraper('username, since:start_date until:end_date').get_items():
    if len(lst1) == limit:
        break
    else:
        lst1.append([tweet.date, tweet.url, tweet.content, tweet.id, tweet.user.username, tweet.replyCount,
                         tweet.retweetCount, tweet.likeCount, tweet.lang, tweet.source])

#loading into pandas dataframe
df = pd.DataFrame(lst1, columns=["Date", "url", "content", "id", "username", "replyCount", "retweetCount", "likeCount",
                               "language", "source"])
st.write(df)

#type of files either json or csv
fileselect = st.sidebar.selectbox(
    label = "Select the type of the file you want",
    options = ["CSV", "json"])

if fileselect == "CSV":
    df.to_csv('df_csv.csv', sep=',')
    CSV = pd.read_csv('df_csv.csv')
    st.write(CSV)
    st.download_button("Download CSV", df.to_csv(), mime = 'text/csv')
if fileselect == "json":
    dfj = df.to_json(orient='records')
    st.write(dfj)
    from pathlib import Path
    st.download_button(
    "Download json",
    data=Path("dfj.json").read_text(),
    file_name="dfj.json",
    mime="application/json",)
