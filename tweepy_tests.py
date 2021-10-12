import time
import tweepy
import csv 
import json 
import tweepy
import requests
import base64
from typing import NamedTuple
#ACCESS KEYS TWITTER API
consumer_key = 'dZbG53gSRASfPictPHGWMwNBW'
consumer_secret = 'w6UVNwH7oNChDLyGGdRebRpV1dxY9qv5eevsN6rwFt5VdSFSYh'
access_token = '1304891973959135239-x2hbArreelQQVFSc9FpkmKOvnvto7v'
access_token_secret = 'oSYpVR55zc7xZNnApZAPlT099qdO7vbqTTglT76p8YEr2'
bearer_token = 'AAAAAAAAAAAAAAAAAAAAAM5uTwEAAAAAsFdMGFd%2FJE29VMAMmjdshJzr5KU%3DiRxoBSEClIcECmGewsUQUbPc58E83Px10qMUtO71svbARXb86a' 
path = "datasets/"

MAX_RECENT= 1000 # we can only retrieve 18000 of tweets within 15min
MAX_USER=3200 # we can only retrieve this amount of recent tweets of a user timeline
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
try:
    redirect_url = auth.get_authorization_url()
except tweepy.TweepError:
    print('Error! Failed to get request token.')
auth.set_access_token(access_token, access_token_secret)
# public_tweets = api.home_timeline()
print(redirect_url)
api = tweepy.API(auth)
# Helper function to save data into a JSON file
# file_name: the file name of the data on Google Drive
# file_content: the data you want to save
def save_json(file_name, file_content):
  with open(path + file_name, 'w', encoding='utf-8') as f:
    json.dump(file_content, f, ensure_ascii=False, indent=4)

# In this example, the handler is time.sleep(15 * 60),
# but you can of course handle it in any way you want.
def limit_handled(cursor, list_name):
  while True:
    try:
      yield cursor.next()
    # Catch Twitter API rate limit exception and wait for 15 minutes
    except tweepy.TooManyRequests:
      print("\nData points in list = {}".format(len(list_name)))
      print('Hit Twitter API rate limit.')
      for i in range(3, 0, -1):
        print("Wait for {} mins.".format(i * 5))
        time.sleep(15 * 60)
    # Catch any other Twitter API exceptions
    except tweepy.error.TweepError:
      print('\nCaught TweepError exception' )

def limit_handled(cursor):
    print('limite_handled called')
    while True:
        try:
            yield next(cursor)
        #except tweepy.RateLimitError:
        except tweepy.TooManyRequests:
            print('TooManyRequests exception raised!!!!!')
            # we have to wait 15 minutes so that we can remake the request
            time.sleep(15 * 60)
            continue
        except StopIteration :
            print("No , No break it it's fine")
            break
def get_all_tweets_of(screen_name):
  alltweets = []   # initialize a list to hold all the Tweets
  # make initial request for most recent tweets 200 is the max allowed
  new_tweets = api.user_timeline(screen_name = screen_name,count=200)
  alltweets.extend(new_tweets)# save most recent tweets
  # save the id of the oldest tweet less one to avoid duplication
  oldest = alltweets[-1].id - 1
  # keep grabbing tweets until there are no tweets left
  while len(new_tweets) > 0:
    print("getting tweets before %s" % (oldest))
    # all subsequent requests use the max_id param to prevent duplicates
    new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print("...%s tweets downloaded so far" % (len(alltweets)))
    ### END OF WHILE LOOP ###
  # transform the tweepy tweets into a 2D array that will 
  # populate the csv
  outtweets = [[tweet.id_str, tweet.created_at,tweet.geo, tweet.text, tweet.favorite_count,
  tweet.in_reply_to_screen_name, tweet.retweeted] for tweet in alltweets]
  # write the csv
  with open(path + '%s_tweets.csv' % screen_name, 'w',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["id","created_at","geocode","text","likes","in reply to","retweeted",])
    writer.writerows(outtweets)
  pass



# Function to save follower objects in a JSON file.
def get_followers():
  
  # Create a list to store follower data
  followers_list = []
  # For-loop to iterate over tweepy cursors
  cursor = tweepy.Cursor(api.followers, count=200).pages()
  for i, page in enumerate(limit_handled(cursor, followers_list)):  
    print("\r"+"Loading"+ i % 5 *".", end='')
    
    # Add latest batch of follower data to the list
    followers_list += page
  
  # Extract the follower information
  followers_list = [x._json for x in followers_list]
  # Save the data in a JSON file
  save_json('followers_data.json', followers_list)

#get_all_tweets('TwitterDev')


def get_all_recent_tweets(subject):    
  alltweets = [] # initialize a list to hold all the Tweets
  # make initial request for most recent tweets 200 is the max
  new_tweets = api.search_tweets(q=subject,count=200)
  # save most recent tweets
  alltweets.extend(new_tweets)
  # save the id of the oldest tweet less one to avoid duplication
  oldest = alltweets[-1].id - 1
  # keep grabbing tweets until there are no tweets left
  while len(new_tweets)>0 and len(alltweets) < MAX_RECENT:
    print("getting tweets before %s" % (oldest))
    # all subsequent requests use the max_id param to prevent
    # duplicates
    new_tweets = api.search_tweets(q=subject,count=200,max_id=oldest)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # update the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1
    print("...%s tweets downloaded so far" % (len(alltweets)))
    ### END OF WHILE LOOP ###
  # transform the tweepy tweets into a 2D array that will 
  # populate the csv
  outtweets = [[tweet.id_str, tweet.created_at, tweet.text, tweet.favorite_count,tweet.in_reply_to_screen_name, tweet.retweeted] for tweet in alltweets]
  # write the csv
  with open(path + '%s_tweets.csv' % subject, 'w',encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["id","created_at","text","likes","in reply to","retweeted"])
    writer.writerows(outtweets)
  pass
#get_all_recent_tweets('taxi')

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

#recent_tweets = get_tweet_ids('Twitter')
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

   params = {'query': f'conversation_id:{conversation_id}',
        #'tweet.fields': 'in_reply_to_user_id', 
        #'tweet.fields':'conversation_id',
        'tweet.fields':'geo',
        #'tweet.fields':'id', 
        #'tweet.fields':'text', 
        #'tweet.fields':'attachments',
        #'tweet.fields':'author_id',
        #'tweet.fields':'context_annotations', 
        #'tweet.fields':'created_at', 
        #'tweet.fields':'entities', 
        #'tweet.fields':'lang',
        #'tweet.fields':'non_public_metrics',
        #'tweet.fields':'organic_metrics',
        #'tweet.fields':'possibly_sensitive', 
        #'tweet.fields':'promoted_metrics,
        #'tweet.fields':'public_metrics',
        #'tweet.fields':'referenced_tweets',
        #'tweet.fields':'reply_settings,
        #'tweet.fields':'source',
        #'tweet.fields':'withheld'   
   }
   
   bearer_header = get_bearer_header()
   resp = requests.get(uri, headers=bearer_header, params=params)
   return resp.json()

basket=getConversation(1445811612775030785)
save_json('myconvo+a',basket)
#get_all_tweets_of('mspuuurple')