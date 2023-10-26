

from nicegui import ui, app
from . import sidebar


def add(page: str="main"):
    left_drawer = sidebar.add(page)
    with ui.header() as header:
        ui.button(
                icon="menu", on_click=lambda: left_drawer.toggle(), color=None
            ).props("flat").style("color: white; padding-top: 0.5%; padding-right: -2%;")
        ui.label("Calendar AI").style("color: white; font-size: 20px; margin-left: 10px;")
