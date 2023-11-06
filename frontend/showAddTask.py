

from nicegui import ui, app

import datetime
import uuid
import sys

sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")

import backend.add_task
import backend.save_task
import backend.send_notification
import backend.checkRequest
import pages.login
from dateutil.parser import parse
import pages.globalState


def share_task(recipients, task_name, username):
    print("Sharing task")
    for person in recipients:
         print(person.value)
    print(task_name, username)
    return None


def add(username):
    temp_array = pages.globalState.events
    total_tasks = []
    check_box_values= []
    task_input_been_created = False
    with ui.menu().style("width: 100%; height: 100%;"):
        with ui.row().style("width: 100%; height: 100%;"):
            with ui.column().style("width: 60%; height: 100%; position: absolute; left: 0%; margin-right: 2%; margin-left: 2%;"):
                        ui.element().classes('my-calendar-addtasks').style("width: 100%; height: 600px;")

            def place_calendar_element():
                        ui.run_javascript(f'renderFullCalendar("my-calendar-addtasks", {temp_array});')
            
            with ui.column().style("position: absolute; right: 10%; width: 20%; height: 100%;"):
                with ui.row().style("display:flex"):
                    with ui.column().style("width: 50%; height: 100%; flex: 1;"):
                        #Requests a task name
                        task_name_input= None
                        start_date = None
                        end_date = None
                        @ui.refreshable
                        def add_task():
                            nonlocal task_name_input, start_date, end_date, task_input_been_created
                            if task_name_input and start_date and end_date:
                                
                                total_tasks.append({"title": task_name_input.value, "start": start_date, "end": end_date, "color":"red"})
                                print(total_tasks)
                                temp_array.append({"title": task_name_input.value, "start": start_date, "end": end_date, "color":"red"})
                                place_calendar_element()
                                update_task_list.refresh()
                                task_name_input.value = ""

                            elif not task_input_been_created:
                                task_name_input = ui.input("Task name").style("top:0%;")
                                task_input_been_created = True
                            else:
                                 ui.notify("Missing fields  ", color="negative")
                            
                        add_task()


                        # if task name input exists, we can then ask them to share, add a time, or determine best time
                        
                        ui.button("Share event", on_click=lambda x : share_event())

                        ui.button("Choose time", on_click=lambda x : choose_time())
                        ui.button("Determine best time ", on_click=lambda x : determine_time())
                        ui.button("Add Task", on_click=lambda x : (add_task()))

                        def share_event():
                            recipients = []
                            card = ui.card().style("width: 100%; height: 100%; z-index: 1000; position: fixed; left: 10%; top: 10%;")
                            with card:
                                ui.label("Share")
                                add_recipient_button = ui.button("Add recipient", on_click=lambda : (render_recipients()))
                                share_button = ui.button("Share with all recipients", on_click=lambda x: share_task(recipients, task_name_input.value, username))
                                def render_recipients():
                                    nonlocal recipients
                                    nonlocal add_recipient_button, share_button, close_button
                                    recipients.append(ui.input("Email"))
                                    add_recipient_button.delete()
                                    share_button.delete()
                                    close_button.delete()
                                    add_recipient_button = ui.button("Add recipient", on_click=lambda : (render_recipients()))
                                    share_button = ui.button("Share with all recipients", on_click=lambda x: (share_task(recipients, task_name_input.value, username)))
                                    close_button = ui.button("Close", on_click=lambda x: card.delete())
                                close_button = ui.button("Close", on_click=lambda x: card.delete())
                        
                        
                        def determine_time():
                            return None
                        

                        def choose_time():
                            card = ui.card().style("width: 100%; height: 100%; z-index: 1000; position: fixed; left: 10%; top: 10%;")
                            with card:
                                with ui.row():
                                    with ui.column():
                                        ui.label("Start Date")
                                        start_date_input = ui.date(value=datetime.datetime.today())
                                    with ui.column():
                                        ui.label("Start Time")#.style("position: absolute; right: 2%; top: 5%;")
                                        start_time = ui.time(value="12:00")#.style("position: absolute; right: 2%; top: 8%;")
                                    
                                    # Create another row for the end date and time
                                with ui.row():
                                    with ui.column():
                                        ui.label("End Date")#.style("position: absolute; right: 2%; top: 12%;")
                                        end_date_input = ui.date(value=datetime.datetime.today())#.style("position: absolute; right: 2%; top: 20%;")
                                    with ui.column():
                                        ui.label("End Time")#.style("position: absolute; right: 2%; top: 30%;")
                                        end_time = ui.time(value="12:00")#.style("position: absolute; right: 2%; top: 45%;")
                                def save_user_made_date():
                                    nonlocal start_date, end_date, start_time, end_time, start_date_input, end_date_input
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

                        
                        ui.button("View updated calendar", on_click=lambda x: place_calendar_element())#.style("position: absolute; right: 2%; bottom: 10%;")

                    with ui.column().style("width: 50%; height: 100%; flex:1; margin-top: 2%;"):
                        ui.label("Your tasks")

                        @ui.refreshable
                        def update_task_list():
                                with ui.column():
                                    total_tasks   

                                    for index, task in enumerate(total_tasks):
                                        with ui.row():
                                            # 
                                            with ui.column():
                                                if task.get("title"):
                                                    ui.label(task.get("title")).style("font-size: 20px; width: 100px;")
                                                else:
                                                    ui.label(task).style("font-size: 20px; width: 100px;")
                                            
                                            with ui.column():
                                                if index < len(check_box_values):
                                                     ui.checkbox("Include", value=check_box_values[index].value)
                                                else:
                                                     check_box_values.append(ui.checkbox("Include", value=True))

                        update_task_list()

        