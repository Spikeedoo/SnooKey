import gui
from pathlib import Path

config = Path("config.txt")
if config.is_file():
    with open("config.txt", encoding='utf-8') as f:
        post_id = f.readline()
        subreddit = f.readline()
        print("POPOUT FOR [" + post_id + "] ON [" + subreddit + "].", flush=True)
        gui = gui.SnooKeyGui(post_id, subreddit)
        gui.start()
else:
    print("You do not have any previous stream configurations.")