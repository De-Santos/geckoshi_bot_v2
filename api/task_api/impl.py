import asyncio
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from api_request import check_user_exists_via_api
from chat_processor.member import check_memberships
from database import get_active_tasks_page, TaskType, Task, get_active_task_by_id, with_session, check_task_is_done, TaskDoneHistory, TransactionOperation
from transaction_manager import make_transaction_from_system, generate_trace, TraceType
from utils.pagination import Pagination
from .dto import TaskDto

logger = logging.getLogger(__name__)


async def get_task_page(user_id: int,
                        page: int = 1,
                        task_type: TaskType = None,
                        limit: int = 1, ) -> Pagination[dict]:
    tasks: Pagination = await get_active_tasks_page(user_id=user_id, page=page, task_type=task_type, limit=limit)
    tasks.map_each(lambda task: TaskDto.model_validate(task, from_attributes=True).model_dump(mode='json'))
    return tasks


@with_session(transaction=True)
async def process_task_done(user_id: int, task_id: int, s: AsyncSession = None) -> bool:
    task: Task = await get_active_task_by_id(task_id, session=s)

    done = await check_task_is_done(task.id, user_id, s=s)

    if done:
        return True

    logger.info(f"Checking task {task.id} for user {user_id} - Validating memberships and API activations")

    subscription_passed = await check_memberships(user_id, task.require_subscriptions)
    api_validation_passed = await check_api_activation(user_id, task)

    if not (subscription_passed and api_validation_passed):
        logger.warning(f"Task {task.id} validation failed for user {user_id}. Subscriptions passed: {subscription_passed}, API passed: {api_validation_passed}")
        return False

    logger.info(f"Task {task.id} successfully validated for user {user_id}. Adding task history and processing transaction.")

    s.add(TaskDoneHistory(reward=task.done_reward, user_id=user_id, task_id=task.id))
    await make_transaction_from_system(user_id, TransactionOperation.INCREMENT, task.done_reward, description="task done",
                                       trace=generate_trace(TraceType.TASK_DONE, str(task.trace_uuid)), session=s, currency_type=task.coin_type)

    logger.info(f"Task {task.id} done successfully for user {user_id}. Reward: {task.done_reward}")
    return True


async def check_api_activation(user_id: int, task: Task) -> bool:
    # Parallel API validation calls using asyncio.gather()
    try:
        results = await asyncio.gather(*[check_user_exists_via_api(user_id, config) for config in task.api_configs])
    except Exception as e:
        logger.error(f"Error checking API activation: {e}")
        return False

    logger.info(f"results list: {results}")

    return all(results)  # Return True if all API checks pass
