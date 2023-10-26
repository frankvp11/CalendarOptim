
from fireo.models import Model
from fireo.fields import  TextField, BooleanField, NestedModel, ListField, NumberField, DateTime
import firebase_admin
cred = firebase_admin.credentials.Certificate('accountkey.json')
app2 = firebase_admin.initialize_app(cred)
from .event import Event
from .stat import Stat





class User(Model):
    class Meta:
        collection_name = "Database"

    events = ListField(NestedModel(Event))
    stats = ListField(NestedModel(Stat))
    joinLink = TextField()