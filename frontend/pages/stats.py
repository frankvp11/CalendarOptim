from nicegui import ui, app
import sys

sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
import backend.get_stats
import components.header
from . import login
import fastapi


def add(request: fastapi.requests.Request):

    username = login.session_info.get(str(request.session.get("id")), {}).get("username")

    stats = []

    @ui.refreshable
    @ui.page("/stats")
    def main():
        nonlocal stats, username
        components.header.add(request, "stats")

        ui.button("Update stats", on_click=lambda: (update_stats(), ui.notify("Stats updated", color="positive")))
        stats = backend.get_stats.getStats(username)
        ui.label(f"You have completed this many regular events: {stats.get('past_regular_events')}")
        ui.label(f"You have completed this many special events: {stats.get('past_non_regular_events')}")

    def update_stats():
        nonlocal stats, username
        stats = backend.get_stats.getStats(username)
        main.refresh()
