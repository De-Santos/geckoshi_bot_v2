import logging
from typing import Annotated

from fastapi import APIRouter, Query
from starlette.responses import JSONResponse

from database import TaskType
from utils.pagination import PaginatedResponse
from .dto import TaskDto
from .impl import get_task_page, process_task_done

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.get(
    '/',
    response_model=PaginatedResponse[TaskDto],
    responses={
        200: {
            "status": "OK",
            "...": "..."
        },
    }
)
async def get_active_task_page(user_id: Annotated[int, Query(alias='id', description='The user id')],
                               page: int = 1,
                               task_type: TaskType = None,
                               limit: int = 1,
                               ):
    result = await get_task_page(user_id, page, task_type, limit)
    return PaginatedResponse(result)


@router.post(
    '/done',
    response_model=bool,
    responses={
        200: {
            "status": "OK",
            "...": "..."
        },
    }
)
async def get_active_task_page(user_id: Annotated[int, Query(alias='id', description='The user id')],
                               task_id: Annotated[int, Query(description='The task id')],
                               ):
    result = await process_task_done(user_id, task_id)
    return JSONResponse({"status": "OK",
                         "done_successfully": result})
