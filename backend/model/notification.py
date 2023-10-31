
from fireo.models import Model
from fireo.fields import  TextField, BooleanField, NestedModel, ListField, NumberField, DateTime, IDField, MapField


class Notification(Model):
    id = IDField(include_in_document=True)
    sender = TextField()
    message = TextField()
    duration = NumberField()
    start_time = DateTime()
    finish_time = DateTime()
    people = MapField()