from nicegui import ui, app


import sys
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
import backend.get_stats

def add(username):


    stats = []


    with ui.menu().style("width: 95%; height:100%;"):
        ui.button("Update stats", on_click=lambda: (update_stats(), ui.notify("Stats updated", color="positive")))
        stats = backend.get_stats.getStats(username)
        ui.label(f"You have completed this many regular events: {stats.get('past_regular_events')}").style("font-size: 20px;")
        ui.label(f"You have completed this many special events: {stats.get('past_non_regular_events')}").style("font-size: 20px;")

        def update_stats():
            nonlocal stats, username
            stats = backend.get_stats.getStats(username)
