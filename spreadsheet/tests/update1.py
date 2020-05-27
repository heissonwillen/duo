# Get the data from the spreadsheet
# Convert data to Json format (to be easy to handle)

import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from . import state

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
spreadsheet_id = "1iPQjZXCwfL58-z4FfjcQFDRn5YTuN5sYiUA3jxqAtJ8"
client_secrets_file = "credentials.json"
range_name = "A2:A2"

def update_spreadsheet():
    print("Getting usernames from spreadsheet.")

    credentials = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
            credentials = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    service = build("sheets", "v4", credentials=credentials)
    sheet = service.spreadsheets()

    values = [
        [
            # Cell values ...
        ],
        # Additional rows
    ]
    data = [
        {
            'range': range_name,
            'values': values
        },
        # Additional ranges to update ...
    ]
    body = {
        'valueInputOption': value_input_option,
        'data': data
    }
    result = service.spreadsheets().values().batchUpdate(
        spreadsheetId=spreadsheet_id, body=body).execute()
    print('{0} cells updated.'.format(result.get('totalUpdatedCells')))
    


if __name__ == '__main__':
    pass

