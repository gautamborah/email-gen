from __future__ import print_function
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying scopes, delete the token.json
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

cred_file = "./src/gmail-helper/client_secret_74881337203-5vi2ppo5f84elttgplh3uvicr4e321i1.apps.googleusercontent.com.json"

def main():
    creds = None
    # Load saved token
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If no valid token, do OAuth login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(cred_file, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save token for later use
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Connect to Gmail API
    service = build('gmail', 'v1', credentials=creds)

    # Fetch messages from inbox
    results = service.users().messages().list(userId='me', labelIds=['INBOX'], maxResults=5).execute()
    messages = results.get('messages', [])

    if not messages:
        print("No messages found.")
    else:
        for msg in messages:
            msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
            snippet = msg_data.get("snippet")
            print(f"📧 {snippet}")

if __name__ == '__main__':
    main()
