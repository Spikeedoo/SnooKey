import requests
import re
from pathlib import Path
from getpass import getpass
import urllib.parse

print()
print("""  /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$  /$$   /$$ /$$$$$$$$ /$$     /$$
 /$$__  $$| $$$ | $$ /$$__  $$ /$$__  $$| $$  /$$/| $$_____/|  $$   /$$/
| $$  \__/| $$$$| $$| $$  \ $$| $$  \ $$| $$ /$$/ | $$       \  $$ /$$/
|  $$$$$$ | $$ $$ $$| $$  | $$| $$  | $$| $$$$$/  | $$$$$     \  $$$$/
 \____  $$| $$  $$$$| $$  | $$| $$  | $$| $$  $$  | $$__/      \  $$/
 /$$  \ $$| $$\  $$$| $$  | $$| $$  | $$| $$\  $$ | $$          | $$
|  $$$$$$/| $$ \  $$|  $$$$$$/|  $$$$$$/| $$ \  $$| $$$$$$$$    | $$
 \______/ |__/  \__/ \______/  \______/ |__/  \__/|________/    |__/""")
print()

print("Welcome to SnooKey v2.0", flush=True)
print("Waiting for access token...", flush=True)

def get_token():
    # Pre request to get Reddit cookie headers
    get_pre_data = requests.request("POST", "https://ssl.reddit.com/api/login/")
    cookie = get_pre_data.headers['set-cookie']
    result = re.search('loid=(.*?);', cookie)
    loid = result.group(1)
    result = re.search('session_tracker=(.*?);', cookie)
    session_tracker = result.group(1)
    result = re.search('edgebucket=(.*?);', cookie)
    edgebucket = result.group(1)
    csv=1

    # Build cookie string
    cookie_string = "csv=" + str(csv) + "; edgebucket=" + edgebucket + "; loid=" + loid + "; session_tracker=" + session_tracker

    # Login
    user_token = ''
    while True:
        username = input("Enter your Reddit username: ").strip()
        password = getpass("Enter your Reddit password: ").strip()

        url = "https://ssl.reddit.com/api/login/" + username

        # Set up payload with login details
        payload = {
            'api_type': 'json',
            'user': username,
            'passwd': password
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Project SnooKey/0.2',
            'Cookie': cookie_string
        }

        # Make login request
        login_flow = requests.request("POST", url, headers=headers, data=payload)
        login_response = login_flow.json()
        if len(login_response["json"]["errors"]) == 0:
            # Login worked
            # Capture session cookie
            reddit_cookie = login_flow.cookies["reddit_session"]
            print("Login success!")
            payload = "{\"scopes\":[\"*\",\"email\",\"pii\"]}"
            headers = {
                'Cookie': 'reddit_session=' + reddit_cookie,
                'authorization': 'Basic b2hYcG9xclpZdWIxa2c6',
                'user-agent': 'Project SnooKey/0.2',
                'content-type': 'application/json; charset=UTF-8',
            }
            # Make request for access token
            at_req = requests.request("POST", url="https://accounts.reddit.com/api/access_token", headers=headers,
                                      data=payload)
            if at_req.status_code == 200:
                at_data = at_req.json()
                user_token = at_data["access_token"]
                break
            else:
                print("Error occurred fetching token!")
                break
        else:
            if (login_response["json"]["errors"][0][0] == "WRONG_PASSWORD"):
                print("Incorrect username/password combo!")
                continue
            else:
                print("Login error occurred!")
                break

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
        # subprocess.check_call(["attrib", '+H', 'config.txt'])
    full_token = "Bearer " + user_token
    return full_token

full_token = ''
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
            full_token = get_token()
        else:
            # Something exists on the first line- we need to test it as a token
            headers = {
                'User-Agent': 'Project SnooKey/0.2',
                'Authorization': "Bearer " + firstline
            }
            token_check = requests.request("GET", url="https://oauth.reddit.com/api/v1/me/prefs/", headers=headers)
            if token_check.status_code == 200:
                # Token worked- use it
                full_token = "Bearer " + firstline
                print("Working token found!  Continuing...", flush=True)
            else:
                # Token did not work- we need a new one
                full_token = get_token()
else:
    print("Getting new token...", flush=True)
    # Config file does not exist- we need a new token
    full_token = get_token()

headers = {
    'User-Agent': 'Project SnooKey/0.2',
    'Authorization': full_token
}

# Live check of valid RPAN subreddits
subreddit_check = requests.request("GET", url="https://strapi.reddit.com/recommended_broadcaster_prompts",
                                   headers=headers)
rpan_subreddits_full = subreddit_check.json()["data"]
valid_list = []
# Loop through all the subreddits
for x in range(len(rpan_subreddits_full)):
    # Extract just the subreddit name and make a new list with the names
    valid_list.append(rpan_subreddits_full[x]["subreddit_name"].lower())

while True:
    subreddit = input("Subreddit you want to broadcast to: ")
    subreddit = subreddit.lower()
    if subreddit in valid_list:
        if subreddit == "pan":
            print(
                "NOTICE: You are only able to stream to r/pan during specific hours.  Please visit reddit.com/r/pan to learn more.")
            break
        else:
            break
    else:
        print("ERROR: " + subreddit + " is not a valid RPAN subreddit!")
        continue

title = urllib.parse.quote(input("Stream title: "))

broadcast_endpoint = "https://strapi.reddit.com/r/%s/broadcasts?title=%s" % (subreddit, title)

payload = {}
headers = {
    'User-Agent': 'Project SnooKey/0.2',
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
    print(
        "The reddit servers said \"NONE SHALL PASS\"!  \nMake sure you are eligible to stream.  If you are using r/pan make sure you are trying during valid hours.")

# Fix to prevent windows .exe from closing on completion
print("")
input("Press enter to exit...")