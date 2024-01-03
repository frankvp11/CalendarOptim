

from nicegui import ui, app
import fastapi
import sys
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/")
sys.path.append("/home/frankvp11/Documents/CalendarAI/CalendarProj/backend/")
from dateutil.parser import parse
import pages.globalState
# import pages.addTasks
import backend.get_notifications
import backend.save_task
import backend.remove_notifications
import backend.checkRequest
# viewStatus, addRequest
# Maintain references to menus
logout_menu = None
notification_menu = None
username = None
notification_button = None
# import pages.login
import main

