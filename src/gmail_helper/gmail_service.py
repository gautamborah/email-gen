# src/gmail_helper/email_reader.py

import os
import base64
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class GmailReader:
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

    def __init__(self, label_ids=["INBOX"]):
        """
        GmailReader automatically handles credentials and token files.
        Looks for 'credentials.json' and 'token.json' in the same directory.
        """
        self.label_ids = label_ids
        self.creds = None
        self.service = None
        self.emails = []
        self.index = -1

        self._load_credentials()
        self._fetch_emails()

    def _load_credentials(self):
        """Load or generate Gmail API credentials."""
        cred_path = "./src/gmail-helper/client_secret_74881337203-5vi2ppo5f84elttgplh3uvicr4e321i1.apps.googleusercontent.com.json"
        token_path = "token.json"

        # Load credentials from token.json if exists
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)

        # If no valid credentials, run OAuth flow
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(cred_path):
                    raise FileNotFoundError(f"{cred_path} not found! Download from Google Cloud Console.")
                flow = InstalledAppFlow.from_client_secrets_file(cred_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for next run in token.json
            with open(token_path, "w") as token_file:
                token_file.write(self.creds.to_json())

        # Initialize Gmail API
        self.service = build("gmail", "v1", credentials=self.creds)

    def _fetch_emails(self):
        """Fetch latest emails from Gmail."""
        results = self.service.users().messages().list(
            userId="me",
            labelIds=self.label_ids,
            maxResults=50
        ).execute()
        self.emails = results.get("messages", [])
        self.index = -1

    def get_next_email(self):
        """Return the next email content as a string. None if no more emails."""
        self.index += 1
        if self.index >= len(self.emails):
            return None

        msg_id = self.emails[self.index]["id"]
        msg = self.service.users().messages().get(userId="me", id=msg_id, format="full").execute()

        payload = msg.get("payload", {})
        parts = payload.get("parts", [])
        body = ""

        if parts:
            for part in parts:
                if part.get("mimeType") == "text/plain":
                    data = part.get("body", {}).get("data")
                    if data:
                        body += base64.urlsafe_b64decode(data).decode("utf-8")
        else:
            data = payload.get("body", {}).get("data")
            if data:
                body += base64.urlsafe_b64decode(data).decode("utf-8")

        return body

    def refresh(self):
        """Refresh the email list (fetch latest emails)."""
        self._fetch_emails()


# Optional: a helper function to login and return GmailReader instance
def login_and_get_reader(label_ids=["INBOX"]):
    """
    Initializes GmailReader and returns the instance.
    Handles OAuth login automatically.
    """
    reader = GmailReader(label_ids=label_ids)
    return reader