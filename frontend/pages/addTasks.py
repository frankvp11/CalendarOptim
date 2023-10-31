import json
from nicegui import ui, app
import components.sidebar
import components.header

name_input = None
start_date = None
end_date = None
start_time = None
end_time = None
name  = None
duration = None

from nicegui import ui
from . import globalState
import datetime
from dateutil.parser import parse

import pages.login
from fastapi.requests import Request

import sys
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")

import backend.add_task
import backend.save_task
import backend.send_notification
import time
import backend.checkRequest
import fastapi
import uuid

def add(request: Request):

    username = pages.login.session_info.get(str(request.session.get("id")), {}).get("username")
    tasks_to_add = []
    updated_tasks_to_add = []
    
    def share_task(recipients, task_name, duration, username):
        events_total = [backend.add_task.check_database(user) for user in recipients]
        events_total.append(backend.add_task.check_database(username)) 
        events_total = sum([event.get("events3") for event in events_total], [])
        best_time = backend.add_task.determine_best_time([{"name":task_name, "duration":float(duration)}], username, events_total)[0].get("best_time")

        recipient_usernames = [[user["username"]  for user in pages.login.users if user['email']==recipient.value][0] for recipient in recipients]
        custom_uuid = str(uuid.uuid4())
        for recipient_username in recipient_usernames:
            backend.send_notification.sendNotification(username, recipient_username, task_name, duration, recipient_usernames, custom_uuid, best_time.get("start"), best_time.get("end")) # sender: str, recipient: str, message, duration, start_time=None, finish_time=None

        backend.checkRequest.addRequest(best_time.get("start"), best_time.get("end"), task_name, recipient_usernames, username, custom_uuid)
        print("Sent request with id ", custom_uuid)
        ui.notify("Task shared successfully", color="positive")

        
    def share_task_func():
        recipients = []
        card = ui.card().style("width: 100%; height:100%;")
        with card:
            ui.label("Share")
            add_recipient_button = ui.button("Add recipient", on_click=lambda : (render_recipients()))
            share_button = ui.button("Share with all recipients", on_click=lambda : share_task(recipients, name.value, duration.value, username))
            def render_recipients():
                nonlocal recipients
                nonlocal add_recipient_button, share_button
                recipients.append(ui.input("Email"))
                add_recipient_button.delete()
                share_button.delete()
                add_recipient_button = ui.button("Add recipient", on_click=lambda : (render_recipients()))
                share_button = ui.button("Share with all recipients", on_click=lambda : (share_task(recipients, name.value, duration.value, username)))
            render_recipients()



    @ui.page("/addTasks")
    def main(request: fastapi.requests.Request):
        ui.add_head_html('''
            <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/main.min.css' rel='stylesheet' />
            <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>
            <script>
                function renderFullCalendar(elementId, events) {
                    var calendarEl = document.querySelector('.' + elementId);
                    
                    if (calendarEl) {
                        window.calendarInstance = new FullCalendar.Calendar(calendarEl, {
                            initialView: 'timeGridWeek',
                            slotMinTime: "05:00:00",
                            slotMaxTime: "22:00:00",
                            allDaySlot: false,
                            timeZone: 'local',
                            height: 'auto',
                            events: events
                        });
                        
                        window.calendarInstance.render();
                    }
                }
            </script>
        ''')

        global name_input, start_date, end_date, start_time, end_time, name, duration

        components.header.add(request, "addTasks")
        with ui.row():
            with ui.column():
                with ui.row():
                    ui.label("Add a task")
                with ui.row():
                    name_input = ui.input("Task Name")
                
                with ui.row():
                    with ui.column():
                        ui.label("Start Date")
                        start_date = ui.date(value=datetime.datetime.today())
                    with ui.column():
                        ui.label("Start Time")
                        start_time = ui.time(value="12:00")
                
                # Create another row for the end date and time
                    with ui.column():
                        ui.label("End Date")
                        end_date = ui.date(value=datetime.datetime.today())
                    with ui.column():
                        ui.label("End Time")
                        end_time = ui.time(value="12:00")

                ui.button("Add a task", on_click=lambda : add_event())

                with ui.row():
                    ui.label("Determine the Best Time to do a task")
                with ui.row():
                    with ui.column():
                        name = ui.input("Task name")
                    with ui.column():
                        duration=  ui.input("Estimated Duration")
                    with ui.column():
                        share_task = ui.button("Share Task", on_click=lambda : share_task_func())

                ui.button("Add task", on_click=lambda : add_task())

                # ui.button("Determine the best time for a task", on_click=lambda : determine_best_time())

                ui.button("View updated calendar").on("click", place_card)
            
            def handle_change(e, index):
                if e.value == True:
                    updated_tasks_to_add.append(tasks_to_add[index])
                else:
                    updated_tasks_to_add.remove(tasks_to_add[index])

            @ui.refreshable
            def update_tasks_list():
                nonlocal tasks_to_add
                
                with ui.column():
                    ui.label("User added tasks")
                    all_tasks = tasks_to_add   # Combine both lists

                    for index, task in enumerate(all_tasks):
                        with ui.row():
                            # Label
                            with ui.column():
                                if 'title' in task:
                                    ui.label(task.get("title")).style("font-size: 20px; width: 100px;")
                                else:
                                    ui.label(task.get("name")).style("font-size: 20px; width: 100px;")
                            
                            with ui.column():
                                ui.checkbox("Include", value=(task in updated_tasks_to_add), on_change=lambda e, i=index : handle_change(e, i)).style("margin-top: -5%;")

            update_tasks_list()
    

            def add_task():
                global name, duration
                nonlocal username
                stuff = backend.add_task.determine_best_time([{"name":name.value, "duration":float(duration.value)}], username, updated_tasks_to_add)
                stuff=  stuff[0].get("best_time")
                start, end, title = stuff.get("start"), stuff.get("end"), stuff.get("summary")
                tasks_to_add.append({"title":str(title), "start":str(start), "end":str(end), "color":"red"})
                updated_tasks_to_add.append({"title":str(title), "start":str(start), "end":str(end), "color":"red"})
                name.value = ""
                duration.value = ""
                update_tasks_list.refresh()

        def add_event():
                global name_input, start_date, end_date
                nonlocal tasks_to_add
                start_datetime, end_datetime = determine_date()

                # Try to parse start and end dates, if it's already a date object it'll just pass
                tasks_to_add.append({"title":str(name_input.value), "start":str(start_datetime), "end":str(end_datetime), "color":"red"})
                updated_tasks_to_add.append({"title":str(name_input.value), "start":str(start_datetime), "end":str(end_datetime), "color":"red"})
                name_input.value = ""
                start_date.value = datetime.datetime.today()
                end_date.value = datetime.datetime.today()

                update_tasks_list.refresh()


    def place_card():
        card_element = ui.card().style("position: fixed; left:5%; top: 5%; z-index: 1000; height: 80%; width:1000px;").classes("my-calendar")
        with card_element:
            ui.button("Close", on_click=card_element.delete)
            ui.button("Save calendar", on_click=lambda : (backend.save_task.add_to_database(tasks_to_add, pages.login.users_id), update_tasks_to_add()))
        temp_array = globalState.events.copy()
        for  task in updated_tasks_to_add:

                temp_array.append({"title":task.get("title"), "start":task.get("start"), "end":task.get("end"), "color":"red"})

        ui.run_javascript(f'renderFullCalendar("my-calendar", {temp_array});')





    def update_tasks_to_add():
        nonlocal tasks_to_add #, checkbox_column
        tasks_to_add2 = []
        for i, task in enumerate(updated_tasks_to_add):

                tasks_to_add2.append({"title":task.get("title"), "start":task.get("start"), "end":task.get("end")})
            # print("Hello frank!")
        globalState.events.extend(tasks_to_add2)
        print("Done updating the tasks to add, along with the global stats")
        tasks_to_add = []
        ui.run_javascript(f'renderFullCalendar("my-calendar", {globalState.events});')
        


    def determine_date():
        global name_input, start_date, end_date, start_date, end_date

        try:
            start_date_object = parse(start_date.value).date()
        except (TypeError, ValueError):
            start_date_object = start_date.value

        try:
            end_date_object = parse(end_date.value).date()
        except (TypeError, ValueError):
            end_date_object = end_date.value

        try:
            start_time_object = parse(start_time.value).time()
        except (TypeError, ValueError):
            start_time_object = start_time.value

        try:
            end_time_object = parse(end_time.value).time()
        except (TypeError, ValueError):
            end_time_object = end_time.value

        start_datetime = datetime.datetime.combine(start_date_object, start_time_object)
        end_datetime = datetime.datetime.combine(end_date_object, end_time_object)
        return start_datetime, end_datetime



