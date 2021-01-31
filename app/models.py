from tortoise import fields
from tortoise.models import Model

from tortoise.contrib.pydantic import pydantic_model_creator
from pydantic import BaseModel


class Event(Model):
    name = fields.CharField(max_length=255)
    timestamp = fields.DatetimeField(auto_now_add=True)

class ScheduleConfiguration(BaseModel):
    initial_delay: int
    interval_range_start: int
    interval_range_end: int
    timeout: int

EventPydantic = pydantic_model_creator(Event, name="Event")
