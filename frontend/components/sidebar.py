from nicegui import ui

left_drawer = None


def add(page) -> None:
    global left_drawer
    
    left_drawer = (
        ui.left_drawer(fixed=False, elevated=True)
        .classes("bg-blue-100")
        .props("overlay")
        .style("position:relative;")
        .props("behavior=mobile")
    )
    ui.button(
                icon="menu", on_click=lambda: left_drawer.toggle(), color=None
            ).props("flat").style("color: white; padding-top: 0.5%; padding-right: -2%;")
    left_drawer.toggle()
    with left_drawer:
        with ui.element("div").style("margin-top: 10px; "):
            with ui.link(target="/stats").style("text-decoration:none; "):
                if page == "stats":
                    stats_row = (
                        ui.row()
                        .style(
                            "border-radius: 20px; margin-top: 5px; margin-bottom: 5px;"
                        )
                        .classes("bg-slate-300")
                    )
                else:
                    stats_row = (
                        ui.row()
                        .style(
                            "border-radius: 20px; margin-top: 5px; margin-bottom: 5px;"
                        )
                        .classes("hover:bg-slate-300")
                    )
                with stats_row:
                    ui.icon("monitor_heart", size="36px").style(
                        "margin-left: 10px; text-align:center; display:block; "
                    )
                    ui.link(text="Stats", target="/stats").style(
                        "text-decoration:none; color:black;  margin-right: 10px; font-size:20px; display:block; margin-top: 1%;"
                    )
        with ui.element("div").style("margin-top: 20px;"):
            with ui.link(target="/addTasks").style("text-decoration:none;"):
                if page == "addTasks":
                    tasks_row = (
                        ui.row()
                        .style(
                            "border-radius: 20px; margin-top: 5px; margin-bottom:5px;"
                        )
                        .classes("bg-slate-300")
                    )
                else:
                    tasks_row = (
                        ui.row()
                        .style(
                            "border-radius: 20px; margin-top: 5px; margin-bottom:5px;"
                        )
                        .classes("hover:bg-slate-300")
                    )
                with tasks_row:
                    ui.icon("schedule", size="36px").style(
                        "margin-left: 10px; text-align:center; display:block; "
                    )
                    ui.link(text="Add Tasks", target="/addTasks").style(
                        "text-decoration:none; color:black;  margin-right: 10px; font-size:20px; display:block; margin-top: 1%;"
                    )
        with ui.element("div").style("margin-top: 20px;"):
            with ui.link(target="/calendar").style("text-decoration:none"):
                if page == "calendar":
                    calendar_row = (
                        ui.row()
                        .style(
                            "border-radius: 20px; margin-top: 5px; margin-bottom:5px;"
                        )
                        .classes("bg-slate-300")
                    )
                else:
                    calendar_row = (
                        ui.row()
                        .style(
                            "border-radius: 20px; margin-top: 5px; margin-bottom:5px;"
                        )
                        .classes("hover:bg-slate-300")
                    )
                with calendar_row:
                    ui.icon("view_week", size="36px").style(
                        "margin-left: 10px; text-align:center; display:block; "
                    )
                    ui.link(text="View Calendar", target="/calendar").style(
                        "text-decoration:none; color:black;  margin-right: 10px; font-size:20px; display:block; margin-top: 1%;"
                    )

    return left_drawer