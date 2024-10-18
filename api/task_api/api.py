import logging
from io import BytesIO
from typing import Annotated

from fastapi import APIRouter, Query, Depends
from starlette.responses import JSONResponse, StreamingResponse

import auth
from database import TaskType
from utils.pagination import PaginatedResponse
from .dto import TaskDto
from .impl import get_task_page, process_task_done, get_task_chat_photo

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/task",
    tags=["task"],
)


@router.get(
    '',
    response_model=TaskDto,
    summary="Get Active Task Page",
    description=(
            "Fetch a paginated list of active tasks for the authenticated user. "
            "This endpoint allows filtering tasks by type and supports pagination "
            "using the 'page' and 'limit' parameters. A valid user authentication token "
            "is required to access this endpoint."
    )
)
async def get_active_task_page(user_id=Depends(auth.auth_dependency),
                               page: int = 1,
                               task_type: TaskType = None,
                               limit: int = 1,
                               ):
    result = await get_task_page(user_id, page, task_type, limit)
    return PaginatedResponse(result)


@router.get(
    '/photo',
    summary="Retrieve Task Chat Photo",
    description="""
This endpoint retrieves a task-related chat photo based on the task ID and the image type requested.

- **task_id**: The unique identifier of the task.
- **img_type**: Type of image requested (either 'small_file_id' or 'big_file_id').
- **user_id**: User identifier obtained from the authorization process.

If the chat associated with the task does not have a photo or the photo cannot be found, 
the response will be a `204 No Content` status.
Otherwise, it returns the photo as a `PNG` image.
""",
)
async def get_task_photo(task_id: Annotated[int, Query(alias='id', description="")],
                         img_type: Annotated[str, Query(alias='type', description="img types: 'small_file_id', 'big_file_id'")],
                         user_id=Depends(auth.auth_dependency)):
    img_bytes = await get_task_chat_photo(user_id, task_id, img_type)
    if img_bytes is None:
        return StreamingResponse(BytesIO(), status_code=204, media_type="image/png")
    return StreamingResponse(img_bytes, media_type="image/png")


@router.post(
    '/done',
    response_model=bool,
    summary="Mark Task as Done",
    description=(
            "Mark a specific task as completed using its task ID. "
            "A valid user authentication token is required to process this request. "
            "On successful completion, the endpoint returns a confirmation."
    )
)
async def get_active_task_page(task_id: Annotated[int, Query(description='The task id')],
                               user_id=Depends(auth.auth_dependency)):
    result = await process_task_done(user_id, task_id)
    return JSONResponse({"status": "OK",
                         "done_successfully": result})
