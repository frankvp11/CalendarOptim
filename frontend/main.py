from nicegui import ui, app
import components.sidebar
import components.header
import pages.login
import pages.viewCalender
import pages.addTasks

import pages.globalState


import fastapi


import sys
sys.path.append("..")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
import backend.add_task

async def update_events_with_url(url):
    # print(url)
    events = await backend.add_task.get_events(url)
    events = events.get("event_times")
    # print(events)
    new_events = [{"title": str(title), "start": str(start), "end": str(end)} for start, end, title in events]

    pages.globalState.events.extend(new_events)





@ui.page("/")
async def main(request: fastapi.requests.Request):
    # Create an HTML container for the FullCalendar
    pages.login.add()
    ui.open("/login")
    pages.viewCalender.add()
    pages.addTasks.add()
    components.header.add()

    stuff= await  backend.add_task.check_database()
    stuff = stuff.get("events3")
    pages.globalState.events = stuff

    url_input = ui.input("URL")
    ui.button("Open", on_click=lambda: update_events_with_url(url_input.value))
    if not pages.login.is_authenticated(request):
        return fastapi.responses.RedirectResponse("/login")


ui.run(title="Calendar")
