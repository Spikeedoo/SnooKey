import webbrowser
import requests
from http.server import HTTPServer, BaseHTTPRequestHandler

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