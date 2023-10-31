from model.user import User 
from model.event import Event
from model.stat import Stat
import datetime




def getStats(username: str):

    user = User.collection.get(username)
    if not user:
        return {"error": "User not found"}

    past_regular_events_count = sum(1 for ev in user.events if ev.end.replace(tzinfo=None) < datetime.datetime.now() and ev.start.replace(tzinfo=None) > datetime.datetime.now()-datetime.timedelta(days=30) and ev.regular_event)
    past_non_regular_events_count = sum(1 for ev in user.events if ev.end.replace(tzinfo=None) < datetime.datetime.now() and ev.start.replace(tzinfo=None) > datetime.datetime.now()-datetime.timedelta(days=30) and not ev.regular_event)

    return {
        "past_regular_events": past_regular_events_count,
        "past_non_regular_events": past_non_regular_events_count
    }
