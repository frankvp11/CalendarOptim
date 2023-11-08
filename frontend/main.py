# from nicegui import ui, app, client
# import components.sidebar
# import components.header
# import pages.login

# # import pages.stats
# # import pages.viewCalender
# # import pages.addTasks
# import json
# import pages.globalState
# import showAddTask2
# import viewStats

# import fastapi
# import datetime
# from dateutil.parser import parse

# import sys
# sys.path.append("..")
# sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
# import backend.add_task
# import backend.checkRequest


# async def update_events_with_url(url):
#     # print(url)
#     events = await backend.add_task.get_events(url, "frank")
#     events = events.get("event_times")
#     # print(events)
#     new_events = [{"title": str(title), "start": str(start), "end": str(end)} for start, end, title in events]

#     pages.globalState.events.extend(new_events)


# def update_calendar():
#         print("Updating Calendar!")
#         stuff=  backend.add_task.check_database("frank")
                
#         stuff = stuff.get("events3")
#         pages.globalState.events = stuff
#         ui.run_javascript(f'renderFullCalendar("my-calendar", {pages.globalState.events});')

# import pages.login
# @ui.refreshable
# @ui.page("/")
# async def main(request: fastapi.requests.Request, client: client.Client):
#     # Create an HTML container for the FullCalendar
#     # pages.login.add()
    
#     ui.open("/login")
#     @pages.login.login_page
#     def login():
#         pages.login.login_form().on('success', lambda: ui.open('/'))

#     components.header.add(request)

#     client.on_connect(update_calendar)

#     with ui.row():
#         with ui.column().style("width: 90%; height: 100%;"):
#             ui.element().classes('my-calendar').style("width: 100%; height: 600px;")
#             ui.add_head_html('''
#                     <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>
#                     <script>
#                     document.addEventListener('DOMContentLoaded', function() {{
#                         var calendarEvents = {events_json};

#                         window.calendarInstance = new FullCalendar.Calendar(document.querySelector('.my-calendar'), {{
#                             initialView: 'timeGridWeek',
#                             slotMinTime: "05:00:00",
#                             slotMaxTime: "22:00:00",
#                             allDaySlot: false,
#                             timeZone: 'local',
#                             height: 'auto',
#                             events: 
#                                 calendarEvents
                            
#                         }});
#                         window.calendarInstance.render();
#                     }});
#                     </script>
#                 '''.format(events_json=json.dumps(pages.globalState.events)))
#         with ui.column():
#             with ui.row():
#                 ui.button("Add Task", on_click=lambda x: showAddTask2.add(username=pages.login.users_id))
#             with ui.row():
#                 ui.button("View Stats", on_click=lambda x: viewStats.add(username=pages.login.users_id))


# storage_secret = "your-secret-key"


# ui.run(title="Calendar", storage_secret=storage_secret)


import pages.user
from nicegui import ui, app, client
import fastapi
import components.header
import json
from datetime import datetime
import pages.globalState
import showAddTask2
import viewStats
import backend.add_task


@pages.user.login_page
def login():
    pages.user.login_form().on('success', lambda: (ui.open('/'), main()))

def update_calendar():


        print("Updating Calendar!")
        stuff=  backend.add_task.check_database(pages.user.about()['email'])
                
        stuff = stuff.get("events3")
        pages.globalState.events = stuff
        ui.run_javascript(f'renderFullCalendar("my-calendar", {pages.globalState.events});')


import asyncio


@ui.refreshable
@pages.user.page("/")
async def main():
    # Create an HTML container for the FullCalendar
    print(pages.user.about())

    components.header.add()
    update_calendar()
    with ui.row():
        with ui.column().style("width: 90%; height: 100%;"):
            ui.element().classes('my-calendar').style("width: 100%; height: 600px;")
            if len(pages.globalState.events) > 0:
                 print("events exists")
            # Call the renderFullCalendar function when the DOM is ready
            ui.add_head_html('''
                <link href='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/main.min.css' rel='stylesheet' />
                <script src='https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js'></script>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {
                        renderFullCalendar("my-calendar", eventsData);
                    });

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
            # await asyncio.sleep(1)
            
                # Replace `eventsData` with your actual events data

        
        

        with ui.column():
                with ui.row():
                    ui.button("Add Task", on_click=lambda x: showAddTask2.add(username=pages.user.about()['email']))
                with ui.row():
                    ui.button("View Stats", on_click=lambda x: viewStats.add(username=pages.user.about()['email']))
                with ui.row():
                     url = ui.input("Enter URL")
                with ui.row():
                     ui.button("Add", on_click=lambda x: backend.add_task.get_events(url.value, pages.user.about()['email']))


@pages.user.page('/async')
async def async_page():
    await ui.button('Wait for it...').clicked()
    ui.label('This is an async page')


ui.run(title="calendar", storage_secret='randomsecret')

