import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler
import subprocess
from pathlib import Path

print("Welcome to SnooKey v1.0", flush=True)
print("Waiting for access token...", flush=True)

def get_token():
        # 'Reddit for Android' Client ID
        client_id = "ohXpoqrZYub1kg"
        response_type = "token"
        scope = "*"
        callback = "http://localhost:65010/callback"
        state = "SNOOKEY"
        request_url = "https://www.reddit.com/api/v1/authorize?client_id=%s&response_type=%s&redirect_uri=%s&scope=%s&state=%s" % (
        client_id, response_type, callback, scope, state)

        # Open browser to get access token
        webbrowser.open(request_url, new=0)

        # Get the token from the callback page
        callbackhtml = open('callback.html', 'r').read()

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

        config = Path("config.txt")
        # Check if config file exists
        if config.is_file():
            # Exists - write to it
            with open("config.txt", 'r+', encoding='utf-8') as f:
                f.write(user_token)
        else:
            # Doesn't exist - create it, write to it, and hide it
            with open("config.txt", 'w', encoding='utf-8') as f:
                f.write(user_token)
            subprocess.check_call(["attrib", '+H', 'config.txt'])
        full_token = "Bearer " + user_token
        return full_token

full_token=''
config = Path("config.txt")
# Check if config file exists
if config.is_file():
    # It exists- open it
    with open("config.txt", encoding='utf-8') as f:
        # First line of the file- supposed to be last used access token
        firstline = f.readline()
        if firstline == "":
            print("Getting new token...", flush=True)
            # This line is empty- we need a new token
            full_token=get_token()
        else:
            # Something exists on the first line- we need to test it as a token
            headers = {
                'User-Agent': 'Project SnooKey/0.1',
                'Authorization': "Bearer " + firstline
            }
            token_check = requests.request("GET", url="https://oauth.reddit.com/api/v1/me/prefs/", headers=headers)
            if token_check.status_code == 200:
                # Token worked- use it
                full_token = "Bearer " + firstline
                print("Working token found!  Continuing...", flush=True)
            else:
                # Token did not work- we need a new one
                full_token=get_token()
else:
    print("Getting new token...", flush=True)
    # Config file does not exist- we need a new token
    full_token=get_token()

headers = {
    'User-Agent': 'Project SnooKey/0.1',
    'Authorization': full_token
}

# Live check of valid RPAN subreddits - currently broken due to endpoint
#subreddit_check = requests.request("GET", url="https://strapi.reddit.com/recommended_broadcast_subreddits")
#rpan_subreddits = subreddit_check.json()["data"]
# Crappy hotfix below
rpan_subreddits = ["pan", "animalsonreddit", "distantsocializing", "glamourschool", "headlineworthy", "readwithme", "redditinthekitchen", "redditmasterclasses", "redditsessions", "shortcircuit", "talentshow", "theartiststudio", "thegamerlounge", "theyoushow", "whereintheworld"]

while True:
    subreddit = input("Subreddit you want to broadcast to: ")
    subreddit = subreddit.lower()
    if subreddit in rpan_subreddits:
        if subreddit == "pan":
            print("NOTICE: You are only able to stream to r/pan during specific hours.  Please visit reddit.com/r/pan to learn more.")
            break
        else:
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
  print("")
  print("YOUR STREAMER KEY: " + response["data"]["streamer_key"])
  print("YOU ARE LIVE: " + response["data"]["post"]["outboundLink"]["url"])

else:
  # Failed
  print("")
  print("ERROR CODE " + str(token_req.status_code))
  print("The reddit servers said \"NONE SHALL PASS\"!  \nMake sure you are eligible to stream.  If you are using r/pan make sure you are trying during valid hours.")

# Fix to prevent windows .exe from closing on completion
print("")
input("Press enter to exit...")