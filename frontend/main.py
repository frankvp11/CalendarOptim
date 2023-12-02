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


calendar = None

@pages.user.login_page
def login():
    pages.user.login_form().on('success', lambda: (ui.open('/'), main()))


# def update_calendar():
#         global calendar
#         print("Updating Calendar!")
#         stuff=  backend.add_task.check_database(pages.user.about()['email'])
#         stuff = stuff.get("events3")
#         pages.globalState.events = stuff
#         print(pages.globalState.events[-5:])

#         if calendar == None:
#              print("CAlendar is none")
#              return
#         calendar.update()





import asyncio


@ui.refreshable
@pages.user.page("/")
async def main():
    # Create an HTML container for the FullCalendar
    global calendar

    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js"></script>')
    
    components.header.add()
    pages.globalState.events = backend.add_task.check_database(pages.user.about()['email']).get("events3")
    with ui.row():
        with ui.column().style("width: 90%; height: 100%;"):
            def format_date(date_str:datetime):
                # Parse the date string and format it consistently
                if isinstance(date_str, str):
                    date_str = datetime.fromisoformat(date_str)
                return date_str.strftime('%Y-%m-%d %H:%M:%S')

            def handle_calendar_click(event):
                try:
                    start = format_date(event.args['info']['event']['start'])
                    end = format_date(event.args['info']['event']['end'])
                    title = event.args['info']['event']['title']
                except Exception as e:
                    title = None

                if title:
                    show_event_card(title, start, end)

            def show_event_card(title, start, end):
                card = ui.card().style("background-color: #f0f0f0; position: absolute; z-index: 10000; top: 50%; left: 50%; transform: translate(-50%, -50%);")
                with card:
                    ui.label(title)
                    ui.button("Click me to remove the event!", on_click=lambda: (calendar.remove_event(title=title.strip(), start=start, end=end), card.delete()))
                    ui.button("Close", on_click=lambda e: card.delete())

            if len(pages.globalState.events) > 0:
                 ui.label(str(pages.globalState.events[-1]) + "hi frank")
                 print("events exists")
                 print(pages.globalState.events[-5:])
            
            options = {
                    'initialView': 'timeGridWeek',
                    'slotMinTime': '05:00:00',
                    'slotMaxTime': '22:00:00',
                    'allDaySlot': False,
                    'timeZone': 'local',
                    'height': 'auto',
                    'width': 'auto',
                    'events': pages.globalState.events,
            }

            calendar = ui.fullcalendar(options=options, on_click=lambda x : handle_calendar_click(x))            

        

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

