# SnooKey
Some reddit users figured out a way to stream to RPAN (Reddit's livestreaming platform) from desktop streaming software 
(like OBS).  Project SnooKey is my attempt at making this possibilty more accessible to RPAN users.

## SUPPORT COMMUNITY CREATORS!
These wonderful people have contributed their time to the project and their own unique implementations.  Show them some love!  
**u/IOnlyPlayAsDrif made an updated version to improve the user experience: [Snookey2](https://github.com/IOnlyPlayAsDrift/Snookey2)**  
**u/premek_v made a bash based version for Linux systems! [SnooKey (Bash)](https://github.com/premek/rpan)**  
**u/mingoXII is working on a version of SnooKey with a GUI! [SnooKey3](https://github.com/warpspeedchic/Snookey3)**  

## START HERE
### Method 1 (Windows only)
If you have a windows machine, you can run SnooKey without installing python by simply cloning the repository
(see 'Installation' section) and running ```snookey.exe```

### Method 2 (All platforms)
For this to work you will need Python3 installed to your system.      
*IF YOUR TERMINAL THINKS 'PYTHON' IS NOT A COMMAND, PYTHON HAS MOST LIKELY NOT BEEN ADDED TO YOUR PATH*     
[Install Python for Windows](https://realpython.com/installing-python/#windows)   
[Install Python for Linux](https://realpython.com/installing-python/#linux)   
[Install Python for OS X](https://realpython.com/installing-python/#macos-mac-os-x)   
Make sure the python requests module is installed for the script to work:
```
pip install requests
```
OR
```
pip3 install requests
```

## Installation
Download the zip file by pressing the green 'Clone or download' button and selecting 'Download ZIP'   
**OR**    
Clone the repository with:
```
git clone https://github.com/Spikeedoo/SnooKey.git
```
Navigate to the repository:
```
cd SnooKey
```

## Using SnooKey
Once you have SnooKey downloaded, it is time to run the script.     
(**If you used method #1 simply run ```snookey.exe```**)
```
python snookey.py
```
OR
```
python3 snookey.py
```
After some Reddit backend changes, the current auth flow will ask you to enter your username and password. 

After a successful login, follow the next two prompts by passing the subreddit you want to broadcast to and your stream's title:
```
Subreddit you want to broadcast to: <i.e. distantsocializing>
Stream title: <i.e. RPAN and chill!>
```
If all goes well you will be given your streamer key and the rpan link people will visit your stream from.

## How to use your streamer key
Step 1: Open up your desktop streaming software (in my example, OBS)    
![snookey02](examples/snookey02.PNG)    
Step 2: Navigate to your stream settings (Settings > Stream in OBS)   
![snookey03](examples/snookey03.PNG)    
Step 3: Make sure your Service is set to 'Custom' and fill in the following settings:
- Server: rtmp://ingest.redd.it/inbound/
- Stream Key: (your stream key)

![snookey04](examples/snookey04.PNG)    
Now hit 'Apply' and 'OK'

Hit 'Start Streaming' and watch the magic happen!

Right now we believe 1080x1920 downscaled to 720x1280 is the way to go.

Please be responsible and follow the [Rules](https://www.redditinc.com/policies/broadcasting-content-policy).  Cheers.  
