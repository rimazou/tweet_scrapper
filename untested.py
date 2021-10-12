import tweepy
import requests
import json
import base64
import urllib.parse
from typing import NamedTuple
consumer_key = 'dZbG53gSRASfPictPHGWMwNBW'
consumer_secret = 'w6UVNwH7oNChDLyGGdRebRpV1dxY9qv5eevsN6rwFt5VdSFSYh'
access_token = '1304891973959135239-x2hbArreelQQVFSc9FpkmKOvnvto7v'
access_token_secret = 'oSYpVR55zc7xZNnApZAPlT099qdO7vbqTTglT76p8YEr2'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAM5uTwEAAAAAsFdMGFd%2FJE29VMAMmjdshJzr5KU%3DiRxoBSEClIcECmGewsUQUbPc58E83Px10qMUtO71svbARXb86a' 
path = "C:/Users/Rima/Documents/git_projects/pyth_projects/"
        
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

print(api.auth.username)
class twi_cred(NamedTuple):
    consumer_key : str
    consumer_key_secret : str
    access_token : str
    access_token_secret : str


twitter_creds= twi_cred(consumer_key,consumer_secret,access_token,access_token_secret)


def get_tweet_ids(username :str):
    scandy_tweets = api.user_timeline(screen_name=username, count=5)
    tweet_id_list = []
    for twit in scandy_tweets:
        json_str = json.loads(json.dumps(twit._json))
        tweet_id_list.append(json_str['id'])
    return tweet_id_list


def get_bearer_token():
    uri_token_endpoint = 'https://api.twitter.com/oauth2/token'
    key_secret = f"{consumer_key}:{consumer_secret}".encode('ascii')
    b64_encoded_key = base64.b64encode(key_secret)
    b64_encoded_key = b64_encoded_key.decode('ascii')

    auth_headers = {
        'Authorization': 'Basic {}'.format(b64_encoded_key),
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
        }

    auth_data = {
        'grant_type': 'client_credentials'
        }

    auth_resp = requests.post(uri_token_endpoint, headers=auth_headers, data=auth_data)
    print(auth_resp.status_code)
    bearer_token = auth_resp.json()['access_token']
    return bearer_token



#bearer_tokenn = get_bearer_token()

bearer_header = {
    'Accept-Encoding': 'gzip',
    'Authorization': 'Bearer {}'.format(bearer_token),
    'oauth_consumer_key': consumer_key 
}

recent_tweets = get_tweet_ids('Twitter')
# returns a bearer_header to attach to requests to the Twitter api v2 enpoints which are 
# not yet supported by tweepy 
def get_bearer_header():
   uri_token_endpoint = 'https://api.twitter.com/oauth2/token'
   key_secret = f"{twitter_creds.consumer_key}:{twitter_creds.consumer_key_secret}".encode('ascii')
   b64_encoded_key = base64.b64encode(key_secret)
   b64_encoded_key = b64_encoded_key.decode('ascii')

   auth_headers = {
       'Authorization': 'Basic {}'.format(b64_encoded_key),
       'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
       }

   auth_data = {
       'grant_type': 'client_credentials'
       }

   auth_resp = requests.post(uri_token_endpoint, headers=auth_headers, data=auth_data)
   bearer_token = auth_resp.json()['access_token']

   bearer_header = {
       'Accept-Encoding': 'gzip',
       'Authorization': 'Bearer {}'.format(bearer_token),
       'oauth_consumer_key': twitter_creds.consumer_key 
   }
   return bearer_header

# Returns the conversation_id of a tweet from v2 endpoint using the tweet id
def getConversationId(id):
   uri = 'https://api.twitter.com/2/tweets?'

   params = {
       'ids':id,
       'tweet.fields':'conversation_id'
   }
   
   bearer_header = get_bearer_header()
   resp = requests.get(uri, headers=bearer_header, params=params)
   return resp.json()['data'][0]['conversation_id']

# Returns a conversation from the v2 enpoint  of type [<original_tweet_text>, <[replies]>]
def getConversation(conversation_id):
   uri = 'https://api.twitter.com/2/tweets/search/recent?'
#c'est ici que je ne reçois aucune donnée quand je mets tous les parametres
   params = {'query': f'conversation_id:{conversation_id}',
        'tweet.fields': 'in_reply_to_user_id', 
        'tweet.fields':'conversation_id',
        'tweet.fields':'geo',
        'tweet.fields':'data', 
        'tweet.fields':"id", 
        'tweet.fields':"text", 
        'tweet.fields':"attachments", 
        'tweet.fields':"author_id",
        'tweet.fields':"context_annotations", 
        'tweet.fields':"created_at", 
        'tweet.fields':"entities",
        'tweet.fields':"lang",
        'tweet.fields': "non_public_metrics",
        'tweet.fields':"organic_metrics",
        'tweet.fields':"possibly_sensitive", 
        'tweet.fields':"promoted_metrics",
        'tweet.fields':"public_metrics",
        'tweet.fields':"referenced_tweets",
        'tweet.fields': "reply_settings",
        'tweet.fields':  "source",
        'tweet.fields':"withheld"   
       }
   
   bearer_header = get_bearer_header()
   resp = requests.get(uri, headers=bearer_header, params=params)
   return resp.json()


def getConversationId(id):
    uri = 'https://api.twitter.com/2/tweets?'
    params = {
       'ids':id,
       'tweet.fields':'conversation_id'
    }
    bearer_header = get_bearer_header()
    resp = requests.get(uri, headers=bearer_header, params=params)
    return resp.json()['data'][0]['conversation_id']
