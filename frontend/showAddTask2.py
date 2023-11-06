from nicegui import ui
from dateutil.parser import parse
import datetime

import sys
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
import backend.add_task
import backend.send_notification
import backend.checkRequest
import pages.login
import uuid
import fastapi

start_date = None
end_date = None
task_name = None
task_duration = None
share_with_people = []
share_username = None
check_box_values = []
def add_task(username):
    print("Adding task")
    global start_date, end_date, task_name, check_box_values, share_with_people

    
    best_time = {"start":start_date, "end":end_date}
    list_of_people = [person for (person, checkbox) in zip(share_with_people, check_box_values) if checkbox.value]
    print(best_time)
    recipient_usernames = [[user["username"]  for user in pages.login.users if user['email']==recipient][0] for recipient in list_of_people]
    custom_uuid = str(uuid.uuid4())
    for recipient_username in recipient_usernames:
        backend.send_notification.sendNotification(username, recipient_username, task_name.value, task_duration.value, recipient_usernames, custom_uuid, best_time.get("start"), best_time.get("end")) # sender: str, recipient: str, message, duration, start_time=None, finish_time=None
    backend.checkRequest.addRequest(best_time.get("start"), best_time.get("end"), task_name.value, recipient_usernames, username, custom_uuid)
    print("Sent request with id ", custom_uuid)
    ui.notify("Task shared successfully", color="positive")




def share_event():
    global share_username, share_with_people
    card = ui.menu().style("width: 80%; height: 100%;")
    with card:
        @ui.refreshable
        def inside_func():
            global share_username, share_with_people, check_box_values
            print(check_box_values)

            with ui.row():
                with ui.column().style("width: 25%; margin-top: 2%; margin-left: 2%;"):
                    ui.label("Add User's Email").style("font-size: 1.5vw")
                    if share_username is not None:
                        share_with_people.append(share_username.value)
                        share_username = ui.input("Email")
                    else:
                        share_username = ui.input("Email")
                with ui.column().style("width: 20%; margin-top: 2%; margin-right: 2%;"):
                    ui.button("Add Person", on_click=lambda : inside_func.refresh()).style("font-size: 1vw;")
    
                with ui.column().style("width: 40%; margin-top: 2%; margin-right: 2%;"):
                    for index, person in enumerate(share_with_people):
                        with ui.row().style("width: 100%;"):
                            with ui.column().style("width: 40%; margin-right: 2%"):
                                ui.label(person).style("font-size: 24px;")
                            with ui.column().style("width: 40%;"):
                                if index < len(check_box_values):
                                    check_box_values[index] = ui.checkbox("Include", value=check_box_values[index].value)
                                    continue
                                check_box_values.append(ui.checkbox("Include", value=True))
        inside_func()


def choose_time():
    global start_date, end_date
    print("Choose time!")
    card = ui.menu().style("width: 80%; height: 100%;")
    with card:
        with ui.row():
            with ui.column():
                ui.label("Start Date")
                start_date_input = ui.date(value=datetime.datetime.today())
            with ui.column():
                ui.label("Start Time")
                start_time = ui.time(value="12:00")

        # Create another row for the end date and time
        with ui.row():
            with ui.column():
                ui.label("End Date")
                end_date_input = ui.date(value=datetime.datetime.today())
            with ui.column():
                ui.label("End Time")
                end_time = ui.time(value="12:00")

        def save_user_made_date():
            global start_date, end_date
            nonlocal  start_time, end_time, start_date_input, end_date_input
            card.delete()
            if not isinstance(start_date_input.value, datetime.datetime):
                start_day = parse(start_date_input.value)
            else:
                start_day = start_date_input.value
            if not isinstance(end_date_input.value, datetime.datetime):
                end_day = parse(end_date_input.value)
            else:
                end_day = end_date_input.value
            if not isinstance(start_time, datetime.datetime):
                start_time = parse(start_time.value)
            else:
                start_time = start_time.value
            if not isinstance(end_time, datetime.datetime):
                end_time = parse(end_time.value)
            else:
                end_time = end_time.value
            end_date = datetime.datetime.combine(end_day, end_time.time())
            start_date = datetime.datetime.combine(start_day, start_time.time())    

        ui.button("Save", on_click=lambda x: save_user_made_date())


def determine_time(username):
    global share_with_people, check_box_values, task_duration, task_name, start_date, end_date
    list_of_people = [person for (person, checkbox) in zip(share_with_people, check_box_values) if checkbox.value]
    events_total = [backend.add_task.check_database(user) for user in list_of_people]
    events_total.append(backend.add_task.check_database(username))
    events_total = sum([event.get("events3") for event in events_total], [])
    best_time = backend.add_task.determine_best_time([{"name":task_name.value, "duration":float(task_duration.value)}], username, events_total)[0].get("best_time")
    print(best_time)
    start_date, end_date = best_time.get("start"), best_time.get("end")

    # recipient_usernames = [[user["username"]  for user in pages.login.users if user['email']==recipient][0] for recipient in list_of_people]
    # custom_uuid = str(uuid.uuid4())
    # for recipient_username in recipient_usernames:
    #     backend.send_notification.sendNotification(username, recipient_username, task_name.value, task_duration.value, recipient_usernames, custom_uuid, best_time.get("start"), best_time.get("end")) # sender: str, recipient: str, message, duration, start_time=None, finish_time=None
    # backend.checkRequest.addRequest(best_time.get("start"), best_time.get("end"), task_name.value, recipient_usernames, username, custom_uuid)
    # print("Sent request with id ", custom_uuid)
    # ui.notify("Task shared successfully", color="positive")
    
    # def share_task(recipients, task_name, duration, username):
    #     events_total = [backend.add_task.check_database(user) for user in recipients]
    #     events_total.append(backend.add_task.check_database(username)) 
    #     events_total = sum([event.get("events3") for event in events_total], [])
    #     best_time = backend.add_task.determine_best_time([{"name":task_name, "duration":float(duration)}], username, events_total)[0].get("best_time")

    #     recipient_usernames = [[user["username"]  for user in pages.login.users if user['email']==recipient.value][0] for recipient in recipients]
    #     custom_uuid = str(uuid.uuid4())
    #     for recipient_username in recipient_usernames:
    #         backend.send_notification.sendNotification(username, recipient_username, task_name, duration, recipient_usernames, custom_uuid, best_time.get("start"), best_time.get("end")) # sender: str, recipient: str, message, duration, start_time=None, finish_time=None

    #     backend.checkRequest.addRequest(best_time.get("start"), best_time.get("end"), task_name, recipient_usernames, username, custom_uuid)
    #     print("Sent request with id ", custom_uuid)
    #     ui.notify("Task shared successfully", color="positive")



def add(username):
    global task_name, task_duration
    right_drawer = (
        ui.right_drawer(fixed=False, elevated=True)
        .classes("bg-blue-100")
        .props("overlay")
        .style("position:relative; ")
        .props("behavior=mobile")
    )
    right_drawer.toggle()
    with right_drawer:
        task_name = ui.input("Task name")
        task_duration = ui.input("Task duration (hours)")
        with ui.button("Share event" ): # on_click=lambda x : share_event()
            share_event()
        with ui.button("Choose time"): #  on_click=lambda x : choose_time()
            choose_time()
        ui.button("Determine best time ", on_click=lambda x : determine_time(username))

        ui.button("Add task", on_click=lambda x : (add_task(username)))