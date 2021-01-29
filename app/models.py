from tortoise import fields
from tortoise.models import Model

from tortoise.contrib.pydantic import pydantic_model_creator


class Event(Model):
    name = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField(auto_now_add=True)


EventPydantic = pydantic_model_creator(Event, name="Event")
