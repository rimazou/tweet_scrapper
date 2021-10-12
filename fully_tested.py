import manager as ma
import time
import tweepy
import csv 
import json 
import tweepy
import requests
import base64
from typing import NamedTuple
# converts a Status object into a json
def status_tojson(status) :
    x ={"created_at" : str(status.created_at),
        "id": status.id,
        "id_str" : status.id_str,
        "text": status.text,
        "entities":status.entities,
        "source":status.source,
        "source_url":status.source_url,  
        "in_reply_to_status_id":status.in_reply_to_status_id,
        "in_reply_to_status_id_str":status.in_reply_to_status_id_str,
        "in_reply_to_user_id":status.in_reply_to_user_id,
        "in_reply_to_user_id_str":status.in_reply_to_user_id_str,
        "in_reply_to_screen_name":status.in_reply_to_screen_name, 
        "user.screen_name":status.user.screen_name,
        "geo":status.geo,
        "coordinates":status.coordinates,
        "place":status.place,
        "contributors":status.contributors,
        "is_quote_status":status.is_quote_status,
        "retweet_count":status.retweet_count,
        "favorite_count":status.favorite_count,  
        "favorited":status.favorited,
        "retweeted":status.retweeted,
        "lang" : status.lang}
    return x
#writes json objects into file must call the function for each item in a list 
def save_json(file_name, file_content):
  with open(ma.path + file_name, 'w', encoding='utf-8') as f:
    json.dump(file_content, f, ensure_ascii=False, indent=4)
auth = tweepy.OAuthHandler(ma.consumer_key, ma.consumer_secret)
api = tweepy.API(auth)
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
auth.set_access_token(ma.access_token, ma.access_token_secret)
public_statuses = api.home_timeline()
def listat_tolisjason(list):
    jsons=[]
    for i in list:
        jsons.append(status_tojson(i))
    return jsons




