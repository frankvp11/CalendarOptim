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
from dateutil.parser import parse
import backend.remove_notifications
import backend.checkRequest
import backend.get_notifications
import backend.add_task
import backend.save_task

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

all_events = []


@ui.refreshable
@pages.user.page("/")
async def main():
    # Create an HTML container for the FullCalendar
    global calendar, all_events

    ui.add_head_html('<script src="https://cdn.jsdelivr.net/npm/fullcalendar@6.1.9/index.global.min.js"></script>')
    
    add()
    all_events = []
    if not all_events:
        print(pages.user.about()['email'])
        all_events = backend.add_task.check_database(pages.user.about()['email']).get("events3")
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


            
            options = {
                    'initialView': 'timeGridWeek',
                    'slotMinTime': '05:00:00',
                    'slotMaxTime': '22:00:00',
                    'allDaySlot': False,
                    'timeZone': 'local',
                    'height': 'auto',
                    'width': 'auto',
                    'events': all_events,
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






def close_menus():
    global logout_menu, notification_menu
    if logout_menu:
        logout_menu = None
    if notification_menu:
        notification_menu = None

import pages.user
async def temp2():
    await pages.user.logout()

def open_logout_menu():
    global logout_menu

    with ui.menu() as menu:
        logout_menu = menu
        ui.button("Logout", on_click=lambda X: temp2())



def view_calendar_change(start_time, finish_time, summary, noti_id):
    global notification_menu, all_events
    start_time = parse(start_time)
    finish_time = parse(finish_time)
    
    start_time = start_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    finish_time = finish_time.strftime('%Y-%m-%d %H:%M:%S.%f')
    
    start_time2 = parse(start_time).strftime('%Y-%m-%d %H:%M')
    finish_time2 = parse(finish_time).strftime('%Y-%m-%d %H:%M')

    ui.notify(f"Your schedule will change from {start_time2} to {finish_time2}")
    card_element = ui.card().style("position: fixed; left:5%; top: 5%; z-index: 1000; height: 80%; width:1000px;").classes("my-calendar")

    def run_updates(noti_id, status):
        nonlocal start_time, finish_time, summary, start_time2, finish_time2
        global username, notification_button, all_events
        nonlocal card_element
        add_to_cal = backend.checkRequest.updateStatus(noti_id.get("id"), username, status)
        if add_to_cal:
             print("Updating Calendar after accepting invitation")
            #  card_element.delete()
            #  main.refresh()
             #all_events.append({"title":summary, "start":start_time2, "end":finish_time2})

             calendar.add_event(title=summary, start=start_time2, end=finish_time2)
             calendar.update()
             temp.refresh()
             print("ATtempting to updated!")
             print(all_events[-2:])
             return
        
        if notification_button.text:
            notification_button.text = str(int(notification_button.text) - 1)
        card_element.delete()
        print("Before refreshing things from the notification page, this is the events")
        print(all_events[-5:])
        print("new line")
        main.refresh()
        ui.notify("Updated calendar", color="positive")

    with card_element:
            options = {
                    'initialView': 'timeGridWeek',
                    'slotMinTime': '05:00:00',
                    'slotMaxTime': '22:00:00',
                    'allDaySlot': False,
                    'timeZone': 'local',
                    'height': 'auto',
                    'width': 'auto',
                    'events': all_events + [{"title":summary, "start":start_time2, "end":finish_time2, "color":"red"}],
            }

            ui.fullcalendar(options=options)
            ui.button("Close", on_click=card_element.delete)
            ui.button("Accept invitation", on_click=lambda : (run_updates(noti_id, 1)))
            ui.button("Reject invitation", on_click=lambda : (run_updates(noti_id, 2)))

def update_notification_menu(username, notification):
     global notification_menu, notification_button
     backend.remove_notifications.remove_notification_by_id(username, notification)
     temp.refresh()
     if notification_button.text:
        notification_button.text = str(int(notification_button.text) - 1)


@ui.refreshable
def temp(menu):
            notifications = backend.get_notifications.getNotifications(username)

            notification_menu = menu
            notifications = notifications.get("notifications")  
            notification_button.text = str(len(notifications)) if notifications else ""
            ui.label(f"You have {len(notifications)} notifications").style("font-size: 24px;")
            if notifications:
                for notification in notifications:
                    

                    start_time = notification.get('start_time')
                    finish_time = notification.get('finish_time')
                    summary = notification.get("summary")
                    if summary and start_time and finish_time:
                        start_time = notification.get('start_time').strftime('%Y-%m-%d %H:%M')
                        finish_time = notification.get('finish_time').strftime('%Y-%m-%d %H:%M')

                        ui.label(summary).style("font-size: 16px;")
                        ui.button("View how this would change your schedule", on_click=lambda x, s_time=start_time, f_time=finish_time, msg=notification.get('message'), nid=notification.get("id"): view_calendar_change(s_time, f_time, msg, notification))
                    else:
                        with ui.row():
                            ui.label(summary).style("font-size: 16px;")
                            ui.button(icon="delete_forever", on_click=lambda x: (update_notification_menu(username, notification)))
         

@ui.refreshable
def open_notification_menu():
    global notification_menu, username

    with ui.menu().style("width: 40%; height: 30%;") as menu:
        temp(menu)

def add(page: str="main"):

    global username, notification_button
    username = pages.user.about()['email']
    notifications = backend.get_notifications.getNotifications(username)#.get("notifications")
    amount_of_notifications = len(notifications.get("notifications")) if notifications.get("notifications") else 0
    with ui.header() as header:
        ui.label("Calendar AI").style("color: white; font-size: 20px; margin-left: 10px;")
    
        with ui.row().style("position: absolute; right: 5%;"):
            notification_button = ui.button(icon="notifications", text=amount_of_notifications, on_click=lambda x : open_notification_menu()).style("color: red;")
             
        with ui.row().style("position: absolute; right: 2%;"):
                        ui.button(icon="account_circle", color=None).on(
                            "click", lambda x: open_logout_menu()
                        ).props("flat").style("color: white; font-size:1rem;")
                    


ui.run(title="calendar", storage_secret='randomsecret')
