from pywhatkit import whats
from cloud import gcalendar
import datetime

def main():
    gcalendar.initConnection()    
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        nextDay = datetime.datetime.utcnow() + datetime.timedelta(hours=10)
        nextDay = nextDay.isoformat() + 'Z'
        
        events_today = gcalendar.getService().events().list(calendarId='primary', timeMin=now, 
                                                    timeMax = nextDay, maxResults=10, singleEvents=True,
                                                    orderBy='startTime').execute()
        eventsToday = events_today.get('items', [])
        message = "ביפ בופ אני הבוט של יוסטון :) \nהאירועים להיום : \n"

        if not eventsToday:
            print('Nothing Today.')
            return

        for event in eventsToday:
            message += event['summary'] + "\n"

        print(message)

        whats.sendwhatmsg_to_group_instantly(gcalendar.GROUP_TEST, message, 7, True)
        
    except Exception as error:
        print('An error occurred: %s' % error)
        raise

if __name__ == '__main__':
    main()