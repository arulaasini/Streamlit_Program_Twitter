# Program to scrape data from twitter and moving it to MongoDB
# Importing Relevant libraries
import pandas as pd
import snscrape.modules.twitter as sntwitter
import json
import pymongo
from pymongo import MongoClient
from datetime import datetime

# Scraping data from twitter
def twitter_scraper():
    limit = int(input("Enter the number of tweets: "))
    username = input("Enter the username without @ [ex: #python]: ")
    start_date = input("Enter the start date YYYY/MM/DD: ")
    end_date = input("Enter the end date YYYY/MM/DD: ")
    lst1 = []
    for tweet in sntwitter.TwitterSearchScraper('username, since:start_date until:end_date').get_items():
        if len(lst1) == limit:
            break
        else:
            lst1.append([tweet.date, tweet.url, tweet.content, tweet.id, tweet.user.username, tweet.replyCount,
                         tweet.retweetCount, tweet.likeCount, tweet.lang, tweet.source])

# Pandas dataframe
    df = pd.DataFrame(lst1,
                      columns=["Date Created", "url", "Content", "ID", "Username", "Number of replies", "Number of retweets", "number of likes",
                               "language", "Source of tweet"])

# Converting dataframe into json
    dfj = df.to_json(orient='records')

# converting dataframe into csv
    df.to_csv('df_csv.csv', sep=',')
    df_dict = pd.read_csv('df_csv.csv', header=None, index_col=0)

# converting csv into dictionary
    df_dict = df.to_dict('records')
    
    print (dfj)
    print(df_csv.csv)

#moving json file to Mongodb
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["Twitterscraper"] ##database name
    collection = db["artificialintelligence"] ##collection name

#loading the json file
    with open('dfj.json') as file:
        file_data = load(file)
    if isinstance(file_data, list):
            Collection.insert_many(file_data)
    else:
            Collection.insert_one(file_data)

# moving csv file into MongoDB after converting it to dictionary
    myclient = MongoClient("mongodb://localhost:27017/")
    db = myclient["Twitterscraper"]
    collection = db["artificialintelligence"]
    db.Twitterscraper.insert_many(df_dict)
