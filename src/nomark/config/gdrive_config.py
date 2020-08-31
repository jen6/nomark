from typing import Optional
from urllib.parse import quote_plus
from requests.sessions import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os


class GdriveConfig:
    _SCOPES = [
        "https://www.googleapis.com/auth/drive",
        "https://www.googleapis.com/auth/drive.file",
    ]

    blog_folder: str

    def __init__(self, article_title: str, image_folder: str = "imghosting"):
        self.article_title = quote_plus(article_title)
        self.blog_folder = quote_plus(image_folder)
        self.credit = self.get_credit()

    def get_credit(self):
        creds = None
        home = os.path.expanduser("~")
        if os.path.exists(home + "/.cred/token.pickle"):
            with open(home + "/.cred/token.pickle", "rb") as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    home + "/.cred/credentials.json", self._SCOPES
                )
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(home + "/.cred/token.pickle", "wb") as token:
                pickle.dump(creds, token)

        return creds
