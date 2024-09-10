import logging

from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

import database
from .auth import auth_dependency
from .dto import TaskDTO

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/task",
    tags=["tasks"],
    dependencies=[Depends(auth_dependency)],
)


@router.post('/')
async def create_task(t: TaskDTO):
    logger.info(f"Received request to create task: {t}")

    await database.save_task(t.to_entity())

    return JSONResponse({"status": "OK"})
