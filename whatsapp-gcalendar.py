import datetime
import os.path
from pywhatkit import whats
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# , 'https://www.googleapis.com/auth/calendar',
# 'https://www.googleapis.com/auth/calendar.events.readonly', 'https://www.googleapis.com/auth/calendar.events']

GROUP_ID = "KRVu9MZAIjkIcHep58dMS7"
GROUP_TEST = "LhccGDPEPKy3FCfLcdH739"
USER_TEST = "+972525420276"

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 4 events on the user's calendar.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)
        # Call the Calendar API
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        nextWeek =  datetime.datetime.utcnow() + datetime.timedelta(days=7)
        nextWeek = nextWeek.isoformat() + 'Z'
        print('Getting the upcoming 10 events')
        events_result = service.events().list(calendarId='k7d2r6hs1srcf5rp8ckac77lt0@group.calendar.google.com', timeMin=now, 
                                              timeMax = nextWeek, maxResults=10, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        now = datetime.datetime.now()
        message = "המשמרות בשבוע הבא : \n"

        for event in events:
            if ('לילה' in event['summary']):
                start = event['start'].get('dateTime', event['start'].get('date'))
                dt = datetime.datetime.strptime(start, '%Y-%m-%d')
                dt = '{0}/{1}/{2}'.format(dt.day, dt.month, dt.year)
                msg = 'בתאריך :' + dt + ' ' + event['summary']
                message += msg + "\n"
        
        
        print(message)
        
        whats.sendwhatmsg_to_group(GROUP_ID, message, now.hour, now.minute + 1, 15)

    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()