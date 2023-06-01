from tortoise import Tortoise
from tortoise.contrib.pydantic import pydantic_model_creator

from models import Placeholder

Tortoise.init_models(["srcs.app.models", "srcs.tasks.models"], "models")

PlaceholderSchema = pydantic_model_creator(Placeholder)

