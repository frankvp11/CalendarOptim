from nicegui import ui, app
import starlette.middleware.sessions
import fastapi.requests
import fastapi.responses
import uuid

app.add_middleware(
    starlette.middleware.sessions.SessionMiddleware, secret_key="super-secret-key"
)
users = [("frank", "password123")]
session_info: dict[str, dict] = {}


def is_authenticated(request: fastapi.requests.Request) -> bool:
    return session_info.get(str(request.session.get("id")), {}).get(
        "authenticated", False
    )


def revoke_authentication(request: fastapi.requests.Request) -> None:
    session_info.pop(request.session["id"])
    request.session["id"] = None

def add():
    @ui.page("/login")
    def login(
        request: fastapi.requests.Request,
    ) -> None | fastapi.responses.RedirectResponse:
        ui.query("body").classes(replace="bg-gray-200")

        def try_login() -> (
            None
        ):  # local function to avoid passing username and password as arguments
            if (username.value, password.value) in users:
                session_info[request.session["id"]] = {
                    "username": username.value,
                    "authenticated": True,
                }
                ui.open("/")
            else:
                ui.notify("Wrong username or password", color="negative")

        if is_authenticated(request):
            return fastapi.responses.RedirectResponse("/")

        request.session["id"] = str(uuid.uuid4())
        with ui.card().classes("absolute-center").style("width:20%; height:25%; min-width: 200px; min-height: 250px;"):
            username = (
                ui.input("Username").on("keydown.enter", try_login).style("width:100%")
            )
            password = (
                ui.input("Password", password=True, password_toggle_button=True)
                .props("type=password")
                .on("keydown.enter", try_login)
                .style("width: 100%;")
            )
            ui.button("Log in", on_click=try_login).style("width:100%;")


    @ui.page("/logout")
    def logout(
        request: fastapi.requests.Request,
    ) -> None | fastapi.responses.RedirectResponse:
        if is_authenticated(request):
            revoke_authentication(request)
            return fastapi.responses.RedirectResponse("/login")
        return fastapi.responses.RedirectResponse("/")