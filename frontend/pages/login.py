# from nicegui import ui, app
# import starlette.middleware.sessions
# import fastapi.requests
# import fastapi.responses
# import uuid


# from descope import DescopeClient, AuthException
# from starlette.middleware.base import BaseHTTPMiddleware
# from fastapi.responses import RedirectResponse
# from nicegui import app, Client, ui
# from fastapi import Request

# try:
#     descope_client = DescopeClient(project_id='P2Xs7eIEJAW3pqOnTydPYGWsmNm7')
# except Exception as error:
#     print("Failed to initialize Descope client. Error:")
#     print(error)


# class DescopeAuthMiddleware(BaseHTTPMiddleware):
#     """This middleware restricts access to certain NiceGUI pages using Descope authentication."""

#     async def dispatch(self, request: Request, call_next):
#         # Extract the session token from the user's storage
#         try:
#             jwt = app.storage.user['descope']['sessionToken']['jwt']
#             refresh_jwt = app.storage.user['descope']['refreshSessionToken']['jwt']
#         except TypeError:
#             jwt = None
#         except KeyError:
#             jwt = None

#         def handle_restrictions(path):
#             if path in ["/login"]:
#                 return False
#             else:
#                 # If you have dynamic endpoints, e.g. "/dynamic_endpoint/{id}", you can add them to the list below.
#                 for route in [Client.page_routes.values(), "/dynamic_endpoint/"]:
#                     if path in route:
#                         return True
#                 else:
#                     return False

#         # Check if the user is trying to access a restricted route
#         if handle_restrictions(request.url.path):
#             # If there's no session token or the user is not authenticated, redirect to login
#             if not jwt or not app.storage.user.get('authenticated', False):
#                 app.storage.user['referrer_path'] = request.url.path  # remember where the user wanted to go
#                 return RedirectResponse('/login')

#             # Validate the session token using Descope
#             try:
#                 descope_client.validate_session(session_token=refresh_jwt)
#             except AuthException:
#                 # If validation fails, clear the user's storage and redirect to the login page
#                 app.storage.user.clear()
#                 return RedirectResponse('/login')

#         # If the user is authenticated or accessing an unrestricted route, proceed to the next middleware or endpoint
#         return await call_next(request)


# # Add the middleware to your FastAPI app

# app.add_middleware(DescopeAuthMiddleware)


# users = [{"username": "frank", "password":"password123", "email":"frankvanpaassen3@gmail.com"},{"username": "admin", "password":"admin", "email":"admin@gmail.com"}, {"username": "user", "password":"user", "email":"frankvanpaassen2@gmail.com"}]
# session_info: dict[str, dict] = {}
# users_id = None



# def is_authenticated(request: fastapi.requests.Request) -> bool:
#     return session_info.get(str(request.session.get("id")), {}).get(
#         "authenticated", False
#     )



# def revoke_authentication(request: fastapi.requests.Request) -> None:
#     session_info.pop(request.session["id"])
#     request.session["id"] = None

# def add():
#     @ui.page("/login")
#     def login(request: fastapi.requests.Request) -> None | fastapi.responses.RedirectResponse:
#         ui.open("/login")
#         ui.query("body").classes(replace="bg-gray-200")

#         def verify_account(email, username):
#             if any(user["username"] == username for user in users) or any(user["email"] == email for user in users):
#                 return False
#             else:
#                 return True

                
#         def add_account() -> None:
#             global users_id
#             with ui.card().classes("absolute-center").style("width:100%; height:100%; min-width: 200px; min-height: 250px;"):
#                 full_width_style = "width: 100%;"
#                 email = ui.input("Email").on("keydown.enter", lambda : ( try_create_account(email.value, username.value, password.value))).style(full_width_style)
#                 username = ui.input("Username").on("keydown.enter", lambda : ( try_create_account(email.value, username.value, password.value))).style(full_width_style)
#                 password = ui.input("Password", password=True, password_toggle_button=True).on("keydown.enter", lambda : (try_create_account(email.value, username.value, password.value))).style(full_width_style)
#                 ui.button("Create account", on_click=lambda: ( try_create_account(email.value, username.value, password.value))).style(full_width_style)

                
#                 print("Creating account page")
                
#                 users_id = username.value
        
#         def try_create_account(email, username, password) -> None:
#             global users_id
#             if verify_account(email, username):
#                 ui.notify("Account created successfully", color="positive")
#                 session_info[request.session["id"]] = {
#                     "username": username,
#                     "authenticated": True,
#                 }
#                 users.append({"username": username, "password": password, "email": email})


#                 print("Account created successfully")
#                 users_id = username

                
#                 ui.open("/")
#                 return fastapi.responses.RedirectResponse("/")
#             else:
#                 ui.notify("Username or email already in use", color="negative")
#                 ui.button("Log in?", on_click=lambda: login(email, username).style("width: 100%;"))



#         def try_login(username, password) -> None:  
#             global users_id
#             # local function to avoid passing username and password as arguments
#             matched_user = next((user for user in users if user["username"] == username and user["password"] == password), None)

