from nicegui import ui, app, client
import components.sidebar
import components.header
import pages.login

# import pages.stats
# import pages.viewCalender
# import pages.addTasks
import json
import pages.globalState
import showAddTask2
import viewStats

import fastapi
import datetime
from dateutil.parser import parse

import sys
sys.path.append("..")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
import backend.add_task
import backend.checkRequest
async def update_events_with_url(url):
    # print(url)
    events = await backend.add_task.get_events(url, pages.login.users_id)
    events = events.get("event_times")
    # print(events)
    new_events = [{"title": str(title), "start": str(start), "end": str(end)} for start, end, title in events]

    pages.globalState.events.extend(new_events)


def update_calendar():
        print("Updating Calendar!")
        stuff=  backend.add_task.check_database(pages.login.users_id)
                
        stuff = stuff.get("events3")
        pages.globalState.events = stuff
        ui.run_javascript(f'renderFullCalendar("my-calendar", {pages.globalState.events});')

@ui.refreshable
@ui.page("/")
async def main(request: fastapi.requests.Request, client: client.Client):
    # Create an HTML container for the FullCalendar
    pages.login.add()
    ui.open("/login")

    components.header.add(request)

    client.on_connect(update_calendar)
    # url_input = ui.input("URL")
    # ui.button("Open", on_click=lambda: update_events_with_url(url_input.value))
    if not pages.login.is_authenticated(request):
        return fastapi.responses.RedirectResponse("/login")
    with ui.row():
        with ui.column().style("width: 90%; height: 100%;"):
            ui.element().classes('my-calendar').style("width: 100%; height: 600px;")
            ui.add_head_html('''
                    <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>
                    <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        var calendarEvents = {events_json};

                        window.calendarInstance = new FullCalendar.Calendar(document.querySelector('.my-calendar'), {{
                            initialView: 'timeGridWeek',
                            slotMinTime: "05:00:00",
                            slotMaxTime: "22:00:00",
                            allDaySlot: false,
                            timeZone: 'local',
                            height: 'auto',
                            events: 
                                calendarEvents
                            
                        }});
                        window.calendarInstance.render();
                    }});
                    </script>
                '''.format(events_json=json.dumps(pages.globalState.events)))
        with ui.column():
            with ui.row():
                ui.button("Add Task", on_click=lambda x: showAddTask2.add(username=pages.login.users_id))
            with ui.row():
                ui.button("View Stats", on_click=lambda x: viewStats.add(username=pages.login.users_id))




ui.run(title="Calendar")
