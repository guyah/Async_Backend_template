import logging

from fastapi import Path, Depends, status
from fastapi.routing import APIRouter

from srcs.app.decorators import handle_does_not_exists
from srcs.app.models import Placeholder
from srcs.app.schemas import PlaceholderSchema

from srcs.tasks.schemas import TaskSchema
from srcs.flows.flows import flow_placeholder
from srcs.main import app

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/placeholder')

@handle_does_not_exists(Placeholder)
async def get_placeholder_by_id(id: int = Path(...)) -> Placeholder:
    return await Placeholder.filter(id=id).first()

@router.get("/{id}")
async def placeholder_list(
    placeholder: Placeholder = Depends(get_placeholder_by_id)
) -> list[PlaceholderSchema]:
    return await PlaceholderSchema.from_queryset(Placeholder.filter(id=placeholder.id))

@router.post("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def generate_flow(placeholder: Placeholder = Depends(get_placeholder_by_id)) -> TaskSchema:
    task = await flow_placeholder.delay(placeholder.id)
    return await TaskSchema.from_tortoise_orm(task)

app.include_router(router)
