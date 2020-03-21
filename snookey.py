import webbrowser
import requests

# 'Reddit for Android' Client ID
client_id = "ohXpoqrZYub1kg"
response_type = "token"
scope = "*"
callback = "http://localhost:65010/callback"
state = "SNOOKEY"
request_url = "https://www.reddit.com/api/v1/authorize?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s&state=%s" % (client_id, response_type, callback, scope, state)

webbrowser.open(request_url, new=0)

print("HINT: Your code can be found on the localhost callback page.")
user_token = input("Please enter your access token: ")
full_token = "Bearer " + user_token
subreddit = input("Subreddit do you want to broadcast to: ")
title = input("Stream title: ")

broadcast_endpoint = "https://strapi.reddit.com/r/%s/broadcasts?title=%s" % (subreddit, title)

payload = {}
headers = {
  'User-Agent': 'SnooKey/0.1 by u/Spikeedoo',
  'Authorization': full_token
}

token_req = requests.request("POST", url=broadcast_endpoint, headers=headers, data=payload)

if token_req.status_code == 200:
  response = token_req.json()
  print("YOUR STREAMER KEY: " + response["data"]["streamer_key"])
  print("YOU ARE LIVE: " + response["data"]["post"]["outboundLink"]["url"])
else:
  print("ERROR CODE " + str(token_req.status_code))
  print("The reddit servers said \"NONE SHALL PASS\"!  Your access token may be invalid... Please try again")