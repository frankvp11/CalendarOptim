



from model.user import User 
from model.event import Event
from model.stat import Stat
from model.notification import Notification
import datetime
# import uuid



def sendNotification(sender: str, recipient: str, message, duration, recipient_list, uuid, start_time=None, finish_time=None):
    # Fetch the recipient user
    user = User.collection.get(recipient)
    if not user:
        print("Recipient user not found.")
        return

    # Create a new notification object
    notif = Notification()
    notif.id = uuid
    notif.sender = sender
    notif.message = message
    notif.duration = duration
    notif.start_time = start_time 
    notif.finish_time = finish_time 
    notif.people = {recipient: 0 for recipient in recipient_list}

    # notif.save()  

  
    user.notifications.append(notif)
    user.save()

    print(f"Notification sent to {recipient}.")
    return 

    





