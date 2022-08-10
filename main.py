from dotenv import load_dotenv
import requests
import tweepy
import os

# load keys from environment
load_dotenv()
api_key = os.getenv("API-KEY")
api_secret = os.getenv("API-SECRET")
access_token = os.getenv("ACCESS-TOKEN")
access_secret = os.getenv("ACCESS-SECRET")

# start twitter client
twitter = tweepy.Client(
  consumer_key=api_key, consumer_secret=api_secret,
  access_token=access_token, access_token_secret=access_secret
)

# get short story
try:
  url = 'https://shortstories-api.herokuapp.com/'
  r = requests.get(url)
  data = r.json()
except requests.exceptions.RequestException as err:
  raise SystemExit(err)

# process story data
story_list = []
title = data['title'] + '. By: ' + data['author'] + '\n#shortstory #shortstories'
story_list.append(title)

# break down the story to required tweet char length(280)
story = data['story']
done = False
while not done:
  sub = story[:280] # get max characters
  cut_index = sub.rfind('. ') # get last complete sentence

  # get valid complete text within char limit
  sub = story.strip()[:cut_index + 1]
  story_list.append(sub.strip())
  story = story.strip()[cut_index + 1:] # get remaining text
  if (len(story) < 280):
    # stop looping if rem text is less than char limit
    done = True
    story_list.append(story.strip())

moral = 'Moral: ' + data['moral']
story_list.append(moral)

# send tweet
# loop through list with correct length texts
for i in range(len(story_list)):
  if (i == 0):
    t_response = twitter.create_tweet(
      text=story_list[i]
    )
  else:
    # reply to previously posted text to create thread
    t_response = twitter.create_tweet(
      text=story_list[i],
      in_reply_to_tweet_id=t_response[0]['id']
    )