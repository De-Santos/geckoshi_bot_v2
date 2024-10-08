import logging
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse

import auth
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
    response_model=TaskDto,
    summary="Get Active Task Page",
    description=(
            "Fetch a paginated list of active tasks for the authenticated user. "
            "This endpoint allows filtering tasks by type and supports pagination "
            "using the 'page' and 'limit' parameters. A valid user authentication token "
            "is required to access this endpoint."
    ),
    responses={
        200: {
            "status": "OK",
            "...": "..."
        },
    }
)
async def get_active_task_page(user_id=Depends(auth.auth_dependency),
                               page: int = 1,
                               task_type: TaskType = None,
                               limit: int = 1,
                               ):
    result = await get_task_page(user_id, page, task_type, limit)
    return PaginatedResponse(result)


@router.post(
    '/done',
    response_model=bool,
    summary="Mark Task as Done",
    description=(
            "Mark a specific task as completed using its task ID. "
            "A valid user authentication token is required to process this request. "
            "On successful completion, the endpoint returns a confirmation."
    ),
    responses={
        200: {
            "status": "OK",
            "...": "..."
        },
    }
)
async def get_active_task_page(task_id: Annotated[int, Query(description='The task id')],
                               user_id=Depends(auth.auth_dependency)):
    result = await process_task_done(user_id, task_id)
    return JSONResponse({"status": "OK",
                         "done_successfully": result})
