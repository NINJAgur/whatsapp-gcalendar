import datetime
import os.path
import pywhatkit

from bidi.algorithm import get_display
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
# , 'https://www.googleapis.com/auth/calendar',
# 'https://www.googleapis.com/auth/calendar.events.readonly', 'https://www.googleapis.com/auth/calendar.events']

USER_DICT = {
  "יעקב": "Jacob Solomon",
  "רועי": "Roei Goldwasser",
  "שני": "Shany Avitbol",
  "עידן": "Edan Gurin",
  "אופיר": "Ofir Itzhakov"
}

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
        pywhatkit.sendwhatmsg_to_group("LhccGDPEPKy3FCfLcdH739", "AUTOMATED MESSAGE : SHIFTS NEXT WEEK", now.hour, now.minute + 1, 15, True)
        
        # Prints the start and name of the next 10 events
        for event in events:
            if ('לילה' in event['summary']):
                start = event['start'].get('dateTime', event['start'].get('date'))
                # msg = get_display('בתאריך :' + start + ' ' + event['summary'])
                uname = event['summary'].split("-",1)[1].strip()
                event['summary'] = event['summary'].replace(uname, USER_DICT[uname])
                event['summary'] = event['summary'].replace("לילה", "shift")
                msg = 'Date: ' + start + ' ' + event['summary']
                print(msg)
                now = datetime.datetime.now()
                pywhatkit.sendwhatmsg_to_group("LhccGDPEPKy3FCfLcdH739", msg , now.hour, now.minute + 1, 15, True)


    except HttpError as error:
        print('An error occurred: %s' % error)


if __name__ == '__main__':
    main()