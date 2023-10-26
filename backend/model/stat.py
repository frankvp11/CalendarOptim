
from fireo.models import Model
from fireo.fields import  TextField, BooleanField, NestedModel, ListField, NumberField, DateTime


class Stat(Model):
    data_point = NumberField()