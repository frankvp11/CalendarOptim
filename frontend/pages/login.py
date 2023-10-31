from nicegui import ui, app
import starlette.middleware.sessions
import fastapi.requests
import fastapi.responses
import uuid

app.add_middleware(
    starlette.middleware.sessions.SessionMiddleware, secret_key="super-secret-key"
)
users = [{"username": "frank", "password":"password123", "email":"frankvanpaassen3@gmail.com"},{"username": "admin", "password":"admin", "email":"admin@gmail.com"}, {"username": "user", "password":"user", "email":"frankvanpaassen2@gmail.com"}]
session_info: dict[str, dict] = {}
users_id = None



def is_authenticated(request: fastapi.requests.Request) -> bool:
    return session_info.get(str(request.session.get("id")), {}).get(
        "authenticated", False
    )



def revoke_authentication(request: fastapi.requests.Request) -> None:
    session_info.pop(request.session["id"])
    request.session["id"] = None

def add():
    @ui.page("/login")
    def login(request: fastapi.requests.Request) -> None | fastapi.responses.RedirectResponse:
        ui.open("/login")
        ui.query("body").classes(replace="bg-gray-200")

        def verify_account(email, username):
            if any(user["username"] == username for user in users) or any(user["email"] == email for user in users):
                return False
            else:
                return True

                
        def add_account() -> None:
            global users_id
            with ui.card().classes("absolute-center").style("width:100%; height:100%; min-width: 200px; min-height: 250px;"):
                full_width_style = "width: 100%;"
                email = ui.input("Email").on("keydown.enter", lambda : ( try_create_account(email.value, username.value, password.value))).style(full_width_style)
                username = ui.input("Username").on("keydown.enter", lambda : ( try_create_account(email.value, username.value, password.value))).style(full_width_style)
                password = ui.input("Password", password=True, password_toggle_button=True).on("keydown.enter", lambda : (try_create_account(email.value, username.value, password.value))).style(full_width_style)
                ui.button("Create account", on_click=lambda: ( try_create_account(email.value, username.value, password.value))).style(full_width_style)

                
                print("Creating account page")
                
                users_id = username.value
        
        def try_create_account(email, username, password) -> None:
            global users_id
            if verify_account(email, username):
                ui.notify("Account created successfully", color="positive")
                session_info[request.session["id"]] = {
                    "username": username,
                    "authenticated": True,
                }
                users.append({"username": username, "password": password, "email": email})


                print("Account created successfully")
                users_id = username

                
                ui.open("/")
                return fastapi.responses.RedirectResponse("/")
            else:
                ui.notify("Username or email already in use", color="negative")
                ui.button("Log in?", on_click=lambda: login(email, username).style("width: 100%;"))



        def try_login(username, password) -> None:  
            global users_id
            # local function to avoid passing username and password as arguments
            matched_user = next((user for user in users if user["username"] == username and user["password"] == password), None)

            if matched_user:
                session_info[request.session["id"]] = {
                    "username": username,
                    "authenticated": True,
                }
                users_id = username
                ui.open("/")
                return fastapi.responses.RedirectResponse("/")

            else:

                ui.notify("Wrong username or password", color="negative")
                ui.button("Create a new account?", on_click=lambda: add_account()).style("width: 100%;")

        if is_authenticated(request):
            return fastapi.responses.RedirectResponse("/")

        request.session["id"] = str(uuid.uuid4())
        with ui.card().classes("absolute-center").style("width:20%; height:25%; min-width: 200px; min-height: 250px;"):
            
            username = (
                ui.input("Username").on("keydown.enter", lambda : try_login(username.value, password.value)).style("width:100%")
            )
            password = (
                ui.input("Password", password=True, password_toggle_button=True)
                .props("type=password")
                .on("keydown.enter", lambda : try_login(username.value, password.value))
                .style("width: 100%;")
            )
            ui.button("Log in", on_click=lambda : try_login(username.value, password.value)).style("width:100%;")


    @ui.page("/logout")
    def logout(
        request: fastapi.requests.Request,
    ) -> None | fastapi.responses.RedirectResponse:
        if is_authenticated(request):
            revoke_authentication(request)
            return fastapi.responses.RedirectResponse("/login")
        return fastapi.responses.RedirectResponse("/")