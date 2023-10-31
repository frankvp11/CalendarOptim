



from model.user import User 
from model.event import Event
from model.stat import Stat
from model.notification import Notification
import datetime





def remove_notification_by_id(username: str, notification):
    user = User.collection.get(username)
    if not user:
        return {"error": "User not found"}

    notification_to_remove = next((notif for notif in user.notifications if notif.id == notification.get("id")), None)

    # Remove the notification
    print("people", notification_to_remove.people)
    user.notifications.remove(notification_to_remove)
    user.save()  # This assumes the user object has a save method to update the database

    return {"success": "Notification removed successfully"}

