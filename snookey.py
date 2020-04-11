import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import gui

print("Welcome to SnooKey v1.0", flush=True)
print("Waiting for access token...", flush=True)

# 'Reddit for Android' Client ID
client_id = "ohXpoqrZYub1kg"
response_type = "token"
scope = "*"
callback = "http://localhost:65010/callback"
state = "SNOOKEY"
request_url = "https://www.reddit.com/api/v1/authorize?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s&state=%s" % (client_id, response_type, callback, scope, state)

#Open browser to get access token
webbrowser.open(request_url, new=0)

# Get the token from the callback page
callbackhtml = open('callback.html', 'r').read()
user_token = ''
class Serv(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        if self.path.startswith('/callback'):
            self.wfile.write(bytes(callbackhtml, 'utf-8'))
        if self.path.startswith('/submittoken'):
            self.wfile.write(bytes('<html><body><h1>You may close this tab now.</h1></body></html>', 'utf-8'))
            global user_token
            user_token = self.requestline.split(' ')[1].split('?token=')[1]

httpd = HTTPServer(('localhost', 65010), Serv)
httpd.handle_request()
httpd.handle_request()

full_token = "Bearer " + user_token

rpan_subreddits = ["pan", "AnimalsOnReddit", "distantsocializing", "GlamourSchool", "RedditInTheKitchen", "RedditMasterClasses", "RedditSessions",
                   "talentShow", "TheArtistStudio", "TheGamerLounge", "TheYouShow", "whereintheworld"]
while True:
    subreddit = input("Subreddit you want to broadcast to: ")
    if subreddit in rpan_subreddits:
        if subreddit == "pan":
            print("NOTICE: You are only able to stream to r/pan during specific hours.  Please visit reddit.com/r/pan to learn more.")
            break
    else:
        print("ERROR: " + subreddit + " is not a valid RPAN subreddit!")
        continue

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
  post_id = response["data"]["share_link"].split("/rpan/")[1]

  print("", flush=True)
  print("YOUR STREAMER KEY: " + response["data"]["streamer_key"], flush=True)
  print("YOU ARE LIVE: " + response["data"]["post"]["outboundLink"]["url"], flush=True)

  with open("config.txt", 'w', encoding='utf-8') as f:
      f.write(post_id+"\n")
      f.write(subreddit+"\n")

  # Start popout
  gui = gui.SnooKeyGui(post_id=post_id, subreddit=subreddit)
  gui.start()
else:
  # Failed
  print("")
  print("ERROR CODE " + str(token_req.status_code))
  print("The reddit servers said \"NONE SHALL PASS\"!  \nMake sure you are eligible to stream.  If you are using r/pan make sure you are trying during valid hours.")

# Fix to prevent windows .exe from closing on completion
print("")
input("Press enter to exit...")