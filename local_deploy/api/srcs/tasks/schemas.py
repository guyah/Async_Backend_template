from tortoise.contrib.pydantic import pydantic_model_creator
from models import Task


TaskSchema = pydantic_model_creator(Task)
