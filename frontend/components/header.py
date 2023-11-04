

from nicegui import ui, app
from . import sidebar
import fastapi
import sys
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
from dateutil.parser import parse
import pages.globalState
import pages.addTasks
import backend.get_notifications
import backend.save_task
import backend.remove_notifications
import backend.checkRequest
# viewStatus, addRequest
# Maintain references to menus
logout_menu = None
notification_menu = None
username = None
import pages.login

def close_menus():
    global logout_menu, notification_menu
    if logout_menu:
        logout_menu = None
    if notification_menu:
        notification_menu = None

def temp2():
    ui.open("/logout")
    return fastapi.responses.RedirectResponse("/logout")

def open_logout_menu():
    global logout_menu

    with ui.menu() as menu:
        logout_menu = menu
        ui.button("Logout", on_click=lambda X: temp2())



def view_calendar_change(start_time, finish_time, summary, noti_id):
    global notification_menu
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
        global username

        add_to_cal = backend.checkRequest.updateStatus(noti_id.get("id"), username, status)
        if add_to_cal:
             print("Updating Calendar after accepting invitation")
             pages.globalState.events.append({"title":summary, "start":start_time2, "end":finish_time2})

        temp.refresh()
    with card_element:
            ui.button("Close", on_click=card_element.delete)
            ui.button("Accept invitation", on_click=lambda : (run_updates(noti_id, 1)))
            ui.button("Reject invitation", on_click=lambda : (run_updates(noti_id, 2)))
    temp_array = pages.globalState.events.copy()

    temp_array.append({"title":summary, "start":start_time2, "end":finish_time2, "color":"red"})

    ui.run_javascript(f'renderFullCalendar("my-calendar", {temp_array});')


@ui.refreshable
def temp(menu):
            notifications = backend.get_notifications.getNotifications(username)

            notification_menu = menu
            notifications = notifications.get("notifications")  
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
                            ui.button(icon="delete_forever", on_click=lambda x: (backend.remove_notifications.remove_notification_by_id(username, notification), temp.refresh()))
         

@ui.refreshable
def open_notification_menu():
    global notification_menu, username

    with ui.menu().style("width: 40%; height: 30%;") as menu:
        temp(menu)

def add(request, page: str="main"):
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

    global username
    username = pages.login.session_info.get(str(request.session.get("id")), {}).get("username")
    notifications = backend.get_notifications.getNotifications(username)#.get("notifications")
    amount_of_notifications = len(notifications.get("notifications")) if notifications.get("notifications") else 0
    left_drawer = sidebar.add(page)
    with ui.header() as header:
        ui.button(
                icon="menu", on_click=lambda: left_drawer.toggle(), color=None
            ).props("flat").style("color: white; padding-top: 0.5%; padding-right: -2%;")
        ui.label("Calendar AI").style("color: white; font-size: 20px; margin-left: 10px;")
    
        with ui.row().style("position: absolute; right: 5%;"):
            ui.button(icon="notifications", text=amount_of_notifications, on_click=lambda x : open_notification_menu()).style("color: red;")
             
        with ui.row().style("position: absolute; right: 2%;"):
                        ui.button(icon="account_circle", color=None).on(
                            "click", lambda x: open_logout_menu()
                        ).props("flat").style("color: white; font-size:1rem;")
                    
