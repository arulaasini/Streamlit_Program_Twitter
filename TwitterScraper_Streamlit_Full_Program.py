#Importing Relevant libraries
import pandas as pd
import snscrape.modules.twitter as sntwitter
import json
from datetime import datetime
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px

st.title("""***SCRAPING DATA FROM TWITTER USING PYTHON***""")
st.write("""This app scrapes the data from the twitter""")
st.write('***Description of the dataset:***')
st.write("""
The dataset includes id, date, url, username, content, replycount, retweetcount,
likecount, language and source of the tweets
""")

#scraping the data from the twitter
limit = st.number_input("Enter the number of tweets: ")
username = st.text_input("Enter the username without @ symbol (ex: #python or python): ")
since = st.date_input("start date[yyyy/mm/dd]")
until = st.date_input("end date[yyyy/mm/dd]")
lst1 = []
for tweet in sntwitter.TwitterSearchScraper('username since until').get_items():
    if len(lst1) == limit:
        break
    else:
        lst1.append(
            [tweet.date, tweet.url, tweet.content, tweet.id, tweet.user.username, tweet.replyCount, tweet.retweetCount,
             tweet.likeCount, tweet.lang, tweet.source])
    # Pandas dataframe
df = pd.DataFrame(lst1,
                      columns=["Date", "url", "content", "id", "username", "replyCount", "retweetCount", "likeCount",
                               "language", "source"])
st.write(df)
#either json or csv
fileselect = st.sidebar.selectbox(
label = "Select the type of the file",
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
mime="application/json")
#visualization
chart_select = st.sidebar.selectbox(
    label = "Chart Type",
    options = ['Scatterplots', 'Lineplots', 'Histogram', 'Boxplot'])
numeric_columns = list(df.select_dtypes(['int']).columns)
if chart_select == 'Scatterplots':
    st.sidebar.subheader('Scatterplot Settings')
try:
    x_values = st.sidebar.selectbox('X axis', options = numeric_columns)
    y_values = st.sidebar.selectbox('Y axis', options = numeric_columns)
    plot = px.scatter(data_frame=df, x = x_values, y = y_values)
    st.write(plot)
except Exception as e:
    print(e)
if chart_select == 'Histogram':
    st.sidebar.subheader('Histogram Settings')
try:
    x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
    plot = px.histogram(data_frame=df, x = x_values)
    st.write(plot)
except Exception as e:
    print(e)
if chart_select == 'Lineplots':
    st.sidebar.subheader('Lineplot Settings')
try:
    x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
    y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
    plot = px.line(data_frame=df, x=x_values, y=y_values)
    st.write(plot)
except Exception as e:
    print(e)
if chart_select == 'Boxplot':
    st.sidebar.subheader('Boxplot Settings')
try:
   x_values = st.sidebar.selectbox('X axis', options=numeric_columns)
   y_values = st.sidebar.selectbox('Y axis', options=numeric_columns)
   plot = px.box(data_frame=df, x=x_values, y=y_values)
   st.write(plot)
except Exception as e:
   print(e)
