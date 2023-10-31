from fireo.models import Model
from fireo.fields import TextField, BooleanField, NestedModel, ListField, NumberField, DateTime, IDField, MapField
from .notification import Notification
from .event import Event

class TaskStatus(Model):
    # Auto-generated ID for each TaskStatus instance
    id = IDField(include_in_document=True)
    
    event = NestedModel(Event)
    
    # A dictionary to store people as keys and integers as values
    people_status = MapField()

 


# class NestedTaskStatus(Model):
#     # Auto-generated ID for each TaskStatus instance
#     id = IDField(include_in_document=True)
    
#     event = NestedModel(Event)
    
#     # A dictionary to store people as keys and integers as values
#     people_status = MapField()
# 0 represents pending
# 1 represents rejected
# 2 represents accepted