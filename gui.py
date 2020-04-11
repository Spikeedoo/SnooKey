import praw
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from threading import Thread
from time import sleep

class SnooKeyGui:
    def __init__(self, post_id, subreddit):
        self.post_id = post_id
        self.subreddit = subreddit

    def start(self):
        # PRAW Config
        reddit = praw.Reddit(client_secret=None, client_id="ahBF0SfzDT_WgQ", user_agent="Project SnooKey/0.1", username="", password="")

        # Set up GUI
        app = QApplication([])
        text_area = QPlainTextEdit()
        text_area.setFocusPolicy(Qt.NoFocus)
        layout = QVBoxLayout()
        layout.addWidget(text_area)
        window = QWidget()
        window.setLayout(layout)
        window.show()

        subreddit = reddit.subreddit(self.subreddit)
        new_messages = []
        def fetch_new_messages():
            while True:
                # Loop through comments
                for comment in subreddit.stream.comments(skip_existing=True):
                    if comment.parent() == self.post_id:
                        # Append comment to message array
                        string = "%s: %s" % (str(comment.author), str(comment.body))
                        new_messages.append(string)
                    sleep(.5)
        # Fetch messages on other thread
        thread = Thread(target=fetch_new_messages, daemon=True)
        thread.start()

        def display_new_messages():
            while new_messages:
                # Append new messages to text box
                text_area.appendPlainText(new_messages.pop(0))


        # Set up timer interval
        timer = QTimer()
        timer.timeout.connect(display_new_messages)
        timer.start(1000)
        app.exec_()