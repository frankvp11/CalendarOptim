

from fireo.models import Model
from fireo.fields import  TextField, BooleanField, NestedModel, ListField, NumberField, DateTime


class Event(Model):
    start = DateTime()
    end = DateTime()
    summary = TextField()
    regular_event = BooleanField()