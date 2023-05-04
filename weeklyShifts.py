from pywhatkit import whats
from cloud import gcalendar
import datetime

def main():
    gcalendar.initConnection()
    
    try :
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        nextWeek =  datetime.datetime.utcnow() + datetime.timedelta(days=7)
        nextWeek = nextWeek.isoformat() + 'Z'
        events_result = gcalendar.getService().events().list(calendarId='primary', timeMin=now, 
                                        timeMax = nextWeek, maxResults=20, singleEvents=True,
                                        orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        message = "ביפ בופ אני הבוט של יוסטון :) \nהמשמרות בשבוע הנוכחי : \n"

        for event in events:
            if ('לילה' in event['summary']):
                start = event['start'].get('dateTime', event['start'].get('date'))
                dt = datetime.datetime.strptime(start, '%Y-%m-%d')
                dt = '{0}/{1}/{2}'.format(dt.day, dt.month, dt.year)
                msg = 'בתאריך :' + dt + ' ' + event['summary']
                message += msg + "\n"
        
        print(message)
        whats.sendwhatmsg_to_group_instantly(gcalendar.GROUP_TEST, message, 7, True)
        
    except Exception as error:
        print('An error occurred: %s' % error)
        raise
    
if __name__ == '__main__':
    main()