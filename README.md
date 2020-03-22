# SnooKey
Some reddit users figured out a way to stream to RPAN (Reddit's livestreaming platform) from desktop streaming software 
(like OBS).  Project SnooKey is my attempt at making this possibilty more accessible to RPAN users.

## Prerequisites
For this to work you will need Python3 installed to your system.      
*IF YOUR TERMINAL THINKS 'PYTHON' IS NOT A COMMAND, PYTHON HAS MOST LIKELY NOT BEEN ADDED TO YOUR PATH*

## Getting Started & Installation
First, find a folder that you can clone the SnooKey repository to.  Navigate to the folder and run:
```
git clone https://github.com/Spikeedoo/SnooKey.git
```
Navigate to the repository:
```
cd SnooKey
```

## Using SnooKey
Once you are inside SnooKey's clone repo, run the script:
```
python snookey.py
```
This command will open a link in your browser allowing you to get an access code from Reddit    
**NOTE:** The Reddit app you are allowing access is not mine.  It is the client_id of the mobile, in this case android, version of Reddit.    
Copy the access code from the localhost callback url and reply to the prompt in your terminal:
```
Please enter your access token: <enter access token here>
```
Follow the next two prompts by passing the subreddit you want to broadcast to and your stream's title:
```
Subreddit you want to broadcast to: <i.e. 'distantsocializing'>
Stream title: <i.e. 'Hello!'>
```
If all goes well you will be given your streamer key and the rpan link people will visit your stream from.

## How to use your streamer key
Step 1: Open up your desktop streaming software (in my example, OBS)    
Step 2: Navigate to your stream settings (Settings > Stream in OBS)   
Step 3: Make sure your Service is set to 'Custom' and fill in the following settings:
- Server: rtmp://ingest.redd.it/inbound/
- Stream Key: <your stream key>
Now hit 'Apply' and 'OK'

Hit 'Start Streaming' and watch the magic happen!
