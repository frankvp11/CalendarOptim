
from model.taskrequest import TaskStatus
from model.notification import Notification
from model.event import Event
from model.user import User
import datetime
from .add_task import check_database
import sys
sys.path.append("..")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/frontend/")
# import sys
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
# sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
import pages.globalState
from send_notification import sendNotification
import uuid

def addRequest(start, stop, summary: str, people: list, sender, uuid):
    task = TaskStatus()
    task.id = uuid
    task.event = Event(start=start, end=stop, summary=summary, regular_event=False)
    task.people_status = {person: 0 for person in people}
    task.people_status[sender] = 1
    task.save()




def viewStatus(notification):
    task = TaskStatus.collection.fetch()
    if not task:
        return {"error": "Task not found"}
    else:
        for t in task:
            if t.notification == notification:
                rand = t
                break

def retrieve(custom_uuid):
    try:
        task_status = TaskStatus.collection.get(custom_uuid)
        if task_status:
            print(f"Successfully retrieved TaskStatus with UUID: {custom_uuid}")
            print(task_status.to_dict())
            return task_status
        else:
            print(f"No TaskStatus found with UUID: {custom_uuid}")
            return None
    except Exception as e:
        print(f"Error retrieving TaskStatus: {e}")
        return None

     

def deleteTaskRequest(task, person, custom_uuid):
    print(task, person, custom_uuid)
    user = User.collection.get(person)
    if user and user.notifications:
        # Create a new list excluding the notification with the specified custom_uuid
        updated_notifications = [notification for notification in user.notifications if notification.id != custom_uuid]
        
        # Update the user's notifications list
        user.notifications = updated_notifications
        
        # Save the user document back to Firestore
        user.save()
        print(f"Notification with UUID {custom_uuid} deleted.")
    else:
        print("Notification not found for person", person)





def deleteTaskStatus(custom_uuid):
    try:
        # task_to_delete = TaskStatus.collection.get(custom_uuid)
        # if task_to_delete:
            TaskStatus.collection.delete(f"task_status/" +custom_uuid)
            print("Deleted task with uuid ", custom_uuid)
        # else:
            # print(f"Task with UUID {custom_uuid} not found!")
    except Exception as e:
        print(f"Error during deletion: {e}")



def update_persons_calendar(username, start, end, summary):
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

def return_notifications(username, status, custom_uuid): # sender: str, recipient: str, message, duration, recipient_list, uuid, start_time=None, finish_time=None
    user = User.collection.get(username)
    if user and user.notifications:
        # Create a new list excluding the notification with the specified custom_uuid
        sendee = [notification for notification in user.notifications if notification.id == custom_uuid][0]#.sender

    print("Returning notifications to say that I accepted/rejected")
    if status == 1:
        message = f"{username} has accepted your invitation to {sendee.message}"
    else:
        message = f"{username} has rejected your invitation to {sendee.message}"
    
    sendNotification(username, sendee.sender,  "Accepted invitatoin", sendee.duration, [], str(uuid.uuid4()), summary=message)
                # sender: str, recipient: str, message, duration, recipient_list, uuid, start_time=None, finish_time=None
    return



def updateStatus(custom_uuid, person, status):

    # Directly query for the task with the specific ID
    task = TaskStatus.collection.fetch()
    for t in task:
        if t.id == custom_uuid:
            task = t

    if not task:  # If the task with the specified ID is not found
        print("Task not found!")
        return {"error": "Task not found"}

    if (sum(value == 1 for value in task.people_status.values()) == len(task.people_status)-1):
        print("Everyone accepted")

        return_notifications(person,   status, custom_uuid)

        for person in task.people_status.keys():
            print("Must update ", person)
            update_persons_calendar(person, task.event.start, task.event.end, task.event.summary)
            deleteTaskRequest(task, person, custom_uuid)
            check_database(person)
        
        deleteTaskStatus(custom_uuid)

        return True
    # Update the person's status in the task
    elif sum(value  for value in task.people_status.values()) == ((len(task.people_status) * 2) -3):
        print("Everyone rejected")
        deleteTaskStatus(custom_uuid)
        return_notifications(person, status, custom_uuid)

        for person in task.people_status.keys():
            deleteTaskRequest(task, person, custom_uuid)

        return False
    else:
        task.people_status[person] = status

        return_notifications(person,   status, custom_uuid)
        deleteTaskRequest(task, person, custom_uuid)
        ## Send a new notification, to the person so sent the invite, that he/she accepted or rejected
        ## the invite


        task.save()

    return False
