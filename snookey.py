import webbrowser
import requests

# 'Reddit for Android' Client ID
client_id = "ohXpoqrZYub1kg"
response_type = "token"
scope = "*"
callback = "http://localhost:65010/callback"
state = "SNOOKEY"
request_url = "https://www.reddit.com/api/v1/authorize?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s&state=%s" % (client_id, response_type, callback, scope, state)

#Open browser to get access token
webbrowser.open(request_url, new=0)

#Get user input
print("HINT: Your code can be found on the localhost callback page.")
user_token = input("Please enter your access token: ")
full_token = "Bearer " + user_token
subreddit = input("Subreddit you want to broadcast to: ")
title = input("Stream title: ")

broadcast_endpoint = "https://strapi.reddit.com/r/%s/broadcasts?title=%s" % (subreddit, title)

payload = {}
headers = {
  'User-Agent': 'Project SnooKey/0.1',
  'Authorization': full_token
}

# Request broadcast slot
token_req = requests.request("POST", url=broadcast_endpoint, headers=headers, data=payload)

if token_req.status_code == 200:
  # Success!  Stream prepped
  response = token_req.json()
  print("")
  print("YOUR STREAMER KEY: " + response["data"]["streamer_key"])
  print("YOU ARE LIVE: " + response["data"]["post"]["outboundLink"]["url"])
else:
  # Failed
  print("")
  print("ERROR CODE " + str(token_req.status_code))
  print("The reddit servers said \"NONE SHALL PASS\"!  Make sure you:")
  print("[*] Are eligible to stream")
  print("[*] Have a valid access token")
  print("[*] Selected a valid RPAN subreddit (no typos)")

# Fix to prevent windows .exe from closing on completion
print("")
input("Press enter to exit...")