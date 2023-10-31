import datetime
import pytz
from model.user import User
from model.event import Event
from model.stat import Stat

def add_to_database(tasks: list[dict], username:str):
    print(tasks)
    for task in tasks:
        start_str = task['start']
        end_str = task['end']
        try:
            start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.timezone('America/Toronto')).replace(tzinfo=None)
            end = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S.%f').astimezone(pytz.timezone('America/Toronto')).replace(tzinfo=None)
        except ValueError:
            start = datetime.datetime.strptime(start_str, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('America/Toronto')).replace(tzinfo=None)
            end = datetime.datetime.strptime(end_str, '%Y-%m-%d %H:%M:%S').astimezone(pytz.timezone('America/Toronto')).replace(tzinfo=None)
        
        summary = task['title']
        print(f"Recieved add command! Adding task which starts at {start} and ends at {end}")

        user = User.collection.get(username)
        if not user:
            user = User(id=username)
            user.events = []
            user.stats = []
            user.save()


        # Check if the event already exists to prevent duplicate entries
        event_exists = any(ev.start == start and ev.end == end and ev.summary == summary for ev in user.events)
        if not event_exists:
            event = Event(start=(start+datetime.timedelta(hours=4)), end=(end + datetime.timedelta(hours=4)), summary=summary, regular_event=False)
            user.events.append(event)
        
        user.save()
    print("Done updating teh database!")
    return {"status": "Task added successfully"}