from nicegui import ui, app
import json

import components.header
from . import globalState



def add():
    @ui.refreshable
    @ui.page("/calendar")
    def main():
        components.header.add("calendar")   

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
        '''.format(events_json=json.dumps(globalState.events)))
        return 0

    ui.timer(5, main.refresh())

