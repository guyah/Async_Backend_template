import logging

from tortoise import fields
from tortoise.models import Model

logger = logging.getLogger(__name__)

class Placeholder(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    text = fields.TextField(null=True)
    excluded = fields.BooleanField(default=False)
    generated = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f'<PlaceHolder: "{self}" ({self.id})>'

