
from model.user import User 
from model.event import Event
from model.stat import Stat
from model.notification import Notification
import datetime




def getNotifications(username: str):

    user = User.collection.get(username)
    if not user:
        return {"error": "User not found"}
    
    # notifications = [notif.to_dict() for notif in Notification.collection.all() if notif.user == user]
    notifications = [notif.to_dict() for notif in user.notifications]

    return {
        "notifications": notifications
    }
