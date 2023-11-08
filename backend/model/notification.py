
from fireo.models import Model
from fireo.fields import  TextField, BooleanField, NestedModel, ListField, NumberField, DateTime, IDField, MapField


class Notification(Model):
    id = IDField(include_in_document=True)
    sender = TextField()
    message = TextField()
    summary = TextField()
    duration = NumberField()
    start_time = DateTime()
    finish_time = DateTime()
    people = MapField()

#users = [{"username": "frank", "password":"password123", "email":"frankvanpaassen3@gmail.com"},{"username": "admin", "password":"admin", "email":"admin@gmail.com"}, {"username": "user", "password":"user", "email":"frankvanpaassen2@gmail.com"}]