#             if matched_user:
#                 session_info[request.session["id"]] = {
#                     "username": username,
#                     "authenticated": True,
#                 }
#                 users_id = username
#                 ui.open("/")
#                 return fastapi.responses.RedirectResponse("/")

#             else:

#                 ui.notify("Wrong username or password", color="negative")
#                 ui.button("Create a new account?", on_click=lambda: add_account()).style("width: 100%;")

#         if is_authenticated(request):
#             return fastapi.responses.RedirectResponse("/")

#         request.session["id"] = str(uuid.uuid4())
#         with ui.card().classes("absolute-center").style("width:20%; height:25%; min-width: 200px; min-height: 250px;"):
            
#             username = (
#                 ui.input("Username").on("keydown.enter", lambda : try_login(username.value, password.value)).style("width:100%")
#             )
#             password = (
#                 ui.input("Password", password=True, password_toggle_button=True)
#                 .props("type=password")
#                 .on("keydown.enter", lambda : try_login(username.value, password.value))
#                 .style("width: 100%;")
#             )
#             ui.button("Log in", on_click=lambda : try_login(username.value, password.value)).style("width:100%;")


#     @ui.page("/logout")
#     def logout(
#         request: fastapi.requests.Request,
#     ) -> None | fastapi.responses.RedirectResponse:
#         if is_authenticated(request):
#             revoke_authentication(request)
#             return fastapi.responses.RedirectResponse("/login")
#         return fastapi.responses.RedirectResponse("/")
import json
import os
import logging
from typing import Any, Callable, Dict

from descope import AuthException, DescopeClient
from nicegui import ui, Client, app, helpers

os.environ['DESCOPE_PROJECT_ID'] = "P2Xs7eIEJAW3pqOnTydPYGWsmNm7"

DESCOPE_ID = os.environ.get('DESCOPE_PROJECT_ID', '')



try:
        descope_client = DescopeClient(project_id=DESCOPE_ID)
except AuthException as ex:
        print(ex.error_message)

def login_form() -> ui.element:
        """Create and return the Descope login form."""
        with ui.card().classes('w-96 mx-auto'):
            return ui.element('descope-wc').props(f'project-id="{DESCOPE_ID}" flow-id="sign-up-or-in"') \
                .on('success', lambda e: app.storage.user.update({'descope': e.args['detail']['user']}))

def about() -> Dict[str, Any]:
        """Return the user's Descope profile.

        This function can only be used after the user has logged in.
        """
        return app.storage.user['descope']

async def logout() -> None:
        """Logout the user."""
        result = await ui.run_javascript('return await sdk.logout()')
        if result['code'] == 200:
            app.storage.user['descope'] = None
        else:
            logging.error(f'Logout failed: {result}')
            ui.notify('Logout failed', type='negative')
        ui.open(page.LOGIN_PATH)

class page(ui.page):
        """A page that requires the user to be logged in.

        It allows the same parameters as ui.page, but adds a login check.
        As recommended by Descope, this is done via JavaScript and allows to use Flows.
        But this means that the page has already awaited the client connection.
        So `ui.add_head_html` will not work.
        """
        SESSION_TOKEN_REFRESH_INTERVAL = 30
        LOGIN_PATH = '/login'

        def __call__(self, func: Callable[..., Any]) -> Callable[..., Any]:
            async def content(client: Client):
                ui.add_head_html('<script src="https://unpkg.com/@descope/web-component@latest/dist/index.js"></script>')
                ui.add_head_html('<script src="https://unpkg.com/@descope/web-js-sdk@latest/dist/index.umd.js"></script>')
                ui.add_body_html(f'''
                    <script>
                        const sdk = Descope({{ projectId: 'P2Xs7eIEJAW3pqOnTydPYGWsmNm7', persistTokens: true, autoRefresh: true }});
                        const sessionToken = sdk.getSessionToken()
                    </script>                 
                ''')
                await client.connected()
                if await self._is_logged_in():
                    if self.path == self.LOGIN_PATH:
                        self._refresh()
                        ui.open('/')
                        return
                else:
                    if self.path != self.LOGIN_PATH:
                        ui.open(self.LOGIN_PATH)
                        return
                    ui.timer(self.SESSION_TOKEN_REFRESH_INTERVAL, self._refresh)

                if helpers.is_coroutine_function(func):
                    await func()
                else:
                    func()

            return super().__call__(content)

        @staticmethod
        async def _is_logged_in() -> bool:
            if not app.storage.user.get('descope'):
                return False
            token = await ui.run_javascript('return sessionToken && !sdk.isJwtExpired(sessionToken) ? sessionToken : null;')
            if not token:
                return False
            try:
                descope_client.validate_session(session_token=token)
                return True
            except AuthException:
                logging.exception('Could not validate user session.')
                ui.notify('Wrong username or password', type='negative')
                return False

        @staticmethod
        def _refresh() -> None:
            ui.run_javascript('sdk.refresh()')

def login_page(func: Callable[..., Any]) -> Callable[..., Any]:
    """Marks the special page that will contain the login form."""
    return page(page.LOGIN_PATH)(func)
